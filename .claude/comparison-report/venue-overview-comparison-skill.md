# Venue Overview Comparison Skill

Generate a compelling 2-4 sentence narrative summary that frames the venue's performance **change** between two periods, explaining what improved, declined, or remained stable and why those shifts matter operationally.

## Purpose

The Venue Overview for a comparison report is the narrative centerpiece that tells the *story of change*. Unlike snapshot reports which describe current state, comparison reports answer: "What changed since the last period, and what does that mean for the venue?"

The overview should:
- Lead with the overall trend (improved/declined/stable)
- Cite the most significant changes (with deltas and direction)
- Acknowledge trends and reversals
- Explain what the changes mean operationally

## Input

- `metrics_analysis.current`: Characterization + metric_flags for current period
- `metrics_analysis.previous`: Characterization + metric_flags for previous period
- `comment_analysis.current`: Themes for current period
- `comment_analysis.previous`: Themes for previous period
- `combined_ranking`: Merged and sorted by change magnitude (deltas)

## Output

A 2-4 sentence narrative paragraph that:
- Opens with the overall performance trajectory (up/down/stable)
- Cites the #1 change driver with delta and direction
- Acknowledges any reversals or contradictions
- Explains operational implications
- Uses directional language (improved/declined/emerged/resolved)

## Rules

### Foundation
- MUST start with overall trajectory: "Performance improved/declined/remained stable..."
- MUST cite deltas explicitly: "improved by 0.8 points" or "declined from 14 to 8 mentions"
- MUST include direction indicators where applicable: ↑ (improvement), ↓ (decline), → (stable)
- MUST NOT frame findings as absolute state ("is good") but as change ("improved")

### Change Framing
- **Improvements:** Use "improved", "recovered", "increased", "strengthened", "resolved"
- **Declines:** Use "declined", "worsened", "decreased", "weakened", "emerged"
- **Stable:** Use "remained strong", "stayed consistent", "held steady", "maintained"

### Narrative Quality
- SHOULD explain what drove the biggest change (e.g., "equipment reliability fixes reduced...")
- SHOULD acknowledge contradictions honestly (e.g., "improved overall but one area declined")
- SHOULD use specific details from themes (game names, facility problems, operational issues)
- MUST NOT introduce numbers or claims not traceable to the input stages
- MUST be clear, concise, and make sense

### Formatting
- MUST use inline HTML limited to `<strong>` tags only
- MUST be 2-4 sentences (typically 3)
- MUST be a single paragraph (no line breaks)
- MUST NOT cite exact metric percentages/scores (avoid "2.6/5" or "26%")
- MAY cite comparative language ("up from", "down to", "more than before")
- MAY cite comment theme counts ("mentioned in 14 vs. 8 comments")

## Examples

### ✅ Good Examples (Comparison-Focused)

**Example 1: Overall Improvement**
```
"Performance improved significantly from Q1 to Q2, driven by equipment 
reliability fixes that reduced complaint frequency from 14 to 8 mentions. 
Staff responsiveness remained strong throughout. However, F&B service speed 
declined slightly, suggesting new operational challenges emerged during growth."
```

**Why this works:**
- Opens with overall trend (improved significantly)
- Cites #1 change with delta (14→8 mentions)
- Acknowledges stable strength (remained strong)
- Calls out secondary concern (declined slightly)
- Explains operational context (emerged during growth)

---

**Example 2: Mixed Picture**
```
"The venue stabilized after Q1 volatility, with strong improvement in equipment 
reliability (down to 2 issues from 6) offsetting emerging F&B speed concerns (wait 
times up from 8 to 12 minutes). Staff responsiveness improved slightly but not 
enough to offset the F&B challenge, creating an opportunity to refocus operational 
attention."
```

**Why this works:**
- Frames as stabilization (stabilized after volatility)
- Cites concrete deltas (6→2 issues, 8→12 minutes)
- Balances positive/negative (offsetting)
- Explains operational implication (opportunity to refocus)
- Uses specific, traceable data

---

**Example 3: Reversal**
```
"Surprisingly, despite continued strong guest satisfaction (NPS up from 8.1 to 8.4), 
operational issues increased from 22% to 28%, suggesting guests are forgiving but 
patience is wearing thin. The uptick is driven primarily by longer equipment issue 
resolution times (3.2 to 2.8 minutes), creating a deteriorating satisfaction trajectory 
if not addressed."
```

**Why this works:**
- Opens with unexpected finding (surprisingly)
- Cites contradiction (satisfaction up, issues up)
- Interprets what it means (patience wearing thin)
- Names the root cause (resolution times)
- Warns of trajectory (deteriorating)

---

### ❌ What NOT to Do

**Bad: Just repeats two separate snapshots**
```
"Q1 had strong NPS of 8.1 and 22% issues. Q2 has NPS of 8.4 and 28% issues."
```
**Why this fails:** No narrative. Just data juxtaposition. No explanation of what changed or why it matters.

---

**Bad: Cites exact metrics like snapshot reports**
```
"NPS improved from 8.1/10 to 8.4/10, and equipment issues increased from 22% to 28%."
```
**Why this fails:** Specific percentages/scores aren't the story. Deltas and meaning matter.

---

**Bad: Uses absolute framing instead of change framing**
```
"This venue has strong NPS and equipment problems. Staff is responsive."
```
**Why this fails:** Describes current state (snapshot), not change (comparison). Missing deltas, improvement/decline language, and trend direction.

---

## Comparison Language Guide

| Magnitude of Change | Phrasing |
|---|---|
| **Large improvement** (≥+1.0 points) | "significantly improved", "substantial gains", "remarkable recovery" |
| **Moderate improvement** (+0.5 to +1.0) | "improved", "strengthened", "moved in the right direction" |
| **Minor improvement** (+0.1 to +0.5) | "slight improvement", "modest gains", "edged upward" |
| **Minor decline** (-0.1 to -0.5) | "slight decline", "modest softening", "edged downward" |
| **Moderate decline** (-0.5 to -1.0) | "declined", "weakened", "moved in the wrong direction" |
| **Large decline** (≤-1.0 points) | "significant decline", "deterioration", "sharp reversal" |
| **Stable** (±0.1 points) | "remained stable", "held steady", "stayed consistent" |

---

## Direction Indicators

Use these to mark trend direction when helpful:

- **↑** = Improvement of 0.5+ points (green)
- **↓** = Decline of 0.5+ points (red)
- **→** = Minor change between -0.5 and +0.5 (neutral)

---

## Related Skills

- See `ups-downs-comparison-skill.md` for how to structure positive/negative findings with change framing
- See `impact-drivers-comparison-skill.md` for how to rank and explain top changes
- See `recommendations-comparison-skill.md` for how to generate actions based on changes

## Resources

- `README.md` - Integration guide for comparison reports
- `synthesis_template.md` - The actual prompt that implements this skill
