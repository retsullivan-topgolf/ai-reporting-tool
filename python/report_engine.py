#!/usr/bin/env python3
"""
Metric assessment logic shared by the HTML/PDF/Markdown report builders.

This module reads templates/metrics.json - one entry per Performance
Summary / Experience Metrics row: higher-is-better direction and assessment
thresholds (Excellent/Strong/Moderate/Weak, etc), each with its own
status-pill color. Deliberately has no network benchmark - see the file's
_no_benchmark_comment for why individual venue reports don't compare a venue
against "the network."

Edit templates/metrics.json to tune a threshold; this module is the only
place that knows how to interpret it, so create_html_reports.py /
create_pdf_reports.py / create_markdown_reports.py never need a code change
for that.

Note: this module used to also hold a keyword/metric-driven "fallback"
narrative generator (overview/ups/downs/impact/recommendations, driven by
templates/drivers.json) that ran whenever the AI analysis in ai_analysis.py
was unavailable. That fallback has been removed - when AI analysis isn't
available, reports now say so plainly instead of substituting a
differently-derived narrative that could disagree with what the AI path
would have said. See report_content.get_analysis(). templates/drivers.json
is no longer read by any code but has been left in place in case its content
is useful again later (e.g. as a reference for tuning the AI prompt).
"""
import json
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')


def _load_json(filename):
    path = os.path.join(TEMPLATE_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_metrics_registry():
    return _load_json('metrics.json')


# ---------------------------------------------------------------------------
# Metric assessment (Performance Summary + Experience Metrics sections).
# Driven entirely by templates/metrics.json. Judges a venue's own score
# against a fixed quality bar for that metric - not against other venues, so
# this works the same whether the report was generated from one venue's data
# or a full network pull. Independent of AI analysis availability - these
# tables always render from the raw metrics.
# ---------------------------------------------------------------------------

def _assessment_tier(metric_key, value, metrics_registry):
    """Shared lookup for get_assessment/get_assessment_class - kept as one
    function so the two can never disagree on which tier a value falls into."""
    thresholds = metrics_registry[metric_key]['assessment_thresholds']
    higher_is_better = metrics_registry[metric_key]['higher_is_better']
    if higher_is_better:
        for tier in thresholds:
            if tier['min'] is None or value >= tier['min']:
                return tier
    else:
        for tier in thresholds:
            if tier['max'] is None or value < tier['max']:
                return tier
    # Thresholds should always end in a None catch-all; this is a config
    # error, not a data condition, so fail loudly rather than guess.
    raise ValueError(f"No assessment tier matched for metric '{metric_key}' value {value}")


def get_assessment(metric_key, value, metrics_registry):
    """Return the assessment level (e.g. 'Excellent', 'Weak') for a metric
    value, per that metric's assessment_thresholds in metrics.json.

    value may be None (e.g. resolution_avg for a venue with no reported
    issues, so nobody answered the resolution question) - that's "N/A", not
    a data point to score against the thresholds."""
    if value is None:
        return "N/A"
    return _assessment_tier(metric_key, value, metrics_registry)['level']


def get_assessment_class(metric_key, value, metrics_registry):
    """CSS class ('good'/'moderate'/'poor'/'unknown') for the status pill,
    per that same tier's 'class' in metrics.json. See get_assessment() re:
    value=None."""
    if value is None:
        return "unknown"
    return _assessment_tier(metric_key, value, metrics_registry)['class']
