# Multi-Venue Impact Drivers Comparison Skill

Explain the top 3 factors affecting **network change** between periods, ranked by **change magnitude** (not current magnitude).

## Purpose

Impact drivers for comparison answer: "What three factors changed the most for the network between these periods, and how did venues respond?"

Unlike snapshot (which ranks by current magnitude), comparison ranks by **delta magnitude** – a metric that improved significantly ranks higher than one that's currently low but unchanged.

## Input

- Metrics and themes from both periods
- Combined ranking by **change magnitude** (deltas)
- Current and previous network averages

## Output

Exactly 3 drivers (ordered by change magnitude):

```json
{
  "impact": [
    {
      "title": "Short driver name (NPS, Equipment Reliability, etc.)",
      "description": "1-2 sentence explaining: what changed, by how much, what that means for network"
    },
    ...
  ]
}
```

## Rules

### Ranking (Critical)
- MUST rank by **change magnitude** (delta), not current magnitude
- Sort descending by absolute delta (whether positive or negative)
- Include both improvements and declines in top 3

### Content
For each driver:
- **Change direction:** Improved/declined/emerged
- **Network delta:** Network average change (e.g., "NPS improved +0.3")
- **Range:** How much venues varied in this change (e.g., "Grand Prairie +0.6, El Paso -0.2")
- **Implication:** What this divergence means

## Examples

**#1: Large Improvement**
```
{
  "title": "Equipment Reliability (+0.3 network points)",
  "description": "Issue rate improved from 28% to 25%, with most venues showing gains 
  of 0.3-0.6 points. Grand Prairie led (+0.8), while El Paso worsened (+0.3 worse), 
  suggesting equipment maintenance differences drive network variance."
}
```

**#2: Significant Decline**
```
{
  "title": "F&B Service Speed (-0.2 network points)",
  "description": "Wait times increased from 3.4 to 3.2/5 on average, particularly at 
  El Paso (down 0.4 points). Most venues held steady, suggesting El Paso-specific 
  staffing or workflow challenges."
}
```

---

## Related Skills

- See `multi-venue-ranking-comparison-skill.md` for how each venue positioned on these drivers
- See `multi-venue-impact-drivers-comparison-skill.md` for current-period drivers (not just change)

## Resources

- `README.md` - Integration guide
- `synthesis_template.md` - Implementation
