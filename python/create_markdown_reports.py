#!/usr/bin/env python3
"""
Generate Markdown venue reports from venue_data.json - the Markdown
counterpart to create_html_reports.py.

Uses the exact same AI analysis and metric-assessment context as the HTML
report via report_content.py, so the two formats never say something
different about the same data. The only thing this script does differently
is content SHAPE, not content: the HTML template expects inline HTML
(`<strong>`, `<li>...</li>`) in ups/downs/recommendation strings, while
Markdown wants `**bold**` and plain bullet text - see _to_markdown() below.

There is no keyword-based fallback narrative - if AI analysis isn't
available, the Markdown report says so (via the ai_unavailable /
ai_unavailable_message context, same as the HTML/PDF reports) and only
renders the metrics sections, which don't depend on AI.
"""
import json
import sys
import os

from jinja2 import Environment, FileSystemLoader

from analyze_venues import get_ai_analysis
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
    print(f"\nUsage: python create_markdown_reports.py <path_to_json_file> [--timestamp YYYYMMDD_HHMMSS] [--analysis <analysis_file>]")
    print(f"\nExamples:")
    print(f"  python create_markdown_reports.py venue_data.json")
    print(f"  python create_markdown_reports.py venue_data.json --timestamp 20260914_143022 --analysis ai_analysis_results.json")
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
report_template = jinja_env.get_template('venue-snapshot-report.md.j2')

def _to_markdown(html_fragment):
    """Convert the limited inline HTML the AI analysis produces
    (`<strong>...</strong>` only - see the "Formatting rules" section of
    .claude/single-venue-report/synthesis.md) into Markdown equivalents. A single
    targeted replacement is enough - no general HTML-to-Markdown conversion
    needed."""
    text = html_fragment.replace('<strong>', '**').replace('</strong>', '**')
    return text.strip()


def get_markdown_analysis(data, precomputed_analysis=None):
    """Same analysis as report_content.get_analysis(), converted to
    Markdown-safe text instead of the HTML-ready shape that function returns
    (its recommendation items are pre-wrapped in `<li>...</li>` for the HTML
    template). 
    
    If precomputed_analysis is provided, uses that instead of calling
    get_ai_analysis(). This allows multiple report formats to reuse the same
    analysis without re-running expensive API calls.

    Returns {'ai_available': False, 'unavailable_reason': str} unchanged
    (no Markdown conversion needed) when AI analysis isn't available."""
    
    # Use precomputed analysis if provided
    if precomputed_analysis is not None:
        if precomputed_analysis.get('ai_available'):
            print(f"[analysis] Using precomputed AI analysis for {data['venue']}")
            ai_result = precomputed_analysis['analysis']
        else:
            print(f"[analysis] AI analysis unavailable for {data['venue']}: {precomputed_analysis.get('unavailable_reason')}")
            return {'ai_available': False, 'unavailable_reason': precomputed_analysis.get('unavailable_reason', 'Unknown error')}
    else:
        # Fall back to computing analysis on-the-fly (for backward compatibility)
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


def generate_markdown_report(data, precomputed_analysis=None):
    """Generate a complete Markdown report by rendering
    templates/venue-snapshot-report.md.j2 with this venue's data.
    
    If precomputed_analysis is provided, it will be used instead of calling
    get_ai_analysis(). This allows multiple report formats to reuse the same
    analysis without re-running expensive API calls."""

    # Dates, metric displays, and assessments - identical to the HTML report.
    context = report_content.build_metrics_context(data, metrics_registry)

    analysis = get_markdown_analysis(data, precomputed_analysis=precomputed_analysis)

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

    return report_template.render(**context)


# Generate reports for all venues in the data
for venue_key in sorted(venue_data.keys()):
    data = venue_data[venue_key]
    venue_analysis = precomputed_analysis.get(venue_key) if precomputed_analysis else None
    markdown = generate_markdown_report(data, precomputed_analysis=venue_analysis)

    venue_name = data['venue']

    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Build filename with optional timestamp
    if timestamp:
        filename = os.path.join(reports_dir, f"Topgolf_Venue_Report_{venue_name.replace(' ', '_')}_{timestamp}_1PAGE.md")
    else:
        filename = os.path.join(reports_dir, f"Topgolf_Venue_Report_{venue_name.replace(' ', '_')}_1PAGE.md")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"Generated: {filename}")

print(f"\nMarkdown reports generated successfully! ({len(venue_data)} venue(s))")
