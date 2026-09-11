#!/usr/bin/env python3
"""
Data-driven engine for the keyword-based fallback analysis and the metric
assessment/status logic used by create_html_reports.py.

This module exists so that adding or tuning a theme (a new game launch, a
recurring complaint, a new metric) means editing the JSON registries in
templates/ - not adding another `if/elif` branch duplicated across several
Python functions. It reads two files:

- templates/metrics.json - one entry per Performance Summary / Experience
  Metrics row: higher-is-better direction and assessment thresholds
  (Excellent/Strong/Moderate/Weak, etc), each with its own status-pill color.
  Deliberately has no network benchmark - see the file's _no_benchmark_comment
  for why individual venue reports don't compare a venue against "the
  network."
- templates/drivers.json - one entry per narrative "driver" (a keyword theme
  like parking, or a metric-based signal like low resolution scores): how to
  detect it, how to score it for ranking, and what copy to render in the
  Ups/Downs cards, the Impact ranking, and the Recommendations section.

Both are plain data. This module is the only place that knows how to
interpret them; create_html_reports.py just calls generate_fallback_analysis()
and gets back a dict in the same shape ai_analysis.get_ai_analysis() returns:

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

so create_html_reports.py never needs to know which path produced it.
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


def load_driver_registry():
    return _load_json('drivers.json')


# ---------------------------------------------------------------------------
# Metric assessment (Performance Summary + Experience Metrics sections).
# Driven entirely by templates/metrics.json. Judges a venue's own score
# against a fixed quality bar for that metric - not against other venues, so
# this works the same whether the report was generated from one venue's data
# or a full network pull.
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


# ---------------------------------------------------------------------------
# Driver evaluation (keyword theme detection, scoring, ups/downs/impact/
# recommendations). Driven entirely by templates/drivers.json.
# ---------------------------------------------------------------------------

def build_theme_map(data, driver_registry):
    """Bucket guest comments by keyword-based driver id, e.g. {'parking': [...
    matching comments], 'sonic': [...]}. Only drivers with a 'keywords' list
    participate; a comment can match more than one driver."""
    theme_map = {d['id']: [] for d in driver_registry['drivers'] if 'keywords' in d}
    for comment in data.get('comments', []):
        text = comment['text'].lower()
        for driver in driver_registry['drivers']:
            keywords = driver.get('keywords')
            if not keywords:
                continue
            if any(keyword in text for keyword in keywords):
                theme_map[driver['id']].append(comment)
    return theme_map


def _eval_metric_compare(cond, data):
    field, op, value = cond['field'], cond['op'], cond['value']
    actual = data[field]
    if actual is None:
        # Unknown (e.g. resolution_avg when nobody answered the resolution
        # question) can't satisfy any comparison - a driver that depends on
        # it simply doesn't fire, rather than crashing or guessing.
        return False
    if op == '>':
        return actual > value
    if op == '>=':
        return actual >= value
    if op == '<':
        return actual < value
    if op == '<=':
        return actual <= value
    if op == '==':
        return actual == value
    raise ValueError(f"Unknown comparison operator '{op}' in drivers.json")


def _eval_detect(driver, data, theme_map):
    detect = driver.get('detect')
    if detect is None:
        return False, None
    dtype = detect['type']
    if dtype == 'keyword_theme':
        comments = theme_map.get(driver['id'], [])
        min_count = detect.get('min_count', 1)
        return len(comments) >= min_count, len(comments)
    if dtype == 'metric_compare':
        return _eval_metric_compare(detect, data), None
    if dtype == 'all':
        return all(_eval_metric_compare(c, data) for c in detect['conditions']), None
    if dtype == 'any':
        return any(_eval_metric_compare(c, data) for c in detect['conditions']), None
    raise ValueError(f"Unknown detect type '{dtype}' in drivers.json")


def _eval_score(driver, data, theme_count, total_responses):
    score = driver.get('score')
    if score is None:
        return 0.0
    stype = score['type']
    if stype == 'keyword_count_pct':
        return (theme_count or 0) / total_responses * 100
    if stype in ('field_value', 'metric_gap_pct', 'metric_ratio_pct') and data.get(score['field']) is None:
        # Should only happen if a driver's own detect condition didn't
        # already rule this out (see _eval_metric_compare) - treat an
        # unknown field as "no signal" rather than crashing.
        return 0.0
    if stype == 'field_value':
        return float(data[score['field']])
    if stype == 'metric_gap_pct':
        target = score['target']
        return (target - data[score['field']]) / target * 100 if target else 0.0
    if stype == 'metric_ratio_pct':
        return data[score['field']] / score['max'] * 100
    raise ValueError(f"Unknown score type '{stype}' in drivers.json")


def _render_context(data, theme_count):
    context = dict(data)
    context['theme_count'] = theme_count or 0
    total_responses = data.get('responses') or 1
    context['theme_pct'] = (theme_count or 0) / total_responses * 100
    return context


def _render(template, context):
    return template.format(**context)


def evaluate_drivers(data, driver_registry):
    """Evaluate every driver against this venue's data once, up front. Each
    result carries everything downstream ups/downs/impact/recommendations
    generation needs, so those functions never touch raw thresholds."""
    theme_map = build_theme_map(data, driver_registry)
    total_responses = data.get('responses') or 1
    results = []
    for driver in driver_registry['drivers']:
        active, theme_count = _eval_detect(driver, data, theme_map)
        score = _eval_score(driver, data, theme_count, total_responses) if active else 0.0
        context = _render_context(data, theme_count)
        results.append({
            'driver': driver,
            'active': active,
            'score': score,
            'context': context,
        })
    return results, theme_map


def _down_bullet_text(driver, context):
    if 'down_bullet_tiers' in driver:
        score = context.get('issues_pct')  # tiers are currently only used by 'equipment'
        for tier in sorted(driver['down_bullet_tiers'], key=lambda t: t['min_score'], reverse=True):
            if score >= tier['min_score']:
                return _render(tier['text'], context)
        return None
    if 'down_bullet' in driver:
        return _render(driver['down_bullet'], context)
    return None


def generate_ups(evaluated, fallbacks):
    candidates = [e for e in evaluated if e['active'] and 'up_bullet' in e['driver']]
    candidates.sort(key=lambda e: e['driver'].get('ups_priority', 999))
    ups = [_render(e['driver']['up_bullet'], e['context']) for e in candidates[:3]]
    if not ups:
        ups = [fallbacks['ups_empty']]
    return ups


def generate_downs(evaluated, fallbacks):
    candidates = [e for e in evaluated if e['active'] and
                  ('down_bullet' in e['driver'] or 'down_bullet_tiers' in e['driver'])]
    candidates.sort(key=lambda e: e['driver'].get('downs_priority', 999))
    downs = []
    for e in candidates[:3]:
        text = _down_bullet_text(e['driver'], e['context'])
        if text:
            downs.append(text)
    return downs


def generate_impact_and_candidates(evaluated):
    """Returns (impact_top3, all_candidates). all_candidates (not just the
    top 3 shown in the Impact section) is what Recommendations ranks against,
    matching the original heuristic's behavior."""
    primary = [e for e in evaluated if e['active'] and e['driver'].get('impact_priority') == 'primary']
    candidates = list(primary)
    if len(candidates) < 3:
        filler = [e for e in evaluated if e['active'] and e['driver'].get('impact_priority') == 'filler']
        candidates += filler
    candidates.sort(key=lambda e: e['score'], reverse=True)

    impact_top3 = []
    for e in candidates[:3]:
        driver = e['driver']
        impact_top3.append({
            'title': driver['label'],
            'description': _render(driver['impact_description'], e['context']),
        })
    return impact_top3, candidates


