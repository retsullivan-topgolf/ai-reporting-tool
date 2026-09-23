---
name: metrics_analysis
description: Multi-venue Stage 1 - aggregate metrics across all venues, identify network patterns and outliers
---

# Purpose

Aggregate metrics from all venues into a network-wide analysis that identifies:
- Network-wide average performance (e.g., network NPS is 8.2/10)
- Performance variance by venue (which venues are above/below average?)
- Outliers (best and worst performers)
- Network-wide concerns and strengths

This is fundamentally different from single-venue metrics_analysis: instead of analyzing one venue's 5 metrics in isolation, this analyzes how all 7 venues compare to each other and to the network average.

# Inputs

Required:

- `venues`: Array of venue objects, each containing:
  - `venue`: Venue name (string)
  - `responses`: Response count (integer)
  - `metrics`: Object with the following fields (each a float or null):
    - `ltr_avg`: Likelihood to Return (1-5 scale)
    - `fun_avg`: Fun (1-5 scale)
    - `helpful_avg`: Helpful (1-5 scale)
    - `issues_pct`: Issues Percentage (0-100)
    - `resolution_avg`: Issue Resolution (1-5 scale)
    - `nps_avg`: Combined NPS (1-10 scale, may be null)
    - `fb_average`: F&B Average (1-5 scale, may be null for some venues)

Example input:
```json
{
  "venues": [
    {
      "venue": "Grand Prairie",
      "responses": 45,
      "metrics": {
        "ltr_avg": 4.4,
        "fun_avg": 4.1,
        "helpful_avg": 3.8,
        "issues_pct": 22,
        "resolution_avg": 3.9,
        "nps_avg": 8.8,
        "fb_average": 3.5
      }
    },
    {
      "venue": "Austin",
      "responses": 38,
      "metrics": {
        "ltr_avg": 4.0,
        "fun_avg": 3.9,
        ...
      }
    },
    ...
  ],
  "assessment_tiers": {...}
}
```

If any required venue is missing or incomplete, ask the user to provide complete data.

# Context

Always use:

- Network average (mean across all venues with available data) as the baseline for comparison
- Range (min/max) to show variance
- Outliers to identify best/worst performers
- Per-venue metrics to understand where network problems originate
- Missing data (some venues may lack F&B metrics) - handle gracefully by noting availability

