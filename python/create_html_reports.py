#!/usr/bin/env python3
import json
import sys
import os

from jinja2 import Environment, FileSystemLoader

import report_engine
import report_content

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
    print(f"\nUsage: python create_html_reports.py <path_to_json_file> [--timestamp YYYYMMDD_HHMMSS] [--analysis <analysis_file>]")
    print(f"\nExamples:")
    print(f"  python create_html_reports.py venue_data.json")
    print(f"  python create_html_reports.py venue_data.json --timestamp 20260914_143022 --analysis ai_analysis_results.json")
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

# Metric assessment thresholds live in templates/metrics.json - see
# report_engine.py for how they're interpreted. Edit that file to tune a
# threshold; this script should not need a code change for that.
metrics_registry = report_engine.load_metrics_registry()

# Jinja2 environment for the single-source-of-truth HTML template. The
# template lives in ../templates/venue-snapshot-browser.html so it can also be
# opened directly to preview markup/CSS changes (it renders with Jinja
# placeholders visible when opened raw - render a real report to preview it
# with data).
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=False)
report_template = jinja_env.get_template('venue-snapshot-browser.html')


# Generate reports for all venues in the data
for venue_key in sorted(venue_data.keys()):
    data = venue_data[venue_key]
    # Dates, metric displays, assessments, and the AI analysis all live in
    # report_content.py so create_pdf_reports.py can render the identical
    # HTML (see render_html_report()'s docstring).
    venue_analysis = precomputed_analysis.get(venue_key) if precomputed_analysis else None
    html = report_content.render_html_report(data, metrics_registry, report_template, precomputed_analysis=venue_analysis)

    # Convert key back to proper venue name (e.g., 'dallas' -> 'Dallas')
    venue_name = data['venue']

    # Save to file (in reports folder)
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Build filename with optional timestamp
    if timestamp:
        filename = os.path.join(reports_dir, f"Topgolf_Venue_Report_{venue_name.replace(' ', '_')}_{timestamp}_snapshot.html")
    else:
        filename = os.path.join(reports_dir, f"Topgolf_Venue_Report_{venue_name.replace(' ', '_')}_snapshot.html")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated: {filename}")

print(f"\nReports generated successfully! ({len(venue_data)} venue(s))")
