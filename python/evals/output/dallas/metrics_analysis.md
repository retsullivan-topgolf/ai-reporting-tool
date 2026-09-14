# Stage 1: Metrics Analysis Eval

**Venue:** Dallas

## Input sent to the skill

```json
{
  "venue": "Dallas",
  "responses": 29,
  "metrics": {
    "ltr_avg": 7.1,
    "fun_avg": 3.9,
    "helpful_avg": 4.0,
    "issues_pct": 51.7,
    "resolution_avg": 3.5
  },
  "assessment_tiers": {
    "ltr": "Strong",
    "fun": "Strong",
    "helpful": "Strong",
    "issues": "Critical",
    "resolution": "Strong"
  }
}
```

## Raw AI output

```json
{
  "characterization": "Strong Fun and Helpful scores indicate the core experience resonates well, but a 51.7% issue rate\u00e2\u20ac\u201daffecting more than half of respondents\u00e2\u20ac\u201dreveals significant operational friction that's likely dampening guest satisfaction despite solid resolution efforts.",
  "metric_flags": [
    {
      "metric": "issues",
      "polarity": "negative",
      "magnitude": 52,
      "note": "51.7% of guests reported an issue - a systemic rate, not isolated incidents"
    }
  ]
}
```

## Automated checks

| Check | Result | Detail |
|---|---|---|
| output matches expected schema (characterization + metric_flags[]) | PASS |  |
| metric_flags ordered by magnitude (highest first) | PASS | magnitudes=[52] |
| every flag uses a known metric name (ltr/fun/helpful/issues/resolution) | PASS |  |
| every flag's magnitude is within 0-100 | PASS |  |
| characterization avoids network/comparison language (rule: 'MUST NOT reference network/company averages or comparisons to other venues') | PASS |  |

## Manual review notes

Automated checks above only cover mechanically-checkable rules (ordering, schema, banned phrases, count bounds). Read the raw output above and judge it against the rest of the skill doc's Rules section by hand - specificity, whether themes are genuinely grounded in the input, narrative quality, etc.
