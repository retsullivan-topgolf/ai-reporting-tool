#!/usr/bin/env python3
"""
Generate single-venue snapshot reports in HTML, Markdown, and/or PDF formats.

This unified script consolidates the functionality of create_html_reports.py,
create_markdown_reports.py, and create_pdf_reports.py into a single entry point
that handles all three formats.

Usage:
    python create_single_venue_snapshot_report.py <venue_data.json> [--format html|markdown|pdf|all] [--timestamp YYYYMMDD_HHMMSS] [--analysis <analysis_file>]

Examples:
    python create_single_venue_snapshot_report.py venue_data.json
    python create_single_venue_snapshot_report.py venue_data.json --format all
    python create_single_venue_snapshot_report.py venue_data.json --format html,pdf --timestamp 20260914_143022 --analysis ai_analysis_results.json
"""
import json
import sys
import os
import time

from jinja2 import Environment, FileSystemLoader

from analyze_venues import get_ai_analysis
import report_engine
import report_content

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    # Playwright is optional - only needed for PDF generation
    sync_playwright = None

# Parse command line arguments
json_file = 'venue_data.json'
timestamp = None
analysis_file = None
formats = None

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
    elif arg == '--format':
        if i + 1 >= len(sys.argv):
            print("Error: --format requires a value")
            sys.exit(1)
        formats = sys.argv[i + 1].split(',')
        i += 2
    else:
        json_file = arg
        i += 1

# Default to all formats if not specified
if not formats:
    formats = ['html', 'markdown', 'pdf']

# Normalize format names
formats = [f.strip().lower() for f in formats]

# Handle format shortcuts
if len(formats) == 1:
    if formats[0] == 'all':
        formats = ['html', 'markdown', 'pdf']
    elif formats[0] == 'both':  # legacy alias for html+markdown
        formats = ['html', 'markdown']

# Validate formats
valid_formats = {'html', 'markdown', 'pdf'}
for fmt in formats:
    if fmt not in valid_formats:
        print(f"Error: invalid format '{fmt}'. Must be one of: html, markdown, pdf, all")
        sys.exit(1)

# Check if files exist
if not os.path.exists(json_file):
    print(f"Error: File not found: {json_file}")
    print(f"\nUsage: python create_single_venue_snapshot_report.py <path_to_json_file> [--format html|markdown|pdf|all] [--timestamp YYYYMMDD_HHMMSS] [--analysis <analysis_file>]")
    print(f"\nExamples:")
    print(f"  python create_single_venue_snapshot_report.py venue_data.json")
    print(f"  python create_single_venue_snapshot_report.py venue_data.json --format all")
    print(f"  python create_single_venue_snapshot_report.py venue_data.json --format html,pdf --timestamp 20260914_143022 --analysis ai_analysis_results.json")
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

# Metric assessment thresholds live in templates/metrics.json
metrics_registry = report_engine.load_metrics_registry()

# Jinja2 environment for templates
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=False)

# Markdown-specific environment with trim_blocks/lstrip_blocks
jinja_env_markdown = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)

# Register strftime filter for date formatting in templates
def strftime_filter(value, format_str):
    from datetime import datetime
    if isinstance(value, str) and value.lower() == 'now':
        return datetime.now().strftime(format_str)
    elif isinstance(value, datetime):
        return value.strftime(format_str)
    return str(value)

jinja_env.filters['strftime'] = strftime_filter
jinja_env_markdown.filters['strftime'] = strftime_filter

# Reports directory
reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reports')
os.makedirs(reports_dir, exist_ok=True)


def _to_markdown(html_fragment):
    """Convert limited inline HTML to Markdown equivalents."""
    text = html_fragment.replace('<strong>', '**').replace('</strong>', '**')
    return text.strip()


