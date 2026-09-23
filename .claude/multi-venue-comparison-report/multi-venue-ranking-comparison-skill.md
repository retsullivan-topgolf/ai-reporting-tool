# Multi-Venue Ranking Comparison Skill

Rank all venues by current-period absolute performance, with ranking movement shown as secondary context. Explain tier shifts and venue positioning between periods.

## Purpose

The Venue Ranking for comparison shows both "who's best right now" (absolute ranking) and "who moved up/down" (ranking movement). This two-level view helps identify which venues are improving, which are falling behind, and which are holding steady.

## Input

- Current and previous period metrics for all venues
- Venue rankings from both periods
- Change deltas for each venue

## Output

Array of ranked venues (sorted by current NPS) with movement:

```json
{
  "rank": 1,
  "venue": "Grand Prairie",
  "nps_current": 8.8,
  "nps_previous": 8.2,
  "nps_delta": 0.6,
  "previous_rank": 2,
  "rank_movement": "up 1 spot",
  "tier": "top_performer",
  "summary": "1-2 sentence explaining current position and movement"
}
```

## Rules

### Primary Ranking (Current Period)
- MUST rank by current-period NPS/composite score (absolute)
- Rank 1 = highest NPS, Rank 7 = lowest NPS (same as snapshot)
- Do NOT reorder based on movement magnitude

### Secondary Context (Ranking Movement)
- MUST show previous rank for each venue
- MUST cite rank movement (up/down X spots, or "held steady")
- MUST cite NPS delta (current - previous)
- MUST explain what the movement means

### Tier Assignments
Same as snapshot (based on current-period absolute performance):
- **top_performer:** Current NPS ≥8.5
- **solid_performer:** Current NPS 8.0-8.4
- **middle_performer:** Current NPS 7.5-7.9
- **needs_support:** Current NPS <7.5

### Summary Content
For each venue, explain:
- Current position (rank, tier, NPS)
- Movement from previous period (up/down X, delta)
- Why the movement occurred (tie to major drivers if significant change)

## Examples

### ✅ Good Ranking Comparison Example

```json
[
  {
    "rank": 1,
    "venue": "Grand Prairie",
    "nps_current": 8.8,
    "nps_previous": 8.2,
    "nps_delta": 0.6,
    "previous_rank": 2,
    "rank_movement": "up 1 spot",
    "tier": "top_performer",
    "summary": "Moved from 2nd to 1st (up 0.6 NPS) by addressing equipment reliability. Now leads the network with strong performance across all metrics."
  },
  {
    "rank": 2,
    "venue": "Austin",
    "nps_current": 8.4,
    "nps_previous": 7.8,
    "nps_delta": 0.6,
    "previous_rank": 3,
    "rank_movement": "up 1 spot",
    "tier": "top_performer",
    "summary": "Improved significantly (0.6 NPS) and moved up one spot, but trail Grand Prairie. Tracking Grand Prairie's equipment maintenance practices."
  },
  {
    "rank": 7,
    "venue": "El Paso",
    "nps_current": 7.0,
    "nps_previous": 7.2,
    "nps_delta": -0.2,
    "previous_rank": 7,
    "rank_movement": "held 7th",
    "tier": "needs_support",
    "summary": "Declined -0.2 NPS while holding bottom rank. Equipment issues worsened (32% to 36%), requiring urgent operational support."
  }
]
```

**Why this works:**
- Primary ranking by current NPS (8.8, 8.4, ... 7.0)
- Movement shown secondary (up 1, up 1, held)
- Deltas cited (0.6, 0.6, -0.2)
- Summary explains what changed and why
- Tier assigned by current performance

---

## Ranking Movement Semantics

- **Moved up X spots:** Venue's rank improved (was rank N, now rank N-X)
- **Moved down X spots:** Venue's rank worsened (was rank N, now rank N+X)
- **Held steady/Held Xth:** Venue's rank didn't change
- **New entrant:** Venue wasn't in previous ranking (too few responses, etc.)

---

## Movement Explanation Guidelines

For significant movement (±2+ spots):
- Cite what drove the change (equipment improved, F&B worsened, etc.)
- Explain if venue improved more/less than network average
- Note if movement suggests venue-specific vs. network-wide factors

For stable venues:
- Note if they're maintaining strength or treading water
- Mention if they're resisting network trend (e.g., "improved while network declined")

---

## Related Skills

- See `multi-venue-overview-comparison-skill.md` for overall network trend
- See `multi-venue-impact-drivers-comparison-skill.md` for what drove each venue's movement
- See `multi-venue-ups-downs-comparison-skill.md` for network patterns

## Resources

- `README.md` - Integration guide
- `synthesis_template.md` - The actual prompt
