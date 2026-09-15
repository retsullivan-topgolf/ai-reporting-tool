#!/usr/bin/env python3
"""
Shared, format-agnostic report content: the AI analysis fetch and the
metric-assessment/date/display context that both create_html_reports.py and
create_markdown_reports.py need.

Neither of the two output scripts should reimplement this logic - if HTML and
Markdown reports ever say something different about the same venue_data.json,
it's because one of them drifted from this module, not because the analysis
itself differs by output format.

get_analysis() returns the "HTML-ready" shape (recommendation items are
already `<li>...</li>` strings, matching what templates/venue-1page-browser.html
expects - see create_html_reports.py). create_markdown_reports.py calls the
AI analysis independently and converts the inline HTML (`<strong>`, `<li>`)
to Markdown - see create_markdown_reports.py.

There is no keyword/metric-based fallback narrative any more. If the AI
analysis (ai_analysis.get_ai_analysis()) isn't available - CLI missing,
timed out, bad response, etc. - get_analysis() returns an "unavailable"
marker instead of substituting a differently-derived narrative, and callers
show that fact to the reader rather than fabricate a story. The metrics
sections (Performance Summary, Experience Metrics) never depend on AI at
all - see build_metrics_context() below - so those keep rendering normally
either way.
"""
import html
from datetime import datetime

from ai_analysis import get_ai_analysis
import report_engine


def _format_analysis_as_html(ai_result):
    """Convert raw AI analysis result to HTML-ready format with <li> items."""
    def as_list_items(items):
        return [f"<li>{item}</li>" for item in items]

    return {
        'ai_available': True,
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


def get_analysis(data, precomputed_analysis=None):
    """Get the overview/ups/downs/impact/recommendations content for a venue
    from the AI-based analysis (via Claude Code CLI) - it's the only source
    for this narrative, since it's the only one that actually reads the
    guest comments rather than just the aggregate metrics.

    If precomputed_analysis is provided (from a pre-generated analysis file),
    use that instead of calling get_ai_analysis(). This allows multiple report
    formats to reuse the same analysis without re-running expensive API calls.

    On success, returns:

        {
          "ai_available": True,
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

    Recommendation items are HTML `<li>` strings in this return value (ready
    to drop into the HTML template) - Markdown consumers should not call
    this function directly; see create_markdown_reports.py.

    When AI analysis isn't available, returns:

        {"ai_available": False, "unavailable_reason": str}

    and callers are expected to show unavailable_reason to the reader in
    place of the narrative sections.
    """
    # Use precomputed analysis if provided
    if precomputed_analysis is not None:
        if precomputed_analysis.get('ai_available'):
            print(f"[analysis] Using precomputed AI analysis for {data['venue']}")
            return _format_analysis_as_html(precomputed_analysis['analysis'])
        else:
            print(f"[analysis] AI analysis unavailable for {data['venue']}: {precomputed_analysis.get('unavailable_reason')}")
            return {
                'ai_available': False,
                'unavailable_reason': precomputed_analysis.get('unavailable_reason', 'Unknown error'),
            }
    
    # Fall back to computing analysis on-the-fly (for backward compatibility)
    ai_result, error = get_ai_analysis(data)
    if ai_result is not None:
        print(f"[analysis] Using AI-generated analysis for {data['venue']}")
        return _format_analysis_as_html(ai_result)

    print(f"[analysis] AI analysis unavailable for {data['venue']}: {error}")
    return {'ai_available': False, 'unavailable_reason': error}


UNAVAILABLE_MESSAGE_TEMPLATE = (
    "AI-generated analysis (venue overview, ups/downs, impact drivers, and "
    "recommendations) is not available for this report: {reason}. The metrics "
    "below come directly from this period's survey data and are unaffected."
)


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

    context = {
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

    # Add optional Return Likelihood and Price Value metrics (if present in data)
    if 'return_likelihood_avg' in data and data['return_likelihood_avg'] is not None:
        context['return_likelihood_avg_display'] = f"{data['return_likelihood_avg']:.1f}"
        context['return_likelihood_assessment'] = report_engine.get_assessment('return_likelihood', data['return_likelihood_avg'], metrics_registry)
        context['return_likelihood_assessment_class'] = report_engine.get_assessment_class('return_likelihood', data['return_likelihood_avg'], metrics_registry)

    if 'price_value_avg' in data and data['price_value_avg'] is not None:
        context['price_value_avg_display'] = f"{data['price_value_avg']:.1f}"
        context['price_value_assessment'] = report_engine.get_assessment('price_value', data['price_value_avg'], metrics_registry)
        context['price_value_assessment_class'] = report_engine.get_assessment_class('price_value', data['price_value_avg'], metrics_registry)

    # Add optional F&B metrics (if present in data)
    fb_metrics = ['food_value', 'food_speed', 'food_quality', 'beverage_value', 'beverage_speed', 'beverage_quality']
    fb_values = []
    for metric in fb_metrics:
        data_field = f'{metric}_avg'
        if data_field in data and data[data_field] is not None:
            context[f'{metric}_avg_display'] = f"{data[data_field]:.1f}"
            context[f'{metric}_assessment'] = report_engine.get_assessment(metric, data[data_field], metrics_registry)
            context[f'{metric}_assessment_class'] = report_engine.get_assessment_class(metric, data[data_field], metrics_registry)
            fb_values.append(data[data_field])

    # Calculate F&B Average if we have any F&B metrics
    if fb_values:
        fb_average = sum(fb_values) / len(fb_values)
        context['fb_average'] = fb_average
        context['fb_average_display'] = f"{fb_average:.1f}"
        context['fb_average_assessment'] = report_engine.get_assessment('fb_average', fb_average, metrics_registry)
        context['fb_average_assessment_class'] = report_engine.get_assessment_class('fb_average', fb_average, metrics_registry)

    return context


def render_html_report(data, metrics_registry, template, precomputed_analysis=None):
    """Render templates/venue-1page-browser.html for this venue's data.

    Used by both create_html_reports.py (writes the .html file directly) and
    create_pdf_reports.py (feeds this same HTML string into headless Chromium
    via Playwright). Routing the PDF through this exact function - not a
    second template or a re-derived context - is what keeps the PDF's
    styling/layout identical to the HTML report instead of a hand-maintained
    approximation of it.
    
    If precomputed_analysis is provided, it will be used instead of calling
    get_ai_analysis(). This allows multiple report formats to reuse the same
    analysis without re-running expensive API calls.
    """
    context = build_metrics_context(data, metrics_registry)
    analysis = get_analysis(data, precomputed_analysis=precomputed_analysis)

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
        # The reason string ultimately comes from a subprocess's stderr (see
        # ai_analysis.py) - not attacker-controlled, but not guaranteed
        # HTML-safe either (e.g. a raw "<" from a CLI usage hint). The
        # Jinja environments here run with autoescape=False, so this is the
        # only place anything gets escaped before landing in the page - do
        # it explicitly rather than relying on the text never containing a
        # stray "<" or "&".
        context.update({
            'ai_unavailable': True,
            'ai_unavailable_message': UNAVAILABLE_MESSAGE_TEMPLATE.format(
                reason=html.escape(analysis['unavailable_reason'])
            ),
        })

    return template.render(**context)
