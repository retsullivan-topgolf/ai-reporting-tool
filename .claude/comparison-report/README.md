# Comparison Report Skills

## Overview

These skills guide Stage 3 (synthesis) analysis for **single-venue period comparison** reports. They frame all findings as *change* (improvement/decline/stable) rather than absolute magnitude, enabling comparison-specific narrative, ups/downs selection, impact ranking, and recommendations.

**Applies to:** Single-venue reports comparing two time periods (e.g., current month vs. previous month)

**Key principle:** Focus on **change magnitude** and **direction** (↑/↓/→), not absolute magnitude. Every finding should cite deltas and explain what changed and why it matters.

## Directory Contents

- **README.md** (this file) - Architecture and integration guide
- **venue-overview-comparison-skill.md** - Write 2-4 sentence narrative comparing two periods
- **ups-downs-comparison-skill.md** - Select findings that changed between periods
- **impact-drivers-comparison-skill.md** - Rank by **change magnitude**, not absolute magnitude
- **recommendations-comparison-skill.md** - Generate actions for sustaining/addressing changes

## Integration with Synthesis Pipeline

### Report Type Flow

When `get_ai_analysis(data, report_type='comparison', previous_data=data_prev)` is called:

1. **Stage 1 (metrics_analysis)** runs **twice**:
   - Once on `data` (current period) → `metrics_current`
   - Once on `data_prev` (previous period) → `metrics_previous`

2. **Stage 2 (comment_analysis)** runs **twice**:
   - Once on `data` with `metric_flags_current` → `comment_current`
   - Once on `data_prev` with `metric_flags_previous` → `comment_previous`

3. **Stage 3 (synthesis)** runs **once** with both periods' data:
   - Input: `current` + `previous` metrics and comments
   - Template: `single-venue-report/synthesis_template.md` (same template as snapshot)
   - Section skills: Loaded from `comparison-report/` (these files)
   - Output: Single unified analysis focusing on change and trends

### Synthesis Composition

The synthesis prompt is composed at runtime:

```python
_compose_synthesis_skill('comparison') →
  Load: single-venue-report/synthesis_template.md
  Inject:
    <!-- SKILL:venue-overview --> ← comparison-report/venue-overview-comparison-skill.md
    <!-- SKILL:ups-downs --> ← comparison-report/ups-downs-comparison-skill.md
    <!-- SKILL:impact-drivers --> ← comparison-report/impact-drivers-comparison-skill.md
    <!-- SKILL:recommendations --> ← comparison-report/recommendations-comparison-skill.md
  Return: Full prompt with all sections
```

This is the same composition mechanism used for snapshot reports, just with different skill files.

## Skill File Specifications

### Venue Overview Comparison Skill
- **Purpose:** Write 2-4 sentence narrative comparing two periods
- **Key difference from snapshot:** Frame as "improved/declined/stable", cite deltas
- **Example:** "Performance improved significantly from Q1 to Q2, driven by equipment reliability fixes that reduced complaint frequency from 14 to 8 mentions."
- **See:** `venue-overview-comparison-skill.md` for full rules and examples

### Ups/Downs Comparison Skill
- **Purpose:** Select findings that changed between periods
- **Key difference from snapshot:** Include delta alongside magnitude, highlight reversals
- **Example:** "<strong>Equipment reliability improved:</strong> Complaint frequency dropped from 14 to 8 mentions, indicating fixes are working."
- **See:** `ups-downs-comparison-skill.md` for full rules and examples

### Impact Drivers Comparison Skill
- **Purpose:** Rank by **change magnitude**, not absolute magnitude
- **Key difference from snapshot:** Sort by delta, not absolute value
- **Example:** "Improved most significantly (+0.8 points), with complaint frequency dropping from 14 to 8 mentions."
- **See:** `impact-drivers-comparison-skill.md` for full rules and examples

### Recommendations Comparison Skill
- **Purpose:** Generate actions for sustaining improvements or addressing declines
- **Key difference from snapshot:** "Sustain momentum" for improvements, "Address emerging issues" for declines
- **Example:** Critical tier addresses the #1 change (biggest improvement or decline)
- **See:** `recommendations-comparison-skill.md` for full rules and examples

## Synthesis Input Format

The synthesis stage receives both periods' data in this structure:

```json
{
  "venue": "Grand Prairie",
  "responses": 45,
  "metrics_analysis": {
    "current": {
      "characterization": "Performance has improved...",
      "metric_flags": [...]
    },
    "previous": {
      "characterization": "Previous period showed...",
      "metric_flags": [...]
    }
  },
  "comment_analysis": {
    "current": {
      "themes": [...]
    },
    "previous": {
      "themes": [...]
    }
  }
}
```

Each skill file receives this full structure and extracts what it needs for comparison context.

## Comparison-Specific Rules

All comparison skills follow these cross-cutting rules:

1. **Always cite deltas** - e.g., "improved by 0.8 points" or "declined from 14 to 8"
2. **Include direction indicators** - ↑ (improvement ≥+0.5), ↓ (decline ≤-0.5), → (minor change)
3. **Frame as change, not absolute state** - "improved" not "is good", "emerged" not "exists"
4. **Show baseline** - "declined from 8 to 12 minutes" (both values)
5. **Explain trend implication** - What does this change mean for operations?
6. **Highlight reversals** - Issues that were weak and are now strong, or vice versa
7. **Acknowledge what's stable** - "remained strong" for consistent performance

## Output Validation

The synthesis stage validates that comparison skills produce:

1. **Overview**: 2-4 sentence narrative with deltas and direction indicators
2. **Ups/Downs**: 2-3 ups and 2-3 downs, each framed as change
3. **Impact**: Top 3 findings ranked by **change magnitude** (delta), each with direction
4. **Recommendations**:
   - `critical`: 3-4 actions addressing #1 change
   - `secondary`: 3-4 actions addressing #2 change
   - `maintain`: 3-4 actions reinforcing what's stable and strong

## Testing Comparison Reports

To test a single-venue comparison report:

```bash
cd python

# Generate data for both periods
python generate_venue_data.py "Grand Prairie"
cp venue_data.json venue_data_current.json

# (Simulate different period by loading previous month's data)
# python generate_venue_data.py "Grand Prairie" --prev-period

# Generate comparison report
python generate_report.py \
  --report-type comparison \
  --venue "Grand Prairie" \
  --start-date 2026-01-01 --end-date 2026-01-31 \
  --prev-start 2025-12-01 --prev-end 2025-12-31 \
  --format html
```

## Related Documentation

- `single-venue-report/README.md` - Architecture for snapshot reports
- `single-venue-report/synthesis_template.md` - Shared synthesis template
- `SKILLS_IMPLEMENTATION_PLAN.md` - Full implementation plan (Phase 1 details)

## Next Steps (Python Integration)

After these skill files are complete:

1. Update `analyze_venues.py`:
   - Add `report_type` parameter to `get_ai_analysis()`
   - Add `previous_data` parameter
   - Implement two-period Stage 1+2 orchestration for comparison reports
   - Wire up `_compose_synthesis_skill('comparison')`

2. Update `create_single_venue_comparison_report.py`:
   - Pass `report_type='comparison'` when calling analysis
   - Pass `previous_data` (currently missing)
   - Verify both periods' data flows through pipeline

3. Test end-to-end comparison report generation
