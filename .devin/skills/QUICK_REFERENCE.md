# Skills Quick Reference

## The Four Skills at a Glance

```
┌─────────────────────────────────────────────────────────────────┐
│ COMBINED RANKING (from metrics + comments, sorted by magnitude) │
│                                                                 │
│ 1. LTR (positive, 82)                                           │
│ 2. Equipment reliability (negative, 71)                         │
│ 3. Staff responsiveness (positive, 65)                          │
│ 4. Food service speed (negative, 45)                            │
│ 5. Game selection (positive, 38)                                │
└─────────────────────────────────────────────────────────────────┘
        ↓ ↓ ↓ ↓ ↓
        │ │ │ │ └─────────────────────────────────────────┐
        │ │ │ └──────────────────────────┐                │
        │ │ └──────────────┐             │                │
        │ └────────┐       │             │                │
        └────┐    │       │             │                │
             ↓    ↓       ↓             ↓                ↓
    ┌──────────────────────────────────────────────────────────┐
    │ VENUE OVERVIEW SKILL                                     │
    │ "Tell the story of what's happening"                     │
    │ Uses: #1-3 to explain why they matter                    │
    │ Output: 2-4 sentence narrative                           │
    │ Key: Avoid redundant metric numbers                      │
    └──────────────────────────────────────────────────────────┘
             ↑
             │
    "This venue is performing well overall, driven by strong
     satisfaction with the experience. However, equipment
     reliability issues are creating friction that's preventing
     the entertainment experience from reaching its potential.
     Staff responsiveness is a bright spot, with most guests
     noting quick resolution of problems."

    ┌──────────────────────────────────────────────────────────┐
    │ UPS/DOWNS SKILL                                          │
    │ "Find 2-3 positive and 2-3 negative findings"            │
    │ Uses: Top items of each polarity (not just top 3)        │
    │ Output: 2-3 ups + 2-3 downs with explanations            │
    │ Key: Include lower-magnitude items with distinct value   │
    └──────────────────────────────────────────────────────────┘
             ↑
             │
    Ups:
    - Strong recommendation intent (87% LTR)
    - Responsive staff (quick resolution)
    - Game selection (variety appreciated)

    Downs:
    - Equipment reliability (screen tracking failures)
    - Food service speed (15-20 minute waits)

    ┌──────────────────────────────────────────────────────────┐
    │ IMPACT DRIVERS SKILL                                     │
    │ "Explain the top 3 factors affecting performance"        │
    │ Uses: Exactly #1, #2, #3 from ranking                    │
    │ Output: 3 drivers with 1-2 sentence explanations         │
    │ Key: Follow magnitude ranking strictly; cite numbers     │
    └──────────────────────────────────────────────────────────┘
             ↑
             │
    1. Recommendation Intent (82)
       "87% LTR indicates strong overall satisfaction and
        loyalty, the primary driver of venue performance."

    2. Equipment Reliability (71)
       "Screen tracking failures mentioned in 14 comments are
        the most significant operational issue, directly
        impacting the Fun experience."

    3. Staff Responsiveness (65)
       "Quick problem resolution is valued by guests, with 8
        specifically praising staff for getting them back to
        playing quickly."

    ┌──────────────────────────────────────────────────────────┐
    │ RECOMMENDATIONS SKILL                                    │
    │ "Generate actionable next steps"                          │
    │ Uses: #1 negative (critical), #2 negative (secondary),   │
    │       #1 positive (maintain)                             │
    │ Output: 3 tiers × 3-4 actions each                       │
    │ Key: Follow ranking priority order strictly              │
    └──────────────────────────────────────────────────────────┘
             ↑
             │
    CRITICAL (address #1 negative: Equipment Reliability)
    - Preventive maintenance: Daily screen calibration checks
    - Rapid response: Resolve issues within 2 minutes
    - Root cause analysis: Investigate hardware/software/calibration
    - Guest communication: Inform guests of issues and ETA

    SECONDARY (address #2 negative: Food Service Speed)
    - Kitchen optimization: Review order flow during peaks
    - Queue system: Visible queue so guests know wait time
    - Staff training: Emphasize speed during peaks
    - Menu simplification: Reduce complexity during peaks

    MAINTAIN (reinforce #1 positive: Recommendation Intent)
    - Satisfaction tracking: Continue monitoring LTR scores
    - Staff recognition: Reward responsive staff behaviors
    - Experience consistency: Protect overall quality
    - Feedback loop: Share positive feedback with staff
```

