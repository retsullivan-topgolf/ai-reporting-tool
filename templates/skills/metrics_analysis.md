# Metrics Analysis

Stage 1 of 3 in the venue report analysis pipeline (see `templates/skills/comment_analysis.md`
and `templates/skills/synthesis.md` for the other two). This stage looks only at the five
aggregate survey metrics for one venue - it never sees the free-text comments, which is what
keeps it fast. Your job is to turn five numbers into a short, honest characterization plus a set
of comparable "concern magnitudes" that a later synthesis step can rank against comment themes on
the same scale.

## What you're given

- `venue`, `responses` (survey count for the period)
- `metrics`: `ltr_avg` (0-10), `fun_avg` (0-5), `helpful_avg` (0-5), `issues_pct` (0-100),
  `resolution_avg` (0-5, or `null`)
- `assessment_tiers`: the already-computed tier for each metric (e.g. "Strong", "Critical") from
  `templates/metrics.json`'s fixed quality bar. These are deterministic lookups, not your job to
  recompute - use them as ground truth for how good/bad each number is in isolation. Your job is
  the interpretation *across* metrics that a single threshold lookup can't capture.

`resolution_avg` may be `null` - that means nobody reported an issue, so nobody answered the
resolution question. That's the normal, good outcome of a low issue rate, not a missing or weak
score. Never flag a null resolution_avg as a concern.

This report covers one venue in isolation. Don't state or imply a network/company average, a
network rank, or a comparison to "other venues" - there's no such data here. Judge the venue only
against the absolute scales given.

## What to produce

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
    }
  ]
}
```

**`characterization`**: Look for combinations a single metric can't show on its own - e.g. strong
Fun/Helpful scores next to a high issue rate usually means the core experience is good but
operations are undermining it; a low LTR despite low issues might mean the problem isn't
incidents at all, but something the survey's other questions don't capture. Say what the numbers
suggest together, not a list of each one restated in prose.

**`metric_flags`**: One entry per metric that's worth calling out - typically anything that isn't
squarely "Moderate"/middle-of-the-road. Skip metrics with nothing notable to say (a "Strong" Fun
score with nothing unusual about it doesn't need an entry). Each entry:

- `metric`: one of `ltr`, `fun`, `helpful`, `issues`, `resolution`
- `polarity`: `"positive"` or `"negative"`
- `magnitude`: 0-100, how much this metric matters to overall guest satisfaction for *this*
  venue - see scoring below. This is what makes a metric flag comparable to a comment theme from
  stage 2, so take it seriously; don't default to round numbers like 50 for everything.
- `note`: one sentence, cite the actual number

### Scoring magnitude (keep this consistent across venues)

The goal is a number that means roughly the same thing regardless of which metric or which venue
produced it, so synthesis can sort metric flags and comment themes together into one ranked list.

- For `issues_pct`, the magnitude is close to the raw percentage - it's already "% of guests
  affected," which is about as direct a magnitude as a metric gets. A 52% issue rate is a bigger
  deal than a 15% one, roughly in proportion.
- For `ltr`, `fun`, `helpful`, `resolution` (all higher-is-better, 0-10 or 0-5 scales): magnitude
  scales with how far the score falls below (for a negative flag) or how far above a solid
  baseline it sits (for a positive flag), as a percentage of the scale's full range. A score
  barely below the "Strong" bar is a mild negative; a score near the bottom of the scale is a
  severe one.
- Don't inflate magnitude just to make a section feel important. A venue that's genuinely solid
  everywhere should produce few or no negative flags and modest magnitudes - that's the correct,
  honest output, not a failure to find something wrong.

Order `metric_flags` by magnitude, highest first.
