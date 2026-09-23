---
name: comment_analysis
description: Multi-venue Stage 2 - aggregate comment themes across all venues, track venue-specific patterns
---

# Purpose

Aggregate comment themes from all venues into a network-wide analysis that identifies:
- Network-wide themes (which issues/strengths appear across the network?)
- Venue-specific patterns (which venues mention each theme?)
- Network consensus vs. venue outliers (e.g., "equipment reliability is only a problem at El Paso")
- Severity variation (is a theme consistently severe, or does it vary by venue?)

This is fundamentally different from single-venue comment_analysis: instead of analyzing one venue's comments in isolation, this analyzes which themes appear across multiple venues and identifies venue-specific clusters.

# Inputs

Required:

- `venues`: Array of venue objects, each containing:
  - `venue`: Venue name (string)
  - `responses`: Response count (integer)
  - `comments`: Array of comment objects, each with:
    - `text`: Comment text (string)
    - `ltr`: Likelihood to Return score (1-5, if available)
    - `fun`: Fun score (1-5, if available)
    - (other optional fields like `issues`, `resolution`, etc.)
- `metric_flags`: From the metrics_analysis stage (per-metric concerns flagged)

Example input:
```json
{
  "venues": [
    {
      "venue": "Grand Prairie",
      "responses": 45,
      "comments": [
        {
          "text": "Screen tracking worked great, no issues.",
          "ltr": 5,
          "fun": 5
        },
        ...
      ]
    },
    {
      "venue": "Austin",
      "responses": 38,
      "comments": [...]
    },
    ...
  ],
  "metric_flags": [...]
}
```

If any required input is missing, ask the user to provide it.

# Context

Always use:

- Network-wide theme patterns (not individual venue themes)
- Venue breakdown for each theme (which venues, how often, severity)
- Magnitude calibrated to network-wide prevalence (not just total mention count)
- Metric flags from Stage 1 to contextualize which themes matter most
- Honest acknowledgment of venue-specific outliers (e.g., "this is only a problem at one venue")

Treat the provided comments as the source of truth. This analysis covers the entire network - identify network-wide patterns and venue-specific clusters, not individual venue performance.

# Workflow

1. Read all inputs carefully: `venues`, `metric_flags`.
2. Validate that all venues have comment arrays.
3. For each comment across all venues:
   - Extract theme/sentiment
   - Track which venue the comment comes from
   - Note severity (based on scores, language intensity)
4. Aggregate themes across venues:
   - Count total mentions across network
   - Break down by venue (which venues mention this theme, how many times)
   - Identify severity by venue (is it high everywhere or only in one location?)
5. For each theme:
   - Compute network-wide magnitude (0-100 scale)
   - Identify best-represented venue (most mentions)
   - Identify worst-represented venue (fewest mentions)
   - Flag venue-specific outliers ("only mentioned at venue X")
6. Sort all themes by network-wide magnitude (highest first)

# Output

Respond with ONLY a single JSON object (no markdown fences, no commentary):

```json
{
  "themes": [
    {
      "label": "Theme name (noun form)",
      "polarity": "positive" or "negative",
      "mention_count": 18,
      "magnitude": 68,
      "network_summary": "2-3 sentence summary of network-wide pattern and variance",
      "venue_breakdown": [
        {
          "venue": "El Paso",
          "mentions": 8,
          "severity": "high",
          "representative_detail": "\"Screen stopped tracking constantly, really frustrating.\""
        },
        {
          "venue": "Austin",
          "mentions": 6,
          "severity": "medium",
          "representative_detail": "\"Screen stopped tracking mid-game, but staff fixed it quickly.\""
        },
        ...
      ],
      "representative_detail": "\"Screen stopped tracking constantly, really frustrating.\" (El Paso)"
    },
    ...
  ]
}
```

# Rules

