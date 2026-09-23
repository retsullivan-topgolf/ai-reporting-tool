#!/usr/bin/env python3
"""
AI-powered analysis of guest comments for venue reports.

This runs as a 3-stage pipeline, each stage its own `claude` CLI call, chained
by this module:

  1. metrics_analysis  - reads only the 5 aggregate metrics, produces a short
                          characterization plus per-metric "concern flags" on
                          a 0-100 magnitude scale.
  2. comment_analysis   - reads the free-text guest comments plus Stage 1's
                          metric_flags (for categorization context), produces
                          themes (positive and negative) on the same 0-100
                          magnitude scale.
  3. synthesis          - reads only the two stages' structured output (not
                          the raw metrics/comments again) and produces the
                          final overview/ups/downs/impact/recommendations
                          report content.

Each stage's guidelines live as a standalone Markdown doc in
.claude/single-venue-report/ (metrics_analysis.md, comment_analysis.md, synthesis.md) so
they can be read, reviewed, and iterated on independently of this file - see
those docs for what each stage is actually being asked to do and why the
magnitude scale matters.

Why 3 calls instead of 1? The previous version of this module sent one giant
prompt asking the model to read every comment, reconcile it with all 5
metrics, and produce the entire 4-section report in a single turn. That's a
lot of reasoning and a large structured output in one shot, and in practice
it was the cause of real timeouts once venues had a non-trivial number of
comments. Splitting into 3 focused stages means each individual `claude`
call does much less work, is separately cacheable (see Caching below), and
can be tested/timed independently - at the cost of 3 subprocess round-trips
instead of 1.

Why the CLI instead of the Anthropic API directly?
- Users of this tool authenticate to Claude Code via their company's existing
  Claude subscription/login (no separate API key to create or manage).
- `claude --print --output-format json "<prompt>"` is Anthropic's officially
  documented headless/scripting mode for Claude Code, so this is a supported
  use of the tool rather than a workaround.


If any stage isn't available - CLI missing, timed out, bad response, etc. -
`get_ai_analysis()` returns (None, reason) and the whole pipeline stops at
that stage; there is no keyword-based fallback analysis. The caller is
expected to show the reason to the reader in place of the AI-generated
narrative (overview, ups/downs, impact, recommendations) while still showing
the metrics, which don't depend on AI at all. See report_content.get_analysis().

Caching
-------
Each of the 3 stages is cached independently in CACHE_DIR, keyed on a hash of
that stage's own guideline doc plus its own input payload. That means:
- Re-running report generation for unchanged data is instant and free after
  the first run, same as before.
- Editing one stage's guideline doc (e.g. tuning synthesis.md while metrics
  and comment analysis are already working well) only invalidates that
  stage's cache - metrics_analysis and comment_analysis results are reused
  as-is, which matters a lot while iterating on prompts.
- Any change to a venue's underlying metrics or comments (new CSV pull)
  naturally produces new cache keys for the stages that read that data.
Set AI_ANALYSIS_FORCE_REFRESH=1 in the environment to bypass the cache for a
run without deleting it. Run `python analyze_venues.py --clear-cache` to wipe it.
"""
import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone

import report_engine

CLAUDE_TIMEOUT_SECONDS = 600  # per stage, not for the whole 3-stage pipeline (5 minutes)

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.cache', 'ai_analysis')
SKILLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.claude', 'single-venue-report')
CLAUDE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.claude')