def _items_to_li(items, context):
    return [f"<li><strong>{item['label']}:</strong> {_render(item['description'], context)}</li>" for item in items]


def generate_recommendations(candidates, fallbacks):
    negatives = [e for e in candidates if e['driver']['polarity'] == 'negative']
    positives = [e for e in candidates if e['driver']['polarity'] == 'positive']
    # candidates is already sorted by score descending (see generate_impact_and_candidates)

    top_negative = negatives[0] if negatives else None
    second_negative = negatives[1] if len(negatives) > 1 else None
    top_positive = positives[0] if positives else None

    generic_items = fallbacks['generic_recommendation_items']

    # Critical priority: the #1-ranked negative driver.
    if top_negative and 'critical' in top_negative['driver'].get('recommendations', {}):
        critical_title = top_negative['driver']['label']
        critical_items = _items_to_li(top_negative['driver']['recommendations']['critical'], top_negative['context'])
    elif top_negative:
        critical_title = top_negative['driver']['label']
        critical_items = _items_to_li(generic_items, top_negative['context'])
    else:
        critical_title = fallbacks['critical_default_title']
        critical_items = _items_to_li(generic_items, {})

    # Secondary priority: the #2-ranked negative driver.
    if second_negative:
        secondary_title = second_negative['driver']['label']
        secondary_items = _items_to_li(
            second_negative['driver'].get('recommendations', {}).get('secondary', generic_items),
            second_negative['context'],
        )
    else:
        secondary_title = fallbacks['secondary_default_title']
        secondary_items = _items_to_li(generic_items, {})

    # Maintain strengths: a driver flagged maintain_override_if_detected wins
    # regardless of ranking (e.g. a new game launch is worth calling out even
    # if it isn't the top-scoring positive driver); otherwise the top-ranked
    # positive driver; otherwise a generic fallback.
    override = next(
        (e for e in candidates if e['active'] and e['driver'].get('maintain_override_if_detected')
         and 'maintain' in e['driver'].get('recommendations', {})),
        None,
    )
    maintain_source = override or top_positive
    if maintain_source and 'maintain' in maintain_source['driver'].get('recommendations', {}):
        maintain_block = maintain_source['driver']['recommendations']['maintain']
        maintain_title = maintain_block['title']
        maintain_items = _items_to_li(maintain_block['items'], maintain_source['context'])
    else:
        maintain_title = fallbacks['maintain_default']['title']
        maintain_items = _items_to_li(fallbacks['maintain_default']['items'], {})

    return {
        'critical': {'title': critical_title, 'items': critical_items},
        'secondary': {'title': secondary_title, 'items': secondary_items},
        'maintain': {'title': maintain_title, 'items': maintain_items},
    }


