# Multi-Venue Ups/Downs Comparison Skill

Select 2-3 network patterns that **improved** and 2-3 that **declined** between periods, framing as network-wide trends with venue-level context.

## Purpose

Ups and Downs highlight findings where the network showed meaningful **change**: what's getting better? What's getting worse? How do venues align or diverge on these trends?

## Input

- Metrics from both periods (current & previous)
- Themes from both periods
- Combined ranking by **change magnitude** (deltas)

## Output

Two arrays (2-3 items each):

```json
{
  "ups": [
    "<strong>Short title:</strong> 1-2 sentence showing improvement"
  ],
  "downs": [
    "<strong>Short title:</strong> 1-2 sentence showing decline"
  ]
}
```

## Rules

### Selection & Framing
- **Ups:** Select improvements across network (magnitude improved 0.5+ points or new positive theme)
  - Frame as "improved", "strengthened", "recovered", "become more consistent"
  - Show if all venues improved or some diverged
- **Downs:** Select declines across network (magnitude declined -0.5+ points or new negative theme)
  - Frame as "declined", "worsened", "emerged", "became inconsistent"
  - Show venue-level variance in the decline

### Venue Context
- MUST mention if network showed consensus (all venues moved same direction)
- MUST note if venues diverged ("except at El Paso")
- MUST cite specific deltas (e.g., "from 28% to 25%" or "dropped from 8.2 to 8.0")

### Mechanics
- Use `<strong>` tags for titles only
- 1-2 sentences per item
- Ground in numbers and themes from input

## Examples

**Improvement - Network Consensus:**
```
<strong>Equipment reliability improved across all venues:</strong> Issue rate 
dropped from network average 28% to 25%, with all venues showing gains of 0.3-0.6 
points. This improvement was the primary driver of network satisfaction gains.
```

**Decline - Venue Divergence:**
```
<strong>F&B service speed declined unevenly:</strong> While most venues maintained 
wait times, El Paso saw significant deterioration (from 3.2 to 2.8/5). This suggests 
venue-specific staffing or workflow challenges rather than network-wide operational 
changes.
```

---

## Related Skills

- See `multi-venue-overview-comparison-skill.md` for network trend context
- See `multi-venue-impact-drivers-comparison-skill.md` for top drivers of change

## Resources

- `README.md` - Integration guide
- `synthesis_template.md` - Implementation
