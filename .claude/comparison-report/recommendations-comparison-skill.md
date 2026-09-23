# Recommendations Comparison Skill

Generate actionable next steps organized into three tiers: `critical` (sustain improvements), `secondary` (address declines), and `maintain` (protect strengths), each with 3-4 concrete actions tied to the top changes.

## Purpose

Recommendations for comparison reports differ from snapshot reports: instead of "fix the #1 problem", the focus is "sustain momentum on what's improving and address emerging issues before they become critical".

Actions should:
- **Critical:** Sustain and amplify the #1 change (biggest improvement or decline)
- **Secondary:** Address the #2 change or manage operational consistency
- **Maintain:** Protect the #1 strength to avoid regression
- All actions reference the baseline period to give context

## Input

- `metrics_analysis.current` & `.previous`: Metric flags and characterizations
- `comment_analysis.current` & `.previous`: Themes with counts and summaries
- `combined_ranking`: All findings ranked by change magnitude

## Output

Three recommendation tiers in this structure:

```json
{
  "recommendations": {
    "critical": {
      "title": "Short priority name",
      "items": [
        "<strong>Action name:</strong> 1-2 sentence description",
        ...
      ]
    },
    "secondary": {
      "title": "Short priority name",
      "items": [...]
    },
    "maintain": {
      "title": "Short priority name",
      "items": [...]
    }
  }
}
```

## Rules

### Tier Selection (Critical)
- **Critical:** Address the #1 change from combined ranking
  - If #1 is a **positive change** (improvement): "Sustain" the improvement
  - If #1 is a **negative change** (decline): "Address" the decline
  - Actions focus on maintaining momentum or stopping deterioration
  
- **Secondary:** Address the #2 change, OR focus on operational consistency if only one tier has changes
  - If improvements dominate: secondary addresses prevention of new issues
  - If declines dominate: secondary addresses secondary issues
  - If mixed: secondary handles the second-ranked item
  
- **Maintain:** Reinforce the #1 strength (a strong metric or loved theme)
  - Something worth protecting, not fixing
  - Actions preserve what's working and prevent regression
  - Should NOT be the same as critical action (can have secondary strength to maintain if critical is negative)

### Tier Naming
- **Critical tier name:** 
  - "Sustain [improvement name]" (if improvement) ← e.g., "Sustain Equipment Reliability Improvements"
  - "Address [decline name]" (if decline) ← e.g., "Address F&B Service Speed Decline"
- **Secondary tier name:**
  - Depends on context (prevent, improve, address consistency)
- **Maintain tier name:**
  - "Protect [strength name]" ← e.g., "Protect Staff Responsiveness"

### Action Content
Each action should:
- Start with a **bold action name** (1-3 words)
- Include 1-2 sentences explaining:
  - What to do (concrete step)
  - Why (tie back to the change and baseline)
  - Expected outcome or metric target
- Reference baseline period: "was X in Q1, now Y in Q2, target..."

### Action Count
- MUST include 3-4 concrete action items per section
- Actions MUST be operationally feasible
- Actions MUST be directly traceable to a ranked finding
- Actions MAY reference specific details from comment themes

### Mechanics
- MUST use inline HTML limited to `<strong>` tags only
- MUST ground every claim in a number or stated theme from input
- MUST NOT compare to other venues or network

## Examples

### ✅ Good Recommendations Examples

**Critical: Sustain Equipment Reliability Improvements**
```json
{
  "title": "Sustain Equipment Reliability Improvements",
  "items": [
    "<strong>Maintain daily calibration schedule:</strong> The 0.8-point improvement came from implementing daily screen checks. Continue this regimen daily to prevent regression—the baseline of 14 issues shows what happens without maintenance.",
    "<strong>Document and standardize the fix process:</strong> Capture exactly what worked (staff training, calibration steps, tools used) so the improvement can be replicated if issues resurface.",
    "<strong>Monitor weekly for early warning signs:</strong> Track screen failures weekly to catch any uptick early. Target: keep issues below 8 mentions per period (current level).",
    "<strong>Celebrate with staff:</strong> Acknowledge the team for the 43% reduction in complaints. This improvement was achieved through operational discipline and staff effort."
  ]
}
```

**Why this works:**
- Title shows sustaining momentum (Sustain, not Fix)
- Each action directly addresses what drove the improvement
- References baseline (14 issues) to show what's being protected
- Includes team recognition (important for sustainability)
- Actions are concrete and operationally feasible

---

**Critical: Address F&B Service Speed Decline**
```json
{
  "title": "Address F&B Service Speed Decline",
  "items": [
    "<strong>Investigate root cause immediately:</strong> Wait times increased from 8 to 12 minutes (50% slower). Determine whether this is staffing, menu complexity, volume increases, or workflow inefficiency. Root cause dictates the fix.",
    "<strong>Implement targeted fix based on root cause:</strong> If staffing: add hours during peak times. If menu: test simplified offerings. If workflow: audit point-of-service process. Target: return to 8-minute baseline within 30 days.",
    "<strong>Set guest-facing communication:</strong> If F&B wait times will improve, communicate expected wait times at order time so guests can manage expectations.",
    "<strong>Monitor daily for regression:</strong> Unlike equipment issues (which impact game play directly), F&B speed can drift silently. Track daily and trend weekly to catch any further slippage."
  ]
}
```

