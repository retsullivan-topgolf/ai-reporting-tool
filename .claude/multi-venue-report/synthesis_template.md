---
name: synthesis_template
description: Multi-venue Stage 3 synthesis template - merge aggregated metrics/comments into network analysis with venue rankings
---

# Purpose

Synthesize the outputs from the multi-venue metrics analysis and comment analysis stages into a unified, ranked view of network-wide performance and per-venue guidance.

Unlike single-venue synthesis which focuses on one venue's metrics and comments, this stage merges network-wide aggregated findings into one coherent narrative that:
- Explains overall network performance
- Ranks venues by composite score (NPS or similar)
- Identifies network-wide patterns and venue-specific outliers
- Generates both network-wide recommendations and venue-specific guidance

# Inputs

Required:

- `venues`: Array of all venues with their metrics
- `metrics_analysis`: Structured output from multi-venue metrics_analysis.md containing:
  - `characterization`: Network-wide summary
  - `network_metrics`: Array of {metric, magnitude, network_avg, range, note}
  - `venue_outliers`: Array of {venue, rank, nps, note}
- `comment_analysis`: Structured output from multi-venue comment_analysis.md containing:
  - `themes`: Array of {label, magnitude, venue_breakdown, representative_detail}

If any required input is missing or incomplete, ask the user to provide the required information before continuing.

# Context

Always use:

- Both network-wide metrics characterization and comment themes as equally valid sources
- Magnitude scores from both stages (calibrated to same 0-100 scale)
- A single combined ranking of all metric flags and comment themes sorted by magnitude
- Venue breakdown from themes (which venues experience each issue/strength)
- Venue performance data (NPS, composite scores) to rank and explain tiers

