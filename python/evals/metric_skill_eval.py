#!/usr/bin/env python3
"""
Stage 1 eval runner: templates/skills/metrics_analysis.md

Runs a CSV through the real generate_reports.py, builds the exact payload
ai_analysis.py sends for the metrics_analysis stage, calls the real skill
via the real `claude` CLI, and reports both the raw output and a set of
mechanically-checkable rule checks. See EVALS.md.

Usage:
    python metric_skill_eval.py
    python metric_skill_eval.py --csv "../../example-data/topgolf_qualtrics_30_responses - DALLAS.csv" --venue-key dallas --run-id dallas
"""
import argparse
import sys

import eval_common as ec

STAGE = "metrics_analysis"


def run_checks(venue, result):
    checks = []

    flags = result.get("metric_flags", [])
    magnitudes = [f.get("magnitude") for f in flags]
    checks.append(ec.check(
        "metric_flags ordered by magnitude (highest first)",
        ec.is_ordered_desc(magnitudes),
        f"magnitudes={magnitudes}",
    ))

    valid_metric_names = {"ltr", "fun", "helpful", "issues", "resolution"}
    bad_names = [f.get("metric") for f in flags if f.get("metric") not in valid_metric_names]
    checks.append(ec.check(
        "every flag uses a known metric name (ltr/fun/helpful/issues/resolution)",
        not bad_names,
        f"unexpected metric names={bad_names}" if bad_names else "",
    ))

    out_of_range = [f.get("magnitude") for f in flags if not (0 <= (f.get("magnitude") or -1) <= 100)]
    checks.append(ec.check(
        "every flag's magnitude is within 0-100",
        not out_of_range,
        f"out-of-range magnitudes={out_of_range}" if out_of_range else "",
    ))

    if venue.get("resolution_avg") is None:
        has_resolution_flag = any(f.get("metric") == "resolution" for f in flags)
        checks.append(ec.check(
            "no resolution flag when resolution_avg is null (rule: 'MUST NOT flag resolution_avg as a "
            "concern if it is null')",
            not has_resolution_flag,
            "a resolution flag was returned despite resolution_avg being null" if has_resolution_flag else "",
        ))

    banned_phrases = ["network average", "network-wide", "compared to other", "other venues", "benchmark", "rank"]
    characterization = (result.get("characterization") or "").lower()
    hits = [p for p in banned_phrases if p in characterization]
    checks.append(ec.check(
        "characterization avoids network/comparison language (rule: 'MUST NOT reference network/company "
        "averages or comparisons to other venues')",
        not hits,
        f"matched phrases={hits}" if hits else "",
    ))

    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", help="Path to a Qualtrics-format CSV (default: eval_config.json's default_csv)")
    parser.add_argument("--venue-key", help="Venue key within venue_data.json to test (default: eval_config.json's default_venue_key)")
    parser.add_argument("--run-id", help="Name for this run's output folder under output/ (default: eval_config.json's default_run_id)")
    parser.add_argument("--config", help="Path to eval_config.json (default: evals/eval_config.json)")
    args = parser.parse_args()

    config = ec.load_config(args.config)
    csv_path = ec.resolve_path(args.csv or config["default_csv"])
    venue_key = args.venue_key or config["default_venue_key"]
    run_id = args.run_id or config["default_run_id"]

    run_dir = ec.run_dir_for(config, run_id)
    venue = ec.load_venue(csv_path, venue_key, run_dir)

    payload = ec.ai_analysis._build_metrics_payload(venue)
    raw_result, error = ec.invoke_skill(ec.ai_analysis.METRICS_ANALYSIS_SKILL, payload, STAGE, venue["venue"])

    checks = []
    if error:
        checks.append(ec.check("skill call succeeded", False, error))
    else:
        valid = ec.ai_analysis._validate_metrics_analysis(raw_result)
        checks.append(ec.check("output matches expected schema (characterization + metric_flags[])", valid))
        if valid:
            checks.extend(run_checks(venue, raw_result))

    report_path = run_dir / f"{STAGE}.md"
    ec.write_markdown_report(
        report_path,
        title="Stage 1: Metrics Analysis Eval",
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