**Why this works:**
- Title shows addressing a decline (Address, not Prevent)
- Action #1 focuses on root cause (50% slower is significant)
- Includes multiple scenario responses (staffing, menu, workflow)
- References baseline (8 minutes) as target to return to
- Includes guest communication (operationally practical)
- Recognizes the decline is trending wrong and needs monitoring

---

**Maintain: Protect Staff Responsiveness**
```json
{
  "title": "Protect Staff Responsiveness",
  "items": [
    "<strong>Document staff training practices:</strong> Staff responsiveness remained strong (8 positive mentions in both periods). Capture what's working in the training program and knowledge base so it's not lost to turnover.",
    "<strong>Share best practices network-wide:</strong> Staff are consistently fixing issues within 2 minutes (from comments). Document this process and ensure all team members know the standard.",
    "<strong>Recognize and reward staff:</strong> 8 guests specifically praised staff for rapid problem resolution. Public recognition (e.g., employee of the month, bonus, team huddles) keeps morale and performance high.",
    "<strong>Monitor for burnout:</strong> Staff handling frequent issues (8 mentions) need support. Ensure workload is manageable and provide breaks/support so responsiveness doesn't decline from fatigue."
  ]
}
```

**Why this works:**
- Title shows protecting strength (Protect, not Improve)
- Focuses on sustaining excellence, not fixing weakness
- Addresses knowledge preservation (training, best practices)
- Includes non-monetary recognition (important for retention)
- Acknowledges staff load (burnout prevention)

---

### Context: Mixed Scenarios

**When improvements dominate (#1 and #2 are both positive):**
```
- Critical: Sustain #1 improvement
- Secondary: Sustain #2 improvement
- Maintain: Protect strength from #1 metric flag (avoid regression while improving themes)
```

**When declines dominate (#1 and #2 are both negative):**
```
- Critical: Address #1 decline
- Secondary: Address #2 decline
- Maintain: Protect the #1 positive strength (something still working well)
```

**When mixed (#1 is improvement, #2 is decline):**
```
- Critical: Sustain #1 improvement (build on momentum)
- Secondary: Address #2 decline (prevent it from spiraling)
- Maintain: Protect the strength that remained stable
```

---

### ❌ What NOT to Do

**Bad: Generic actions with no tie to changes**
```
"<strong>Improve operations:</strong> Focus on making things better."
```
**Why this fails:** No specificity. What operation? Why this action? Based on what data?

---

**Bad: Confusing critical and maintain tiers**
```
Critical: "Fix staff responsiveness" ← But staff improved!
Maintain: "Keep equipment working" ← But equipment is new problem!
```
**Why this fails:** Tier semantics are backwards. Critical should sustain the improvement (staff), maintain should protect what's working (something else positive).

---

**Bad: Missing baseline reference**
```
"<strong>Reduce wait times:</strong> Work to speed up F&B service."
```
**Why this fails:** No baseline ("from X to Y") and no target. How much faster? Based on what data?

---

**Bad: Too general or aspirational**
```
"<strong>Enhance guest experience:</strong> Make all aspects of the venue better."
```
**Why this fails:** Not tied to a specific change. Not operationally feasible. No metrics.

---

## Action Writing Checklist

For each action, verify:
- [ ] **Bold title:** 1-3 words, action-focused (Verb + Noun)
- [ ] **What:** Clear specific action (implement X, document Y, monitor Z)
- [ ] **Why:** Tied to the change (e.g., "the 0.8-point improvement came from...")
- [ ] **Baseline:** References previous period (e.g., "was X in Q1")
- [ ] **Target:** Specifies goal or metric (e.g., "target X by month-end")
- [ ] **Feasibility:** Something operations can actually do
- [ ] **Length:** 1-2 sentences (not a paragraph)

---

## Critical Tier Semantics

- **For improvements:** Use "Sustain", "Maintain momentum", "Protect gains", "Build on success"
- **For declines:** Use "Address", "Reverse", "Stop deterioration", "Prevent regression"
- **For stability:** Less common in critical tier, but if #1 change is stable and high-value: "Maintain consistency of [strong item]"

---

## Related Skills

- See `impact-drivers-comparison-skill.md` for understanding which changes rank #1/#2
- See `venue-overview-comparison-skill.md` for overall trajectory framing
- See `ups-downs-comparison-skill.md` for broader findings beyond top 3

## Resources

- `README.md` - Integration guide for comparison reports
- `synthesis_template.md` - The actual prompt that implements this skill