Treat the provided venue metrics as the source of truth. This analysis covers the entire network as a single unit of analysis - identify network-wide patterns, not individual venue performance (that's done in the ranking skill).

# Workflow

1. Read all inputs carefully: `venues`, `assessment_tiers`.
2. Validate that all required venues have complete metric data.
3. For each metric (LTR, Fun, Helpful, Issues, Resolution, NPS, F&B):
   - Compute network average (mean) across all venues with available data
   - Compute range (min, max)
   - Identify outliers (venues significantly above/below network average)
   - Flag high-variance metrics (range > 0.5 points)
4. Create a network-wide characterization that synthesizes overall performance
5. Generate per-metric analysis with outlier identification
6. Identify venue-specific outliers (best/worst performer overall)

# Output

Respond with ONLY a single JSON object (no markdown fences, no commentary):

```json
{
  "characterization": "2-3 sentence network-wide summary of overall performance",
  "network_metrics": [
    {
      "metric": "nps",
      "polarity": "positive",
      "magnitude": 82,
      "network_avg": 8.2,
      "range": "7.1 - 8.8",
      "note": "Strong network-wide NPS (8.2/10 average), ranging from 7.1 (El Paso) to 8.8 (Grand Prairie)"
    },
    {
      "metric": "issues",
      "polarity": "negative",
      "magnitude": 65,
      "network_avg": 28,
      "range": "18% - 35%",
      "note": "Issue frequency varies significantly (18% at Grand Prairie vs. 35% at El Paso), suggesting venue-specific operational factors"
    },
    ...
  ],
  "venue_outliers": [
    {
      "venue": "Grand Prairie",
      "rank": 1,
      "nps": 8.8,
      "note": "Best performer—strong across all metrics"
    },
    {
      "venue": "El Paso",
      "rank": 7,
      "nps": 7.1,
      "note": "Needs support—high issue rate (35%) and low resolution satisfaction"
    },
    ...
  ]
}
```

# Rules

## Network Aggregation
- MUST compute network average (mean) for each metric across all venues
- MUST compute range (min/max) for each metric
- MUST flag high-variance metrics (range > 0.5 points)
- MUST identify which venues are above/below network average for each metric
- MUST handle missing data gracefully (some venues may lack F&B metrics)
  - Note in output: "F&B metrics available for 5/7 venues"
  - Exclude venues with missing data from that metric's average

## Magnitude Scoring
- Magnitude is calibrated to 0-100 scale (same as single-venue comment themes)
- For positive metrics (NPS, LTR, Fun, etc.):
  - 90-100: Excellent (network average ≥8.0 on 1-10 scale or ≥4.0 on 1-5 scale)
  - 70-89: Strong (average ≥7.0 or ≥3.5)
  - 50-69: Moderate (average ≥5.0 or ≥2.5)
  - 30-49: Weak (average <5.0 or <2.5)
  - 0-29: Critical (average <3.0 or <1.5)
- For negative metrics (Issues %):
  - 90-100: Critical (average ≥50%)
  - 70-89: High (average ≥30%)
  - 50-69: Moderate (average ≥20%)
  - 30-49: Low (average ≥10%)
  - 0-29: Minimal (average <10%)

## Outlier Identification
- MUST identify best performer (highest NPS or composite score)
- MUST identify worst performer (lowest NPS or composite score)
- MUST note venues that are significantly above/below network average (±0.5 points)
- MUST rank venues (1 = best, 7 = worst) based on NPS or composite score
- Outliers should explain WHY they're outliers (e.g., "strong across all metrics" vs. "high issue rate")

## Characterization
- MUST start with overall network performance (strong/moderate/weak)
- MUST acknowledge venue variance ("varies significantly by location")
- MUST identify network-wide concerns (e.g., "equipment reliability is primary concern")
- MUST NOT focus on individual venues (that's done in ranking skill)
- MUST be 2-3 sentences
- MUST be grounded in numbers from the venue metrics

## Formatting
- MUST use inline HTML limited to `<strong>` tags only
- MUST ground every claim in a number from the input stages
- MUST NOT state or imply comparisons to other networks or previous periods (this is single-period analysis)

# Example

**Input:**
- 7 venues with metrics
- Network NPS average: 8.2 (range 7.1-8.8)
- Network LTR average: 4.1 (range 3.8-4.4)
- Network Issues average: 28% (range 18%-35%)
- Grand Prairie: 8.8 NPS, 18% issues (best performer)
- El Paso: 7.1 NPS, 35% issues (worst performer)

**Output:**
```json
{
  "characterization": "The venue network shows strong overall satisfaction (8.2 NPS average) with consistent guest experiences across most locations. However, performance varies significantly by venue, with Grand Prairie leading (8.8 NPS) and El Paso lagging (7.1 NPS). Equipment reliability is the primary network-wide concern, with issue frequency ranging from 18% to 35% depending on venue.",
  "network_metrics": [
    {
      "metric": "nps",
      "polarity": "positive",
      "magnitude": 82,
      "network_avg": 8.2,
      "range": "7.1 - 8.8",
      "note": "Strong network-wide NPS (8.2/10 average). Range of 1.7 points suggests venue-specific operational factors influence satisfaction."
    },
    {
      "metric": "ltr",
      "polarity": "positive",
      "magnitude": 80,
      "network_avg": 4.1,
      "range": "3.8 - 4.4",
      "note": "Strong Likelihood to Return across network (4.1/5 average). All venues above 3.5 threshold."
    },
    {
      "metric": "issues",
      "polarity": "negative",
      "magnitude": 70,
      "network_avg": 28,
      "range": "18% - 35%",
      "note": "Issue frequency varies significantly. Grand Prairie achieves 18% (acceptable) while El Paso faces 35% (high). This 17-point spread is the primary venue-specific variance."
    },
    {
      "metric": "fun",
      "polarity": "positive",
      "magnitude": 78,
      "network_avg": 4.0,
      "range": "3.7 - 4.3",
      "note": "Fun scores solid network-wide (4.0/5 average). No venue falls below 3.5 threshold."
    }
  ],
  "venue_outliers": [
    {
      "venue": "Grand Prairie",
      "rank": 1,
      "nps": 8.8,
      "note": "Best performer. Highest NPS (8.8), lowest issues (18%), strong Fun (4.3). Model for network."
    },
    {
      "venue": "Austin",
      "rank": 2,
      "nps": 8.4,
      "note": "Strong performer. NPS above network average, solid on all metrics."
    },
    {
      "venue": "El Paso",
      "rank": 7,
      "nps": 7.1,
      "note": "Needs support. Lowest NPS (7.1), highest issues (35%), lowest Fun (3.7). Opportunity for significant improvement."
    }
  ]
}
```

# Related Skills

For detailed guidance on how to use this analysis, see:
- `multi-venue-overview-skill.md` - How to write the network narrative
- `multi-venue-ranking-skill.md` - How to rank and explain venue tiers
- `multi-venue-impact-drivers-skill.md` - How to identify top drivers

## Input Sources

This stage reads the venue metrics directly from the input. It is Stage 1 of 3 in the multi-venue pipeline.
