---
name: metrics-analysis
description: Analyze aggregate survey metrics for a venue and produce a characterization with comparable concern magnitudes
---

# Purpose

Analyze the aggregate survey metrics for a single venue and produce a short characterization of what the numbers say together, plus a set of comparable "concern magnitudes" that a later synthesis step can rank against comment themes on the same scale. This is Stage 1 of 3 in a venue report analysis pipeline.

Metrics may include core metrics (LTR, Fun, Helpfulness, Issues, Resolution) and optional metrics (NPS, Price Value, F&B metrics).

# Inputs

Required:

- `venue`: venue name
- `responses`: survey count for the period
- `metrics`: object containing:
  - `ltr_avg` (0-5 scale) - Likelihood to Return: customer intent to return to this or another venue
  - `fun_avg` (0-5 scale)
  - `helpful_avg` (0-5 scale)
  - `issues_pct` (0-100 scale)
  - `resolution_avg` (0-5 scale, or `null` if no issues reported)
- `assessment_tiers`: pre-computed tier for each metric (e.g. "Strong", "Critical") from `templates/metrics.json`

Optional (if present in data):

- `nps_avg` (0-10 scale) - Combined NPS, a Qualtrics-computed recommend-intent metric distinct from LTR
- `price_value_avg` (0-5 scale) - perceived value for money
- `food_value_avg` (0-5 scale) - food offering value
- `food_speed_avg` (0-5 scale) - food service speed
- `food_quality_avg` (0-5 scale) - food quality
- `beverage_value_avg` (0-5 scale) - beverage offering value
- `beverage_speed_avg` (0-5 scale) - beverage service speed
- `beverage_quality_avg` (0-5 scale) - beverage quality
- `food_avg` (0-5 scale) - computed average of the food metrics (value, speed, quality)
- `beverage_avg` (0-5 scale) - computed average of the beverage metrics (value, speed, quality)
- `fb_average` (0-5 scale) - computed average of all F&B metrics (food + beverage combined)

If no source information is available, ask the user to provide the required information before continuing.

# Context

Always use:

- The assessment tiers as ground truth for how good/bad each number is in isolation
- The absolute scales given; do not reference network/company averages or comparisons to other venues
- The understanding that `resolution_avg` may be `null` (normal outcome of low issue rate, not a weakness)

When applicable, use:

- Cross-metric patterns (e.g., strong Fun/Helpful scores alongside high issue rate suggests operations undermining core experience)


Treat the provided metrics and assessment tiers as the source of truth. Do not invent information solely to make the output appear more complete.

# Workflow

1. Read the venue name, response count, and all metrics (both core and optional).
2. Review the assessment tiers to understand how each metric rates in isolation.
3. Analyze cross-metric patterns and relationships to form a characterization (1-2 sentences).
   - If F&B metrics are present, consider how they relate to overall satisfaction (e.g., strong F&B may offset operational issues, or weak F&B may be dragging down satisfaction)
   - If NPS or Price Value are present, consider what they reveal about customer intent and value perception
4. Identify metrics worth flagging (typically anything not squarely "Moderate"/middle-of-the-road).
5. For each flagged metric, compute magnitude using the scoring rules below.
6. Order metric_flags by magnitude, highest first.
7. Validate the completed output against the Output and Rules sections before returning it.

# Output

Respond with ONLY a single JSON object (no markdown fences, no commentary):

```json
{
  "characterization": "1-2 sentence read on what these five numbers say about the venue, focused on how they relate to each other rather than restating each one",
  "metric_flags": [
    {
      "metric": "issues",
      "polarity": "negative",
      "magnitude": 68,
      "note": "52% of guests reported an issue - a systemic rate, not isolated incidents"
    },
    {
      "metric": "fun",
      "polarity": "positive",
      "magnitude": 18,
      "note": "Fun score of 4.2/5 is solidly Strong, showing the core activity delivers"
    }
  ]
}
```

**`characterization`**: Look for combinations a single metric can't show on its own. Say what the numbers suggest together, not a list of each one restated in prose. Use natural language targeted to managers, c-suite executives, and owners to describe the relationships between metrics.

Example sythesized characterisation: "Strong Fun and Helpfulness scores indicate the core experience resonates well, but a 52% issue rate reveals significant operational friction that's undermining guest satisfaction despite the quality of games and excellence of service."

**`metric_flags`**: One entry per metric that's worth calling out. Each entry must include:

- `metric`: one of `ltr`, `fun`, `helpful`, `issues`, `resolution`, `nps`, `price_value`, `food_value`, `food_speed`, `food_quality`, `beverage_value`, `beverage_speed`, `beverage_quality`, `food`, `beverage`, `fb_average`
- `polarity`: `"positive"` or `"negative"`
- `magnitude`: 0-100, representing how much this metric matters to overall guest satisfaction for this venue
- `note`: one sentence, cite the actual number

# Rules

## Characterization

- MUST synthesize cross-metric patterns, not restate individual scores
- MUST focus on what the numbers suggest together
- MUST be 1-2 sentences
- MUST NOT reference network/company averages or comparisons to other venues
- MUST NOT imply this venue is being ranked against others

## Metric Flags

- MUST include one entry per metric worth calling out (typically anything not "Moderate")
- MUST NOT flag metrics with nothing notable to say (e.g., a "Strong" Fun score with nothing unusual)
- MUST NOT flag `resolution_avg` as a concern if it is `null` (this is normal for low issue rates)
- MUST NOT flag optional metrics (NPS, Price Value, F&B) if they are not present in the input data
- MUST order flags by magnitude, highest first
- if all metrics are moderate, return an array with all of them with their respective magnitudes
- When F&B metrics are present, consider flagging the `fb_average` if it's notably strong or weak, as it represents the overall food & beverage experience

## Magnitude Scoring

The goal is a number that means roughly the same thing regardless of which metric or venue produced it.

- For `issues_pct`: magnitude is close to the raw percentage (it's already "% of guests affected"). A 52% issue rate is roughly twice as significant as a 26% rate.
- For `ltr`, `fun`, `helpful`, `resolution` (higher-is-better scales): magnitude scales with how far the score falls below (negative flag) or rises above (positive flag) a solid baseline, as a percentage of the scale's full range. A score barely below "Strong" is mild; a score near the bottom is severe.
- MUST NOT inflate magnitude to make a section feel important. A genuinely solid venue should produce few or no negative flags and modest magnitudes.

# Example

The following demonstrates formatting only. Do not assume these requirements apply to the user's source.

```json
{
  "characterization": "Strong Fun and Helpfulness scores indicate the core experience resonates well, but a 52% issue rate reveals significant operational friction that's undermining guest satisfaction despite the quality of the activity itself.",
  "metric_flags": [
    {
      "metric": "issues",
      "polarity": "negative",
      "magnitude": 52,
      "note": "52% of guests reported an issue - a systemic rate, not isolated incidents"
    },
    {
      "metric": "ltr",
      "polarity": "negative",
      "magnitude": 35,
      "note": "LTR of 3.2/5 is below the Good threshold, likely depressed by the high issue rate"
    },
    {
      "metric": "fun",
      "polarity": "positive",
      "magnitude": 18,
      "note": "Fun score of 4.2/5 is solidly Strong, showing the core activity delivers"
    }
  ]
}
```

# Resources

No additional references, scripts, or assets are required for this Skill, though you may reference the project context and `templates/metrics.json` as needed.
