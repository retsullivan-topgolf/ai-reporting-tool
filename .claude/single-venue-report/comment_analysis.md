---
name: comment-analysis
description: Analyze free-text guest comments to identify themes and score them on a 0-100 magnitude scale comparable to metrics
---

# Purpose

Extract and score themes from guest comments for a single venue. This is Stage 2 of 3 in the venue report analysis pipeline. 

Unlike the metrics stage which works with aggregate scores, this stage focuses on free-text comments and identifies specific, recurring themes guests are actually describing. Each theme is scored on a 0-100 magnitude scale so that comment-driven themes can be ranked fairly against metric-driven ones in the synthesis stage.

# Inputs

Required:

- `venue`: venue name
- `responses`: total survey count for the period (not all respondents left a comment)
- `comments`: list of comment objects, each containing:
  - `text`: the guest's free-text comment
  - `ltr`: that guest's Likelihood to Return score (1-5)
  - `fun`: that guest's Fun score (0-5)
- `metric_flags`: list of metric flags from Step 1, each containing:
  - `metric`: the metric name
  - `polarity`: the metric polarity (positive or negative)
  - `magnitude`: the metric magnitude (0-100)
  - `note`: the metric note (optional)

Optional:

- `@metrics.json`: reference file showing what metrics are tracked and how they are scored, useful for categorizing comments into default metric categories

If no comments are provided or comments lack the required fields, ask the user to provide the required information before continuing.

# Context

Always use:

- The actual comment text itself, not pattern-matching against a fixed keyword list
- The venue's LTR and Fun scores to understand whether a theme appeared in generally happy or unhappy experiences
- Specific, recurring details (named games, facility problems, safety issues, visit phases like parking or food) rather than generic labels
- Mention count as a baseline but not the only driver of magnitude

When applicable, use:

- The `@metrics.json` file to align comment themes with tracked metric categories (including F&B-related themes like food quality, beverage service, pricing)
- Severity of outcomes (left without playing, safety issues, food/beverage issues, etc.) to adjust magnitude upward even for low-mention themes
- The distinction between sentiment ("had a great time!") and substance (specific, describable themes)
- Specific F&B details (named menu items, service speed, quality issues, value perception) when guests mention food or beverage experiences

Treat the provided comments and project context as the source of truth. Do not invent themes from generic comments or force weak themes into existence when sample size is low.

# Workflow

1. Read all provided comments carefully, noting the text, LTR, and Fun score for each.
2. Identify distinct, specific themes by grouping comments that describe the same underlying issue or experience, regardless of wording differences.
3. For each theme, determine:
   - A short, specific label (2-4 words) - use named games, facility names, or specific issues when available
   - Polarity: `"positive"` or `"negative"`
   - Split comments with multiple types of feedback into into separate entries
   - Mention count: how many distinct comments raised this theme (one per comment, even if mentioned multiple times within that comment)
   - A summary in your own words (1-2 sentences) of what guests are saying
   - A representative detail: a short verbatim quote or close paraphrase that grounds the theme in real feedback
4. Score each theme's magnitude (0-100) using the magnitude scoring guidelines below.
5. Order themes by magnitude (highest first).
6. Validate the completed output against the Output and Rules sections before returning it.

# Output

Respond with ONLY a single JSON object (no markdown fences, no commentary):
example JSON:

```json 
{
  "themes": [
    {
      "label": "Equipment reliability",
      "polarity": "negative",
      "mention_count": 14,
      "magnitude": 71,
      "summary": "Screens losing shot tracking mid-session, described as usually resolved quickly but happening often enough to be the dominant complaint",
      "representative_detail": "\"The screen stopped tracking shots for a few minutes, but someone came over quickly and fixed it.\""
    },
    {
      "label": "Staff responsiveness",
      "polarity": "positive",
      "mention_count": 8,
      "magnitude": 65,
      "summary": "Staff quickly addressing equipment issues and helping guests get back to playing",
      "representative_detail": "\"Someone came over quickly to fix the screen and get us back in the game.\""
    }
  ]
}
```