## Theme Aggregation
- MUST aggregate themes across all venues into network-wide list
- MUST count total mentions across all venues
- MUST break down by venue (venue name, mention count, severity)
- MUST identify venue-specific outliers (e.g., "only mentioned at one venue")
- MUST NOT separate themes by venue (e.g., don't have "Equipment (El Paso)" and "Equipment (Austin)" as separate themes)

## Magnitude Scoring
- Magnitude is calibrated to 0-100 scale (same as single-venue analysis)
- Accounts for:
  - Network-wide prevalence (is this mentioned by multiple venues or just one?)
  - Total mention count (how frequently across all venues?)
  - Severity level (is it high or low severity when mentioned?)
  - Consistency (does every venue mention it or just a few?)
- Formula concept:
  - High prevalence + high severity + high consistency = higher magnitude (e.g., 80+)
  - Low prevalence + low severity + low consistency = lower magnitude (e.g., 20-40)
  - Mixed patterns get middle ranges (e.g., 40-60)

## Venue Breakdown
For each theme, track:
- `venue`: Venue name
- `mentions`: Count of mentions at that venue
- `severity`: "high", "medium", or "low" (based on scores, language intensity, mention context)
- `representative_detail`: Quote showing what the issue/strength looks like at that venue

### Severity Levels
- **High:** Theme dominates comments at this venue, scores are low (1-2 on 1-5 scale), language is intense
- **Medium:** Theme appears in several comments, mixed scores (2-3), neutral language
- **Low:** Theme appears occasionally, scores are positive (4-5) or neutral, constructive language

## Outlier Identification
- MUST identify if a theme is:
  - **Network-wide consensus:** All venues mention it (or nearly all)
  - **Clustered:** Only certain venues mention it
  - **Unique to one venue:** Only one venue experiences the issue/strength
- MUST call out outliers in the network summary
- Example phrases:
  - "across all venues" (consensus)
  - "particularly at El Paso with 8 mentions vs. 2-4 at other venues" (clustered)
  - "only mentioned at El Paso" (unique)

## Network Summary
- MUST be 2-3 sentences
- MUST state the overall network pattern (does everyone experience this, or just one venue?)
- MUST cite venue-specific variance (which venues are affected most/least?)
- MUST explain operational implication (why does this matter for the network?)
- MUST NOT just list numbers; synthesize into a narrative

## Formatting
- MUST use inline HTML limited to `<strong>` tags only
- MUST ground every claim in a number or stated detail from input comments
- MUST NOT state or imply comparisons to other periods (this is single-period analysis)
- MUST carry specific details from comments (game names, facility problems, visit phases) rather than generalizing

# Example

**Input:**
- 7 venues with comments
- Theme "Equipment reliability" appears in:
  - El Paso: 8 mentions (high severity)
  - Austin: 6 mentions (medium severity)
  - Grand Prairie: 2 mentions (low severity)
  - Dallas: 2 mentions (low severity)
  - Total: 18 mentions

**Output:**
```json
{
  "themes": [
    {
      "label": "Equipment reliability",
      "polarity": "negative",
      "mention_count": 18,
      "magnitude": 68,
      "network_summary": "Screen tracking failures are the dominant complaint across the network, mentioned in 18 comments (12% of all comments). Severity varies significantly by venue: El Paso experiences frequent failures (8 mentions, high severity), while Grand Prairie and Dallas rarely mention the issue (2 mentions each, low severity). This suggests venue-specific equipment maintenance or installation differences.",
      "venue_breakdown": [
        {
          "venue": "El Paso",
          "mentions": 8,
          "severity": "high",
          "representative_detail": "\"Screen stopped tracking constantly, really frustrating.\""
        },
        {
          "venue": "Austin",
          "mentions": 6,
          "severity": "medium",
          "representative_detail": "\"Screen stopped tracking mid-game, but staff fixed it quickly.\""
        },
        {
          "venue": "Grand Prairie",
          "mentions": 2,
          "severity": "low",
          "representative_detail": "\"Occasional tracking issue, quickly resolved.\""
        },
        {
          "venue": "Dallas",
          "mentions": 2,
          "severity": "low",
          "representative_detail": "\"One screen glitch, but staff was on it.\""
        }
      ],
      "representative_detail": "\"Screen stopped tracking constantly, really frustrating.\" (El Paso)"
    },
    {
      "label": "Staff responsiveness",
      "polarity": "positive",
      "mention_count": 16,
      "magnitude": 62,
      "network_summary": "Staff responsiveness is consistently praised across all venues, mentioned in 16 comments. Guests appreciate quick problem resolution, and this strength is distributed evenly across the network with no significant venue-based variance.",
      "venue_breakdown": [
        {
          "venue": "Grand Prairie",
          "mentions": 5,
          "severity": "high",
          "representative_detail": "\"Staff was amazing, fixed our bay issue right away.\""
        },
        {
          "venue": "Austin",
          "mentions": 4,
          "severity": "high",
          "representative_detail": "\"Someone came over quickly to fix the screen.\""
        },
        {
          "venue": "Dallas",
          "mentions": 4,
          "severity": "medium",
          "representative_detail": "\"Staff helped us pretty quickly.\""
        },
        {
          "venue": "El Paso",
          "mentions": 3,
          "severity": "medium",
          "representative_detail": "\"Staff tried to help but took a while.\""
        }
      ],
      "representative_detail": "\"Staff was amazing, fixed our bay issue right away.\" (Grand Prairie)"
    }
  ]
}
```

# Related Skills

For detailed guidance on how to use this analysis, see:
- `multi-venue-overview-skill.md` - How to write the network narrative using themes
- `multi-venue-ups-downs-skill.md` - How to select network patterns and variance findings
- `multi-venue-impact-drivers-skill.md` - How to rank themes by network-wide magnitude
- `multi-venue-recommendations-skill.md` - How to generate venue-specific actions based on venue breakdown

## Input Sources

This stage reads comments from all venues and metric flags from the Stage 1 metrics_analysis. It is Stage 2 of 3 in the multi-venue pipeline.