def _load_skill(filename):
    path = os.path.join(SKILLS_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def _load_skill_variant(variant_dir, filename):
    """Load a skill file from a specific .claude/<variant_dir>/ folder."""
    path = os.path.join(CLAUDE_ROOT, variant_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def _compose_synthesis_skill(report_type='snapshot'):
    """Build the Stage 3 synthesis prompt by substituting each <!-- SKILL:x --> placeholder
    in the template with that report_type's section-skill content.

    Supports:
    - 'snapshot': Single-venue single-period (Phase 0+)
    - 'comparison': Single-venue period comparison (Phase 1+)
    - 'multi-snapshot': Multi-venue single-period (Phase 2+)
    - 'multi-comparison': Multi-venue period comparison (Phase 2b+)

    Args:
        report_type: One of the supported types above

    Returns:
        Composed synthesis skill text (full prompt to pass to Claude)
    """
    # Configuration: (template_source_dir, section_skill_dir, section_filename_suffix)
    _SYNTHESIS_CONFIG = {
        'snapshot': ('single-venue-report', 'single-venue-report', '-skill.md'),
        'comparison': ('single-venue-report', 'comparison-report', '-comparison-skill.md'),
        'multi-snapshot': ('multi-venue-report', 'multi-venue-report', '-skill.md'),
        'multi-comparison': ('multi-venue-report', 'multi-venue-comparison-report', '-comparison-skill.md'),
    }

    # Section names per variant
    _SECTION_NAMES = {
        'snapshot': ['venue-overview', 'ups-downs', 'impact-drivers', 'recommendations'],
        'comparison': ['venue-overview', 'ups-downs', 'impact-drivers', 'recommendations'],
        'multi-snapshot': ['multi-venue-overview', 'multi-venue-ranking', 'multi-venue-ups-downs', 'multi-venue-impact-drivers', 'multi-venue-recommendations'],
        'multi-comparison': ['multi-venue-overview', 'multi-venue-ranking', 'multi-venue-ups-downs', 'multi-venue-impact-drivers', 'multi-venue-recommendations'],
    }

    # Map section names to placeholder keys
    _PLACEHOLDER_KEYS = {
        'venue-overview': 'venue-overview',
        'ups-downs': 'ups-downs',
        'impact-drivers': 'impact-drivers',
        'recommendations': 'recommendations',
        'multi-venue-overview': 'venue-overview',
        'multi-venue-ranking': 'ranking',
        'multi-venue-ups-downs': 'ups-downs',
        'multi-venue-impact-drivers': 'impact-drivers',
        'multi-venue-recommendations': 'recommendations',
    }

    if report_type not in _SYNTHESIS_CONFIG:
        raise ValueError(f"Unsupported report_type: {report_type}. Supported: 'snapshot', 'comparison', 'multi-snapshot', 'multi-comparison'.")

    template_dir, section_dir, suffix = _SYNTHESIS_CONFIG[report_type]
    template = _load_skill_variant(template_dir, 'synthesis_template.md')

    for name in _SECTION_NAMES[report_type]:
        section_text = _load_skill_variant(section_dir, f"{name}{suffix}")
        placeholder = f"<!-- SKILL:{_PLACEHOLDER_KEYS[name]} -->"
        template = template.replace(placeholder, section_text)

    return template


# Loaded once at import time (small files) so a missing/renamed skill doc
# fails fast and loudly instead of deep inside a subprocess call.
METRICS_ANALYSIS_SKILL = _load_skill('metrics_analysis.md')
COMMENT_ANALYSIS_SKILL = _load_skill('comment_analysis.md')
SYNTHESIS_SKILL = _compose_synthesis_skill('snapshot')  # Compose from template + skills

_metrics_registry_cache = None


def _metrics_registry():
    """Lazily load + memoize templates/metrics.json - the metrics_analysis
    stage needs each metric's already-computed assessment tier (see that
    stage's guideline doc for why: it's given as ground truth rather than
    re-derived) using the exact same thresholds report_content.py uses for
    the Performance Summary / Experience Metrics tables."""
    global _metrics_registry_cache
    if _metrics_registry_cache is None:
        _metrics_registry_cache = report_engine.load_metrics_registry()
    return _metrics_registry_cache


def _build_metrics_payload(data):
    registry = _metrics_registry()
    metrics = {
        "ltr_avg": data["ltr_avg"],
        "fun_avg": data["fun_avg"],
        "helpful_avg": data["helpful_avg"],
        "issues_pct": data["issues_pct"],
        "resolution_avg": data["resolution_avg"],
    }
    assessment_tiers = {
        "ltr": report_engine.get_assessment("ltr", metrics["ltr_avg"], registry),
        "fun": report_engine.get_assessment("fun", metrics["fun_avg"], registry),
        "helpful": report_engine.get_assessment("helpful", metrics["helpful_avg"], registry),
        "issues": report_engine.get_assessment("issues", metrics["issues_pct"], registry),
        "resolution": report_engine.get_assessment("resolution", metrics["resolution_avg"], registry),
    }

    # Add optional NPS and Price Value metrics if present
    if "nps_avg" in data and data["nps_avg"] is not None:
        metrics["nps_avg"] = data["nps_avg"]
        assessment_tiers["nps"] = report_engine.get_assessment("nps", data["nps_avg"], registry)

    if "price_value_avg" in data and data["price_value_avg"] is not None:
        metrics["price_value_avg"] = data["price_value_avg"]
        assessment_tiers["price_value"] = report_engine.get_assessment("price_value", data["price_value_avg"], registry)

    # Add optional F&B metrics if present
    fb_metrics = ["food_value", "food_speed", "food_quality", "beverage_value", "beverage_speed", "beverage_quality"]
    for metric in fb_metrics:
        data_field = f"{metric}_avg"
        if data_field in data and data[data_field] is not None:
            metrics[data_field] = data[data_field]
            assessment_tiers[metric] = report_engine.get_assessment(metric, data[data_field], registry)

    # Add Food/Beverage/F&B averages if present
    for metric in ["food", "beverage", "fb_average"]:
        data_field = "fb_average" if metric == "fb_average" else f"{metric}_avg"
        if data_field in data and data[data_field] is not None:
            metrics[data_field] = data[data_field]
            assessment_tiers[metric] = report_engine.get_assessment(metric, data[data_field], registry)

    return {
        "venue": data["venue"],
        "responses": data["responses"],
        "metrics": metrics,
        "assessment_tiers": assessment_tiers,
    }


def _build_comment_payload(data, metric_flags):
    return {
        "venue": data["venue"],
        "responses": data["responses"],
        "comments": data.get("comments", []),
        "metric_flags": metric_flags,
    }


def _validate_metrics_analysis(result):
    """Validate single-venue metrics_analysis output."""
    if not isinstance(result, dict):
        return False
    if "characterization" not in result or "metric_flags" not in result:
        return False
    if not isinstance(result["metric_flags"], list):
        return False
    return all(
        isinstance(flag, dict) and all(k in flag for k in ("metric", "polarity", "magnitude", "note"))
        for flag in result["metric_flags"]
    )


def _validate_metrics_analysis_multi(result):
    """Validate multi-venue metrics_analysis output."""
    if not isinstance(result, dict):
        return False
    # Multi-venue metrics_analysis returns: characterization, network_metrics, venue_outliers
    if "characterization" not in result:
        return False
    if "network_metrics" not in result or not isinstance(result["network_metrics"], list):
        return False
    # network_metrics is list of dicts with: metric, polarity, magnitude, network_avg, range, note
    for metric in result["network_metrics"]:
        if not isinstance(metric, dict):
            return False
        required_keys = {"metric", "polarity", "magnitude", "network_avg", "range", "note"}
        if not all(k in metric for k in required_keys):
            return False
    if "venue_outliers" not in result or not isinstance(result["venue_outliers"], list):
        return False
    # venue_outliers is list of dicts with: venue, rank, nps, note
    for outlier in result["venue_outliers"]:
        if not isinstance(outlier, dict):
            return False
        required_keys = {"venue", "rank", "note"}
        if not all(k in outlier for k in required_keys):
            return False
    return True


def _validate_comment_analysis(result):
    """Validate comment_analysis output (works for both single-venue and multi-venue).

    Single-venue returns: label, polarity, mention_count, magnitude, summary
    Multi-venue returns: label, polarity, mention_count, magnitude, network_summary, venue_breakdown, representative_detail
    """
    if not isinstance(result, dict):
        return False
    if "themes" not in result or not isinstance(result["themes"], list):
        return False
    return all(
        isinstance(theme, dict)
        and all(k in theme for k in ("label", "polarity", "mention_count", "magnitude"))
        and any(k in theme for k in ("summary", "network_summary"))  # Accept either field
        for theme in result["themes"]
    )


def _validate_synthesis(analysis):
    """Validate synthesis output (works for both single-venue and multi-venue).

    Single-venue: overview, ups, downs, impact, recommendations
    Multi-venue: also includes venue_ranking, and venue_specific in recommendations
    """
    if not isinstance(analysis, dict):
        return False
    required_top = ["overview", "ups", "downs", "impact", "recommendations"]
    if not all(key in analysis for key in required_top):
        return False

    rec = analysis["recommendations"]
    if not all(key in rec for key in ["critical", "secondary", "maintain"]):
        return False

    # Validate recommendations sections (critical, secondary, maintain all have title and items)
    for key in ["critical", "secondary", "maintain"]:
        section = rec[key]
        if not isinstance(section, dict) or "title" not in section or "items" not in section:
            return False

    # Validate impact drivers (each has title and description)
    if not isinstance(analysis["impact"], list):
        return False
    for driver in analysis["impact"]:
        if not isinstance(driver, dict) or "title" not in driver or "description" not in driver:
            return False

    # Multi-venue specific: venue_ranking (optional, but if present must have structure)
    if "venue_ranking" in analysis:
        if not isinstance(analysis["venue_ranking"], list):
            return False
        for venue in analysis["venue_ranking"]:
            if not isinstance(venue, dict) or "venue" not in venue:
                return False

    # Multi-venue specific: venue_specific in recommendations (optional, but if present must be list)
    if "venue_specific" in rec and not isinstance(rec["venue_specific"], list):
        return False

    return True


def _extract_json(text):
    """Pull a JSON object out of Claude's response text, tolerating stray
    markdown code fences some models add despite instructions not to."""
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        # Drop a leading language tag like "json\n"
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    return json.loads(text)


def _cache_path(stage, cache_key):
    return os.path.join(CACHE_DIR, stage, f"{cache_key}.json")


def _stage_cache_key(stage, skill_text, payload):
    """Stable hash of (stage guideline doc + that stage's own input payload).
    Any change to either - a new survey pull for this venue, or an edited
    guideline doc - produces a different key, so stale results are never
    served silently. Independent per stage, which is the whole point: tuning
    synthesis.md doesn't invalidate metrics_analysis/comment_analysis
    results, and vice versa."""
    fingerprint = skill_text + "\n" + json.dumps(payload, sort_keys=True)
    return hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()


def _read_stage_cache(stage, cache_key, venue, validator):
    path = _cache_path(stage, cache_key)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            entry = json.load(f)
        result = entry["result"]
    except Exception as e:
        print(
            f"[analyze_venues] {stage} cache entry for venue '{venue}' at {path} is unreadable "
            f"({e}); ignoring it and re-running this stage."
        )
        return None
    if not validator(result):
        print(
            f"[analyze_venues] {stage} cache entry for venue '{venue}' at {path} no longer "
            "matches the expected schema; ignoring it and re-running this stage."
        )
        return None
    return result


def _write_stage_cache(stage, cache_key, venue, result):
    stage_dir = os.path.join(CACHE_DIR, stage)
    os.makedirs(stage_dir, exist_ok=True)
    entry = {
        "venue": venue,
        "stage": stage,
        "cache_key": cache_key,
        "cached_at": datetime.now(timezone.utc).isoformat(),
        "result": result,
    }
    path = _cache_path(stage, cache_key)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=2)
    except Exception as e:
        # Caching is an optimization, not a correctness requirement - a
        # write failure (e.g. read-only filesystem) shouldn't fail the run.
        print(f"[analyze_venues] Could not write {stage} cache entry for venue '{venue}': {e}")


def clear_cache():
    if os.path.exists(CACHE_DIR):
        shutil.rmtree(CACHE_DIR)
        print(f"[analyze_venues] Cleared cache at {CACHE_DIR}")
    else:
        print(f"[analyze_venues] No cache to clear at {CACHE_DIR}")


def _invoke_claude(prompt, stage, venue):
    """Run one `claude --print` call and return (parsed_json, None) or
    (None, reason). Shared by all 3 stages - each stage differs only in its
    guideline doc, payload, and validator (see _run_stage)."""
    claude_path = shutil.which("claude")
    if not claude_path:
        return None, "'claude' CLI not found on PATH - install/login to Claude Code to enable AI analysis"

    try:
        result = subprocess.run(
            [claude_path, "--print", "--output-format", "json"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=CLAUDE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return None, f"Claude CLI timed out after {CLAUDE_TIMEOUT_SECONDS}s"
    except Exception as e:
        return None, f"failed to invoke Claude CLI ({e})"

    # The CLI can exit non-zero with an EMPTY stderr but a perfectly
    # well-formed JSON envelope on stdout carrying a helpful `result`
    # message (e.g. "Not logged in - please run /login") - prefer that over
    # a blank/unhelpful "exited with code 1" whenever it's present.
    envelope = None
    try:
        envelope = json.loads(result.stdout)
    except Exception:
        pass

    if result.returncode != 0 or (envelope and envelope.get("is_error")):
        if envelope and envelope.get("result"):
            return None, str(envelope["result"])
        stderr = result.stderr.strip()[:500]
        reason = f"Claude CLI exited with code {result.returncode}"
        return None, f"{reason}: {stderr}" if stderr else reason

    if envelope is None:
        return None, "could not parse Claude CLI response as JSON"

    try:
        response_text = envelope["result"]
        parsed = _extract_json(response_text)
    except Exception as e:
        return None, f"could not parse Claude CLI response ({e})"

    return parsed, None


def _run_stage(stage, skill_text, payload, validator, venue, use_cache, force_refresh):
    """Run one pipeline stage with caching: build the prompt from the
    stage's guideline doc + payload, check cache, call Claude if needed,
    validate, cache, and return (result, None) or (None, reason)."""
    cache_key = _stage_cache_key(stage, skill_text, payload)

    if use_cache and not force_refresh:
        cached = _read_stage_cache(stage, cache_key, venue, validator)
        if cached is not None:
            print(f"[analyze_venues] Using cached {stage} result for venue '{venue}' (key {cache_key[:12]}...)")
            return cached, None

    prompt = skill_text + "\n\nInput:\n" + json.dumps(payload, indent=2)
    result, error = _invoke_claude(prompt, stage, venue)
    if result is None:
        print(f"[analyze_venues] {stage} stage failed for venue '{venue}': {error}")
        return None, f"{stage} stage: {error}"

    if not validator(result):
        message = f"{stage} stage: Claude CLI response did not match the expected schema"
        print(f"[analyze_venues] {message} (venue '{venue}').")
        return None, message

    _write_stage_cache(stage, cache_key, venue, result)
    return result, None


def get_ai_analysis(data, report_type='snapshot', previous_data=None, use_cache=True):
    """Run the 3-stage AI analysis pipeline (metrics_analysis ->
    comment_analysis -> synthesis) for one venue's data.

    Args:
        data: Current-period venue data
        report_type: 'snapshot' (single period) or 'comparison' (two periods)
        previous_data: Required when report_type='comparison'; previous period's data
        use_cache: Whether to use cached results

    Returns (analysis, None) on success, where analysis matches the schema
    produced by the appropriate synthesis skill (overview/ups/downs/impact/
    recommendations). Returns (None, reason) if any stage fails - reason is
    a short, human-readable string safe to show directly in a report (e.g.
    in place of the AI-generated overview) rather than just logged to the
    console, prefixed with which stage it came from.

    There is no keyword-based fallback - a None result means the caller
    should say AI analysis wasn't available rather than fabricate a
    narrative from a different method.

    Set use_cache=False, or the AI_ANALYSIS_FORCE_REFRESH environment
    variable, to force fresh calls for every stage even when cache entries
    exist.
    """
    if report_type not in ('snapshot', 'comparison'):
        return None, f"Unsupported report_type: {report_type}. Use 'snapshot' or 'comparison'."

    if report_type == 'comparison' and previous_data is None:
        return None, "report_type='comparison' requires previous_data parameter"

    venue = data.get("venue")
    force_refresh = os.environ.get("AI_ANALYSIS_FORCE_REFRESH", "").strip().lower() in ("1", "true", "yes")

    # Stage 1: Metrics Analysis
    metrics_current, error = _run_stage(
        "metrics_analysis", METRICS_ANALYSIS_SKILL, _build_metrics_payload(data),
        _validate_metrics_analysis, venue, use_cache, force_refresh,
    )
    if metrics_current is None:
        return None, error

    # Stage 2: Comment Analysis (current period)
    comment_current, error = _run_stage(
        "comment_analysis", COMMENT_ANALYSIS_SKILL,
        _build_comment_payload(data, metrics_current.get("metric_flags", [])),
        _validate_comment_analysis, venue, use_cache, force_refresh,
    )
    if comment_current is None:
        return None, error

    # For comparison reports, run Stage 1+2 on previous period too
    metrics_previous = None
    comment_previous = None
    if report_type == 'comparison':
        metrics_previous, error = _run_stage(
            "metrics_analysis", METRICS_ANALYSIS_SKILL, _build_metrics_payload(previous_data),
            _validate_metrics_analysis, venue, use_cache, force_refresh,
        )
        if metrics_previous is None:
            return None, error

        comment_previous, error = _run_stage(
            "comment_analysis", COMMENT_ANALYSIS_SKILL,
            _build_comment_payload(previous_data, metrics_previous.get("metric_flags", [])),
            _validate_comment_analysis, venue, use_cache, force_refresh,
        )
        if comment_previous is None:
            return None, error

    # Stage 3: Synthesis
    # Build synthesis payload based on report type
    if report_type == 'snapshot':
        synthesis_payload = {
            "venue": venue,
            "responses": data["responses"],
            "metrics_analysis": metrics_current,
            "comment_analysis": comment_current,
        }
    else:  # comparison
        synthesis_payload = {
            "venue": venue,
            "responses": data["responses"],
            "metrics_analysis": {
                "current": metrics_current,
                "previous": metrics_previous,
            },
            "comment_analysis": {
                "current": comment_current,
                "previous": comment_previous,
            },
        }

    # Compose synthesis skill for the report type
    synthesis_skill = _compose_synthesis_skill(report_type)

    synthesis_result, error = _run_stage(
        "synthesis", synthesis_skill, synthesis_payload,
        _validate_synthesis, venue, use_cache, force_refresh,
    )
    if synthesis_result is None:
        return None, error

    return synthesis_result, None


def get_aggregated_ai_analysis(aggregated_data, use_cache=True):
    """Run the 3-stage AI analysis pipeline for multi-venue aggregated data.

    This analyzes metrics and comments aggregated across all venues,
    producing network-wide findings, venue rankings, and recommendations.

    Args:
        aggregated_data: Dict with aggregated metrics and comments across all venues:
            {
                "venues": [
                    {"venue": "Grand Prairie", "responses": 45, "metrics": {...}, "comments": [...]},
                    ...
                ]
            }
        use_cache: Whether to use cached results

    Returns:
        (analysis, None) on success with structure:
            {
              "overview": str,
              "ups": [str, ...],
              "downs": [str, ...],
              "impact": [{"title": str, "description": str}, ...],
              "venue_ranking": [{"rank": int, "venue": str, "nps": float, ...}, ...],
              "recommendations": {
                "critical": {...},
                "secondary": {...},
                "maintain": {...},
                "venue_specific": [...]
              }
            }

        (None, reason) if any stage fails
    """
    force_refresh = os.environ.get("AI_ANALYSIS_FORCE_REFRESH", "").strip().lower() in ("1", "true", "yes")

    # Load multi-venue Stage 1 and Stage 2 skills
    metrics_analysis_skill = _load_skill_variant('multi-venue-report', 'metrics_analysis.md')
    comment_analysis_skill = _load_skill_variant('multi-venue-report', 'comment_analysis.md')

    # Build metrics payload for multi-venue
    metrics_payload = {"venues": aggregated_data.get("venues", [])}

    # Stage 1: Metrics Analysis
    metrics_result, error = _run_stage(
        "metrics_analysis_multi", metrics_analysis_skill, metrics_payload,
        _validate_metrics_analysis_multi, "network", use_cache, force_refresh,
    )
    if metrics_result is None:
        return None, error

    # Build comment payload for multi-venue
    # Note: Multi-venue metrics_analysis returns "network_metrics" (not "metric_flags")
    # Transform it to the format expected by comment_analysis
    metric_flags = metrics_result.get("network_metrics", [])

    comment_payload = {
        "venues": aggregated_data.get("venues", []),
        "metric_flags": metric_flags,
    }

    # Stage 2: Comment Analysis
    comment_result, error = _run_stage(
        "comment_analysis_multi", comment_analysis_skill, comment_payload,
        _validate_comment_analysis, "network", use_cache, force_refresh,
    )
    if comment_result is None:
        return None, error

    # Stage 3: Synthesis (multi-venue)
    synthesis_payload = {
        "venues": aggregated_data.get("venues", []),
        "metrics_analysis": metrics_result,
        "comment_analysis": comment_result,
    }

    synthesis_skill = _compose_synthesis_skill('multi-snapshot')

    synthesis_result, error = _run_stage(
        "synthesis_multi", synthesis_skill, synthesis_payload,
        _validate_synthesis, "network", use_cache, force_refresh,
    )
    if synthesis_result is None:
        return None, error

    return synthesis_result, None


def get_period_ai_analysis(period_data, use_cache=True):
    """Run AI analysis on aggregated period data (multiple venues).

    This is a wrapper around get_aggregated_ai_analysis() for backward compatibility.

    Args:
        period_data: Dict with aggregated metrics, venue rankings, and comments
        use_cache: Whether to use cached results

    Returns:
        (analysis, None) on success, or (None, reason) if unavailable
    """
    return get_aggregated_ai_analysis(period_data, use_cache=use_cache)


if __name__ == "__main__":
    import sys

    if "--clear-cache" in sys.argv:
        clear_cache()
    else:
        print(__doc__)
        print("Usage: python analyze_venues.py --clear-cache")
