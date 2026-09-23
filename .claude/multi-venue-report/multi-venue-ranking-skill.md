# Multi-Venue Ranking Skill

Rank all venues by composite score (NPS or similar) and explain the tier structure, positioning each venue within the network hierarchy.

## Purpose

The Venue Ranking provides a clear hierarchical view of network performance: which venues are leading, which are solid, and which need support? It answers: "How do the venues rank relative to each other, and what does each tier mean for the network?"

This skill is unique to multi-venue reports - single-venue reports don't have rankings because they analyze one venue in isolation.

## Input

- `metrics_analysis`: Characterization + network_metrics + venue_outliers from Stage 1
- All venue metrics (for ranking by NPS or composite score)
- `combined_ranking`: For impact context

## Output

Exactly 3-7 ranked venues (one per venue), each with:

```json
{
  "rank": 1,
  "venue": "Grand Prairie",
  "nps": 8.8,
  "composite_score": 8.8,
  "tier": "top_performer",
  "summary": "1-2 sentence summary explaining this venue's ranking and position"
}
```

## Rules

### Ranking (Critical)
- MUST rank venues by NPS (or composite score if NPS unavailable)
- MUST assign tier labels: `top_performer`, `solid_performer`, `middle_performer`, `needs_support`
- MUST use absolute performance (current NPS), not change or relative standing
- MUST rank 1 = best (highest NPS), 7 = worst (lowest NPS)
- MUST NOT reorder based on arbitrary importance

### Tier Assignments
- **top_performer:** NPS ≥ 8.5 or at/above top quartile (best 25% of venues)
- **solid_performer:** NPS 8.0-8.4 or above network average
- **middle_performer:** NPS 7.5-7.9 or near network average
- **needs_support:** NPS < 7.5 or bottom quartile (lowest 25%)

If fewer than 4 venues, use 2-3 tiers. If exactly 3 venues, use `top`, `solid`, `needs_support`.

### Summary Content
For each venue, explain:
- **What:** Current composite score (NPS value)
- **Why this rank:** What makes them rank here? (strong across all metrics? particular weakness?)
- **Tier meaning:** What does this tier mean for the network?
- **Actionable context:** Best practice to model? Area needing support?

