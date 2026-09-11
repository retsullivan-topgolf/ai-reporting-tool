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
"""
import json
import shutil
import subprocess

CLAUDE_TIMEOUT_SECONDS = 120

ANALYSIS_SCHEMA_INSTRUCTIONS = """
You are analyzing guest survey feedback for a Topgolf venue to help write a performance report.

You will be given:
- Aggregate metrics for the venue (LTR, Fun, Helpfulness, Issues %, Resolution) and network benchmarks
- The full list of guest comments (each with their LTR score and Fun score)

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
- "impact": exactly 3 items, ranked most to least impactful.
- Each recommendations section: 3-4 items.
- Inline HTML in list items is limited to <strong> tags only.
- If comments mention a specific recurring issue or highlight (e.g. a particular game, a facility problem),
  call it out by name instead of speaking generically.
"""


def _build_prompt(data):
    comments = data.get("comments", [])
    payload = {
        "venue": data["venue"],
        "responses": data["responses"],
        "metrics": {
            "ltr_avg": data["ltr_avg"],
            "fun_avg": data["fun_avg"],
            "helpful_avg": data["helpful_avg"],
            "issues_pct": data["issues_pct"],
            "resolution_avg": data["resolution_avg"],
        },
        "network_benchmarks": {
            "ltr": 7.8,
            "fun": 4.1,
            "helpful": 4.2,
            "issues": 37.0,
            "resolution": 3.6,
        },
        "comments": comments,
    }
    return (
        ANALYSIS_SCHEMA_INSTRUCTIONS
        + "\n\nVenue data:\n"
        + json.dumps(payload, indent=2)
    )


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


def get_ai_analysis(data):
    """Run the AI-based analysis via the Claude Code CLI.

    Returns a dict matching the schema in ANALYSIS_SCHEMA_INSTRUCTIONS on
    success, or None if the CLI is unavailable or anything goes wrong (with
    a message printed to the console explaining why).
    """
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
            f"for venue '{data.get('venue')}'. Falling back to keyword-based analysis."
        )
        return None
    except Exception as e:
        print(
            f"[ai_analysis] Failed to invoke Claude CLI for venue "
            f"'{data.get('venue')}': {e}. Falling back to keyword-based analysis."
        )
        return None

    if result.returncode != 0:
        print(
            f"[ai_analysis] Claude CLI exited with code {result.returncode} for "
            f"venue '{data.get('venue')}': {result.stderr.strip()[:500]}. "
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
            f"'{data.get('venue')}': {e}. Falling back to keyword-based analysis."
        )
        return None

    if not _validate_analysis(analysis):
        print(
            f"[ai_analysis] Claude CLI response for venue '{data.get('venue')}' "
            "did not match the expected schema. Falling back to keyword-based analysis."
        )
        return None

    return analysis
