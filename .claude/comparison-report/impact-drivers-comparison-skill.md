# Impact Drivers Comparison Skill

Rank the top 3 factors affecting venue performance by **change magnitude** (delta), not absolute magnitude. Explain what changed most, in what direction, and what that means operationally.

## Purpose

For comparison reports, impact drivers answer: "What changed the most between periods, and why does that matter?"

Unlike snapshot reports which rank by absolute importance, comparison reports rank by **magnitude of change**. A metric that was already strong and improved slightly may rank lower than one that was weak and is now showing improvement.

## Input

- `metrics_analysis.current` & `.previous`: Metric flags and characterizations
- `comment_analysis.current` & `.previous`: Themes and mention counts
- `combined_ranking`: All findings ranked by **change magnitude** (delta), not absolute value

## Output

Exactly 3 impact drivers, each with title and description:

```json
{
  "impact": [
    {
      "title": "Short driver name",
      "description": "1-2 sentence explanation: what changed, by how much, what that means"
    },
    ...
  ]
}
```

## Rules

### Ranking (Critical)
- MUST rank by **change magnitude** (delta), not absolute value
- If Equipment reliability improved +0.8 points, it ranks #1 (biggest change)
- Even if Staff responsiveness has higher absolute magnitude, it ranks lower if only +0.2
- Include both positive and negative changes
- MUST NOT reorder based on current importance (follow the delta ranking)

### Content Format
- **Title:** Short driver name (metric or theme)
- **Description:** 1-2 sentences including:
  - What changed (improved/declined/emerged/resolved)
  - Change magnitude with direction (±X points, or X→Y values)
  - Show baseline and current state
  - Explain what this change means operationally or strategically

### Deltas Must Be Explicit
- ✅ "improved by 0.8 points"
- ✅ "declined from 14 to 8 mentions"
- ✅ "up from 8 to 12 minutes (50% increase)"
- ✅ "recovered from critical (-2.1) to acceptable (-0.3)"
- ❌ "improved" (missing magnitude)
- ❌ "up from 14" (missing context of what it's compared to)

### Mechanics
- MUST use 1-2 sentences per driver
- MUST cite baseline and current values from input
- MUST explain operational implication ("this is primary driver of...", "this is the primary concern...", "this suggests...")
- MUST NOT rank based on absolute importance (follow delta ranking strictly)

## Examples

### ✅ Good Impact Driver Examples (Ranked by Change)

**Example 1: Large Improvement #1 in Ranking**
```
{
  "title": "Equipment Reliability (+0.8 points)",
  "description": "Improved most significantly, with complaint frequency dropping from 14 to 8 mentions (43% reduction). This is the primary positive trend driving overall satisfaction gains."
}
```

**Why this works:**
- Ranked #1 because it has the largest positive delta (+0.8)
- Cites concrete delta (14→8, 43%)
- Explains operational significance (primary positive trend)

---

**Example 2: Decline #2 in Ranking (Secondary)**
```
{
  "title": "F&B Service Speed (-0.4 points)",
  "description": "Declined by 0.4 points, with average wait times increasing from 8 to 12 minutes. This emerging issue is the primary concern offsetting equipment improvements."
}
```

**Why this works:**
- Ranked #2 because decline is secondary to the #1 improvement
- Cites concrete delta (8→12 minutes)
- Explains what it offsets (equipment improvements)
- Uses "primary concern" to show operational weight

---

**Example 3: Stability #3 in Ranking**
```
{
  "title": "Staff Responsiveness (→0.1 points)",
  "description": "Remained stable with consistent positive mentions (8 in both periods), showing this strength is being maintained despite operational changes. This consistency is valuable for protecting guest satisfaction."
}
```

**Why this works:**
- Ranked #3 because change is minor (→ indicator)
- Acknowledges stability as valuable
- Explains strategic meaning (protecting satisfaction)
- Shows why stability matters even if small change

---

### Context: Threshold Sensitivity

**When change is exactly at threshold (±0.5):**
```
{
  "title": "Issue Resolution (right at +0.5)",
  "description": "Improved by 0.5 points, marking the threshold from concerning to acceptable performance. This significant improvement suggests operational interventions are working, though continued monitoring is needed."
}
```

**Why this works:**
- Acknowledges threshold crossing ("marking the threshold from X to Y")
- Explains significance (interventions working)
- Flags for monitoring (need to watch for regression)

---

### ❌ What NOT to Do

**Bad: Ranking by absolute magnitude instead of delta**
```
{
  "title": "NPS (8.7/10)",
  "description": "High NPS indicates overall satisfaction..."
}
```
**Why this fails:** Describes current state, not change. NPS might be #1 absolute but #3 in changes if it only improved slightly.

---

**Bad: Missing delta/baseline information**
```
{
  "title": "Equipment Reliability",
  "description": "This is the most important driver affecting performance."
}
```
**Why this fails:** No numbers, no baseline, no change direction. Just opinion.

---

**Bad: Reordering by importance despite delta ranking**
```
1. "NPS (highest absolute value, +0.1 change)" 
2. "Equipment Reliability (+0.8 change)" <- Should be #1
3. "F&B Speed (-0.4 change)"
```
**Why this fails:** Violates delta ranking rule. NPS should be #2 or #3 if only changed +0.1.

---

## Delta Ranking Guide

| Magnitude | Impact Tier | Example |
|---|---|---|
| ≥+1.0 or ≤-1.0 | Transformative | "Equipment reliability improved 1.2 points" or "Issues worsened by -1.1" |
| +0.5 to +0.9 | Significant | "Improved by 0.8 points" |
| +0.1 to +0.4 | Modest | "Edged upward 0.3 points" |
| ±0.0 to ±0.1 | Stable | "Remained consistent" |
| -0.1 to -0.4 | Modest decline | "Edged downward 0.3 points" |
| -0.5 to -0.9 | Significant decline | "Declined by 0.8 points" |

---

## Inclusion Criteria

For the top 3, include:
- **#1:** Largest change (positive or negative)
- **#2:** Second-largest change (positive or negative)
- **#3:** Third-largest change, OR a significant stable/maintained strength if changes are all negative/positive

Example: If top 3 changes are (-0.8), (+0.4), (-0.3):
- #1: Equipment reliability declined -0.8 (largest)
- #2: Staff improved +0.4 (second-largest)
- #3: F&B stability → (tied third, shows what's being protected)

---

## Related Skills

- See `venue-overview-comparison-skill.md` for how to use top driver in opening narrative
- See `ups-downs-comparison-skill.md` for selecting broader findings
- See `recommendations-comparison-skill.md` for how to generate actions based on top drivers

## Resources

- `README.md` - Integration guide for comparison reports
- `synthesis_template.md` - The actual prompt that implements this skill
