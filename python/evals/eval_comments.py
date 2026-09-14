"""
Shared helpers for the skill eval runners (metric_skill_eval.py,
comment_skill_eval.py, synthesis_skill_eval.py). See EVALS.md for the
overall picture.

This module deliberately reuses ai_analysis.py's existing payload
builders, skill text constants, claude CLI invocation, and schema
validators rather than reimplementing them, so the eval suite can't
silently drift from what production actually sends/expects.
"""
import json
import subprocess
import sys
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parent
PYTHON_DIR = EVALS_DIR.parent
GENERATE_REPORTS_SCRIPT = PYTHON_DIR / "generate_reports.py"

# Make `import ai_analysis` / `import report_engine` work regardless of the
# caller's cwd.
if str(PYTHON_DIR) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIR))

import ai_analysis  # noqa: E402  (import after sys.path setup, see above)


# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

def load_config(config_path=None):
    path = Path(config_path) if config_path else EVALS_DIR / "eval_config.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_path(raw_path, base_dir=EVALS_DIR):
    """Resolve a config/CLI path that may be relative to the evals/ folder."""
    p = Path(raw_path)
    return p if p.is_absolute() else (base_dir / p).resolve()


def run_dir_for(config, run_id):
    output_dir = resolve_path(config["output_dir"])
    run_dir = output_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


# --------------------------------------------------------------------------
# CSV -> venue_data.json (via the real generate_reports.py, not a
# reimplementation of its parsing logic)
# --------------------------------------------------------------------------

def generate_venue_data(csv_path, run_dir):
    """Run the real generate_reports.py against csv_path, with its cwd set
    to run_dir so the generated venue_data.json lands there instead of
    clobbering the project's real python/venue_data.json. Returns the
    parsed dict of {venue_key: venue_dict}."""
    csv_path = Path(csv_path).resolve()
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    result = subprocess.run(
        [sys.executable, str(GENERATE_REPORTS_SCRIPT), str(csv_path)],
        cwd=str(run_dir),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"generate_reports.py failed (exit {result.returncode}):\n{result.stderr}"
        )

    venue_data_path = run_dir / "venue_data.json"
    if not venue_data_path.exists():
        raise RuntimeError(
            f"generate_reports.py did not produce {venue_data_path}:\n{result.stdout}"
        )

    with open(venue_data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_venue(csv_path, venue_key, run_dir):
    venue_data = generate_venue_data(csv_path, run_dir)
    if venue_key not in venue_data:
        available = ", ".join(sorted(venue_data.keys()))
        raise KeyError(f"venue key '{venue_key}' not found in {csv_path}. Available: {available}")
    return venue_data[venue_key]


# --------------------------------------------------------------------------
# Skill invocation (always a fresh claude CLI call - no caching, unlike
# production, so editing a skill doc is reflected on the very next run)
# --------------------------------------------------------------------------

def invoke_skill(skill_text, payload, stage, venue_name):
    prompt = skill_text + "\n\nInput:\n" + json.dumps(payload, indent=2)
    return ai_analysis._invoke_claude(prompt, stage, venue_name)


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check(name, passed, detail=""):
    return {"name": name, "passed": bool(passed), "detail": detail}


def is_ordered_desc(values):
    return values == sorted(values, reverse=True)


# --------------------------------------------------------------------------
# Output: raw JSON + human-readable Markdown report
# --------------------------------------------------------------------------

def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def write_markdown_report(path, title, venue_name, input_payload, raw_output, checks, error=None, notes=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [f"# {title}", "", f"**Venue:** {venue_name}", ""]

    if error:
        lines += ["## Error", "", f"```\n{error}\n```", ""]

    lines += ["## Input sent to the skill", "", "```json", json.dumps(input_payload, indent=2), "```", ""]

    lines += ["## Raw AI output", ""]
    if raw_output is not None:
        lines += ["```json", json.dumps(raw_output, indent=2), "```", ""]
    else:
        lines += ["_No output - see Error above._", ""]

    lines += ["## Automated checks", "", "| Check | Result | Detail |", "|---|---|---|"]
    for c in checks:
        result = "PASS" if c["passed"] else "FAIL"
        detail = c["detail"].replace("|", "\\|") if c["detail"] else ""
        lines.append(f"| {c['name']} | {result} | {detail} |")
    lines.append("")

    lines += [
        "## Manual review notes",
        "",
        notes or (
            "Automated checks above only cover mechanically-checkable rules "
            "(ordering, schema, banned phrases, count bounds). Read the raw "
            "output above and judge it against the rest of the skill doc's "
            "Rules section by hand - specificity, whether themes are "
            "genuinely grounded in the input, narrative quality, etc."
        ),
        "",
    ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def print_summary(stage, checks, report_path):
    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    print(f"\n[{stage}] {passed}/{total} automated checks passed")
    for c in checks:
        mark = "PASS" if c["passed"] else "FAIL"
        print(f"  [{mark}] {c['name']}" + (f" - {c['detail']}" if c["detail"] and not c["passed"] else ""))
    print(f"[{stage}] report written to {report_path}")
