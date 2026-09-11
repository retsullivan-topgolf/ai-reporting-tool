#!/usr/bin/env python3
"""
Shared, format-agnostic report content: the analysis fetch (AI first, keyword
fallback second) and the metric-assessment/date/display context that both
create_html_reports.py and create_markdown_reports.py need.

Neither of the two output scripts should reimplement this logic - if HTML and
Markdown reports ever say something different about the same venue_data.json,
it's because one of them drifted from this module, not because the analysis
itself differs by output format.

get_analysis() returns the "HTML-ready" shape (recommendation items are
already `<li>...</li>` strings, matching what templates/venue-1page-browser.html
expects - see create_html_reports.py). create_markdown_reports.py calls the
same analysis functions independently and converts the inline HTML
(`<strong>`, `<li>`) to Markdown - see md_format.py.
"""
from datetime import datetime

from ai_analysis import get_ai_analysis
import report_engine


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
            "critical":  {"title": str, "items": ["<li>...</li>", ...]},
            "secondary": {"title": str, "items": ["<li>...</li>", ...]},
            "maintain":  {"title": str, "items": ["<li>...</li>", ...]},
          },
        }

    so callers never need to know which path produced it. Recommendation
    items are HTML `<li>` strings in this return value (ready to drop into
    the HTML template) - Markdown consumers should not call this function
    directly; see create_markdown_reports.py.
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


def build_metrics_context(data, metrics_registry):
    """Dates, metric displays, and assessments/status-classes shared by both
    output formats. Recommendation/ups/downs/impact content is NOT included
    here - see get_analysis() (HTML) or create_markdown_reports.py (Markdown),
    since the two formats need that content shaped differently."""
    start_date = data['date_range'][0]
    end_date = data['date_range'][1]
    start_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_obj = datetime.strptime(end_date, '%Y-%m-%d')

    ltr_assessment = report_engine.get_assessment('ltr', data['ltr_avg'], metrics_registry)
    fun_assessment = report_engine.get_assessment('fun', data['fun_avg'], metrics_registry)
    helpful_assessment = report_engine.get_assessment('helpful', data['helpful_avg'], metrics_registry)
    issues_assessment = report_engine.get_assessment('issues', data['issues_pct'], metrics_registry)
    resolution_assessment = report_engine.get_assessment('resolution', data['resolution_avg'], metrics_registry)

    return {
        'venue': data['venue'],
        'start_formatted': start_obj.strftime('%B %d, %Y'),
        'end_formatted': end_obj.strftime('%B %d, %Y'),
        'week_formatted': start_obj.strftime('%B %d, %Y'),
        'generated_date': datetime.now().strftime('%B %d, %Y'),

        'ltr_avg_display': f"{data['ltr_avg']:.1f}",
        'fun_avg_display': f"{data['fun_avg']:.1f}",
        'helpful_avg_display': f"{data['helpful_avg']:.1f}",
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

        # "good"/"moderate"/"poor"/"unknown" - only meaningful to the HTML
        # template's CSS classes, but harmless to compute unconditionally.
        'ltr_assessment_class': report_engine.get_assessment_class('ltr', data['ltr_avg'], metrics_registry),
        'fun_assessment_class': report_engine.get_assessment_class('fun', data['fun_avg'], metrics_registry),
        'helpful_assessment_class': report_engine.get_assessment_class('helpful', data['helpful_avg'], metrics_registry),
        'issues_assessment_class': report_engine.get_assessment_class('issues', data['issues_pct'], metrics_registry),
        'resolution_assessment_class': report_engine.get_assessment_class('resolution', data['resolution_avg'], metrics_registry),

        'overall_assessment': build_overall_assessment(data),
    }


def render_html_report(data, metrics_registry, template):
    """Render templates/venue-1page-browser.html for this venue's data.

    Used by both create_html_reports.py (writes the .html file directly) and
    create_pdf_reports.py (feeds this same HTML string into headless Chromium
    via Playwright). Routing the PDF through this exact function - not a
    second template or a re-derived context - is what keeps the PDF's
    styling/layout identical to the HTML report instead of a hand-maintained
    approximation of it.
    """
    context = build_metrics_context(data, metrics_registry)
    analysis = get_analysis(data)
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

    return template.render(**context)