Treat the provided metrics and comment analyses as the source of truth. This report covers the entire venue network - identify network-wide patterns and venue-specific opportunities, not individual venue performance in detail (that's handled by venue-specific actions).

# Workflow

1. Read all inputs carefully: `venues`, `metrics_analysis`, `comment_analysis`.
2. Validate that all required inputs are complete JSON objects with required fields.
3. Create a single combined ranking pool: merge all `network_metrics` entries and all `themes` entries, then sort by `magnitude` (highest first).
4. Build the overview by starting from the metrics characterization and folding in comment themes.
5. Rank venues by NPS (or composite score) with tier assignments.
6. Select 2-3 positive-polarity and 2-3 negative-polarity entries from combined pool for ups/downs.
7. Identify top 3 entries from combined ranking for impact section.
8. Generate recommendations:
   - `critical`: Address the #1-ranked negative finding (network-wide actions)
   - `secondary`: Address the #2-ranked negative finding
   - `maintain`: Reinforce the top-ranked positive finding
   - `venue_specific`: 1-2 sentence action for each venue (especially outliers)
9. Validate the completed output against Output and Rules sections before returning it.

# Output

Respond with ONLY a single JSON object (no markdown fences, no commentary):

```json
{
  "overview": "2-4 sentence network narrative summarizing overall performance and key variance patterns",
  "ups": ["<strong>Short title:</strong> 1-2 sentence description", ...],
  "downs": ["<strong>Short title:</strong> 1-2 sentence description", ...],
  "impact": [
    {"title": "Short driver name", "description": "1-2 sentence explanation"}
  ],
  "venue_ranking": [
    {
      "rank": 1,
      "venue": "Grand Prairie",
      "nps": 8.8,
      "composite_score": 8.8,
      "tier": "top_performer",
      "summary": "1-2 sentence summary of this venue's position"
    },
    ...
  ],
  "recommendations": {
    "critical": {
      "title": "Short priority name",
      "items": ["<strong>Action name:</strong> description", ...]
    },
    "secondary": {...},
    "maintain": {...},
    "venue_specific": [
      {
        "venue": "Venue name",
        "priority": "critical" or "secondary" or "maintain",
        "action": "1-2 sentence action specific to this venue"
      },
      ...
    ]
  }
}
```

# Rules

## Combined Ranking
- MUST merge all `network_metrics` and all `themes` entries into a single pool
- MUST sort the combined pool by `magnitude` (highest first)
- MUST use this combined ranking as the backbone for `impact` and `recommendations` sections
- MUST NOT rank metric flags and comment themes separately
- MUST allow high-magnitude positives to rank above low-magnitude negatives

## Overview Section

<!-- SKILL:venue-overview -->

## Venue Ranking Section

<!-- SKILL:ranking -->

## Ups and Downs Sections

<!-- SKILL:ups-downs -->

## Impact Section

- MUST include the top 3 entries from the combined ranking, most impactful first
- MUST cite the actual number from the source entry's `note` (for metrics) or from the venue breakdown context
- MUST use 1-2 sentences per entry
- MUST explain what this driver means for network-wide performance

## Recommendations Section

<!-- SKILL:recommendations -->

## Formatting

- MUST use inline HTML limited to `<strong>` tags only
- MUST ground every claim in a number or stated finding from input stages
- MUST NOT state or imply comparisons to other networks or previous periods (this is single-period analysis)
- MUST carry specific venue names and details (not generalized language)

# Example

**Input:**
- 7 venues with aggregated metrics and themes
- Top metrics: NPS (8.2 average), Staff (16 mentions), Equipment (18 mentions)
- Top issue: Equipment reliability (18 mentions, varies by venue)
- Best performer: Grand Prairie (8.8 NPS)
- Worst performer: El Paso (7.1 NPS)

**Output (excerpt):**
```json
{
  "overview": "The venue network shows strong overall satisfaction (8.2 NPS average), driven by consistent staff responsiveness and solid game experiences. However, equipment reliability varies significantly by location, with Grand Prairie performing well (8.8 NPS) while El Paso faces challenges (7.1 NPS, 35% issue rate). This variance suggests venue-specific equipment or maintenance differences offer a clear operational lever for network-wide improvement.",
  "ups": [
    "<strong>Consistent staff responsiveness:</strong> Praised across all venues (16 mentions total), with Grand Prairie and Austin leading. This is a network-wide strength worth protecting.",
    "<strong>Strong NPS at top venues:</strong> Grand Prairie (8.8) and Austin (8.4) demonstrate that 8.5+ NPS is achievable. Their practices should be modeled network-wide."
  ],
  "downs": [
    "<strong>Equipment reliability varies significantly:</strong> While Grand Prairie has minimal issues (18%), El Paso faces challenges (35%). This 17-point spread suggests venue-specific factors (maintenance, staffing, equipment age) are at play.",
    "<strong>F&B service speed is a network-wide concern:</strong> Average 3.2/5 across all venues, with no venue exceeding 3.5. This is a systemic issue affecting all locations."
  ],
  "impact": [
    {
      "title": "NPS (Network Average: 8.2)",
      "description": "Strong overall satisfaction drives network performance, ranging from 7.1 (El Paso) to 8.8 (Grand Prairie). The 1.7-point spread indicates venue-specific operational factors significantly impact satisfaction."
    },
    {
      "title": "Equipment Reliability",
      "description": "Issue frequency varies dramatically (18% at Grand Prairie vs. 35% at El Paso), with 18 comments mentioning equipment problems. This is the primary operational lever for network-wide improvement."
    },
    {
      "title": "Staff Responsiveness",
      "description": "Consistently praised across all venues (16 mentions), with no venue falling below 3.5/5. This is a network-wide strength being maintained uniformly."
    }
  ],
  "venue_ranking": [
    {
      "rank": 1,
      "venue": "Grand Prairie",
      "nps": 8.8,
      "composite_score": 8.8,
      "tier": "top_performer",
      "summary": "Best performer across all metrics. Strong NPS (8.8), low issue rate (18%), and excellent staff responsiveness. Model for network."
    },
    {
      "rank": 2,
      "venue": "Austin",
      "nps": 8.4,
      "composite_score": 8.4,
      "tier": "top_performer",
      "summary": "Strong performance with solid NPS (8.4) and good staff responsiveness. Equipment reliability slightly below network average."
    },
    ...
  ],
  "recommendations": {
    "critical": {
      "title": "Standardize Equipment Maintenance Across Network",
      "items": [
        "<strong>Share Grand Prairie's maintenance playbook:</strong> Grand Prairie achieves 18% issue rate vs. network average 28%. Document their daily calibration and maintenance schedule and roll out network-wide.",
        "<strong>Audit El Paso's equipment:</strong> 35% issue rate suggests equipment age, maintenance gaps, or staffing issues. Conduct on-site assessment and develop remediation plan.",
        "<strong>Implement daily equipment checks:</strong> Establish network-wide standard for pre-opening equipment verification to catch issues before guests arrive."
      ]
    },
    "secondary": {...},
    "maintain": {...},
    "venue_specific": [
      {
        "venue": "Grand Prairie",
        "priority": "maintain",
        "action": "Continue current practices—you're the network leader. Share your equipment maintenance playbook with other venues."
      },
      {
        "venue": "Austin",
        "priority": "secondary",
        "action": "Address equipment reliability (6 mentions). Implement Grand Prairie's maintenance schedule and monitor for improvement."
      },
      {
        "venue": "El Paso",
        "priority": "critical",
        "action": "High issue rate (35%) requires urgent attention. Conduct equipment audit, assess staffing, and implement Grand Prairie's maintenance practices."
      }
    ]
  }
}
```

# Resources

## Related Skills

For detailed guidance on each section of this synthesis, see:

- `multi-venue-overview-skill.md` - Guidance on writing the network narrative
- `multi-venue-ranking-skill.md` - Guidance on ranking venues and explaining tiers
- `multi-venue-ups-downs-skill.md` - Guidance on selecting network patterns and variance findings
- `multi-venue-impact-drivers-skill.md` - Guidance on identifying top drivers at network level
- `multi-venue-recommendations-skill.md` - Guidance on generating network and venue-specific actions

## Input Sources

This template references the outputs from:
- Multi-venue `.claude/multi-venue-report/metrics_analysis.md` (Stage 1)
- Multi-venue `.claude/multi-venue-report/comment_analysis.md` (Stage 2)
