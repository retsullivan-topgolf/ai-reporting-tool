# Synthesis

Stage 3 of 3 in the venue report analysis pipeline. You do not see the raw metrics or the raw
comments - by design, so this stage stays fast. You see only the two earlier stages' structured
output:

- `metrics_analysis`: `{characterization, metric_flags: [{metric, polarity, magnitude, note}]}`
  from `templates/skills/metrics_analysis.md`
- `comment_analysis`: `{themes: [{label, polarity, mention_count, magnitude, summary,
  representative_detail}]}` from `templates/skills/comment_analysis.md`

Both stages already scored their findings on the same 0-100 magnitude scale for exactly this
reason: your job is to merge metric flags and comment themes into one ranked view of what matters
most for this venue, not to re-derive importance from scratch. Trust the magnitudes you're given.

This report covers one venue in isolation - don't state or imply a network/company average, a
network rank, or a comparison to "other venues" anywhere in your output.

## What to produce

Respond with ONLY a single JSON object (no markdown fences, no commentary before or after):

```json
{
  "overview": "2-4 sentence narrative paragraph summarizing the venue's overall performance, grounded in both the metrics characterization and the comment themes",
  "ups": ["<strong>Short title:</strong> 1-2 sentence description", ...],
  "downs": ["<strong>Short title:</strong> 1-2 sentence description", ...],
  "impact": [
    {"title": "Short driver name", "description": "1-2 sentence explanation of why this driver matters, citing the underlying number"}
  ],
  "recommendations": {
    "critical": {"title": "Short priority name", "items": ["<strong>Action name:</strong> description", ...]},
    "secondary": {"title": "Short priority name", "items": ["<strong>Action name:</strong> description", ...]},
    "maintain": {"title": "Short priority name", "items": ["<strong>Action name:</strong> description", ...]}
  }
}
```

## How to build each section

**`overview`**: Start from `metrics_analysis.characterization`, then fold in whichever comment
themes explain *why* the numbers look that way (or add something the metrics can't show at all).
The two stages were computed independently - if they seem to tell different stories, say so
honestly rather than papering over it; that's a real finding, not an error.

**Building one ranked candidate list**: Combine every `metric_flags` entry and every `themes`
entry into a single pool, and sort it by `magnitude`, highest first. This combined ranking is the
backbone for `impact` and `recommendations` below - don't rank them separately by topic or by how
positive/negative something feels. A high-magnitude positive (a strong metric, a loved feature)
can rank above a low-magnitude negative, and should.

**`impact`**: The top 3 entries from the combined ranking, most impactful first. `description`
should cite the actual number from the source entry's `note` or `summary`.

**`ups` / `downs`**: 2-3 items each, drawn from positive-polarity and negative-polarity entries in
the combined pool respectively - not necessarily only the top 3 from `impact`, since a venue can
have more than three things worth telling the reader about even if only three make the ranked
Impact section. Prefer higher-magnitude entries when choosing which to include.

**`recommendations`**: Priority order must match the combined ranking - never put a lower-ranked
negative in "critical" while a higher-ranked one is only "secondary".

- `critical` addresses the #1-ranked negative entry in the combined pool.
- `secondary` addresses the #2-ranked negative entry.
- `maintain` reinforces the top-ranked positive entry (a strong metric flag or a loved theme) -
  something worth protecting, not fixing.
- If there's no second negative entry (a venue with only one real problem), fall back to a
  sensible general operational-consistency priority rather than inventing a second real issue.
- Each section: 3-4 concrete action items.

## Formatting rules

- Inline HTML in list items is limited to `<strong>` tags only.
- If a comment theme names something specific (a particular game, a facility problem), carry that
  specific name into `ups`/`downs`/`impact`/`recommendations` instead of genericizing it.
- Ground every claim in a number or a stated theme from the two input stages - don't introduce
  numbers or claims that aren't traceable back to `metrics_analysis` or `comment_analysis`.