def get_markdown_analysis(data, precomputed_analysis=None):
    """Get AI analysis in Markdown format."""
    if precomputed_analysis is not None:
        if precomputed_analysis.get('ai_available'):
            print(f"[analysis] Using precomputed AI analysis for {data['venue']}")
            ai_result = precomputed_analysis['analysis']
        else:
            print(f"[analysis] AI analysis unavailable for {data['venue']}: {precomputed_analysis.get('unavailable_reason')}")
            return {'ai_available': False, 'unavailable_reason': precomputed_analysis.get('unavailable_reason', 'Unknown error')}
    else:
        ai_result, error = get_ai_analysis(data)
        if ai_result is None:
            print(f"[analysis] AI analysis unavailable for {data['venue']}: {error}")
            return {'ai_available': False, 'unavailable_reason': error}
        print(f"[analysis] Using AI-generated analysis for {data['venue']}")
    
    return {
        'ai_available': True,
        'overview': _to_markdown(ai_result['overview']),
        'ups': [_to_markdown(item) for item in ai_result['ups']],
        'downs': [_to_markdown(item) for item in ai_result['downs']],
        'impact': [
            {'title': driver['title'], 'description': _to_markdown(driver['description'])}
            for driver in ai_result['impact']
        ],
        'recommendations': {
            tier: {
                'title': ai_result['recommendations'][tier]['title'],
                'items': [_to_markdown(item) for item in ai_result['recommendations'][tier]['items']],
            }
            for tier in ('critical', 'secondary', 'maintain')
        },
    }


def write_pdf(page, html, filename, attempts=5):
    """Render HTML to PDF with retry logic for transient lock errors."""
    try:
        if os.path.exists(filename):
            os.remove(filename)
    except OSError:
        pass

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
        "Close anything that might have it open and re-run the command."
    ) from last_error


# Generate reports for all venues
for venue_key in sorted(venue_data.keys()):
    data = venue_data[venue_key]
    venue_name = data['venue']
    venue_analysis = precomputed_analysis.get(venue_key) if precomputed_analysis else None

    # Build filename base
    if timestamp:
        filename_base = os.path.join(reports_dir, f"Topgolf_Venue_Report_{venue_name.replace(' ', '_')}_{timestamp}_1PAGE")
    else:
        filename_base = os.path.join(reports_dir, f"Topgolf_Venue_Report_{venue_name.replace(' ', '_')}_1PAGE")

    # Generate HTML
    if 'html' in formats:
        html_template = jinja_env.get_template('venue-snapshot-browser.html')
        html = report_content.render_html_report(data, metrics_registry, html_template, precomputed_analysis=venue_analysis)
        html_filename = f"{filename_base}.html"
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Generated: {html_filename}")

    # Generate Markdown
    if 'markdown' in formats:
        md_template = jinja_env_markdown.get_template('venue-snapshot-report.md.j2')
        context = report_content.build_metrics_context(data, metrics_registry)
        analysis = get_markdown_analysis(data, precomputed_analysis=venue_analysis)
        
        if analysis['ai_available']:
            recommendations = analysis['recommendations']
            context.update({
                'ai_unavailable': False,
                'overview': analysis['overview'],
                'ups': analysis['ups'],
                'downs': analysis['downs'],
                'impact': analysis['impact'],
                'critical_title': recommendations['critical']['title'],
                'critical_items': recommendations['critical']['items'],
                'secondary_title': recommendations['secondary']['title'],
                'secondary_items': recommendations['secondary']['items'],
                'maintain_title': recommendations['maintain']['title'],
                'maintain_items': recommendations['maintain']['items'],
            })
        else:
            context.update({
                'ai_unavailable': True,
                'ai_unavailable_message': report_content.UNAVAILABLE_MESSAGE_TEMPLATE.format(
                    reason=analysis['unavailable_reason']
                ),
            })
        
        markdown = md_template.render(**context)
        md_filename = f"{filename_base}.md"
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"Generated: {md_filename}")

    # Generate PDF
    if 'pdf' in formats:
        if sync_playwright is None:
            print("Warning: Skipping PDF generation - 'playwright' package not installed.")
            print("Install with: pip install playwright && playwright install chromium")
        else:
            try:
                with sync_playwright() as p:
                    try:
                        browser = p.chromium.launch()
                    except Exception as e:
                        print(f"Error: could not launch headless Chromium: {e}")
                        print("Download the browser with: playwright install chromium")
                        sys.exit(1)

                    page = browser.new_page()
                    page.emulate_media(media="print")

                    pdf_template = jinja_env.get_template('venue-snapshot-pdf.html')
                    html = report_content.render_html_report(data, metrics_registry, pdf_template, precomputed_analysis=venue_analysis)
                    pdf_filename = f"{filename_base}.pdf"
                    write_pdf(page, html, pdf_filename)

                    page.close()
                    browser.close()
                    print(f"Generated: {pdf_filename}")
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"Error generating PDF for {venue_name}: {e}")
                sys.exit(1)

print(f"\nReports generated successfully! ({len(venue_data)} venue(s))")
