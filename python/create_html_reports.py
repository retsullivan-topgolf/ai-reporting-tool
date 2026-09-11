#!/usr/bin/env python3
import json
import sys
import os

from jinja2 import Environment, FileSystemLoader

import report_engine
import report_content

# Get JSON file from command line argument or use default
if len(sys.argv) > 1:
    json_file = sys.argv[1]
else:
    json_file = 'venue_data.json'

# Check if file exists
if not os.path.exists(json_file):
    print(f"Error: File not found: {json_file}")
    print(f"\nUsage: python create_html_reports.py <path_to_json_file>")
    print(f"\nExamples:")
    print(f"  python create_html_reports.py venue_data.json")
    print(f"\nNote: First run 'python generate_reports.py <csv_file>' to create venue_data.json")
    sys.exit(1)

print(f"Reading data from: {json_file}")

# Load the venue data
with open(json_file, 'r') as f:
    venue_data = json.load(f)

# Metric assessment thresholds and the keyword/metric-driven fallback content
# (used when AI analysis is unavailable) all live in templates/metrics.json
# and templates/drivers.json - see report_engine.py for how they're
# interpreted. Edit those files to tune a threshold or add a new theme; this
# script should not need a code change for that.
metrics_registry = report_engine.load_metrics_registry()

# Jinja2 environment for the single-source-of-truth HTML template. The
# template lives in ../templates/venue-1page-browser.html so it can also be
# opened directly to preview markup/CSS changes (it renders with Jinja
# placeholders visible when opened raw - render a real report to preview it
# with data).
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=False)
report_template = jinja_env.get_template('venue-1page-browser.html')


# Generate reports for all venues in the data
for venue_key in sorted(venue_data.keys()):
    data = venue_data[venue_key]
    # Dates, metric displays, assessments, and the AI/keyword-fallback
    # analysis all live in report_content.py so create_pdf_reports.py can
    # render the identical HTML (see render_html_report()'s docstring).
    html = report_content.render_html_report(data, metrics_registry, report_template)

    # Convert key back to proper venue name (e.g., 'dallas' -> 'Dallas')
    venue_name = data['venue']

    # Save to file (in reports folder)
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    filename = os.path.join(reports_dir, f"Topgolf_Venue_Report_{venue_name.replace(' ', '_')}_1PAGE.html")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated: {filename}")

print(f"\nReports generated successfully! ({len(venue_data)} venue(s))")
