# Multi-Venue Recommendations Comparison Skill

Generate network-level actions for sustaining/amplifying improvements and addressing declines, plus venue-specific guidance for outliers and divergent venues.

## Purpose

Recommendations for comparison answer: "What should the network do to sustain momentum on improvements and address emerging declines? What does each venue specifically need?"

Tier semantics differ from snapshot: critical/secondary address the #1/#2 **changes** (biggest improvement or decline), not just issues.

## Input

- Metrics and themes from both periods
- Ranking movement for each venue
- Combined ranking by change magnitude

## Output

Three tiers + venue-specific actions:

```json
{
  "recommendations": {
    "critical": {
      "title": "Sustain [improvement] or Address [decline]",
      "items": ["<strong>Action name:</strong> description", ...]
    },
    "secondary": {...},
    "maintain": {...},
    "venue_specific": [
      {
        "venue": "Venue name",
        "priority": "critical" or "secondary" or "maintain",
        "action": "1-2 sentence action for this venue's situation"
      },
      ...
    ]
  }
}
```

## Rules

### Tier Selection
- **Critical:** Address #1 change (biggest improvement or decline)
  - If improvement: "Sustain momentum", "Amplify gains", "Protect improvements"
  - If decline: "Reverse trend", "Address emerging issue"
- **Secondary:** Address #2 change or cross-cutting theme
- **Maintain:** Reinforce top positive finding (something stable or strong)

### Venue-Specific Actions
Include actions for:
- Venues that improved significantly (acknowledge momentum)
- Venues that declined (support for remediation)
- Venues that diverged from network trend (why? leverage or cautionary tale?)
- All venues if network is small (<5)

### Action Content
- What to do (concrete step)
- Why (tie to change and baseline period)
- Expected outcome or reference to previous performance

## Examples

**Critical: Sustain Equipment Improvement**
```json
{
  "title": "Sustain Equipment Reliability Improvements",
  "items": [
    "<strong>Expand best practices:</strong> Grand Prairie's +0.8 improvement shows what's 
    possible. Roll out their equipment maintenance schedule to Austin (+0.6 gain) and 
    expand to other venues.",
    "<strong>Support El Paso recovery:</strong> Despite overall network improvement, El Paso 
    worsened (+0.3 worse). Conduct equipment audit and implement Grand Prairie's practices."
  ]
}
```

**Venue-Specific Actions:**
```json
{
  "venue": "Grand Prairie",
  "priority": "maintain",
  "action": "You led equipment improvements (+0.8 NPS). Document and share your maintenance 
  practices with Austin and El Paso to expand the network's gains."
},
{
  "venue": "El Paso",
  "priority": "critical",
  "action": "Your equipment issues worsened while the network improved. Partner with Grand 
  Prairie on maintenance practices and commit to baseline recovery (back to -0.0 from current -0.2)."
}
```

---

## Tier Naming Patterns

| Tier | Pattern | Example |
|---|---|---|
| **Critical (improvement)** | "Sustain [improvement]" | "Sustain Equipment Reliability Gains" |
| **Critical (decline)** | "Address [decline]" | "Address F&B Service Speed Decline" |
| **Secondary** | General operational | "Improve operational consistency" |
| **Maintain** | "Protect [strength]" | "Protect staff responsiveness" |

---

## Related Skills

- See `multi-venue-impact-drivers-comparison-skill.md` for what drove the changes
- See `multi-venue-ranking-comparison-skill.md` for venue movement context
- See `multi-venue-overview-comparison-skill.md` for overall network trend

## Resources

- `README.md` - Integration guide
- `synthesis_template.md` - Implementation
