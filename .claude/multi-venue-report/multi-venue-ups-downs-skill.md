# Multi-Venue Ups/Downs Skill

Select 2-3 network-wide strengths and 2-3 network-wide weaknesses, framing each as a **network pattern** (consistency or variance), not individual venue performance.

## Purpose

Ups and Downs for multi-venue reports highlight findings with **network-wide significance**: What's consistently strong across all venues? What's consistently weak? Where do venues diverge?

Unlike single-venue (which selects high/low magnitude items), multi-venue focuses on **patterns**: consistency, variance, and outliers.

## Input

- `metrics_analysis`: Network characterization + venue_outliers
- `comment_analysis`: Themes with venue breakdown
- `combined_ranking`: All findings ranked by magnitude

## Output

Two arrays, each 2-3 items:

```json
{
  "ups": [
    "<strong>Short title:</strong> 1-2 sentence description of strength"
  ],
  "downs": [
    "<strong>Short title:</strong> 1-2 sentence description of weakness"
  ]
}
```

## Rules

### Selection Criteria: Network Patterns, Not Individual Venues
- **Ups:** Select findings that are:
  - Consistently strong across all venues (network consensus)
  - OR high-magnitude positives that matter network-wide
  - OR stable/maintained strengths
- **Downs:** Select findings that are:
  - Consistently weak across all venues (systemic issue)
  - OR high-magnitude negatives affecting network
  - OR significant variance that creates opportunity

### Framing (Critical)
- MUST frame as network patterns or variance, NOT individual venues
- ✅ "Consistent staff responsiveness across all venues"
- ✅ "Equipment reliability varies significantly (18% to 35%)"
- ❌ "Grand Prairie's strong performance" (individual)
- ❌ "Austin has equipment issues" (individual)

### Content Structure
- **Title:** Network-level issue/strength (noun form)
- **Description:** 1-2 sentences explaining:
  - What's the pattern? (consistent, variable, systemic?)
  - Where does it appear? (all venues, specific regions, one outlier?)
  - Why it matters for the network

### Ordering
- MUST prioritize by **magnitude** (highest first)
- Ups: Largest positive magnitudes first
- Downs: Largest negative magnitudes first

### Mechanics
- MUST use inline HTML limited to `<strong>` tags only
- MUST ground every claim in network patterns (numbers, venue breakdown)
- MUST NOT focus on individual venues (that's ranking/recommendations)

## Examples

### ✅ Good Multi-Venue Ups/Downs Examples

**Consistent strength (all venues):**
```
<strong>Consistent staff responsiveness:</strong> Praised across all venues 
(16 mentions total), with Grand Prairie and Austin leading. This is a 
network-wide strength worth protecting.
```

**Why this works:**
- Frames as network strength (consistent)
- Shows it's across all venues (16 mentions total)
- Notes leadership without focusing on individuals (Grand Prairie and Austin leading, but not detailed)
- Clear operational implication (protect it)

---

**Significant variance (outlier pattern):**
```
<strong>Equipment reliability varies significantly:</strong> While Grand Prairie 
has minimal issues (18%), El Paso faces challenges (35%). This 17-point spread 
suggests venue-specific factors (maintenance, staffing, equipment age) are at play, 
creating operational leverage for improvement.
```

**Why this works:**
- Frames as network variance (not a weakness at all venues)
- Shows the range (18% to 35%)
- Names outliers (Grand Prairie vs. El Paso)
- Explains why variance matters (venue-specific factors = operational lever)
- NOT individual venue focus, but pattern focus

---

**Systemic weakness (all venues):**
```
<strong>F&B service speed is a network-wide concern:</strong> Average 3.2/5 
across all venues, with no venue exceeding 3.5. This is a systemic issue 
affecting all locations equally, suggesting operational or workflow challenges 
rather than venue-specific problems.
```

**Why this works:**
- Frames as systemic (all venues affected)
- Cites network average (3.2/5)
- Notes absence of high performer (no venue ≥3.5)
- Explains type of issue (systemic, not venue-specific)
- Suggests solution direction (workflow)

---

**Emerging strength (growth area):**
```
<strong>Strong NPS at top venues:</strong> Grand Prairie (8.8) and Austin (8.4) 
demonstrate that 8.5+ NPS is achievable, pulling the network average to 8.2. 
Their practices should be modeled network-wide.
```

**Why this works:**
- Frames as opportunity (top performers show what's possible)
- Cites examples (Grand Prairie, Austin) without dwelling on them
- Shows network impact (pulling average up)
- Actionable implication (model their practices)

---

### ❌ What NOT to Do

**Bad: Individual venue focus instead of patterns**
```
<strong>Grand Prairie is strong:</strong> 8.8 NPS, low issues, good staff.
```
**Why this fails:** That's venue detail, not network pattern. Ranking skill covers individual venue stories.

---

**Bad: Missing pattern explanation**
```
<strong>Equipment reliability:</strong> Varies across venues, which is a concern.
```
**Why this fails:** What does "varies" mean operationally? 18% to 35% spread? Is it venue-specific or systemic?

---

**Bad: Focusing on individual weakness**
```
<strong>El Paso's challenges:</strong> This venue has multiple issues affecting 
satisfaction.
```
**Why this fails:** Individual venue story. Either frame as "significant variance" pattern or let recommendations handle venue-specific guidance.

---

## Pattern Types to Highlight

### Network Consensus (Strength)
All or nearly all venues show this:
- "Consistent staff responsiveness across all venues"
- "Strong game satisfaction network-wide"

### Network Consensus (Weakness)
All or nearly all venues show this:
- "F&B service speed is a network-wide concern"
- "Issue resolution is below expectations everywhere"

### Significant Variance (Opportunity)
High/low variance that creates leverage:
- "Equipment reliability varies dramatically (18% to 35%), suggesting venue-specific operational factors"
- "NPS ranges widely (7.1 to 8.8), showing what's possible vs. what needs support"

### One Clear Outlier
One venue stands apart from the pattern:
- "Staff responsiveness is strong everywhere except El Paso, where guests note longer response times"
- "Grand Prairie significantly outperforms on equipment reliability while other venues cluster around 28% issues"

---

## Selection Strategy

1. Sort all findings (metrics + themes) by **magnitude**
2. For ups: Select top 2-3 positive findings that are either:
   - Network consensus (consistent, all venues)
   - High magnitude (affects many guests)
   - Stable strength (maintained across venues)
3. For downs: Select top 2-3 negative findings that are either:
   - Network consensus (affects all venues)
   - High magnitude (many complaints)
   - Significant variance (creates operational lever)

---

## Related Skills

- See `multi-venue-overview-skill.md` for how to introduce variance in opening narrative
- See `multi-venue-impact-drivers-skill.md` for explaining what drives network patterns
- See `multi-venue-ranking-skill.md` for individual venue positioning

## Resources

- `README.md` - Integration guide for multi-venue reports
- `synthesis_template.md` - The actual prompt that implements this skill
