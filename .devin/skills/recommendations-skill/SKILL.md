# Recommendations Skill

Generate actionable, prioritized recommendations organized into three tiers: critical (address top negative), secondary (address second negative), and maintain (reinforce top positive).

## Purpose

The Recommendations section translates findings into concrete actions. Each tier targets a specific ranked finding from the combined ranking, ensuring recommendations are data-driven and operationally feasible.

## Input

- `combined_ranking`: merged metrics + comment themes, sorted by magnitude (highest first)
- `metrics_analysis`: metric_flags with polarity, magnitude, and note
- `comment_analysis`: themes with polarity, magnitude, and summary
- `venue`: venue name (for context)

## Output

Three recommendation tiers:

```json
{
  "recommendations": {
    "critical": {
      "title": "Short priority name",
      "items": [
        "<strong>Action name:</strong> description",
        "<strong>Action name:</strong> description",
        "<strong>Action name:</strong> description",
        "<strong>Action name:</strong> description"
      ]
    },
    "secondary": {
      "title": "Short priority name",
      "items": [
        "<strong>Action name:</strong> description",
        "<strong>Action name:</strong> description",
        "<strong>Action name:</strong> description",
        "<strong>Action name:</strong> description"
      ]
    },
    "maintain": {
      "title": "Short priority name",
      "items": [
        "<strong>Action name:</strong> description",
        "<strong>Action name:</strong> description",
        "<strong>Action name:</strong> description",
        "<strong>Action name:</strong> description"
      ]
    }
  }
}
```

## Rules

### Tier Assignment
- `critical`: MUST address the #1-ranked negative entry from the combined pool
- `secondary`: MUST address the #2-ranked negative entry; if only one negative exists, use a sensible general operational-consistency priority instead
- `maintain`: MUST reinforce the top-ranked positive entry (a strong metric flag or loved theme) - something worth protecting, not fixing

### Ranking Compliance
- MUST follow the combined ranking priority order - never put a lower-ranked negative in "critical" while a higher-ranked one is only "secondary"
- MUST derive each action directly from the combined ranking, addressing the top-ranked issues first

