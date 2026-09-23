# Multi-Venue Recommendations Skill

Generate actionable next steps in three network-level tiers (`critical`, `secondary`, `maintain`), plus venue-specific actions for each location.

## Purpose

Recommendations for multi-venue reports answer: "What should the network do to improve overall performance, and what does each venue specifically need?"

This skill separates network-wide initiatives (which drive systemic improvement) from venue-specific actions (which address local challenges or leverage local strengths).

## Input

- `metrics_analysis`: Network characterization + venue outliers
- `comment_analysis`: Themes with venue_breakdown
- `combined_ranking`: All findings by network-wide magnitude
- Venue ranking and tier assignments

## Output

Three network tiers + venue-specific actions:

```json
{
  "recommendations": {
    "critical": {
      "title": "Short priority name",
      "items": ["<strong>Action name:</strong> description", ...]
    },
    "secondary": {...},
    "maintain": {...},
    "venue_specific": [
      {
        "venue": "Venue name",
        "priority": "critical" or "secondary" or "maintain",
        "action": "1-2 sentence action specific to this venue"
      },
      ...
    ]
  }
}
```

## Rules

### Network Tier Selection
- **Critical:** Address the #1-ranked negative finding network-wide
  - Actions: Standardization, best practice sharing, systemic fixes
  - Example: "Standardize Equipment Maintenance" if equipment is #1 issue
- **Secondary:** Address the #2-ranked negative finding, OR operational consistency
  - Actions: Secondary improvement areas, support for lagging venues
- **Maintain:** Reinforce the #1-ranked positive finding
  - Actions: Protect, document, share practices that work

### Tier Semantics
- **Critical:** "Standardize X", "Implement X network-wide", "Address systemic X"
- **Secondary:** "Improve X", "Enhance consistency in X", "Support venues on X"
- **Maintain:** "Protect X", "Document X", "Share best practices in X"

### Action Content
Each action should:
- Start with **bold action name** (1-3 words)
- Include 1-2 sentences explaining:
  - What to do (concrete step)
  - Why (tie to the finding and network data)
  - Expected outcome or venue-specific insight