# Rules

## Theme Identification

- MUST read comments for actual substance, not pattern-match against fixed keywords
- MUST group comments by what's actually happening, not surface wording (a stuck screen, a game that won't start, and a bay with "problems" could be the same equipment or software issue)
- MUST use specific, named details when available (named games, facility names, visit phases) instead of generic labels like "operational issues"
- MUST NOT invent themes from single generic comments ("had a great time!") - sentiment is not a theme
- MUST NOT force weak themes into existence when sample size is low; an empty or short themes list is correct if comments lack specific, recurring substance
- SHOULD combine themes that are mentioned by multiple guests and are similar in nature
- MUST split comments with multiple types of feedback into separate entries
 - Example of split theme: "The screen stopped tracking shots for a few minutes, but someone came over quickly and fixed it." (LTR: 9, Fun: 5) 
    - This should be split into "Equipment reliability" (negative) and "Staff responsiveness" (positive)

## Theme Entry Structure

- `label`: short, specific name (2-4 words)
- `polarity`: `"positive"` or `"negative"` - split themes that cut both ways into separate entries rather than forcing them into one
- `mention_count`: count of distinct comments that raised this theme
- `magnitude`: 0-100 score (see Magnitude Scoring section)
- `summary`: 1-2 sentences describing what guests are saying, in your own words
- `representative_detail`: short verbatim quote or close paraphrase from one comment that best illustrates the theme

## Magnitude Scoring

The magnitude score (0-100) represents "how much does this matter to overall guest satisfaction here" and must be comparable across themes and against metric flags.

**Baseline calculation:**
- Calculate **comment participation rate**: `total_comments / responses`
- Calculate **mention share among commenters**: `(mention_count / total_comments) * 100`
- This mention-share-among-commenters is your baseline magnitude
- Example: 14 mentions out of 20 total comments = (14/20)*100 = 70 baseline
- This approach recognizes that a theme mentioned by 70% of people who took time to comment is more significant than the same 14 mentions would be if spread across 50 total surveys (28%)

**Adjustments for negative themes:**
- Apply a **confidence multiplier** (0.8-1.0x) to the baseline based on comment participation, since negative themes need validation to be actionable
  - Use 0.8x when comment participation is low (<20% of respondents commented) - negative themes are less validated
  - Use 0.9x for moderate participation (20-50% of respondents commented) - negative themes are moderately validated
  - Use 1.0x for high participation (>50% of respondents commented) - negative themes are robustly validated and fully weighted
  - Rationale: A problem mentioned by 50% of commenters is more credible if those commenters represent 60% of all respondents vs. 10%
  - Example: 50 baseline with 40% participation (moderate) * 0.9 = 45
