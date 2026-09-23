# Multi-Venue Impact Drivers Skill

Explain the top 3 factors affecting **network performance**, citing network averages and showing how venues vary on each driver.

## Purpose

Impact drivers for multi-venue reports answer: "What three factors matter most for the network, and how do venues differ on each?"

Unlike single-venue (which ranks items by magnitude at one venue), multi-venue ranks by network-wide magnitude and then explains the venue-level variance within each driver.

## Input

- `metrics_analysis`: Network metrics with network_avg and range
- `comment_analysis`: Themes with venue_breakdown
- `combined_ranking`: All findings sorted by magnitude

## Output

Exactly 3 impact drivers:

```json
{
  "impact": [
    {
      "title": "Short driver name (NPS, Equipment Reliability, etc.)",
      "description": "1-2 sentence explanation of network average, range, and variance implication"
    },
    ...
  ]
}
```

## Rules

### Ranking (Critical)
- MUST rank by **network-wide magnitude**, not individual venue magnitude
- MUST include top 3 entries from combined ranking
- MUST NOT reorder based on arbitrary importance
- Include both positive and negative drivers

### Content Structure
For each driver, explain:
- **Network average:** What's the network-wide performance level?
- **Range:** How much do venues differ? (min to max)
- **Why it matters:** What does this range mean operationally?

Example: "NPS (Network Average: 8.2), ranging from 7.1 (El Paso) to 8.8 (Grand Prairie). The 1.7-point spread indicates venue-specific operational factors significantly impact satisfaction."

### Venue Variance Explanation
- MUST cite the range (min to max)
- MUST name the outlier venues (best and worst)
- MUST explain what the variance suggests operationally
  - Systemic issue affecting all? (low average, no high outliers)
  - Venue-specific differences? (high variance suggests operational factors)
  - Best practices possible? (top performer shows what's achievable)

### Magnitude Scoring
- Magnitude already computed from Stage 1/2
- Rank by that magnitude (highest first)
- Do NOT recompute

### Mechanics
- MUST use 1-2 sentences per driver
- MUST cite network average + range with venue names
- MUST explain variance implication (operational meaning)
- MUST ground in numbers from input

## Examples

### ✅ Good Multi-Venue Impact Driver Examples

**#1 Positive with Variance:**
```
{
  "title": "NPS (Network Average: 8.2)",
  "description": "Strong overall satisfaction drives network performance, 
  ranging from 7.1 (El Paso) to 8.8 (Grand Prairie). The 1.7-point spread 
  indicates venue-specific operational factors significantly impact satisfaction."
}
```

**Why this works:**
- Network average upfront (8.2)
- Range with venue names (7.1 to 8.8)
- Explains what variance means (venue-specific factors)

---

**#2 Negative with Venue Clustering:**
```
{
  "title": "Equipment Reliability",
  "description": "Issue frequency varies dramatically across the network (18% 
  at Grand Prairie vs. 35% at El Paso), with 18 comments mentioning equipment 
  problems. This spread suggests maintenance, staffing, or equipment-age differences 
  create significant operational leverage for improvement."
}
```

**Why this works:**
- Cites specific range (18% to 35%)
- Names best/worst performers (Grand Prairie vs. El Paso)
- Explains what variance means (maintenance/staffing differences = leverage)
- Grounds in comment volume (18 mentions)

---

**#3 Consistent Strength (All Venues):**
```
{
  "title": "Staff Responsiveness",
  "description": "Consistently praised across all venues (16 mentions), with no 
  venue falling below 3.5/5. This uniform strength is being maintained network-wide, 
  reducing operational variance and creating a reliable service differentiator."
}
```

**Why this works:**
- Notes consistency (all venues, no variance)
- Cites the positive finding (16 mentions, 3.5 minimum)
- Explains implication (uniform strength, differentiator)
- Shows why it's in top 3 (network-wide advantage)

---

### ❌ What NOT to Do

**Bad: Just citing magnitude without venue context**
```
"NPS is the top driver at 8.2 points."
```
**Why this fails:** Missing the variance story. What does 8.2 mean? How do venues differ?

---

**Bad: Explaining individual venues instead of network pattern**
```
"Grand Prairie has excellent NPS (8.8) driven by strong maintenance and staff training. 
Austin is good at 8.4. El Paso struggles at 7.1 because of old equipment."
```
**Why this fails:** Individual venue stories. Impact drivers explain network-level patterns.

---

**Bad: Missing range/outlier information**
```
"Equipment reliability is a concern for the network, with 18 comments mentioning issues."
```
**Why this fails:** No context on network average, which venues are affected, or variance meaning.

---

## Variance Interpretation Guide

| Range | Interpretation | Implication |
|---|---|---|
| **0.0-0.2 points** | Minimal variance | Systemic issue (all venues affected equally) OR universal strength (all doing well). Little venue-specific leverage. |
| **0.2-0.5 points** | Low variance | Some venue differences but mostly consistent. Minor operational leverage. |
| **0.5-1.0 points** | Moderate variance | Clear venue-to-venue differences. Operational factors (maintenance, staffing) visible. Moderate leverage. |
| **>1.0 points** | High variance | Significant venue-to-venue differences. High operational leverage—top performer shows what's possible. |

---

## Network Average Framing

When citing network averages:
- **For positive metrics (NPS, LTR, Fun, etc.):**
  - "Strong network-wide X (8.2 average)"
  - "Average X of 4.1/5"
  - "Network average X of 75%"
- **For negative metrics (Issues %):**
  - "Network average X of 28%"
  - "Average issue rate of 28% across venues"

Always pair with range: "Network average X, ranging from A to B"

---

## Selection and Ranking

1. Sort all network_metrics + themes by magnitude (highest first)
2. Select top 3 entries
3. For each, explain:
   - Network average (the headline number)
   - Range (min-max with venue names)
   - Variance implication (why the range matters)

---

## Related Skills

- See `multi-venue-overview-skill.md` for introducing top drivers in opening narrative
- See `multi-venue-ranking-skill.md` for how venues position on each driver
- See `multi-venue-ups-downs-skill.md` for network patterns that complement drivers
- See `multi-venue-recommendations-skill.md` for actions based on top drivers

## Resources

- `README.md` - Integration guide for multi-venue reports
- `synthesis_template.md` - The actual prompt that implements this skill