Do NOT explain individual metric breakdowns (that's detail level). Stay at tier and overall positioning level.

### Summary Format
- 1-2 sentences per venue
- Lead with the composite score
- Explain tier positioning ("best performer", "needs support", etc.)
- Note distinctive strength or weakness if relevant
- Use positive/constructive language even for low-performing venues

### Mechanics
- MUST use inline HTML limited to `<strong>` tags only
- MUST ground tier assignments in numbers (e.g., "8.8 NPS places them in top tier")
- MUST NOT compare to external benchmarks (only to network)
- MUST NOT explain why (that's drivers skill); only state rank and characterize tier

## Examples

### ✅ Good Venue Ranking Examples

**Example 1: Complete 7-venue network**
```json
[
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
    "summary": "Strong performance with solid NPS (8.4) and good staff responsiveness. Equipment reliability slightly below network average but manageable."
  },
  {
    "rank": 3,
    "venue": "Dallas",
    "nps": 8.1,
    "composite_score": 8.1,
    "tier": "solid_performer",
    "summary": "Solid performance near network average (8.1 NPS). Balanced across metrics with no particular weakness or standout strength."
  },
  {
    "rank": 4,
    "venue": "San Antonio",
    "nps": 7.9,
    "composite_score": 7.9,
    "tier": "solid_performer",
    "summary": "Performing near network average with good fundamentals. Some variance in staff responsiveness but overall stable."
  },
  {
    "rank": 5,
    "venue": "Fort Worth",
    "nps": 7.5,
    "composite_score": 7.5,
    "tier": "middle_performer",
    "summary": "Performing below network average (7.5 NPS). Opportunities in equipment reliability and F&B service speed."
  },
  {
    "rank": 6,
    "venue": "The Colony",
    "nps": 7.3,
    "composite_score": 7.3,
    "tier": "needs_support",
    "summary": "Below network average and showing weakness in multiple areas. Needs targeted operational support, particularly on equipment maintenance."
  },
  {
    "rank": 7,
    "venue": "El Paso",
    "nps": 7.1,
    "composite_score": 7.1,
    "tier": "needs_support",
    "summary": "Lowest performer in network (7.1 NPS). High issue rate (35%) and low resolution satisfaction require urgent attention and support."
  }
]
```

**Why this works:**
- Clear tier progression (2 top, 2 solid, 1 middle, 2 needs support)
- Each summary explains positioning without individual metric breakdowns
- Constructive language even for lowest performers ("needs support" not "failing")
- Tier assignments align with NPS values
- Balanced between praise and opportunity framing

---

**Example 2: Smaller network (3 venues)**
```json
[
  {
    "rank": 1,
    "venue": "Location A",
    "nps": 8.6,
    "composite_score": 8.6,
    "tier": "top",
    "summary": "Best performer with strong NPS (8.6) and balanced metrics. Sets the standard for the network."
  },
  {
    "rank": 2,
    "venue": "Location B",
    "nps": 8.0,
    "composite_score": 8.0,
    "tier": "solid",
    "summary": "Solid performance (8.0 NPS) with good fundamentals across most metrics."
  },
  {
    "rank": 3,
    "venue": "Location C",
    "nps": 7.2,
    "composite_score": 7.2,
    "tier": "needs_support",
    "summary": "Below-average performer (7.2 NPS) with opportunities in equipment reliability and service speed."
  }
]
```

**Why this works:**
- Simplified tier labels for 3-venue network
- Each venue clearly positioned
- Summary is concise but meaningful

---

### ❌ What NOT to Do

**Bad: Individual metric breakdowns instead of tier summary**
```
"Grand Prairie has 8.8 NPS, 4.4 LTR, 4.1 Fun, 18% issues, 3.9 resolution, 3.5 F&B."
```
**Why this fails:** That's individual metric detail, not ranking context. Stay at tier level.

---

**Bad: Rank by change or improvement instead of absolute performance**
```
Rank 1: "Austin (improved by +0.6 points)"
```
**Why this fails:** Ranking must be by absolute current performance (NPS), not change. Multi-comparison does change ranking.

---

**Bad: Negative/judgmental language for low performers**
```
"El Paso is failing the network and needs to get their act together."
```
**Why this fails:** "Needs support" or "opportunity" framing is more constructive. These are operational challenges, not moral failures.

---

**Bad: Omitting tier assignment**
```json
{
  "rank": 1,
  "venue": "Grand Prairie",
  "nps": 8.8,
  "summary": "Best performer"
}
```
**Why this fails:** Tier is required (helps readers understand the tier structure). Omitting it makes ranking harder to interpret.

---

## Tier Semantics

- **top_performer:** 1-2 venues. These are the network leaders. Their practices should be modeled.
- **solid_performer:** 2-3 venues. These are performing well, delivering value. Maintain current practices.
- **middle_performer:** 1-2 venues (if any). These are near average. Targeted improvements possible.
- **needs_support:** 1-2 venues. These need operational attention. Pair with resources and best practices from top performers.

---

## Ranking Edge Cases

**Tied scores:** If two venues have identical NPS:
- Use secondary metrics (Fun, LTR average) as tiebreaker
- Note in summary if tiebreaker was used

**Missing NPS:** If NPS unavailable:
- Use LTR (Likelihood to Return) as composite score
- Or use weighted average of available metrics
- Explain in summary what composite score is based on

**All venues very similar:** If little variance (all within 0.3 points):
- Still rank them
- Tier assignments might be broader (e.g., all "solid_performer")
- Acknowledge in summary that performance is relatively consistent

---

## Related Skills

- See `multi-venue-overview-skill.md` for how to introduce the network and acknowledge variance
- See `multi-venue-impact-drivers-skill.md` for explaining what drives each tier's performance
- See `multi-venue-recommendations-skill.md` for venue-specific actions based on ranking

## Resources

- `README.md` - Integration guide for multi-venue reports
- `synthesis_template.md` - The actual prompt that implements this skill
