#!/usr/bin/env python3
import json
from datetime import datetime
import sys
import os

from jinja2 import Environment, FileSystemLoader

from ai_analysis import get_ai_analysis
import report_engine

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


def get_analysis(data):
    """Get the overview/ups/downs/impact/recommendations content for a venue.

    Tries the AI-based analysis (via Claude Code CLI) first, since it actually
    reads the guest comments instead of just the aggregate metrics. Falls back
    to the keyword/metric-based heuristics in report_engine.py if the AI
    analysis isn't available. Either way, returns the same shape:

        {
          "overview": str,
          "ups": [str, ...],
          "downs": [str, ...],
          "impact": [{"title": str, "description": str}, ...],
          "recommendations": {
            "critical":  {"title": str, "items": [str, ...]},
            "secondary": {"title": str, "items": [str, ...]},
            "maintain":  {"title": str, "items": [str, ...]},
          },
        }

    so generate_html_report() never needs to know which path produced it.
    """
    ai_result = get_ai_analysis(data)
    if ai_result is not None:
        print(f"[analysis] Using AI-generated analysis for {data['venue']}")

        def as_list_items(items):
            return [f"<li>{item}</li>" for item in items]

        return {
            'overview': ai_result['overview'],
            'ups': ai_result['ups'],
            'downs': ai_result['downs'],
            'impact': ai_result['impact'],
            'recommendations': {
                tier: {
                    'title': ai_result['recommendations'][tier]['title'],
                    'items': as_list_items(ai_result['recommendations'][tier]['items']),
                }
                for tier in ('critical', 'secondary', 'maintain')
            },
        }

    print(f"[analysis] Using keyword-based fallback analysis for {data['venue']}")
    return report_engine.generate_fallback_analysis(data)


def build_overall_assessment(data):
    """One-sentence roll-up shown in the Performance Summary highlight box."""
    performance_word = 'strong' if data['ltr_avg'] >= 7.0 else 'moderate'
    fun_word = 'excellent' if data['fun_avg'] >= 4.0 else 'good'
    closing = (
        'Equipment reliability is a key concern affecting guest satisfaction.'
        if data['issues_pct'] > 50
        else 'The venue maintains good operational consistency.'
    )
    return (
        f"{data['venue']} demonstrates {performance_word} performance with "
        f"{fun_word} entertainment value. {closing}"
    )


def generate_html_report(venue_key, data):
    """Generate complete HTML report by rendering the shared Jinja2 template
    (templates/venue-1page-browser.html) with this venue's data."""

    # Calculate dates
    start_date = data['date_range'][0]
    end_date = data['date_range'][1]
    start_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_obj = datetime.strptime(end_date, '%Y-%m-%d')

    start_formatted = start_obj.strftime('%B %d, %Y')
    end_formatted = end_obj.strftime('%B %d, %Y')
    week_formatted = start_obj.strftime('%B %d, %Y')

    # Generate content (AI-based analysis of guest comments, with keyword-based fallback)
    analysis = get_analysis(data)
    recommendations = analysis['recommendations']

    # Assessments (Excellent/Strong/Moderate/Weak, etc) judge each metric
    # against a fixed quality bar for that metric - not against other venues.
    # There's deliberately no network-benchmark comparison here: an individual
    # venue report is usually generated from a single venue's data, so a
    # "network average" would often be stale or fictional for whatever CSV
    # was actually processed. See templates/metrics.json for more on why, and
    # templates/REPORT_TEMPLATES_VENUE_RANKINGS.md for the report type where
    # cross-venue comparison does belong.
    ltr_assessment = report_engine.get_assessment('ltr', data['ltr_avg'], metrics_registry)
    fun_assessment = report_engine.get_assessment('fun', data['fun_avg'], metrics_registry)
    helpful_assessment = report_engine.get_assessment('helpful', data['helpful_avg'], metrics_registry)
    issues_assessment = report_engine.get_assessment('issues', data['issues_pct'], metrics_registry)
    resolution_assessment = report_engine.get_assessment('resolution', data['resolution_avg'], metrics_registry)

    # Status-pill CSS class ("good"/"moderate"/"poor") for each assessment -
    # this is what actually varies by venue; previously these cards/table used
    # a hardcoded class regardless of the venue's real numbers.
    ltr_assessment_class = report_engine.get_assessment_class('ltr', data['ltr_avg'], metrics_registry)
    fun_assessment_class = report_engine.get_assessment_class('fun', data['fun_avg'], metrics_registry)
    helpful_assessment_class = report_engine.get_assessment_class('helpful', data['helpful_avg'], metrics_registry)
    issues_assessment_class = report_engine.get_assessment_class('issues', data['issues_pct'], metrics_registry)
    resolution_assessment_class = report_engine.get_assessment_class('resolution', data['resolution_avg'], metrics_registry)

    context = {
        'venue': data['venue'],
        'start_formatted': start_formatted,
        'end_formatted': end_formatted,
        'week_formatted': week_formatted,
        'generated_date': datetime.now().strftime('%B %d, %Y'),

        'overview': analysis['overview'],

        'ltr_avg_display': f"{data['ltr_avg']:.1f}",
        'fun_avg_display': f"{data['fun_avg']:.1f}",
        'helpful_avg_display': f"{data['helpful_avg']:.1f}",
        # resolution_avg is None when no guests reported issues (nobody was
        # asked the resolution question) - "N/A", not a 0/5 score.
        'resolution_avg_display': (
            "N/A" if data['resolution_avg'] is None else f"{data['resolution_avg']:.1f} / 5"
        ),
        'issues_pct_card_display': f"{data['issues_pct']:.0f}%",
        'issues_pct_table_display': f"{data['issues_pct']:.1f}%",

        'ltr_assessment': ltr_assessment,
        'fun_assessment': fun_assessment,
        'helpful_assessment': helpful_assessment,
        'issues_assessment': issues_assessment,
        'resolution_assessment': resolution_assessment,

        # "good"/"moderate"/"poor". The template composes this two different
        # ways: "status-pill <word>" for the Experience Metrics table pills,
        # and "status-<word>" for the Performance Summary cards (two
        # different CSS conventions already defined in the stylesheet).
        'ltr_assessment_class': ltr_assessment_class,
        'fun_assessment_class': fun_assessment_class,
        'helpful_assessment_class': helpful_assessment_class,
        'issues_assessment_class': issues_assessment_class,
        'resolution_assessment_class': resolution_assessment_class,

        'overall_assessment': build_overall_assessment(data),

        'ups': analysis['ups'],
        'downs': analysis['downs'],
        'impact': analysis['impact'],

        'critical_title': recommendations['critical']['title'],
        'critical_items': recommendations['critical']['items'],
        'secondary_title': recommendations['secondary']['title'],
        'secondary_items': recommendations['secondary']['items'],
        'maintain_title': recommendations['maintain']['title'],
        'maintain_items': recommendations['maintain']['items'],
    }

    return report_template.render(**context)

# Generate reports for all venues in the data
for venue_key in sorted(venue_data.keys()):
    data = venue_data[venue_key]
    html = generate_html_report(venue_key, data)

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