---

## How to Read a Skill File

Each skill file has this structure:

```markdown
# [Skill Name]

## Purpose
What this section does and why it matters

## Input
What data it receives (from combined ranking)

## Output
What it produces (JSON structure)

## Rules
Hard requirements (MUST, SHOULD, MAY)

## Examples
Real output samples showing good vs bad

## Strategy
How to approach the task
```

---

## Key Concepts

### Combined Ranking
- Merges all metrics + comment themes
- Sorted by magnitude (highest first)
- All skills use the same ranking
- Ensures consistent prioritization

### Magnitude (0-100)
- How much this factor affects guest satisfaction
- 70+: High impact
- 40-69: Medium impact
- <40: Low impact

### Polarity
- **Positive**: Something working well
- **Negative**: Something that needs fixing

### Traceability
- Every claim must come from a metric or comment theme
- No invented or untraced claims
- Numbers must be cited when available

---

## Quick Lookup

| Question | Answer | Skill |
|----------|--------|-------|
| How do I write the overview? | Tell the story without repeating metric numbers | venue-overview-skill |
| How do I pick ups/downs? | Select from combined ranking; include lower-magnitude items with value | ups-downs-skill |
| How do I explain impact? | Use top 3 from ranking; cite numbers; explain why they matter | impact-drivers-skill |
| How do I generate recommendations? | Critical=#1 negative, Secondary=#2 negative, Maintain=#1 positive | recommendations-skill |
| What if metrics and comments disagree? | Acknowledge the contradiction honestly; it's a real finding | venue-overview-skill |
| Can I include items not in top 3? | Yes for ups/downs; no for impact (impact is always top 3) | ups-downs-skill / impact-drivers-skill |
| How many actions per tier? | 3-4 actions per tier (critical, secondary, maintain) | recommendations-skill |
| Should I cite exact metric numbers? | No in overview; yes in impact and recommendations | venue-overview-skill |

---

## File Locations

```
.devin/skills/
├── QUICK_REFERENCE.md                    ← You are here
├── SKILLS_OVERVIEW.md                    ← Master guide
├── venue-overview-skill/
│   ├── SKILL.md                          ← Read this for overview guidance
│   └── OVERVIEW_METRICS_GUIDANCE.md      ← Detailed metrics handling
├── ups-downs-skill/
│   └── SKILL.md                          ← Read this for ups/downs guidance
├── impact-drivers-skill/
│   └── SKILL.md                          ← Read this for impact guidance
└── recommendations-skill/
    └── SKILL.md                          ← Read this for recommendations guidance
```

---

## Common Tasks

### I want to change how the overview sounds
→ Edit `venue-overview-skill/SKILL.md`

### I want to change which ups/downs are selected
→ Edit `ups-downs-skill/SKILL.md`

### I want to change the impact explanation style
→ Edit `impact-drivers-skill/SKILL.md`

### I want to change the recommendations structure
→ Edit `recommendations-skill/SKILL.md`

### I want to understand the whole system
→ Read `SKILLS_OVERVIEW.md`

### I want to see examples of good output
→ Look at the Examples section in each skill

### I want to understand the strategy
→ Look at the Strategy section in each skill

---

## Next Steps

1. **Understand the system**: Read `SKILLS_OVERVIEW.md`
2. **Pick a skill**: Choose the section you want to understand
3. **Read the skill**: Open `[skill-name]/SKILL.md`
4. **Review examples**: Look at the Examples section
5. **Understand strategy**: Read the Strategy section
6. **Edit if needed**: Make changes to the skill file
7. **Regenerate**: Clear cache and regenerate reports

---

## Questions?

- **How do skills work together?** → See SKILLS_OVERVIEW.md
- **How do I edit a skill?** → See the skill's SKILL.md file
- **What's the combined ranking?** → See SKILLS_OVERVIEW.md > Key Concepts
- **How do I understand the output?** → See the Examples section in each skill
- **How do I change the structure?** → See the Strategy section in each skill
