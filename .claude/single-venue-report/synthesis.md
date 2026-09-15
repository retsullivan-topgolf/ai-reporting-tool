---
name: synthesis
description: Merge metric flags and comment themes into a ranked analysis with overview, drivers, and recommendations for a single venue
---

# Purpose

Synthesize the outputs from the metrics analysis and comment analysis stages into a unified, ranked view of what matters most for a venue's performance. This is Stage 3 of 3 in the venue report analysis pipeline.

Unlike the earlier stages which work independently on metrics or comments, this stage merges both structured analyses into one coherent narrative, ranking all findings by magnitude to identify the top impact drivers and generate actionable recommendations.

# Inputs

Required:

- `venue`: venue name (for narrative grounding and context)
- `responses`: total survey count for the period (for context)
- `metrics_analysis`: structured output from `.claude/single-venue-report/metrics_analysis.md` containing:
  - `characterization`: narrative summary of overall performance
  - `metric_flags`: array of `{metric, polarity, magnitude, note}` entries
- `comment_analysis`: structured output from `.claude/single-venue-report/comment_analysis.md` containing:
  - `themes`: array of `{label, polarity, mention_count, magnitude, summary, representative_detail}` entries

If any required input is missing or incomplete (including all fields in `metric_flags` and `themes` arrays), ask the user to provide the required information before continuing.

# Context

Always use:

- Both the metrics characterization and comment themes as equally valid sources of truth
- The magnitude scores from both stages as-is; they are already calibrated to the same 0-100 scale for fair comparison
- A single combined ranking of all metric flags and comment themes sorted by magnitude (highest first)
- Specific names from comment themes (game names, facility problems, etc.) rather than generic labels
- Numbers and claims that are directly traceable back to the input stages

When applicable, use:

- The metrics characterization as the foundation for the overview, then fold in comment themes that explain *why* the numbers look that way
- Honest acknowledgment when metrics and comments tell different stories - that's a real finding, not an error
- The combined ranking to determine priority order for recommendations, not topic-based or sentiment-based ordering
- F&B metrics and themes to explain how food and beverage experiences contribute to overall satisfaction (e.g., strong F&B may offset operational issues, or weak F&B may be a distinct concern)

Treat the provided metrics and comment analyses as the source of truth. This report covers one venue in isolation - do not state or imply network averages, network rankings, or comparisons to other venues.

# Workflow

1. Read all inputs carefully: `venue`, `responses`, `metrics_analysis`, and `comment_analysis`.
2. Validate that both `metrics_analysis` and `comment_analysis` are complete JSON objects with all required fields.
3. Create a single combined ranking pool: merge all `metric_flags` entries and all `themes` entries, then sort by `magnitude` (highest first).
4. Build the overview by starting from the metrics characterization and folding in comment themes that explain the numbers or add context the metrics can't show.
5. Identify the top 3 entries from the combined ranking for the impact section.
6. Select 2-3 positive-polarity and 2-3 negative-polarity entries from the combined pool for ups and downs (not necessarily only the top 3).
7. Generate recommendations by deriving actions from the combined ranking:
   - `critical`: 3-4 concrete actions addressing the #1-ranked negative entry
   - `secondary`: 3-4 concrete actions addressing the #2-ranked negative entry (or a sensible operational fallback if only one negative exists)
   - `maintain`: 3-4 concrete actions reinforcing the top-ranked positive entry
8. Validate the completed output against the Output and Rules sections before returning it.

# Output

Respond with ONLY a single JSON object (no markdown fences, no commentary before or after):

```json
{
  "overview": "2-4 sentence narrative paragraph summarizing the venue's overall performance, grounded in both the metrics characterization and the comment themes",
  "ups": ["<strong>Short title:</strong> 1-2 sentence description", ...],
  "downs": ["<strong>Short title:</strong> 1-2 sentence description", ...],
  "impact": [
    {"title": "Short driver name", "description": "1-2 sentence explanation of why this driver matters, citing the underlying number"}
  ],
  "recommendations": {
    "critical": {"title": "Short priority name", "items": ["<strong>Action name:</strong> description", ...]},
    "secondary": {"title": "Short priority name", "items": ["<strong>Action name:</strong> description", ...]},
    "maintain": {"title": "Short priority name", "items": ["<strong>Action name:</strong> description", ...]}
  }
}
```

