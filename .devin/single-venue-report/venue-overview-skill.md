# Venue Overview Skill

Generate a compelling 2-4 sentence narrative summary of venue performance that tells the story without redundantly repeating metric numbers.

## Purpose

The Venue Overview is the narrative centerpiece of the report. It synthesizes metrics and guest comments into a coherent story that explains *why* the numbers look the way they do, without just restating the metrics that are already displayed in the Performance Summary cards below.

## Input

- `metrics_analysis`: characterization + metric_flags from Stage 1
- `comment_analysis`: themes from Stage 2
- `combined_ranking`: merged and sorted by magnitude (metrics + comments)

## Output

A 3-5 sentence narrative paragraph that:
- Tells the story of what's happening at the venue
- Explains relationships between metrics and comments
- Acknowledges contradictions honestly
- Avoids redundancy with Performance Summary cards

## Rules

### Foundation
- MUST start from the `metrics_analysis.characterization` as the foundation
- MUST fold in comment themes that explain *why* the numbers look that way
- MUST use the combined ranking to identify what matters most

### Metrics Handling
- **MUST avoid** citing the exact metric numbers that appear in the Performance Summary cards (e.g., don't say "2.6/5 resolution" or "26% issues" since those are displayed below)
- **MAY use** general descriptive language like "over half", "roughly 70%", "most guests", "frequently", "consistently" to convey magnitude without redundancy
- **MAY cite** numbers from comment themes (e.g., "mentioned in 14 comments") since those aren't in the metric cards
- **MAY cite** operational context numbers (e.g., "2-minute resolution time") that aren't metric scores

### Narrative Quality
- SHOULD acknowledge honestly when metrics and comments tell different stories - that's a real finding
- SHOULD balance metrics-driven insights (aggregate patterns) with comment-driven insights (specific themes, named issues)
- SHOULD use specific details from comment themes (game names, facility problems, visit phases) rather than generic labels
- MUST NOT introduce numbers or claims not traceable back to the input stages
- MUST be clear and concise and easy to read
- MUST be well-structured and make sense 

### Formatting
- MUST use inline HTML limited to `<strong>` tags only
- MUST be 2-4 sentences (typically 3)
- MUST be a single paragraph (no line breaks)

## Examples

### ❌ Don't Do This (Redundant)
```
"This venue has a 2.6/5 resolution score and 26% issues reported, 
creating friction in the guest experience."
```
**Why:** These exact numbers are already in the Performance Summary cards. Repeating them is redundant.

---

### ✅ Do This Instead (Narrative)
```
"This venue is performing well overall, driven by strong satisfaction 
with the experience. However, equipment reliability issues - particularly 
screen tracking failures - are creating friction that's preventing the 
entertainment experience from reaching its potential. Staff responsiveness 
is a bright spot, with most guests noting quick resolution of problems."
```
**Why:** 
- Tells the story (satisfaction → friction → bright spot)
- Uses specific details (screen tracking failures)
- Avoids exact metrics (no "2.6/5" or "26%")
- Uses descriptive language ("most guests")
- Explains relationships (why Fun is moderate)

---

### ✅ Another Example (Contradictions)
```
"Despite strong game satisfaction scores, a significant portion of guests 
experienced operational issues during their visits. This contradiction - 
high satisfaction with the core experience but friction in operations - 
suggests the venue's games are excellent but support systems need attention. 
Food and beverage service is a particular pain point mentioned frequently 
in comments."
```
**Why:**
- Acknowledges the contradiction (high satisfaction + high issues)
- Explains what it means (games good, operations need work)
- Uses descriptive language ("significant portion", "frequently")
- Avoids exact metrics

---

## Acceptable Magnitude Language

Instead of exact percentages/scores, use:

| Magnitude | Descriptive Language |
|-----------|---|
| ~90%+ | "nearly all", "vast majority", "overwhelming" |
| ~70-89% | "most", "majority", "roughly 70%", "significant portion" |
| ~50-69% | "over half", "roughly half", "many" |
| ~30-49% | "a notable portion", "a meaningful number", "roughly a third" |
| ~10-29% | "some", "a small portion", "a few" |
| <10% | "rarely", "occasionally", "a handful" |

---

## Related Skills

- See `ups-downs-skill.md` for how to structure positive/negative findings
- See `impact-drivers-skill.md` for how to rank and explain top drivers
- See `recommendations-skill.md` for how to generate actions

## Resources

- `overview-metrics-guidance.md` - Detailed guidance on metrics handling
- `synthesis.md` - The actual prompt that implements this skill
