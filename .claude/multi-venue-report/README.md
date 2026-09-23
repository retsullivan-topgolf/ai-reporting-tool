# Multi-Venue Report Skills

## Overview

These skills guide Stage 1-3 (full analysis pipeline) for **multi-venue snapshot** reports. They aggregate metrics and comments across all venues in a single time period, producing network-wide findings, venue rankings, and recommendations.

**Applies to:** Reports analyzing all venues for a single time period (e.g., "all venues in January")

**Key principle:** Aggregate at the network level while preserving venue-specific context. Rankings, patterns, and recommendations must acknowledge venue variance and identify outliers.

## Directory Contents

- **README.md** (this file) - Architecture and integration guide
- **metrics_analysis.md** - Stage 1: NEW - Aggregate metrics across all venues
- **comment_analysis.md** - Stage 2: NEW - Aggregate comment themes with venue attribution
- **synthesis_template.md** - Stage 3 template: NEW - Different output envelope than single-venue
- **multi-venue-overview-skill.md** - Write network narrative acknowledging venue variance
- **multi-venue-ranking-skill.md** - Rank venues by composite score
- **multi-venue-ups-downs-skill.md** - Select network-wide patterns and consistency/variance findings
- **multi-venue-impact-drivers-skill.md** - Explain top 3 factors affecting network performance
- **multi-venue-recommendations-skill.md** - Network-wide actions + venue-specific guidance

## Key Differences from Single-Venue Skills

### Stage 1: Metrics Analysis (NEW)
- **Single-venue input:** One venue's 5 metrics
- **Multi-venue input:** List of all venues with their metrics (7 venues × 5 metrics each)
- **Single-venue output:** Per-metric characterization + flags
- **Multi-venue output:** Network-wide characterization + per-venue outliers + variance analysis

### Stage 2: Comment Analysis (NEW)
- **Single-venue input:** One venue's comments + metric flags
- **Multi-venue input:** All venues' comments (with venue attribution) + network-wide metric flags
- **Single-venue output:** Per-theme summary (label, magnitude, representative detail)
- **Multi-venue output:** Per-theme summary + venue breakdown (which venues mention each theme, severity)

### Stage 3: Output Envelope (NEW)
- **Single-venue:** `overview`, `ups`, `downs`, `impact`, `recommendations`
- **Multi-venue:** `overview`, `ups`, `downs`, `impact`, `recommendations`, **`venue_ranking`**, **`venue_specific`** (in recommendations)

## Integration with Synthesis Pipeline

### Report Type Flow

When `get_ai_analysis(data, report_type='multi-snapshot')` is called with aggregated data:

1. **Stage 1 (metrics_analysis)** runs **once** on network-wide metrics:
   - Input: Dict of all venues with their aggregated metrics
   - Output: Network characterization + per-venue outliers
   - Detects which venues are above/below network average for each metric

2. **Stage 2 (comment_analysis)** runs **once** on all comments:
   - Input: All comments from all venues (with venue labels) + metric flags
   - Output: Themes with venue breakdown (which venues mention, severity)
   - Preserves venue context while identifying network patterns

3. **Stage 3 (synthesis)** runs **once** with aggregated analysis:
   - Input: Aggregated metrics + comments + venue rankings
   - Template: `multi-venue-report/synthesis_template.md` (different from single-venue)
   - Section skills: Loaded from `multi-venue-report/` (these files)
   - Output: Network analysis + venue rankings + venue-specific recommendations

### Synthesis Composition

```python
_compose_synthesis_skill('multi-snapshot') →
  Load: multi-venue-report/synthesis_template.md
  Inject:
    <!-- SKILL:venue-overview --> ← multi-venue-report/multi-venue-overview-skill.md
    <!-- SKILL:ranking --> ← multi-venue-report/multi-venue-ranking-skill.md
    <!-- SKILL:ups-downs --> ← multi-venue-report/multi-venue-ups-downs-skill.md
    <!-- SKILL:impact-drivers --> ← multi-venue-report/multi-venue-impact-drivers-skill.md
    <!-- SKILL:recommendations --> ← multi-venue-report/multi-venue-recommendations-skill.md
  Return: Full prompt with all sections
```

Note: Multi-venue uses `<!-- SKILL:ranking -->` instead of the single-venue impact drivers placeholder because venue rankings are a primary output.

## Skill File Specifications

### Stage 1: metrics_analysis.md (NEW)
- **Purpose:** Aggregate metrics across all venues, identify outliers
- **Input:** Dict of {venue_name: {ltr_avg, fun_avg, ...}, ...}
- **Output:** Network characterization + per-venue analysis with outliers flagged
- **Key rule:** Compute network averages, ranges, and identify best/worst performers
- **See:** `metrics_analysis.md` for full spec

### Stage 2: comment_analysis.md (NEW)
- **Purpose:** Aggregate themes across all venues with venue breakdown
- **Input:** All comments from all venues (with venue labels)
- **Output:** Themes with mention counts, venue breakdown, and magnitude
- **Key rule:** Track which venues mention each theme; identify venue-specific outliers
- **See:** `comment_analysis.md` for full spec

