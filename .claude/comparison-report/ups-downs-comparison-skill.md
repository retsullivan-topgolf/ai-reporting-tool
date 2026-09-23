# Ups/Downs Comparison Skill

Select 2-3 positive and 2-3 negative findings that **changed** between periods, framing each as improvement, decline, or stability rather than absolute state.

## Purpose

Ups and Downs for comparison reports highlight findings with the most **significant change**, not necessarily the highest absolute magnitude. An item with moderate absolute performance but major improvement should be included over an item that's always been weak.

The goal is to answer: "Which changes deserve attention or celebration?"

## Input

- `metrics_analysis.current` & `.previous`: Metric characterizations + flags
- `comment_analysis.current` & `.previous`: Themes with counts
- `combined_ranking`: Findings merged and ranked by **change magnitude** (delta), not absolute magnitude

## Output

Two arrays of findings, each 2-3 items:

```json
{
  "ups": [
    "<strong>Short title:</strong> 1-2 sentence description showing improvement or stability"
  ],
  "downs": [
    "<strong>Short title:</strong> 1-2 sentence description showing decline or emergence"
  ]
}
```

## Rules

### Selection Criteria
- **Ups:** Select 2-3 positive-polarity entries from the current period that either:
  - Improved significantly from the previous period
  - Remained strong and stable (protecting strengths is important)
  - Emerged as new positives (new themes or recovered items)
- **Downs:** Select 2-3 negative-polarity entries that either:
  - Declined significantly (worsened)
  - Emerged (new issues or escalations)
  - Remained problematic if they're the #1 or #2 ranked negative by change

### Framing (Critical)
- MUST frame each finding as **change**, not current state
- Use "improved", "emerged", "resolved", "worsened", "remained" (change verbs)
- MUST NOT say "is strong" (snapshot language); say "improved significantly" (comparison language)
- MUST include delta and direction for each finding
- MUST cite baseline and current values

### Content Format
- **Title:** Short, action-oriented (e.g., "Equipment reliability improved")
- **Description:** 1-2 sentences including:
  - What changed (up/down/resolved/emerged)
  - The magnitude (delta with before→after values)
  - Why it matters operationally

### Ordering
- MUST prioritize by **change magnitude** (not current magnitude)
- Largest improvements first in ups
- Largest declines first in downs
- MAY include lower-magnitude changes if they add distinct operational value

### Mechanics
- MUST use inline HTML limited to `<strong>` tags only
- MUST ground every claim in a number or stated theme
- MUST NOT compare to network or other venues

## Examples

### ✅ Good Ups/Downs Examples

**Equipment reliability improved:**
```
<strong>Equipment reliability improved:</strong> Complaint frequency dropped from 14 
to 8 mentions (43% reduction), indicating equipment fixes are working. Screen 
tracking now resolves within 2 minutes consistently.
```

**Why this works:**
- Title is change-focused (improved)
- Cites delta (14→8, 43%)
- Explains operational outcome (fixes working, consistent resolution)
- Traceable to comment theme data

---

**Staff responsiveness remained strong:**
```
<strong>Staff responsiveness remained strong:</strong> Maintained 8+ positive mentions 
across both periods, showing consistent excellence. Guests continue to praise rapid 
problem resolution.
```

**Why this works:**
- Title acknowledges stability (remained)
- Cites magnitude (8+ in both periods)
- Explains what's valuable (rapid resolution)
- Shows stability as a win to protect

---

**F&B service speed declined:**
```
<strong>F&B service speed declined:</strong> Average wait time increased from 8 to 
12 minutes, with 5 new complaints in Q2 vs. 2 in Q1. This emerging issue is creating 
friction in the overall experience.
```

**Why this works:**
- Title is decline-focused (declined)
- Cites delta (8→12 minutes)
- Cites theme emergence (5 vs. 2 mentions)
- Explains impact (creating friction)

---

**Pricing concerns emerged:**
```
<strong>Pricing concerns emerged:</strong> New theme in Q2 with 3 mentions, with guests 
questioning value relative to venues in the area. This wasn't mentioned in Q1, suggesting 
competitive pressure or pricing changes are being noticed.
```

**Why this works:**
- Title shows emergence (emerged)
- Cites newness (new theme, 3 mentions)
- Explains context (competitive, pricing changes)
- Links to operational decision (pricing)

---

### ❌ What NOT to Do

**Bad: Snapshot framing instead of change framing**
```
<strong>Equipment issues:</strong> Equipment reliability is a problem with 8 mentions, 
creating operational friction.
```
**Why this fails:** Describes current state, not change. Missing delta and improvement language.

---

**Bad: Too absolute, ignores improvement**
```
<strong>Equipment reliability:</strong> Still has issues with 8 complaints, though 
fewer than before.
```
**Why this fails:** Undersells the improvement. Should lead with "improved from 14 to 8", not "still has issues".

---

**Bad: Missing operational implication**
```
<strong>Response time improved:</strong> Went from 3.2 to 2.8 minutes.
```
**Why this fails:** Just a number. Where's the impact? (e.g., "guests now accept occasional failures if resolved this fast").

---

## Comparison-Specific Guidance

### Improvements
Frame improvements positively but realistically:
- ✅ "improved significantly" (if delta ≥ 0.5)
- ✅ "showed modest gains" (if delta 0.1-0.5)
- ✅ "maintained strength" (if already high and staying high)
- ❌ "is good now" (too absolute, sounds snapshot-like)

### Declines
Frame declines clearly and operationally:
- ✅ "declined by X points" or "increased from X to Y"
- ✅ "emerged as new concern" (new theme in current period)
- ✅ "continued to struggle" (was weak, stayed weak)
- ❌ "is still bad" (ignores context of whether it's getting worse)

### Reversals (High Value)
Reversals—issues that were weak and are now strong, or vice versa—are important to highlight:
- ✅ "Equipment reliability recovered from critical to acceptable after maintenance investment"
- ✅ "F&B satisfaction reversed: was strong, now showing warning signs"

---

## Selection Strategy

1. Sort all current-period positive findings by **improvement delta**
   - Include the top 1-2 improving findings
   - Include the top 1 stable/maintained strength (even if not improving)
   - Total: 2-3 ups

2. Sort all current-period negative findings by **decline delta** (descending)
   - Include the top 2 declining/emerging findings
   - Total: 2-3 downs

3. If a finding is stable (not changing much):
   - Include in ups if it's the #1 strength to protect
   - Don't over-weight small changes (→ indicator is minor)

---

## Related Skills

- See `impact-drivers-comparison-skill.md` for how to rank changes by magnitude
- See `venue-overview-comparison-skill.md` for framing overall trajectory
- See `recommendations-comparison-skill.md` for how to generate actions based on changes

## Resources

- `README.md` - Integration guide for comparison reports
- `synthesis_template.md` - The actual prompt that implements this skill
