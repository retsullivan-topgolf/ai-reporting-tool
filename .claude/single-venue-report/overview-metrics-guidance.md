# Venue Overview: Metrics Usage Guidance

## The Rule

**Avoid redundancy with the Performance Summary cards below.**

Don't cite the exact metric numbers that are already displayed in the cards. Instead, use general descriptive language to convey magnitude.

## Examples

### ❌ Don't Do This (Redundant)
```
"This venue has a 2.6/5 resolution score and 26% issues reported, 
creating friction in the guest experience."
```
**Why:** These exact numbers are already in the Performance Summary cards. Repeating them is redundant.

---

### ✅ Do This Instead (Descriptive)
```
"Equipment reliability issues are creating friction in the guest experience, 
with most guests noting slow resolution when problems occur."
```
**Why:** Uses descriptive language ("most guests", "slow resolution") instead of exact metrics (2.6/5, 26%).

---

## Acceptable Patterns

### General Magnitude Language
- "over half" (instead of "52%")
- "roughly 70%" (instead of "71%")
- "most guests" (instead of "87%")
- "a significant portion" (instead of "45%")
- "frequently" (instead of "in 14 comments")
- "consistently" (instead of "in 8 mentions")

### Specific Numbers That Are OK
- Numbers that describe **comment themes**, not metrics
  - "Screen tracking failures mentioned in 14 comments" ✅
  - "8 guests specifically praised staff" ✅
- Numbers that describe **operational context**, not metrics
  - "2-minute resolution time" ✅
  - "Daily calibration checks" ✅

### Specific Numbers That Are NOT OK
- Metric scores that appear in Performance Summary cards
  - "LTR of 8.7/10" ❌ (it's in the card)
  - "Fun score of 3.2/5" ❌ (it's in the card)
  - "26% issues reported" ❌ (it's in the card)
  - "2.6/5 resolution" ❌ (it's in the card)

---

## Why This Matters

The report has a visual hierarchy:

```
┌─────────────────────────────────────┐
│  Overall Assessment (1-2 sentences) │
├─────────────────────────────────────┤
│  Venue Overview (2-4 sentences)     │  ← Narrative story
│                                     │
├─────────────────────────────────────┤
│  Performance Summary Cards          │  ← Metric numbers
│  ┌─────┐ ┌─────┐ ┌─────┐           │
│  │ 8.7 │ │ 3.2 │ │ 26% │           │
│  └─────┘ └─────┘ └─────┘           │
├─────────────────────────────────────┤
│  Ups/Downs/Impact (AI analysis)     │  ← Detailed breakdown
│                                     │
├─────────────────────────────────────┤
│  Recommendations                    │  ← Actions
└─────────────────────────────────────┘
```

**The Venue Overview should tell the story.** The Performance Summary cards show the numbers. Don't repeat the numbers in the story.

---

## Implementation

The synthesis.md prompt now includes this rule:

> MUST avoid citing the exact metric numbers that appear in the Performance Summary cards (e.g., don't say "2.6/5 resolution" or "26% issues" since those are displayed below); however, you MAY use general descriptive language like "over half", "roughly 70%", or "most guests" to convey magnitude without redundancy

This ensures the AI generates overviews that:
- ✅ Tell a compelling narrative
- ✅ Avoid redundancy with the cards below
- ✅ Still convey magnitude through descriptive language
- ✅ Let the specific numbers live in the Performance Summary section where they belong
