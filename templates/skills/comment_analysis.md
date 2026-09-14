# Comment Analysis

Stage 2 of 3 in the venue report analysis pipeline (see `templates/skills/metrics_analysis.md`
and `templates/skills/synthesis.md` for the other two). This stage looks only at the free-text
guest comments for one venue - it never sees the aggregate metrics, which is what keeps it fast
and focused. Your job is to find the real, specific themes guests are actually describing and
score each one on the same 0-100 magnitude scale the metrics stage uses, so a later synthesis
step can rank comment-driven themes against metric-driven ones fairly.

## What you're given

- `venue`, `responses` (total survey count for the period - not all of these left a comment)
- `comments`: a list of `{text, ltr, fun}` - each guest's comment alongside their own LTR (0-10)
  and Fun (0-5) scores from that same response, so you can tell whether a theme showed up in
  otherwise-happy responses or genuinely unhappy ones.

## What to produce

Respond with ONLY a single JSON object (no markdown fences, no commentary):

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
    }
  ]
}
```

**Finding themes**: Read the comments themselves rather than pattern-matching on a fixed keyword
list - guests describe the same problem in lots of different words (a stuck screen, a game that
won't start, and a bay that "kept having problems" are probably all the same underlying equipment
issue). Group by what's actually going on, not by surface wording. Call out anything specific and
recurring by name - a named game, a specific facility problem, a particular part of the visit
(parking, food, a certain question) - instead of a generic label like "operational issues" when a
more specific one is available and accurate.

Don't invent a theme from a single generic comment ("had a great time!") - that's sentiment, not a
theme. A theme needs some specific, describable substance to it, even if only one guest mentioned
it (see magnitude scoring below for how mention count should and shouldn't drive importance).

**Each theme entry**:

- `label`: short, specific name (2-4 words)
- `polarity`: `"positive"` or `"negative"` - a theme that cuts both ways (some guests loved it,
  some didn't) should usually be split into two theme entries rather than forced into one
- `mention_count`: how many distinct comments raised this theme
- `magnitude`: 0-100, see scoring below
- `summary`: 1-2 sentences describing what guests are actually saying, in your own words
- `representative_detail`: a short verbatim quote (or close paraphrase) from one comment that
  best illustrates the theme - this is what makes the theme feel grounded in real feedback rather
  than a generic label

### Scoring magnitude (keep this consistent with the metrics stage)

The target is the same as stage 1: a 0-100 number meaning roughly "how much does this matter to
overall guest satisfaction here," comparable across themes and against metric flags.

- Start from mention share: `mention_count / responses * 100` is a reasonable baseline - a theme
  fourteen different guests brought up unprompted is a bigger deal than one two guests mentioned,
  roughly in proportion to how many people it's touching.
- Adjust up when the guests raising a negative theme also gave notably low LTR/Fun scores in that
  same response (the theme isn't just common, it's actually tanking satisfaction) - and adjust up
  regardless of mention count when even one or two guests describe an unusually severe outcome
  (left without playing, wouldn't recommend at all, an unresolved safety issue). A single comment
  describing a genuinely bad outcome can outscore a theme with more mentions but milder
  descriptions.
- Adjust down when a theme is mentioned but the guest still rated the visit highly overall (a
  minor gripe in an otherwise glowing comment shouldn't score like a dominant complaint).
- Don't let low sample size force weak themes into existence. If a venue only has three comments
  and none of them describe anything specific and recurring, an empty or short `themes` list is
  the correct, honest output.

Order `themes` by magnitude, highest first.
