#!/usr/bin/env python3
"""
Generate Markdown venue reports from venue_data.json - the Markdown
counterpart to create_html_reports.py.

Uses the exact same analysis (AI-based, with keyword/metric fallback) and
metric-assessment context as the HTML report via report_content.py, so the
two formats never say something different about the same data. The only
thing this script does differently is content SHAPE, not content: the HTML
template expects inline HTML (`<strong>`, `<li>...</li>`) in ups/downs/
recommendation strings, while Markdown wants `**bold**` and plain bullet
text - see _to_markdown() below.
"""
import json
import re
import sys
import os

from jinja2 import Environment, FileSystemLoader

from ai_analysis import get_ai_analysis
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
    print(f"\nUsage: python create_markdown_reports.py <path_to_json_file>")
    print(f"\nExamples:")
    print(f"  python create_markdown_reports.py venue_data.json")
    print(f"\nNote: First run 'python generate_reports.py <csv_file>' to create venue_data.json")
    sys.exit(1)

print(f"Reading data from: {json_file}")

# Load the venue data
with open(json_file, 'r') as f:
    venue_data = json.load(f)

# Same registries create_html_reports.py uses - see report_engine.py.
metrics_registry = report_engine.load_metrics_registry()

# Jinja2 environment for the Markdown template. trim_blocks/lstrip_blocks
# keep the {% for %}/{% endfor %} control lines from leaving behind blank
# lines and stray leading whitespace in the rendered Markdown.
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)
report_template = jinja_env.get_template('venue-1page-report.md.j2')

_LI_TAG_RE = re.compile(r'</?li>')


def _to_markdown(html_fragment):
    """Convert the limited inline HTML that shows up in analysis text
    (`<strong>...</strong>` from both the AI and keyword-fallback paths, and
    `<li>...</li>` wrapping that the keyword-fallback path bakes in for
    report_engine.generate_recommendations()) into Markdown equivalents.

    This is the only HTML the analysis pipeline ever produces (see
    ai_analysis.ANALYSIS_SCHEMA_INSTRUCTIONS and report_engine.py), so a
    couple of targeted replacements are enough - no general HTML-to-Markdown
    conversion needed."""
    text = _LI_TAG_RE.sub('', html_fragment)
    text = text.replace('<strong>', '**').replace('</strong>', '**')
    return text.strip()


def get_markdown_analysis(data):
    """Same analysis as report_content.get_analysis(), converted to
    Markdown-safe text instead of the HTML-ready shape that function returns
    (its recommendation items are pre-wrapped in `<li>...</li>` for the HTML
    template). Calls the AI/fallback analysis directly rather than through
    report_content.get_analysis() so this script owns its own text shape."""
    ai_result = get_ai_analysis(data)
    if ai_result is not None:
        print(f"[analysis] Using AI-generated analysis for {data['venue']}")
        analysis = {
            'overview': ai_result['overview'],
            'ups': ai_result['ups'],
            'downs': ai_result['downs'],
            'impact': ai_result['impact'],
            'recommendations': ai_result['recommendations'],
        }
    else:
        print(f"[analysis] Using keyword-based fallback analysis for {data['venue']}")
        analysis = report_engine.generate_fallback_analysis(data)

    return {
        'overview': _to_markdown(analysis['overview']),
        'ups': [_to_markdown(item) for item in analysis['ups']],
        'downs': [_to_markdown(item) for item in analysis['downs']],
        'impact': [
            {'title': driver['title'], 'description': _to_markdown(driver['description'])}
            for driver in analysis['impact']
        ],
        'recommendations': {
            tier: {
                'title': analysis['recommendations'][tier]['title'],
                'items': [_to_markdown(item) for item in analysis['recommendations'][tier]['items']],
            }
            for tier in ('critical', 'secondary', 'maintain')
        },
    }


def generate_markdown_report(data):
    """Generate a complete Markdown report by rendering
    templates/venue-1page-report.md.j2 with this venue's data."""

    # Dates, metric displays, and assessments - identical to the HTML report.
    context = report_content.build_metrics_context(data, metrics_registry)

    analysis = get_markdown_analysis(data)
    recommendations = analysis['recommendations']

    context.update({
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

    return report_template.render(**context)


# Generate reports for all venues in the data
for venue_key in sorted(venue_data.keys()):
    data = venue_data[venue_key]
    markdown = generate_markdown_report(data)

    venue_name = data['venue']

    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    filename = os.path.join(reports_dir, f"Topgolf_Venue_Report_{venue_name.replace(' ', '_')}_1PAGE.md")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"Generated: {filename}")

print(f"\nMarkdown reports generated successfully! ({len(venue_data)} venue(s))")
