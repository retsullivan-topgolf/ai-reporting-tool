#!/usr/bin/env python3
"""
Generate PDF venue reports from venue_data.json.

Renders templates/venue-snapshot-pdf.html - a layout dedicated to the PDF
output (see that file's docstring comment for why it's a separate template
from venue-snapshot-browser.html) - through headless Chromium, using
Playwright's page.pdf(). The data behind it (metrics, assessments, overview,
ups/downs, impact, recommendations) still comes from report_content.py, the
same module create_html_reports.py uses, so the PDF and HTML reports always
agree on the numbers and narrative even though their layouts differ.

One-time setup (see requirements.txt):
    pip install playwright
    playwright install chromium
"""
import json
import sys
import os
import time

from jinja2 import Environment, FileSystemLoader

import report_engine
import report_content

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: the 'playwright' package is not installed.")
    print("\nInstall it with:")
    print("  pip install playwright")
    print("  playwright install chromium")
    sys.exit(1)

# Parse command line arguments
json_file = 'venue_data.json'
timestamp = None
analysis_file = None

i = 1
while i < len(sys.argv):
    arg = sys.argv[i]
    if arg == '--timestamp':
        if i + 1 >= len(sys.argv):
            print("Error: --timestamp requires a value")
            sys.exit(1)
        timestamp = sys.argv[i + 1]
        i += 2
    elif arg == '--analysis':
        if i + 1 >= len(sys.argv):
            print("Error: --analysis requires a value")
            sys.exit(1)
        analysis_file = sys.argv[i + 1]
        i += 2
    else:
        json_file = arg
        i += 1

# Check if files exist
if not os.path.exists(json_file):
    print(f"Error: File not found: {json_file}")
    print(f"\nUsage: python create_pdf_reports.py <path_to_json_file> [--timestamp YYYYMMDD_HHMMSS] [--analysis <analysis_file>]")
    print(f"\nExamples:")
    print(f"  python create_pdf_reports.py venue_data.json")
    print(f"  python create_pdf_reports.py venue_data.json --timestamp 20260914_143022 --analysis ai_analysis_results.json")
    print(f"\nNote: First run 'python generate_venue_data.py <csv_file>' to create venue_data.json")
    sys.exit(1)

if analysis_file and not os.path.exists(analysis_file):
    print(f"Error: Analysis file not found: {analysis_file}")
    print(f"Run 'python run_analyze_venues.py venue_data.json' first to create it.")
    sys.exit(1)

print(f"Reading data from: {json_file}")

# Load the venue data
with open(json_file, 'r') as f:
    venue_data = json.load(f)

# Load precomputed analysis if provided
precomputed_analysis = {}
if analysis_file:
    print(f"Reading analysis from: {analysis_file}")
    with open(analysis_file, 'r') as f:
        precomputed_analysis = json.load(f)

# Same registries create_html_reports.py uses - see report_engine.py.
metrics_registry = report_engine.load_metrics_registry()

# PDF renders from its own template (venue-snapshot-pdf.html), not
# venue-snapshot-browser.html - see that file's docstring comment for why the
# layout is kept separate (section order/content differs by request, and
# reordering a shared template via print CSS turned out to fight with
# Chromium's print pagination). The analysis/metrics context passed in below
# is still built by the exact same report_content.py the HTML report uses,
# so the numbers and narrative always match - only this layout differs.
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=False)
report_template = jinja_env.get_template('venue-snapshot-pdf.html')

reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reports')
os.makedirs(reports_dir, exist_ok=True)


def write_pdf(page, html, filename, attempts=5):
    """Render html and save it to filename, retrying on a transient
    "Permission denied" write error.

    On Windows this almost always means something else briefly has the file
    open when Playwright tries to write it - most commonly antivirus/EDR
    real-time scanning grabbing a newly-written file for a moment (common on
    corporate machines), the PDF already being open in a viewer from a
    previous run, or a search-indexer/OneDrive-style sync lock. All of those
    are transient, so a short retry-with-backoff clears the great majority of
    them without the user needing to do anything. A pre-existing file at the
    same path is removed first (best-effort) in case a previous failed run
    left behind a partial/locked file of the same name.
    """
    try:
        if os.path.exists(filename):
            os.remove(filename)
    except OSError:
        pass  # Not fatal - page.pdf() below will surface the real problem if this matters.

    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            page.set_content(html, wait_until="load")
            page.pdf(
                path=filename,
                format="Letter",
                print_background=True,
                margin={"top": "0.4in", "bottom": "0.4in", "left": "0.4in", "right": "0.4in"},
            )
            return
        except PermissionError as e:
            last_error = e
        except Exception as e:
            # Playwright wraps some OS errors in its own Error type rather
            # than raising PermissionError directly - treat anything whose
            # message mentions a permission/access problem the same way.
            message = str(e).lower()
            if 'permission denied' in message or 'access is denied' in message or 'eperm' in message or 'ebusy' in message:
                last_error = e
            else:
                raise

        if attempt < attempts:
            wait_seconds = 0.5 * attempt
            print(f"  [retry] '{filename}' was locked (attempt {attempt}/{attempts}); retrying in {wait_seconds:.1f}s...")
            time.sleep(wait_seconds)

    raise RuntimeError(
        f"Could not write '{filename}' after {attempts} attempts - it stayed locked/inaccessible the whole time.\n"
        "Common causes on Windows: the file is currently open in a PDF viewer or browser tab, "
        "antivirus/endpoint-security software is scanning it, or a OneDrive-style sync client has it locked.\n"
        "Close anything that might have it open and re-run the command. If it keeps happening, try excluding "
        "the 'reports' folder from real-time antivirus scanning."
    ) from last_error

# Reused across all venues in this run - launching Chromium is the slow part,
# so one browser instance (with one page reused per venue) instead of one per
# venue keeps a multi-venue CSV fast.
try:
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as e:
            print(f"Error: could not launch headless Chromium: {e}")
            print("\nIf this is the first time generating PDFs, download the browser once with:")
            print("  playwright install chromium")
            sys.exit(1)

        page = browser.new_page()
        # Force print CSS (the @media print rules in venue-snapshot-browser.html)
        # rather than relying on page.pdf()'s implicit default, so this stays
        # correct even if that default ever changes.
        page.emulate_media(media="print")

        for venue_key in sorted(venue_data.keys()):
            data = venue_data[venue_key]
            venue_analysis = precomputed_analysis.get(venue_key) if precomputed_analysis else None
            html = report_content.render_html_report(data, metrics_registry, report_template, precomputed_analysis=venue_analysis)

            venue_name = data['venue']
            
            # Build filename with optional timestamp
            if timestamp:
                filename = os.path.join(
                    reports_dir, f"Topgolf_Venue_Report_{venue_name.replace(' ', '_')}_{timestamp}_snapshot.pdf"
                )
            else:
                filename = os.path.join(
                    reports_dir, f"Topgolf_Venue_Report_{venue_name.replace(' ', '_')}_snapshot.pdf"
                )

            write_pdf(page, html, filename)

            print(f"Generated: {filename}")

        page.close()
        browser.close()
except KeyboardInterrupt:
    raise
except Exception as e:
    print(f"\nUnexpected error generating PDFs: {e}")
    sys.exit(1)

print(f"\nPDF reports generated successfully! ({len(venue_data)} venue(s))")