### Multi-Venue Overview Skill
- **Purpose:** Write 2-4 sentence network narrative
- **Key difference:** Acknowledge venue variance explicitly
- **Example:** "The venue network shows strong overall satisfaction (8.2 NPS average), driven by consistent staff responsiveness and solid game experiences. However, equipment reliability varies significantly by location..."
- **See:** `multi-venue-overview-skill.md` for full rules and examples

### Multi-Venue Ranking Skill
- **Purpose:** Rank venues by composite score, explain tiers
- **Key difference:** Shows tier groupings (top/middle/bottom performers)
- **Output structure:** Array of venue rankings with tier assignment
- **See:** `multi-venue-ranking-skill.md` for full rules and examples

### Multi-Venue Ups/Downs Skill
- **Purpose:** Select network-wide strengths and weaknesses
- **Key difference:** Focus on **consistency** vs **variance**, not individual venues
- **Example:** "Consistent staff responsiveness: praised across all venues (16 mentions total)"
- **See:** `multi-venue-ups-downs-skill.md` for full rules and examples

### Multi-Venue Impact Drivers Skill
- **Purpose:** Explain top 3 factors affecting network performance
- **Key difference:** Rank by network-wide magnitude; show venue variance in each driver
- **Example:** "NPS (Network Average: 8.2), ranging from 7.1 to 8.8 across venues"
- **See:** `multi-venue-impact-drivers-skill.md` for full rules and examples

### Multi-Venue Recommendations Skill
- **Purpose:** Generate network-wide and venue-specific actions
- **Key difference:** Separate network actions from venue-specific actions
- **Example:** Critical: "Standardize Equipment Maintenance" (network-wide) + Venue-specific: "Grand Prairie: continue current practices; El Paso: conduct equipment audit"
- **See:** `multi-venue-recommendations-skill.md` for full rules and examples

## Data Aggregation Patterns

### Network Averages
For each metric, compute:
- Network average (mean across all venues)
- Range (min/max)
- Variance (how much venues differ)

### Venue Outliers
Identify venues that are:
- Best performer (top NPS, lowest issues, etc.)
- Worst performer (lowest NPS, highest issues, etc.)
- Significantly above/below network average

### Comment Theme Aggregation
For each theme:
- Total mention count across all venues
- Per-venue breakdown (venue name, mention count, severity)
- Network summary (what's the pattern?)
- Venue-specific outliers (e.g., "Equipment reliability is only a problem at El Paso")

## Synthesis Input Format

The synthesis stage receives this structure:

```json
{
  "venues": [
    {
      "venue": "Grand Prairie",
      "responses": 45,
      "metrics": {
        "ltr_avg": 4.4,
        "fun_avg": 4.1,
        ...
      },
      "comments": [...]
    },
    ...
  ],
  "metrics_analysis": {
    "characterization": "Network shows strong overall satisfaction...",
    "metric_flags": [...],
    "venue_outliers": [...]
  },
  "comment_analysis": {
    "themes": [
      {
        "label": "Equipment reliability",
        "magnitude": 68,
        "venue_breakdown": [
          {"venue": "El Paso", "mentions": 8, "severity": "high"},
          ...
        ]
      },
      ...
    ]
  }
}
```

## Output Validation

The synthesis stage validates that multi-venue skills produce:

1. **Overview**: 2-4 sentence network narrative acknowledging venue variance
2. **Venue Ranking**: Ranked list of venues with tier assignments (top/middle/bottom)
3. **Ups/Downs**: 2-3 items each, focusing on network patterns, not individual venues
4. **Impact**: Top 3 network-wide factors with venue variance noted
5. **Recommendations**:
   - `critical`: 3-4 network-wide actions
   - `secondary`: 3-4 network-wide actions
   - `maintain`: 3-4 network-wide actions
   - `venue_specific`: 1-2 sentence action for each venue (or high-impact venues)

## Testing Multi-Venue Reports

To test a multi-venue report:

```bash
cd python

# Generate data for all venues
python generate_venue_data.py
# (select "Press Enter when prompted to load all venues")

# Generate multi-venue snapshot report
python generate_report.py \
  --report-type multi-snapshot \
  --start-date 2026-01-01 --end-date 2026-01-31 \
  --format html
```

## Related Documentation

- `single-venue-report/README.md` - Architecture for snapshot reports
- `comparison-report/README.md` - Architecture for comparison reports
- `SKILLS_IMPLEMENTATION_PLAN.md` - Full implementation plan (Phase 2 details)

## Next Steps (Python Integration)

After all skill files are complete (Phase 2):

1. Create `get_aggregated_ai_analysis()` in `analyze_venues.py`:
   - Takes aggregated venue data (dict of venue metrics)
   - Runs Stage 1 (metrics_analysis on network metrics)
   - Runs Stage 2 (comment_analysis on all comments)
   - Runs Stage 3 (synthesis with multi-venue template)

2. Update `report_content.py`:
   - Add multi-snapshot support if needed

3. Update report builder scripts:
   - `create_multi_venue_snapshot_report.py` - Call `get_aggregated_ai_analysis()` instead of stub
   - `create_multi_venue_comparison_report.py` - Will be Phase 2b (add comparison variant)

4. Test end-to-end multi-venue report generation
