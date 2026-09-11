#!/usr/bin/env python3
"""
AI-powered analysis of guest comments for venue reports.

Instead of relying on hardcoded keyword matching, this module shells out to
the Claude Code CLI (`claude`) in headless/print mode to analyze the actual
guest comments (Q6_COMMENT) alongside the aggregate metrics, and returns a
structured narrative (overview, ups/downs, impact drivers, recommendations).

Why the CLI instead of the Anthropic API directly?
- Users of this tool authenticate to Claude Code via their company's existing
  Claude subscription/login (no separate API key to create or manage).
- `claude --print --output-format json "<prompt>"` is Anthropic's officially
  documented headless/scripting mode for Claude Code, so this is a supported
  use of the tool rather than a workaround.

If the `claude` CLI isn't installed, isn't logged in, or the call fails for
any reason, `get_ai_analysis()` returns None and the caller is expected to
fall back to the simpler keyword-based analysis so report generation never
hard-fails.

Caching
-------
Every call to get_ai_analysis() costs latency (a CLI subprocess round-trip)
and tokens, so results are cached to disk in CACHE_DIR, keyed on a hash of
the exact payload sent to the model (venue metrics + comments) plus the
prompt/schema instructions themselves. That means:
- Re-running report generation for unchanged data (e.g. while tweaking the
  HTML template) is instant and free after the first run.
- Editing ANALYSIS_SCHEMA_INSTRUCTIONS automatically invalidates old cache
  entries, since the instructions text is part of the hash - no manual
  version bump needed.
- Any change to a venue's underlying metrics or comments (new CSV pull)
  naturally produces a new cache key and triggers a fresh AI call.
Set AI_ANALYSIS_FORCE_REFRESH=1 in the environment to bypass the cache for a
run without deleting it (useful when iterating on the prompt and comparing
against what's cached). Run `python ai_analysis.py --clear-cache` to wipe it.
"""
import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone

CLAUDE_TIMEOUT_SECONDS = 120

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.cache', 'ai_analysis')

ANALYSIS_SCHEMA_INSTRUCTIONS = """
You are analyzing guest survey feedback for a Topgolf venue to help write a performance report.

You will be given:
- Aggregate metrics for the venue (LTR, Fun, Helpfulness, Issues %, Resolution)
- The full list of guest comments (each with their LTR score and Fun score)

This report covers a single venue in isolation - you do NOT have data for any other venue or for the
network as a whole, so do not state or imply a network/company average, a network rank, or a comparison
to "other venues" anywhere in your output (no "above/below network average", no invented benchmark
numbers). Judge the venue only against the absolute scales given (e.g. LTR out of 10, Fun/Helpfulness/
Resolution out of 5, Issues as a %) and against what the comments themselves describe.

metrics.resolution_avg may be null. That means no guests reported an issue, so nobody answered the
resolution question - it is the normal, good outcome of a low issue rate, not a missing or poor score.
Never describe a null resolution_avg as weak, low, or a concern, and never include it as a negative
driver; if issues_pct is also low, you can note that few or no guests needed issue resolution at all.

Read the actual comments carefully and identify real, specific themes (e.g. parking, equipment/bay issues,
staff, food/drink, new games, wait times, pricing, cleanliness, etc.) rather than generic statements. Ground
every claim in either the metrics or the comments provided. Do not invent details that aren't supported by
the data.

Respond with ONLY a single JSON object (no markdown fences, no commentary before or after) matching this
exact shape:

{
  "overview": "2-4 sentence narrative paragraph summarizing the venue's overall performance, grounded in both metrics and comment themes",
  "ups": ["<strong>Short title:</strong> 1-2 sentence description", ...],
  "downs": ["<strong>Short title:</strong> 1-2 sentence description", ...],
  "impact": [
    {"title": "Short driver name", "description": "1-2 sentence explanation of why this driver matters, citing data"}
  ],
  "recommendations": {
    "critical": {"title": "Short priority name", "items": ["<strong>Action name:</strong> description", ...]},
    "secondary": {"title": "Short priority name", "items": ["<strong>Action name:</strong> description", ...]},
    "maintain": {"title": "Short priority name", "items": ["<strong>Action name:</strong> description", ...]}
  }
}

Rules:
- "ups" and "downs": 2-3 items each.
- "impact": exactly 3 items, ordered by actual magnitude of impact on guest satisfaction, most impactful
  first. Rank by the size of the effect the data shows: prefer issues backed by a percentage/rate metric
  or that affect many guests over issues mentioned by only one or two guests, unless the few affected
  guests describe an unusually severe outcome. Do not order by topic, sentiment, or how positive/negative
  an item is - "impact" ranking is about magnitude, and can mix positive and negative drivers.
- "recommendations": the "critical" section must address the #1-ranked "impact" item, "secondary" must
  address the #2-ranked "impact" item, and "maintain" should reinforce the top positive driver (e.g. a
  well-received "impact" item or a strong "ups" theme). The recommendations' priority order must match the
  impact ranking - never put a lower-impact issue in "critical" while a higher-impact one is only
  "secondary".
- Each recommendations section: 3-4 items.
- Inline HTML in list items is limited to <strong> tags only.
- If comments mention a specific recurring issue or highlight (e.g. a particular game, a facility problem),
  call it out by name instead of speaking generically.
"""


