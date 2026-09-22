# Impact Drivers Skill

Identify and explain the top 3 entries from the combined ranking that have the most significant impact on venue performance.

## Purpose

The Impact section surfaces the most important findings - the factors that matter most to overall guest satisfaction and venue success. These are ranked by magnitude and serve as the foundation for recommendations.

## Input

- `combined_ranking`: merged metrics + comment themes, sorted by magnitude (highest first)
- `metrics_analysis`: metric_flags with magnitude and note
- `comment_analysis`: themes with magnitude and summary

## Output

An array of 3 impact drivers:

```json
{
  "impact": [
    {
      "title": "Short driver name",
      "description": "1-2 sentence explanation of why this driver matters, citing the underlying number"
    },
    {
      "title": "Short driver name",
      "description": "1-2 sentence explanation of why this driver matters, citing the underlying number"
    },
    {
      "title": "Short driver name",
      "description": "1-2 sentence explanation of why this driver matters, citing the underlying number"
    }
  ]
}
```

## Rules

### Selection
- MUST include exactly the top 3 entries from the combined ranking, most impactful first
- MUST NOT skip entries or reorder them - follow the magnitude ranking strictly
- MUST include both positive and negative drivers (if the ranking has them)

### Content
- MUST cite the actual number from the source entry's `note` (for metrics) or `summary` (for themes) in each description
- MUST use 1-2 sentences per entry
- MUST explain *why* this driver matters to overall performance, not just what it is
- MUST ground every claim in a number or stated theme from the input stages
- MUST use specific details from comment themes (game names, facility problems, visit phases) rather than generic labels

### Formatting
- MUST use inline HTML limited to `<strong>` tags only
- Title should be 2-5 words describing the driver
- Description should be 1-2 sentences

## Examples

### Example 1: Mixed Positive/Negative Ranking
```json
{
  "impact": [
    {
      "title": "NPS",
      "description": "A Combined NPS of 8.7/10 indicates strong overall satisfaction and loyalty, the primary driver of venue performance. This is the strongest signal of guest satisfaction."
    },
    {
      "title": "Equipment Reliability",
      "description": "Screen tracking failures mentioned in 14 comments are the most significant operational issue, directly impacting the Fun experience and preventing higher satisfaction."
    },
    {
      "title": "Staff Responsiveness",
      "description": "Quick problem resolution is a valued differentiator, with 8 guests specifically praising staff for getting them back to playing quickly despite equipment issues."
    }
  ]
}
```

### Example 2: Mostly Negative Ranking
```json
{
  "impact": [
    {
      "title": "Issue Frequency",
      "description": "52% of guests reported an issue - a systemic rate indicating operational friction across multiple areas. This is the primary factor depressing overall satisfaction."
    },
    {
      "title": "Resolution Satisfaction",
      "description": "2.1/5 resolution score shows guests are unsatisfied with how issues are handled, compounding the impact of the high issue rate."
    },
    {
      "title": "Entertainment Value",
      "description": "Fun score of 3.1/5 is moderate, suggesting the core experience isn't delivering the excitement guests expect despite good game selection."
    }
  ]
}
```

---

## Selection Strategy

### The Combined Ranking

The combined ranking merges all `metric_flags` and all `themes` entries, sorted by magnitude (highest first):

```
1. LTR (positive, 82)
2. Equipment reliability (negative, 71)
3. Staff responsiveness (positive, 65)
4. Food service speed (negative, 45)
5. Game selection (positive, 38)
...
```

**Your job:** Take entries 1, 2, and 3 and explain why they matter.

### What "Impact" Means

Impact = How much this factor affects overall guest satisfaction and venue success.

- **High magnitude** = affects many guests or affects them strongly
- **Positive impact** = drives satisfaction and loyalty
- **Negative impact** = depresses satisfaction and loyalty

### Why Magnitude Matters

The magnitude score already accounts for:
- How many guests mentioned it (comment themes)
- How far it deviates from baseline (metrics)
- How much it affects satisfaction (both sources)

**Don't second-guess the ranking.** If the combined ranking says equipment reliability is #2, it's #2 because it affects more guests or affects them more strongly than other factors.

---

## Explaining Impact

### For Positive Drivers
- Explain what makes this a strength
- Explain why it matters to guest satisfaction
- Cite the number that proves it

**Example:**
> "87% LTR indicates strong overall satisfaction and loyalty, the primary driver of venue performance."

### For Negative Drivers
- Explain what the problem is
- Explain how it affects satisfaction
- Cite the number that proves it

**Example:**
> "Screen tracking failures mentioned in 14 comments are the most significant operational issue, directly impacting the Fun experience."

### For Contradictions
- Acknowledge the contradiction
- Explain what it means
- Cite both numbers

**Example:**
> "Despite strong game satisfaction, 52% issue rate reveals operational friction that's undermining the core experience."

---

## Related Skills

- See `venue-overview-skill.md` for the narrative summary
- See `ups-downs-skill.md` for additional positive/negative findings
- See `recommendations-skill.md` for actions to address the top drivers

## Resources

- `synthesis.md` - The actual prompt that implements this skill
