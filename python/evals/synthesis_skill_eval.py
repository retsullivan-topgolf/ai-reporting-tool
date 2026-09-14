#!/usr/bin/env python3
"""
Stage 3 eval runner: templates/skills/synthesis.md

By default, chains from Stage 1 and Stage 2 results already produced for
the same --run-id (output/<run-id>/metrics_analysis.json and
output/<run-id>/comment_analysis.json). Pass --metrics-input /
--comments-input to use different results instead.

Usage:
    python synthesis_skill_eval.py
    python synthesis_skill_eval.py --run-id dallas
    python synthesis_skill_eval.py --run-id dallas --metrics-input m.json --comments-input c.json
"""
import argparse
import json
import sys
from pathlib import Path

import eval_common as ec

STAGE = "synthesis"


def combined_ranking(metrics_result, comment_result):
    pool = [
        {"name": f.get("metric"), "polarity": f.get("polarity"), "magnitude": f.get("magnitude")}
        for f in metrics_result.get("metric_flags", [])
    ] + [
        {"name": t.get("label"), "polarity": t.get("polarity"), "magnitude": t.get("magnitude")}
        for t in comment_result.get("themes", [])
    ]
    return sorted(pool, key=lambda x: x.get("magnitude") or 0, reverse=True)


def run_checks(metrics_result, comment_result, result):
    checks = []

    ups = result.get("ups", [])
    downs = result.get("downs", [])
    checks.append(ec.check("ups has 2-3 items", 2 <= len(ups) <= 3, f"len(ups)={len(ups)}"))
    checks.append(ec.check("downs has 2-3 items", 2 <= len(downs) <= 3, f"len(downs)={len(downs)}"))

    impact = result.get("impact", [])
    checks.append(ec.check("impact has exactly 3 entries", len(impact) == 3, f"len(impact)={len(impact)}"))

    rec = result.get("recommendations", {})
    for tier in ("critical", "secondary", "maintain"):
        section = rec.get(tier, {})
        items = section.get("items", [])
        checks.append(ec.check(
            f"recommendations.{tier} has 3-4 items",
            3 <= len(items) <= 4,
            f"len(items)={len(items)}",
        ))

    pool = combined_ranking(metrics_result, comment_result)
    if pool:
        top_name = (pool[0].get("name") or "").lower()
        impact_text = " ".join(f"{d.get('title', '')} {d.get('description', '')}" for d in impact).lower()
        checks.append(ec.check(
            "the #1-ranked combined entry (by magnitude) is reflected in the impact section "
            "(rule: 'impact MUST include the top 3 entries from the combined ranking')",
            top_name in impact_text if top_name else True,
            f"top-ranked entry='{pool[0].get('name')}' (magnitude={pool[0].get('magnitude')})",
        ))

        top_negative = next((p for p in pool if p.get("polarity") == "negative"), None)
        if top_negative:
            critical_text = " ".join(rec.get("critical", {}).get("items", [])).lower()
            checks.append(ec.check(
                "the #1-ranked negative entry is reflected in recommendations.critical "
                "(rule: 'critical MUST address the #1-ranked negative entry')",
                (top_negative.get("name") or "").lower() in critical_text,
                f"top negative entry='{top_negative.get('name')}' (magnitude={top_negative.get('magnitude')})",
            ))

        top_positive = next((p for p in pool if p.get("polarity") == "positive"), None)
        if top_positive:
            maintain_text = " ".join(rec.get("maintain", {}).get("items", [])).lower()
            checks.append(ec.check(
                "the #1-ranked positive entry is reflected in recommendations.maintain "
                "(rule: 'maintain MUST reinforce the top-ranked positive entry')",
                (top_positive.get("name") or "").lower() in maintain_text,
                f"top positive entry='{top_positive.get('name')}' (magnitude={top_positive.get('magnitude')})",
            ))

    banned_phrases = ["network average", "network-wide", "compared to other", "other venues", "benchmark", "rank"]
    overview = (result.get("overview") or "").lower()
    hits = [p for p in banned_phrases if p in overview]
    checks.append(ec.check(
        "overview avoids network/comparison language "
        "(rule: 'MUST NOT state or imply network averages, network rankings, or comparisons to other venues')",
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
    parser.add_argument("--metrics-input", help="Path to a Stage 1 (metrics_analysis) JSON result to chain from. "
                                                  "Default: output/<run-id>/metrics_analysis.json")
    parser.add_argument("--comments-input", help="Path to a Stage 2 (comment_analysis) JSON result to chain from. "
                                                   "Default: output/<run-id>/comment_analysis.json")
    args = parser.parse_args()

    config = ec.load_config(args.config)
    csv_path = ec.resolve_path(args.csv or config["default_csv"])
    venue_key = args.venue_key or config["default_venue_key"]
    run_id = args.run_id or config["default_run_id"]

    run_dir = ec.run_dir_for(config, run_id)
    venue = ec.load_venue(csv_path, venue_key, run_dir)

    metrics_input_path = Path(args.metrics_input) if args.metrics_input else run_dir / config["stage_files"]["metrics_analysis"]
    comments_input_path = Path(args.comments_input) if args.comments_input else run_dir / config["stage_files"]["comment_analysis"]
    for label, p in (("Stage 1 (metrics_analysis)", metrics_input_path), ("Stage 2 (comment_analysis)", comments_input_path)):
        if not p.exists():
            print(
                f"[synthesis] {label} result not found at {p}.\n"
                f"Run the earlier stage(s) for --run-id {run_id} first, or pass --metrics-input/--comments-input explicitly."
            )
            sys.exit(2)

    with open(metrics_input_path, "r", encoding="utf-8") as f:
        metrics_result = json.load(f)
    with open(comments_input_path, "r", encoding="utf-8") as f:
        comment_result = json.load(f)

    payload = {
        "venue": venue["venue"],
        "responses": venue["responses"],
        "metrics_analysis": metrics_result,
        "comment_analysis": comment_result,
    }

    raw_result, error = ec.invoke_skill(ec.ai_analysis.SYNTHESIS_SKILL, payload, STAGE, venue["venue"])

    checks = []
    if error:
        checks.append(ec.check("skill call succeeded", False, error))
    else:
        valid = ec.ai_analysis._validate_synthesis(raw_result)
        checks.append(ec.check("output matches expected schema (overview/ups/downs/impact/recommendations)", valid))
        if valid:
            checks.extend(run_checks(metrics_result, comment_result, raw_result))

    report_path = run_dir / f"{STAGE}.md"
    ec.write_markdown_report(
        report_path,
        title="Stage 3: Synthesis Eval",
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