def _build_payload(data):
    """The exact venue data sent to the model. Shared by _build_prompt() (so
    the prompt reflects it) and _cache_key() (so the cache key reflects it) -
    keeping this in one place means the two can never drift apart."""
    comments = data.get("comments", [])
    return {
        "venue": data["venue"],
        "responses": data["responses"],
        "metrics": {
            "ltr_avg": data["ltr_avg"],
            "fun_avg": data["fun_avg"],
            "helpful_avg": data["helpful_avg"],
            "issues_pct": data["issues_pct"],
            "resolution_avg": data["resolution_avg"],
        },
        "comments": comments,
    }


def _build_prompt(data):
    payload = _build_payload(data)
    return (
        ANALYSIS_SCHEMA_INSTRUCTIONS
        + "\n\nVenue data:\n"
        + json.dumps(payload, indent=2)
    )


def _cache_key(data):
    """Stable hash of (prompt instructions + venue payload). Any change to
    either - a new survey pull for this venue, or an edited prompt/schema -
    produces a different key, so stale results are never served silently."""
    payload = _build_payload(data)
    fingerprint = ANALYSIS_SCHEMA_INSTRUCTIONS + "\n" + json.dumps(payload, sort_keys=True)
    return hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()


def _cache_path(cache_key):
    return os.path.join(CACHE_DIR, f"{cache_key}.json")


def _read_cache(cache_key, venue):
    path = _cache_path(cache_key)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            entry = json.load(f)
        analysis = entry["analysis"]
    except Exception as e:
        print(
            f"[ai_analysis] Cache entry for venue '{venue}' at {path} is unreadable "
            f"({e}); ignoring it and re-running the AI analysis."
        )
        return None
    if not _validate_analysis(analysis):
        print(
            f"[ai_analysis] Cache entry for venue '{venue}' at {path} no longer "
            "matches the expected schema; ignoring it and re-running the AI analysis."
        )
        return None
    return analysis


def _write_cache(cache_key, venue, analysis):
    os.makedirs(CACHE_DIR, exist_ok=True)
    entry = {
        "venue": venue,
        "cache_key": cache_key,
        "cached_at": datetime.now(timezone.utc).isoformat(),
        "analysis": analysis,
    }
    path = _cache_path(cache_key)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=2)
    except Exception as e:
        # Caching is an optimization, not a correctness requirement - a
        # write failure (e.g. read-only filesystem) shouldn't fail the run.
        print(f"[ai_analysis] Could not write cache entry for venue '{venue}': {e}")


