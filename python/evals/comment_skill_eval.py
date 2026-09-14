#!/usr/bin/env python3
"""
Stage 2 eval runner: templates/skills/comment_analysis.md

By default, chains from a Stage 1 result already produced by
metric_skill_eval.py for the same --run-id (output/<run-id>/metrics_analysis.json).
Pass --metrics-input to use a different Stage 1 result instead.

Usage:
    python comment_skill_eval.py
    python comment_skill_eval.py --run-id dallas
    python comment_skill_eval.py --run-id dallas --metrics-input path/to/metrics_analysis.json
"""
import argparse
import json
import sys
from pathlib import Path

import eval_common as ec

STAGE = "comment_analysis"


def run_checks(venue, result):
    checks = []

    themes = result.get("themes", [])
    magnitudes = [t.get("magnitude") for t in themes]
    checks.append(ec.check(
        "themes ordered by magnitude (highest first)",
        ec.is_ordered_desc(magnitudes),
        f"magnitudes={magnitudes}",
    ))

    bad_polarity = [t.get("label") for t in themes if t.get("polarity") not in ("positive", "negative")]
    checks.append(ec.check(
        "every theme has polarity 'positive' or 'negative'",
        not bad_polarity,
        f"themes with invalid polarity={bad_polarity}" if bad_polarity else "",
    ))

    out_of_range = [t.get("magnitude") for t in themes if not (0 <= (t.get("magnitude") or -1) <= 100)]
    checks.append(ec.check(
        "every theme's magnitude is within 0-100",
        not out_of_range,
        f"out-of-range magnitudes={out_of_range}" if out_of_range else "",
    ))

    total_comments = len(venue.get("comments", []))
    over_count = [
        t.get("label") for t in themes
        if (t.get("mention_count") or 0) > total_comments
    ]
    checks.append(ec.check(
        "no theme's mention_count exceeds the total number of comments",
        not over_count,
        f"themes with mention_count > total comments ({total_comments})={over_count}" if over_count else "",
    ))

    if total_comments == 0:
        checks.append(ec.check(
            "no themes returned when there are zero comments",
            themes == [],
            f"{len(themes)} theme(s) returned despite zero comments" if themes else "",
        ))

    missing_fields = [
        i for i, t in enumerate(themes)
        if not all(k in t for k in ("label", "polarity", "mention_count", "magnitude", "summary"))
    ]
    checks.append(ec.check(
        "every theme has label/polarity/mention_count/magnitude/summary",
        not missing_fields,
        f"theme indices missing fields={missing_fields}" if missing_fields else "",
    ))

    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", help="Path to a Qualtrics-format CSV (default: eval_config.json's default_csv)")
    parser.add_argument("--venue-key", help="Venue key within venue_data.json to test (default: eval_config.json's default_venue_key)")
    parser.add_argument("--run-id", help="Name for this run's output folder under output/ (default: eval_config.json's default_run_id)")
    parser.add_argument("--config", help="Path to eval_config.json (default: evals/eval_config.json)")
    parser.add_argument("--metrics-input", help="Path to a Stage 1 (metrics_analysis) JSON result to chain from. "
                                                  "Default: output/<run-id>/metrics_analysis.json")
    args = parser.parse_args()

    config = ec.load_config(args.config)
    csv_path = ec.resolve_path(args.csv or config["default_csv"])
    venue_key = args.venue_key or config["default_venue_key"]
    run_id = args.run_id or config["default_run_id"]

    run_dir = ec.run_dir_for(config, run_id)
    venue = ec.load_venue(csv_path, venue_key, run_dir)

    metrics_input_path = Path(args.metrics_input) if args.metrics_input else run_dir / config["stage_files"]["metrics_analysis"]
    if not metrics_input_path.exists():
        print(
            f"[comment_analysis] Stage 1 result not found at {metrics_input_path}.\n"
            f"Run `python metric_skill_eval.py --run-id {run_id}` first, or pass --metrics-input explicitly."
        )
        sys.exit(2)
    with open(metrics_input_path, "r", encoding="utf-8") as f:
        metrics_result = json.load(f)

    payload = ec.ai_analysis._build_comment_payload(venue, metrics_result.get("metric_flags", []))

    raw_result, error = ec.invoke_skill(ec.ai_analysis.COMMENT_ANALYSIS_SKILL, payload, STAGE, venue["venue"])

    checks = []
    if error:
        checks.append(ec.check("skill call succeeded", False, error))
    else:
        valid = ec.ai_analysis._validate_comment_analysis(raw_result)
        checks.append(ec.check("output matches expected schema (themes[])", valid))
        if valid:
            checks.extend(run_checks(venue, raw_result))

    report_path = run_dir / f"{STAGE}.md"
    ec.write_markdown_report(
        report_path,
        title="Stage 2: Comment Analysis Eval",
        venue_name=venue["venue"],
        input_payload=payload,
        raw_output=raw_result,
        checks=checks,
        error=error,
    )
    if not error:
        ec.write_json(run_dir / config["stage_files"][STAGE], raw_result)

    ec.print_summary(STAGE, checks, report_path)
    sys.exit(1 if any(not c["passed"] for c in checks) else 0)


if __name__ == "__main__":
    main()
