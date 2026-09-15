# Ups/Downs Analysis Skill

Identify and articulate 2-3 positive findings (ups) and 2-3 negative findings (downs) from the combined ranking of metrics and comment themes.

## Purpose

The Ups/Downs section provides a balanced view of what's working well and what needs attention. Unlike the Impact section (which focuses on the top 3 drivers), Ups/Downs can include lower-magnitude items that add distinct operational value or context.

## Input

- `combined_ranking`: merged metrics + comment themes, sorted by magnitude
- `metrics_analysis`: metric_flags with polarity and magnitude
- `comment_analysis`: themes with polarity and magnitude

## Output

Two lists:

```json
{
  "ups": [
    "<strong>Short title:</strong> 1-2 sentence description",
    "<strong>Short title:</strong> 1-2 sentence description",
    "<strong>Short title:</strong> 1-2 sentence description"
  ],
  "downs": [
    "<strong>Short title:</strong> 1-2 sentence description",
    "<strong>Short title:</strong> 1-2 sentence description",
    "<strong>Short title:</strong> 1-2 sentence description"
  ]
}
```

## Rules

### Selection
- MUST include 2-3 items each (ups and downs)
- MUST draw from positive-polarity entries (for ups) and negative-polarity entries (for downs) in the combined pool
- MUST NOT limit to only the top 3 from impact - a venue can have more than three notable things
- SHOULD prioritize by magnitude (highest first) when selecting which items to include
- MAY include lower-magnitude items if they add distinct operational value or context that complements the impact section

### Content
- MUST use 1-2 sentences per item
- MUST include specific details from comment themes (named games, facility problems, visit phases) rather than generic labels
- MUST cite the actual number from the source entry's `note` (for metrics) or `summary` (for themes) when relevant
- MUST ground every claim in a number or stated theme from the input stages

### Formatting
- MUST use inline HTML limited to `<strong>` tags only
- Each item MUST start with a short, bold title followed by a colon
- Title should be 2-5 words describing the finding

## Examples

### Ups Example
```json
{
  "ups": [
    "<strong>Strong recommendation intent:</strong> 87% of guests would recommend the venue, indicating solid overall satisfaction with the experience.",
    "<strong>Responsive staff:</strong> Guests consistently praised staff for quickly addressing and resolving equipment issues to get them back to playing.",
    "<strong>Game selection:</strong> Multiple guests mentioned enjoying the variety of games available, with positive comments about newer titles."
  ]
}
```

### Downs Example
```json
{
  "downs": [
    "<strong>Equipment reliability:</strong> Screen tracking failures are the dominant complaint, mentioned in 14 comments and cited as a frequent frustration even when quickly resolved.",
    "<strong>Food service speed:</strong> Multiple guests noted slow food delivery times, with some mentioning 15-20 minute waits during peak hours.",
    "<strong>Pricing concerns:</strong> Several guests questioned the value proposition, particularly for food and beverage offerings."
  ]
}
```

---

## Selection Strategy

### How to Choose Which Items to Include

1. **Start with magnitude** - Sort by magnitude (highest first)
2. **Select top items** - Usually the top 2-3 by magnitude
3. **Consider context** - Ask: "Does this add distinct value beyond the impact section?"
   - If yes, include it even if lower magnitude
   - If no, skip it and move to the next
4. **Balance positive/negative** - Aim for 2-3 of each
5. **Avoid duplication** - Don't repeat the top 3 impact drivers verbatim

### Example Selection Logic

**Combined ranking (by magnitude):**
1. Equipment reliability (negative, 71) → Include in downs
2. LTR/recommendation (positive, 82) → Include in ups
3. Staff responsiveness (positive, 65) → Include in ups
4. Food service speed (negative, 45) → Include in downs (adds operational context)
5. Game selection (positive, 38) → Include in ups (distinct value)
6. Pricing (negative, 32) → Skip (covered by other items)

**Result:**
- Ups: LTR, Staff responsiveness, Game selection
- Downs: Equipment reliability, Food service speed

---

## Related Skills

- See `venue-overview-skill.md` for the narrative summary
- See `impact-drivers-skill.md` for the top 3 ranked drivers
- See `recommendations-skill.md` for actions to address downs

## Resources

- `synthesis.md` - The actual prompt that implements this skill