def clear_cache():
    if os.path.exists(CACHE_DIR):
        shutil.rmtree(CACHE_DIR)
        print(f"[ai_analysis] Cleared cache at {CACHE_DIR}")
    else:
        print(f"[ai_analysis] No cache to clear at {CACHE_DIR}")


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


def _validate_analysis(analysis):
    if not isinstance(analysis, dict):
        return False
    required_top = ["overview", "ups", "downs", "impact", "recommendations"]
    if not all(key in analysis for key in required_top):
        return False
    rec = analysis["recommendations"]
    if not all(key in rec for key in ["critical", "secondary", "maintain"]):
        return False
    for section in rec.values():
        if "title" not in section or "items" not in section:
            return False
    for driver in analysis["impact"]:
        if "title" not in driver or "description" not in driver:
            return False
    return True


def get_ai_analysis(data, use_cache=True):
    """Run the AI-based analysis via the Claude Code CLI, using a cached
    result when one exists for this exact venue payload + prompt.

    Returns a dict matching the schema in ANALYSIS_SCHEMA_INSTRUCTIONS on
    success, or None if the CLI is unavailable or anything goes wrong (with
    a message printed to the console explaining why).

    Set use_cache=False, or the AI_ANALYSIS_FORCE_REFRESH environment
    variable, to force a fresh call even when a cache entry exists.
    """
    venue = data.get("venue")
    force_refresh = os.environ.get("AI_ANALYSIS_FORCE_REFRESH", "").strip().lower() in ("1", "true", "yes")
    cache_key = _cache_key(data)

    if use_cache and not force_refresh:
        cached = _read_cache(cache_key, venue)
        if cached is not None:
            print(f"[ai_analysis] Using cached analysis for venue '{venue}' (key {cache_key[:12]}...)")
            return cached

    claude_path = shutil.which("claude")
    if not claude_path:
        print(
            "[ai_analysis] 'claude' CLI not found on PATH - skipping AI analysis "
            "(install/login to Claude Code to enable it). Falling back to "
            "keyword-based analysis."
        )
        return None

    prompt = _build_prompt(data)

    try:
        result = subprocess.run(
            [claude_path, "--print", "--output-format", "json", prompt],
            capture_output=True,
            text=True,
            timeout=CLAUDE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print(
            f"[ai_analysis] Claude CLI timed out after {CLAUDE_TIMEOUT_SECONDS}s "
            f"for venue '{venue}'. Falling back to keyword-based analysis."
        )
        return None
    except Exception as e:
        print(
            f"[ai_analysis] Failed to invoke Claude CLI for venue "
            f"'{venue}': {e}. Falling back to keyword-based analysis."
        )
        return None

    if result.returncode != 0:
        print(
            f"[ai_analysis] Claude CLI exited with code {result.returncode} for "
            f"venue '{venue}': {result.stderr.strip()[:500]}. "
            "Falling back to keyword-based analysis."
        )
        return None

    try:
        envelope = json.loads(result.stdout)
        if envelope.get("is_error"):
            raise ValueError(envelope.get("result", "unknown error"))
        response_text = envelope["result"]
        analysis = _extract_json(response_text)
    except Exception as e:
        print(
            f"[ai_analysis] Could not parse Claude CLI response for venue "
            f"'{venue}': {e}. Falling back to keyword-based analysis."
        )
        return None

    if not _validate_analysis(analysis):
        print(
            f"[ai_analysis] Claude CLI response for venue '{venue}' "
            "did not match the expected schema. Falling back to keyword-based analysis."
        )
        return None

    _write_cache(cache_key, venue, analysis)
    return analysis


if __name__ == "__main__":
    import sys

    if "--clear-cache" in sys.argv:
        clear_cache()
    else:
        print(__doc__)
        print("Usage: python ai_analysis.py --clear-cache")
