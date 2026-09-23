# Multi-Venue Comparison Report Skills

## Overview

These skills guide Stage 1-3 (full analysis pipeline) for **multi-venue comparison** reports. They aggregate and compare metrics and comments across all venues between two time periods, identifying network trends, ranking changes, and venue-specific patterns.

**Applies to:** Reports comparing all venues' performance between two time periods (e.g., "all venues January vs. December")

**Key principle:** Focus on **change and direction** at the network level (improved/declined/stable). Show how the network changed overall AND how individual venues diverged from that trend.

## Directory Contents

- **README.md** (this file) - Architecture and integration guide
- **multi-venue-overview-comparison-skill.md** - Write network trend narrative
- **multi-venue-ranking-comparison-skill.md** - Rank venues by current performance + show ranking movement
- **multi-venue-ups-downs-comparison-skill.md** - Select network patterns that changed between periods
- **multi-venue-impact-drivers-comparison-skill.md** - Explain top 3 factors by **change magnitude**
- **multi-venue-recommendations-comparison-skill.md** - Actions for sustaining network improvements or addressing declines

## Key Differences from Multi-Venue Snapshot

| Aspect | Snapshot | Comparison |
|--------|---|---|
| **Framing** | Absolute state ("network is 8.2 NPS") | Change/trend ("improved from 8.0 to 8.2") |
| **Venue ranking** | Absolute performance | Absolute + ranking movement shown |
| **Drivers** | Top 3 by magnitude | Top 3 by **change magnitude** (deltas) |
| **Deltas** | Not cited | Always cited explicitly |
| **Stage 1+2** | Run once | Run twice (once per period) |

## Integration with Synthesis Pipeline

### Report Type Flow

When `get_ai_analysis(data, report_type='multi-comparison', previous_data=prev_data)` is called:

1. **Stage 1 (metrics_analysis)** runs **twice**:
   - Once on current-period network metrics → `metrics_current`
   - Once on previous-period network metrics → `metrics_previous`
   - Each produces network average + per-venue analysis

2. **Stage 2 (comment_analysis)** runs **twice**:
   - Once on current-period comments → `comment_current`
   - Once on previous-period comments → `comment_previous`
   - Each produces themes with venue breakdown

3. **Stage 3 (synthesis)** runs **once** with both periods:
   - Input: Both periods' metrics and comments
   - Template: `multi-venue-report/synthesis_template.md` (same as snapshot)
   - Section skills: Loaded from `multi-venue-comparison-report/` (these files)
   - Output: Network trend analysis + venue rankings with movement

### Synthesis Composition

```python
_compose_synthesis_skill('multi-comparison') →
  Load: multi-venue-report/synthesis_template.md
  Inject:
    <!-- SKILL:venue-overview --> ← multi-venue-comparison-report/multi-venue-overview-comparison-skill.md
    <!-- SKILL:ranking --> ← multi-venue-comparison-report/multi-venue-ranking-comparison-skill.md
    <!-- SKILL:ups-downs --> ← multi-venue-comparison-report/multi-venue-ups-downs-comparison-skill.md
    <!-- SKILL:impact-drivers --> ← multi-venue-comparison-report/multi-venue-impact-drivers-comparison-skill.md
    <!-- SKILL:recommendations --> ← multi-venue-comparison-report/multi-venue-recommendations-comparison-skill.md
  Return: Full prompt with all sections
```

## Skill File Specifications

### Multi-Venue Overview Comparison Skill
- **Purpose:** Write 2-4 sentence network trend narrative
- **Key difference:** Lead with overall trend (up/down/stable), show venue-level variance in that trend
- **Example:** "The network improved overall (NPS +0.3), but gains were uneven. Grand Prairie and Austin improved significantly (+0.6 each), while El Paso declined (-0.2)."
- **See:** `multi-venue-overview-comparison-skill.md` for full rules

### Multi-Venue Ranking Comparison Skill
- **Purpose:** Rank venues by current performance + show ranking movement
- **Key difference:** Primary ranking by absolute current NPS; secondary signal is rank movement
- **Example:** "Rank 1: Grand Prairie (NPS 8.8, moved up 1 spot)"
- **See:** `multi-venue-ranking-comparison-skill.md` for full rules

### Multi-Venue Ups/Downs Comparison Skill
- **Purpose:** Select network patterns that changed between periods
- **Key difference:** Focus on change (improved/declined/stable network-wide), not absolute state
- **Example:** "Equipment reliability improved across most venues, except El Paso"
- **See:** `multi-venue-ups-downs-comparison-skill.md` for full rules

### Multi-Venue Impact Drivers Comparison Skill
- **Purpose:** Rank top 3 factors by **change magnitude** (not absolute magnitude)
- **Key difference:** Sort by delta, not current value; show per-period context
- **Example:** "Equipment reliability improved +0.8 points network-wide, from 28% to 20% issue rate"
- **See:** `multi-venue-impact-drivers-comparison-skill.md` for full rules

### Multi-Venue Recommendations Comparison Skill
- **Purpose:** Actions for sustaining improvements or addressing declines
- **Key difference:** "Sustain momentum" for improvements; "address emerging issues" for declines
- **Example:** Critical: "Sustain equipment reliability improvements" (network action) + venue-specific: "El Paso: address new equipment decline"
- **See:** `multi-venue-recommendations-comparison-skill.md` for full rules

## Data Aggregation Patterns (Same as Snapshot)

### Network Averages Across Both Periods
For each metric in each period:
- Network average (mean)
- Range (min/max)
- Variance
- Delta (current - previous)

### Per-Venue Ranking Movement
Track each venue's rank change:
- Rank in current period
- Rank in previous period
- Movement (up/down/stable)

### Comment Theme Changes
For each theme:
- Mention count current vs. previous
- Severity change by venue
- New themes (only current period)
- Resolved themes (only previous period)

## Output Validation

The synthesis stage validates that multi-venue comparison skills produce:

1. **Overview**: 2-4 sentence network trend narrative with venue-level variance
2. **Venue Ranking**: Ranked list with tier assignments + rank movement
3. **Ups/Downs**: 2-3 items each, focusing on network-level changes
4. **Impact**: Top 3 factors ranked by **change magnitude** with per-venue delta context
5. **Recommendations**: Network-wide actions + venue-specific guidance based on movement/divergence

## Related Documentation

- `multi-venue-report/README.md` - Multi-venue snapshot architecture
- `comparison-report/README.md` - Single-venue comparison architecture
- `SKILLS_IMPLEMENTATION_PLAN.md` - Full implementation plan (Phase 2b details)

## Next Steps (Python Integration)

After all skill files are complete (Phase 2b):

1. Update `_compose_synthesis_skill()` in `analyze_venues.py`:
   - Add `'multi-comparison'` configuration

2. Update `get_ai_analysis()`:
   - Support `report_type='multi-comparison'` with two-period orchestration

3. Update `create_multi_venue_comparison_report.py`:
   - Call real analysis instead of stub

4. Test end-to-end multi-venue comparison report generation