- Then apply these three adjustment rules:
  1. Adjust DOWN (typically ±5) when a theme is mentioned but the guest still rated the visit highly overall (a minor gripe in an otherwise glowing comment shouldn't score like a dominant complaint)
  2. Adjust UP (typically ±8-10) when a guest raises a negative theme and has low LTR/Fun scores (the theme isn't just common, it's actually tanking satisfaction)
  3. Adjust UP (typically ±12-15) regardless of mention count when even one or two guests describe an unusually severe outcome (left without playing, wouldn't recommend at all, unresolved safety issue). Note: A single severe outcome should result in final magnitude of at least 40-50, as it represents a critical failure mode.

**Adjustments for positive themes:**
- Apply a **conservative multiplier** (0.8-0.9x) to the baseline, since positive themes are less actionable for improvement but still valuable for understanding strengths
  - Use 0.8x when comment participation is low (<20% of respondents commented)
  - Use 0.85x for moderate participation (20-50% of respondents commented)
  - Use 0.9x for high participation (>50% of respondents commented)
  - Rationale: Higher comment participation means the positive theme is more robustly validated by engaged respondents, so it deserves a higher weight
  - Example: 70 baseline with 40% participation (moderate) * 0.85 = 59.5 → round to 60
- Optionally adjust UP (typically ±8-10) if the theme correlates with high LTR/Fun scores (validates that this strength matters to satisfaction)
- Optionally adjust UP (typically ±12-15) if the theme represents a competitive advantage or differentiator

**Adjustment magnitude guidance:**
- Adjustments (UP or DOWN) typically range from ±5 to ±15 points depending on the strength of evidence
  - Minor adjustments (±5): Theme is mentioned but guest still rated highly (negative) or theme is minor strength (positive)
  - Moderate adjustments (±8-10): Theme clearly impacts satisfaction (negative) or validates a meaningful strength (positive)
  - Major adjustments (±12-15): Theme represents severe outcome or critical failure (negative) or clear competitive advantage (positive)
- Apply adjustments cumulatively (a theme can receive multiple adjustments) but cap final magnitude at 100
- Round magnitude scores to the nearest integer after all adjustments

**General rules:**
- MUST NOT let low sample size force weak themes into existence. If there are not comments with any substance, return a themes array that communicates this.

**Ordering:**
- Order `themes` array by magnitude, highest first

## Comment Categorization

- MAY use `@metrics.json` to align comments with default metric categories
- MAY use a metric category name as the theme label if the comment falls into that category
- MUST allow comments to fall into multiple themes if they cover different aspects of the same issue or different issues in the same comment

# Example

The following demonstrates formatting, magnitude calculation, and theme identification. Do not assume these requirements apply to the user's source.

Given these comments (4 comments from 10 total surveys):
- "The screen stopped tracking shots for a few minutes, but someone came over quickly and fixed it." (LTR: 9, Fun: 5)
- "Equipment kept failing, really frustrating." (LTR: 5, Fun: 2)
- "Staff was amazing - fixed our bay issue right away." (LTR: 10, Fun: 5)
- "Great experience overall!" (LTR: 10, Fun: 5)

**Magnitude calculation:**
- Comment participation rate: 4/10 = 40% (moderate participation)
- Equipment reliability (negative): 2 mentions out of 4 comments = (2/4)*100 = 50 baseline
  - Apply confidence multiplier based on 40% participation (moderate): 50 * 0.9 = 45
  - Guest LTR/Fun: one guest (LTR 5, Fun 2) clearly frustrated, one guest (LTR 9, Fun 5) had minor issue
  - Adjustment rule 2 (low LTR/Fun): Adjust UP moderately for the frustrated guest (±8-10 range): 45 → 53
- Staff responsiveness (positive): 2 mentions out of 4 comments = (2/4)*100 = 50 baseline
  - Apply conservative multiplier based on 40% participation (moderate): 50 * 0.85 = 42.5
  - Adjustment: Adjust UP because guests mentioning this have high LTR/Fun (9-10) (±8-10 range): 42.5 → 52
- Both scores rounded to nearest integer: 53, 52

Output:
```json
{
  "themes": [
    {
      "label": "Equipment reliability",
      "polarity": "negative",
      "mention_count": 2,
      "magnitude": 53,
      "summary": "Screens and equipment losing functionality mid-session, with impact ranging from minor interruptions to significant frustration",
      "representative_detail": "\"Equipment kept failing, really frustrating.\""
    },
    {
      "label": "Staff responsiveness",
      "polarity": "positive",
      "mention_count": 2,
      "magnitude": 52,
      "summary": "Staff quickly addressing and resolving equipment issues to get guests back to playing",
      "representative_detail": "\"Staff was amazing - fixed our bay issue right away.\""
    }
  ]
}
```

Note: The generic "Great experience overall!" comment is not synthesized into a theme because it lacks specific substance.

# Resources

No additional references, scripts, or assets are required for this Skill, though you may reference the project context and `@metrics.json` file as needed.