# ---------------------------------------------------------------------------
# Venue overview narrative. Kept separate from the driver registry above
# since it's a single synthesized paragraph rather than a themed list, but it
# shares the same theme_map so "parking" etc. are only ever detected one way.
# ---------------------------------------------------------------------------

def generate_overview(data, theme_map):
    ltr = data['ltr_avg']

    if ltr >= 8.0:
        char = "high-performing"
    elif ltr >= 7.0:
        char = "strong"
    elif ltr >= 6.0:
        char = "moderate"
    else:
        char = "challenged"

    if data['fun_avg'] >= 4.0:
        strength = "delivers strong entertainment value"
    else:
        strength = "has moderate entertainment appeal"

    if theme_map.get('parking'):
        challenge = "faces parking accessibility challenges"
    elif data['issues_pct'] > 50:
        challenge = "faces critical equipment reliability issues"
    elif data['issues_pct'] > 40:
        challenge = "faces significant equipment challenges"
    elif data['issues_pct'] > 30:
        challenge = "experiences occasional operational issues"
    else:
        challenge = "maintains good operational reliability"

    overview = f"{data['venue']} is a {char} venue that {strength} but {challenge}. "

    if theme_map.get('parking'):
        overview += "Guest feedback indicates parking accessibility is a significant concern affecting the overall visit experience. "
    elif data['issues_pct'] > 50:
        overview += f"The venue shows a clear pattern: equipment issues occur in {data['issues_pct']:.0f}% of visits, significantly impacting guest satisfaction. "
    else:
        overview += f"The venue shows strong fundamentals with {data['fun_avg']:.1f}/5 fun ratings and {data['helpful_avg']:.1f}/5 helpfulness scores. "

    if data['issues_pct'] > 50 and data['resolution_avg'] is not None and data['resolution_avg'] < 3.5:
        overview += "The venue appears to have both capability gaps and execution challenges that need attention."
    elif data['issues_pct'] > 50:
        overview += "The venue has demonstrated resolution capability but needs to prevent issues from occurring."
    else:
        overview += "The venue is executing well across key experience dimensions."

    return overview


def generate_fallback_analysis(data):
    """The keyword/metric-based fallback analysis, in the same shape as
    ai_analysis.get_ai_analysis(). Used whenever the AI analysis is
    unavailable."""
    driver_registry = load_driver_registry()
    fallbacks = driver_registry['fallbacks']

    evaluated, theme_map = evaluate_drivers(data, driver_registry)

    overview = generate_overview(data, theme_map)
    ups = generate_ups(evaluated, fallbacks)
    downs = generate_downs(evaluated, fallbacks)
    impact, candidates = generate_impact_and_candidates(evaluated)
    recommendations = generate_recommendations(candidates, fallbacks)

    return {
        'overview': overview,
        'ups': ups,
        'downs': downs,
        'impact': impact,
        'recommendations': recommendations,
    }