### Venue-Specific Actions
For each venue (or at least outliers), include:
- `venue`: Venue name
- `priority`: "critical", "secondary", or "maintain" (based on that venue's needs)
- `action`: 1-2 sentences of specific guidance for this venue

Venue actions should:
- Reference network context (e.g., "network average is X, you're at Y")
- Acknowledge outlier status (best performer, needs support)
- Suggest specific practices (model after top performer, implement X)
- NOT repeat network-wide action; complement it with venue specificity

### Mechanics
- MUST use inline HTML limited to `<strong>` tags only
- MUST ground every claim in network findings
- MUST NOT compare to other networks
- Network actions: 3-4 per tier
- Venue actions: Include all venues (or at minimum, top 2 and bottom 2)

## Examples

### ✅ Good Multi-Venue Recommendations

**Critical Tier (Network-Wide Action):**
```json
{
  "title": "Standardize Equipment Maintenance Across Network",
  "items": [
    "<strong>Share Grand Prairie's maintenance playbook:</strong> Grand Prairie achieves 18% issue rate vs. network average 28%. Document their daily calibration and maintenance schedule and roll out network-wide.",
    "<strong>Audit El Paso's equipment:</strong> 35% issue rate suggests equipment age, maintenance gaps, or staffing issues. Conduct on-site assessment and develop venue-specific remediation plan.",
    "<strong>Implement daily equipment checks:</strong> Establish network-wide standard for pre-opening equipment verification to catch issues before guests arrive.",
    "<strong>Create equipment maintenance task force:</strong> Assign a lead from Grand Prairie to mentor other venues and track implementation across the network."
  ]
}
```

**Why this works:**
- Title is action-focused (Standardize, not "Equipment Issues")
- References network finding (#1 variance driver)
- Includes best practice sharing (Grand Prairie model)
- Includes support for lagging venue (El Paso audit)
- Actionable steps with network context

---

**Venue-Specific Actions:**
```json
{
  "venue": "Grand Prairie",
  "priority": "maintain",
  "action": "Continue current practices—you're the network leader. Share your equipment maintenance playbook with other venues and mentor El Paso and Austin on daily calibration."
},
{
  "venue": "Austin",
  "priority": "secondary",
  "action": "Adopt Grand Prairie's equipment maintenance schedule to bring your 25% issue rate down to network-leading levels. Implement daily calibration checks and track issues weekly."
},
{
  "venue": "El Paso",
  "priority": "critical",
  "action": "High issue rate (35%) requires urgent attention. Conduct equipment audit to identify root causes (age, maintenance gaps, staffing). Partner with Grand Prairie on maintenance training."
}
```

**Why this works:**
- Each venue gets personalized guidance
- Acknowledges tier/outlier status (leader, lagging)
- References network context (network average, what's possible)
- Suggests specific practices (Grand Prairie model, daily checks)
- Tone matches tier (maintain, secondary, critical)

---

### ❌ What NOT to Do

**Bad: Generic network actions without venue specificity**
```
"All venues should improve equipment reliability and staff responsiveness."
```
**Why this fails:** Vague. What specific actions? Why these areas? No traction.

---

**Bad: Venue actions that repeat network guidance**
```
Venue-specific: "Implement equipment maintenance network-wide"
```
**Why this fails:** That's already in the critical tier. Venue action should be venue-specific (e.g., "adopt Grand Prairie's checklist").

---

**Bad: Confusing tier assignments**
```
Critical: "Improve staff responsiveness" (when staff is already strong)
Maintain: "Fix equipment reliability" (when that's the top negative)
```
**Why this fails:** Tier semantics backwards. Critical should address #1 negative.

---

## Action Format Checklist

For each action, verify:
- [ ] **Bold title:** 1-3 words, action-focused (Standardize, Implement, Share, etc.)
- [ ] **What:** Concrete step (implement X, document Y, audit Z)
- [ ] **Why:** Tied to network finding (e.g., "Grand Prairie achieves 18% vs. network 28%")
- [ ] **Context:** Network average/range cited
- [ ] **Outcome:** Expected result or target (if applicable)
- [ ] **Feasibility:** Something operations can actually do
- [ ] **Length:** 1-2 sentences (not a paragraph)

---

## Venue Assignment Strategy

**Include venue actions for:**
- [ ] Top performer (tier 1-2) - assign priority "maintain"
- [ ] 2nd-ranked venue - assign "maintain" or "secondary" based on findings
- [ ] Any lagging venue (tier 3-4) - assign "critical" or "secondary"
- [ ] Outlier with unique pattern - include even if not top/bottom
- [ ] All venues if network is small (<5 venues)

If network is large (7+ venues), include at minimum:
- Top performer
- Middle performer (one)
- Worst performer
- Any venue with unique pattern/outlier status

---

## Network Actions by Context

### If #1 negative is systemic (all venues affected)
```
Critical: "Address [issue] network-wide"
- Standardize process/workflow
- Implement system-wide fix
- All venues follow same approach
```

### If #1 negative is venue-specific (one or two venues)
```
Critical: "Standardize by learning from leaders"
- Share best-performing venue's practices
- Audit/support lagging venues
- Create peer mentoring
```

### If #1 positive is universal strength
```
Maintain: "Protect and document [strength]"
- Document what's working
- Standardize training/practices
- Ensure knowledge survives turnover
```

---

## Related Skills

- See `multi-venue-impact-drivers-skill.md` for what drives the need for each recommendation
- See `multi-venue-ranking-skill.md` for identifying best performers to model
- See `multi-venue-ups-downs-skill.md` for network patterns that inform recommendations

## Resources

- `README.md` - Integration guide for multi-venue reports
- `synthesis_template.md` - The actual prompt that implements this skill