### Content
- MUST include 3-4 concrete action items per section
- MUST include 3-4 concrete, venue-specific action items per section
- Actions MUST be operationally feasible and directly traceable to a ranked finding from either metrics or comments
- For `critical` and `secondary`: actions MUST directly address the negative finding (e.g., if equipment reliability is #1, actions should target equipment maintenance, diagnostics, or response protocols)
- For `maintain`: actions MUST protect or reinforce the positive finding (e.g., if staff responsiveness is top-ranked positive, actions should preserve those practices and recognize staff)
- Actions MAY reference specific details from comment themes (named games, facility problems, visit phases) rather than generic operational areas
- Each action MUST be 1-2 sentences and start with a short, bold action name

### Formatting
- MUST use inline HTML limited to `<strong>` tags only
- Each item MUST start with a short, bold action name followed by a colon
- Action name should be 2-5 words describing the action
- Description should be 1-2 sentences

## Examples

### Example 1: Equipment Reliability as #1 Negative

**Critical Tier (addressing equipment reliability):**
```json
{
  "title": "Fix Equipment Reliability",
  "items": [
    "<strong>Preventive maintenance schedule:</strong> Implement daily screen calibration checks before peak hours to catch tracking issues before guests encounter them.",
    "<strong>Rapid response protocol:</strong> Ensure staff can resolve screen issues within 2 minutes; guests accept occasional failures if resolution is fast.",
    "<strong>Root cause analysis:</strong> Investigate whether tracking failures are hardware, software, or calibration-related to target the fix appropriately.",
    "<strong>Guest communication:</strong> When equipment fails, proactively inform guests of the issue and expected resolution time to manage expectations."
  ]
}
```

**Secondary Tier (addressing food service speed as #2 negative):**
```json
{
  "title": "Improve Food Service Speed",
  "items": [
    "<strong>Kitchen workflow optimization:</strong> Review order flow and staffing during peak hours to identify bottlenecks in food preparation.",
    "<strong>Order queueing system:</strong> Implement a visible queue system so guests know their position and expected wait time.",
    "<strong>Staff training:</strong> Ensure kitchen staff understand the impact of slow service on overall satisfaction and prioritize speed.",
    "<strong>Menu simplification:</strong> Consider reducing menu complexity during peak hours to speed up preparation times."
  ]
}
```

**Maintain Tier (reinforcing strong LTR/recommendation intent):**
```json
{
  "title": "Protect Recommendation Intent",
  "items": [
    "<strong>Guest satisfaction tracking:</strong> Continue monitoring LTR and Fun scores to ensure equipment fixes maintain the strong recommendation intent.",
    "<strong>Staff recognition:</strong> Acknowledge and reward the responsive staff behaviors that guests are noticing and appreciating.",
    "<strong>Experience consistency:</strong> Protect the overall experience quality that's driving the 87% recommendation rate.",
    "<strong>Feedback loop:</strong> Regularly share positive guest feedback with staff to reinforce what's working well."
  ]
}
```

---

### Example 2: Multiple Negatives with Only One Positive

**Critical Tier (addressing #1 negative):**
```json
{
  "title": "Reduce Issue Frequency",
  "items": [
    "<strong>Daily equipment checks:</strong> Implement a pre-opening checklist covering all games and facilities to catch issues before guests arrive.",
    "<strong>Maintenance scheduling:</strong> Establish a preventive maintenance calendar for high-use equipment to reduce unexpected failures.",
    "<strong>Staff training:</strong> Ensure all staff can quickly diagnose and resolve common issues to minimize guest impact.",
    "<strong>Issue tracking system:</strong> Log all reported issues to identify patterns and systemic problems."
  ]
}
```

**Secondary Tier (addressing #2 negative):**
```json
{
  "title": "Improve Issue Resolution",
  "items": [
    "<strong>Resolution time targets:</strong> Set and track target resolution times (e.g., 5 minutes for most issues) to improve guest satisfaction.",
    "<strong>Escalation protocol:</strong> Define clear escalation paths for issues staff can't resolve quickly.",
    "<strong>Guest compensation:</strong> Empower staff to offer compensation (free play, discount) when resolution takes longer than expected.",
    "<strong>Follow-up process:</strong> Check in with guests after issue resolution to ensure satisfaction."
  ]
}
```

**Maintain Tier (reinforcing top positive - even if lower magnitude):**
```json
{
  "title": "Operational Consistency",
  "items": [
    "<strong>Service standard documentation:</strong> Document the rapid-response practices that staff are already doing well so consistency is maintained across shifts.",
    "<strong>Staff training refresh:</strong> Ensure all staff know the equipment troubleshooting steps to maintain the responsiveness guests are experiencing.",
    "<strong>Shift handoff process:</strong> Establish clear communication between shifts to maintain service standards.",
    "<strong>Performance metrics:</strong> Track and reward staff who maintain high service standards."
  ]
}
```

---

## Tier Selection Strategy

### Step 1: Identify Negative Entries
From the combined ranking, find all entries with `polarity: "negative"`:

```
Ranking:
1. LTR (positive, 82)           ← Skip
2. Equipment reliability (negative, 71)  ← #1 negative
3. Staff responsiveness (positive, 65)   ← Skip
4. Food service speed (negative, 45)     ← #2 negative
5. Game selection (positive, 38)         ← Skip
```

### Step 2: Assign Tiers
- **Critical**: Address #1 negative (Equipment reliability)
- **Secondary**: Address #2 negative (Food service speed)
- **Maintain**: Reinforce top positive (LTR - #1 in ranking)

### Step 3: Generate Actions
For each tier, generate 3-4 concrete actions that directly address that finding.

---

## Action Generation Guidelines

### For Critical/Secondary (Addressing Negatives)

**Start with the problem:**
- What is the issue? (from comment theme or metric)
- How many guests are affected? (magnitude)
- What's the impact? (why it matters)

**Then derive actions:**
- What can we do to fix this?
- What's operationally feasible?
- What's directly traceable to the finding?

**Example:**
- Problem: "Screen tracking failures mentioned in 14 comments"
- Actions:
  1. Daily calibration checks (preventive)
  2. 2-minute resolution protocol (responsive)
  3. Root cause analysis (diagnostic)
  4. Guest communication (expectation management)

### For Maintain (Reinforcing Positives)

**Start with the strength:**
- What are we doing well? (from metric or theme)
- Why do guests value it? (magnitude)
- What's the impact? (why it matters)

**Then derive actions:**
- How do we protect this?
- How do we reinforce it?
- How do we ensure consistency?

**Example:**
- Strength: "87% LTR - strong recommendation intent"
- Actions:
  1. Continue tracking (measurement)
  2. Staff recognition (reinforcement)
  3. Experience consistency (protection)
  4. Feedback loop (communication)

---

## Related Skills

- See [venue-overview-skill](../venue-overview-skill/SKILL.md) for the narrative summary
- See [ups-downs-skill](../ups-downs-skill/SKILL.md) for additional findings
- See [impact-drivers-skill](../impact-drivers-skill/SKILL.md) for the top 3 ranked drivers

## Resources

- `.claude/single-venue-report/synthesis.md` - The actual prompt that implements this skill