# Rules

## Combined Ranking

- MUST merge all `metric_flags` and all `themes` entries into a single pool
- MUST sort the combined pool by `magnitude` (highest first)
- MUST use this combined ranking as the backbone for `impact` and `recommendations` sections
- MUST NOT rank metric flags and comment themes separately by topic or sentiment
- MUST allow high-magnitude positives to rank above low-magnitude negatives

## Overview Section

- MUST start from the `metrics_analysis.characterization` as the foundation
- MUST fold in comment themes that explain *why* the numbers look that way or add context metrics can't show
- SHOULD acknowledge honestly when metrics and comments tell different stories - that's a real finding
- MUST NOT introduce numbers or claims not traceable back to the input stages
- MUST avoid citing the exact metric numbers that appear in the Performance Summary cards (e.g., don't say "2.6/5 resolution" or "26% issues" since those are displayed below); however, you MAY use general descriptive language like "over half", "roughly 70%", or "most guests" to convey magnitude without redundancy

## Impact Section

- MUST include the top 3 entries from the combined ranking, most impactful first
- MUST cite the actual number from the source entry's `note` (for metrics) or `summary` (for themes) in each description
- MUST use 1-2 sentences per entry

## Ups and Downs Sections

- MUST include 2-3 items each
- MUST draw from positive-polarity entries (for ups) and negative-polarity entries (for downs) in the combined pool
- MUST NOT limit to only the top 3 from impact - a venue can have more than three notable things
- SHOULD prioritize by magnitude (highest first) when selecting which items to include
- MAY include lower-magnitude items if they add distinct operational value or context that complements the impact section
- MUST use 1-2 sentences per item

## Recommendations Section

- MUST follow the combined ranking priority order - never put a lower-ranked negative in "critical" while a higher-ranked one is only "secondary"
- `critical`: MUST address the #1-ranked negative entry from the combined pool
- `secondary`: MUST address the #2-ranked negative entry; if only one negative exists, use a sensible general operational-consistency priority instead
- `maintain`: MUST reinforce the top-ranked positive entry (a strong metric flag or loved theme) - something worth protecting, not fixing
- MUST include 3-4 concrete action items per section

## Recommendations Generation

- MUST derive each action directly from the combined ranking, addressing the top-ranked issues first
- MUST include 3-4 concrete, venue-specific action items per section
- Actions MUST be operationally feasible and directly traceable to a ranked finding from either metrics or comments
- For `critical` and `secondary`: actions MUST directly address the negative finding (e.g., if equipment reliability is #1, actions should target equipment maintenance, diagnostics, or response protocols)
- For `maintain`: actions MUST protect or reinforce the positive finding (e.g., if staff responsiveness is top-ranked positive, actions should preserve those practices and recognize staff)
- Actions MAY reference specific details from comment themes (named games, facility problems, visit phases) rather than generic operational areas
- Each action MUST be 1-2 sentences and start with a short, bold action name

## Overview Narrative Balance

- MUST start from the `metrics_analysis.characterization` as the foundation
- MUST fold in comment themes that explain *why* the numbers look that way or add context metrics alone can't show
- SHOULD balance metrics-driven insights (aggregate scores, percentages) with comment-driven insights (specific themes, named issues)
- When metrics and comments tell different stories, MUST acknowledge this honestly as a real finding (e.g., "high satisfaction scores despite frequent equipment issues")
- MUST NOT introduce numbers or claims not directly traceable to the input stages

## Formatting

- MUST use inline HTML limited to `<strong>` tags only
- MUST carry specific names from comment themes (game names, facility problems, visit phases) into ups/downs/impact/recommendations instead of genericizing them
- MUST ground every claim in a number or stated theme from the input stages - no untraced claims
- MUST NOT state or imply network averages, network rankings, or comparisons to other venues

# Example

The following demonstrates formatting and synthesis approach. Do not assume these requirements apply to the user's source.

**Input:**
- Metrics: characterization = "Strong overall satisfaction with high LTR (87%) but equipment reliability issues are dragging down Fun scores"; metric_flags = [{metric: "LTR", polarity: "positive", magnitude: 82, note: "87% would recommend"}, {metric: "Equipment reliability", polarity: "negative", magnitude: 71, note: "Screen tracking failures in 14 comments"}]
- Comments: themes = [{label: "Equipment reliability", polarity: "negative", magnitude: 71, summary: "Screens losing shot tracking mid-session"}, {label: "Staff responsiveness", polarity: "positive", magnitude: 65, summary: "Staff quickly addressing issues"}]

**Combined ranking (by magnitude):**
1. LTR (positive, 82)
2. Equipment reliability (negative, 71)
3. Staff responsiveness (positive, 65)

**Output:**
```json
{
  "overview": "This venue is performing well overall, driven by strong satisfaction with the experience. However, equipment reliability issues - particularly screen tracking failures - are creating friction that's preventing the entertainment experience from reaching its potential. Staff responsiveness is a bright spot, with most guests noting quick resolution of problems.",
  "ups": [
    "<strong>Strong recommendation intent:</strong> 87% of guests would recommend the venue, indicating solid overall satisfaction with the experience.",
    "<strong>Responsive staff:</strong> Guests consistently praised staff for quickly addressing and resolving equipment issues to get them back to playing."
  ],
  "downs": [
    "<strong>Equipment reliability:</strong> Screen tracking failures are the dominant complaint, mentioned in 14 comments and cited as a frequent frustration even when quickly resolved."
  ],
  "impact": [
    {"title": "Recommendation Intent", "description": "87% LTR indicates strong overall satisfaction and loyalty, the primary driver of venue performance."},
    {"title": "Equipment Reliability", "description": "Screen tracking failures mentioned in 14 comments are the most significant operational issue, directly impacting the Fun experience."},
    {"title": "Staff Responsiveness", "description": "Quick problem resolution is a valued differentiator, with 8 guests specifically praising staff for getting them back to playing quickly."}
  ],
  "recommendations": {
    "critical": {
      "title": "Fix Equipment Reliability",
      "items": [
        "<strong>Preventive maintenance schedule:</strong> Implement daily screen calibration checks before peak hours to catch tracking issues before guests encounter them.",
        "<strong>Rapid response protocol:</strong> Ensure staff can resolve screen issues within 2 minutes; guests accept occasional failures if resolution is fast.",
        "<strong>Root cause analysis:</strong> Investigate whether tracking failures are hardware, software, or calibration-related to target the fix appropriately."
      ]
    },
    "secondary": {
      "title": "Operational Consistency",
      "items": [
        "<strong>Service standard documentation:</strong> Document the rapid-response practices that staff are already doing well so consistency is maintained across shifts.",
        "<strong>Staff training refresh:</strong> Ensure all staff know the equipment troubleshooting steps to maintain the responsiveness guests are experiencing."
      ]
    },
    "maintain": {
      "title": "Protect Recommendation Intent",
      "items": [
        "<strong>Guest satisfaction tracking:</strong> Continue monitoring LTR and Fun scores to ensure equipment fixes maintain the strong recommendation intent.",
        "<strong>Staff recognition:</strong> Acknowledge and reward the responsive staff behaviors that guests are noticing and appreciating.",
        "<strong>Experience consistency:</strong> Protect the overall experience quality that's driving the 87% recommendation rate."
      ]
    }
  }
}
```

# Resources

## Related Skills

For detailed guidance on each section of this synthesis, see:

- `venue-overview-skill.md` - Guidance on writing the overview narrative
- `ups-downs-skill.md` - Guidance on selecting and articulating ups/downs
- `impact-drivers-skill.md` - Guidance on identifying and explaining impact drivers
- `recommendations-skill.md` - Guidance on generating actionable recommendations

See also:
- `overview-metrics-guidance.md` - Detailed guidance on how to handle metrics in the overview

## Input Sources

This Skill references the outputs from:
- `.claude/single-venue-report/metrics_analysis.md` (Stage 1)
- `.claude/single-venue-report/comment_analysis.md` (Stage 2)
