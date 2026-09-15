# AI Reporting Tool Skills Overview

This directory contains modular skills that guide the AI-powered report generation pipeline. Each skill defines how a specific section of the report should be written.

## Skills Structure

```
.devin/skills/
├── venue-overview-skill/
│   ├── SKILL.md
│   └── OVERVIEW_METRICS_GUIDANCE.md
├── ups-downs-skill/
│   └── SKILL.md
├── impact-drivers-skill/
│   └── SKILL.md
├── recommendations-skill/
│   └── SKILL.md
└── SKILLS_OVERVIEW.md (this file)
```

## Quick Reference

| Skill | Purpose | Output | Guidance |
|-------|---------|--------|----------|
| **venue-overview-skill** | Narrative summary of venue performance | 2-4 sentence paragraph | Avoid redundant metric numbers; use descriptive language |
| **ups-downs-skill** | Positive and negative findings | 2-3 ups + 2-3 downs | Select from combined ranking; add operational context |
| **impact-drivers-skill** | Top 3 factors affecting performance | 3 drivers with explanations | Follow magnitude ranking strictly; cite numbers |
| **recommendations-skill** | Actionable next steps | 3 tiers × 3-4 actions | Critical/Secondary/Maintain structure; address ranked findings |

## How They Work Together

### The Pipeline

```
CSV Input
    ↓
generate_reports.py
    ↓ (creates venue_data.json)
generate_ai_analysis.py
    ↓
ai_analysis.py (3-stage pipeline)
    ├─ Stage 1: metrics_analysis.md
    ├─ Stage 2: comment_analysis.md
    └─ Stage 3: synthesis.md
         ├─ Uses venue-overview-skill
         ├─ Uses ups-downs-skill
         ├─ Uses impact-drivers-skill
         └─ Uses recommendations-skill
    ↓
ai_analysis_results.json
    ↓
create_html_reports.py / create_markdown_reports.py / create_pdf_reports.py
    ↓
Reports (HTML/Markdown/PDF)
```

### The Combined Ranking

All four skills work from the same **combined ranking** of metrics + comment themes, sorted by magnitude:

```
1. LTR (positive, 82)
2. Equipment reliability (negative, 71)
3. Staff responsiveness (positive, 65)
4. Food service speed (negative, 45)
5. Game selection (positive, 38)
...
```

**Each skill uses this ranking differently:**

| Skill | Uses | How |
|-------|------|-----|
| **overview** | Top findings | Explains why #1-3 matter; tells the story |
| **ups/downs** | Top 2-3 of each polarity | Selects notable positive/negative findings |
| **impact** | Top 3 (any polarity) | Explains why these 3 are most impactful |
| **recommendations** | #1 and #2 negatives + #1 positive | Generates actions for critical/secondary/maintain |

## Skill Details

### 1. Venue Overview Skill

**File:** `venue-overview-skill/SKILL.md`

**Purpose:** Write a compelling 2-4 sentence narrative that tells the story of what's happening at the venue.

**Key Rule:** Avoid redundantly repeating metric numbers that are already in the Performance Summary cards. Use descriptive language like "over half", "most guests", "frequently" instead.

**Example:**
```
"This venue is performing well overall, driven by strong satisfaction 
with the experience. However, equipment reliability issues - particularly 
screen tracking failures - are creating friction that's preventing the 
entertainment experience from reaching its potential."
```

**Related:** See `OVERVIEW_METRICS_GUIDANCE.md` for detailed metrics handling guidance.

---

### 2. Ups/Downs Skill

**File:** `ups-downs-skill/SKILL.md`

**Purpose:** Identify 2-3 positive findings (ups) and 2-3 negative findings (downs) from the combined ranking.

**Key Rule:** Don't limit to only the top 3 from impact. Include lower-magnitude items if they add distinct operational value or context.

**Example:**
```json
{
  "ups": [
    "<strong>Strong recommendation intent:</strong> 87% of guests would recommend the venue.",
    "<strong>Responsive staff:</strong> Guests praised staff for quickly resolving issues.",
    "<strong>Game selection:</strong> Multiple guests enjoyed the variety of games available."
  ],
  "downs": [
    "<strong>Equipment reliability:</strong> Screen tracking failures mentioned in 14 comments.",
    "<strong>Food service speed:</strong> Multiple guests noted slow food delivery times."
  ]
}
```

---

### 3. Impact Drivers Skill

**File:** `impact-drivers-skill/SKILL.md`

**Purpose:** Explain the top 3 entries from the combined ranking that have the most impact on venue performance.

**Key Rule:** Follow the magnitude ranking strictly. Don't skip or reorder entries. Include both positive and negative drivers.

**Example:**
```json
{
  "impact": [
    {
      "title": "Recommendation Intent",
      "description": "87% LTR indicates strong overall satisfaction and loyalty, the primary driver of venue performance."
    },
    {
      "title": "Equipment Reliability",
      "description": "Screen tracking failures mentioned in 14 comments are the most significant operational issue."
    },
    {
      "title": "Staff Responsiveness",
      "description": "Quick problem resolution is valued by guests, with 8 specifically praising staff responsiveness."
    }
  ]
}
```

---

### 4. Recommendations Skill

**File:** `recommendations-skill/SKILL.md`

**Purpose:** Generate actionable recommendations organized into three tiers: critical, secondary, and maintain.

**Key Rule:** Follow the combined ranking priority order. Critical addresses #1 negative, secondary addresses #2 negative, maintain reinforces #1 positive.

**Example:**
```json
{
  "recommendations": {
    "critical": {
      "title": "Fix Equipment Reliability",
      "items": [
        "<strong>Preventive maintenance:</strong> Daily screen calibration checks before peak hours.",
        "<strong>Rapid response:</strong> Ensure staff can resolve issues within 2 minutes.",
        "<strong>Root cause analysis:</strong> Investigate hardware, software, or calibration issues.",
        "<strong>Guest communication:</strong> Proactively inform guests of issues and resolution time."
      ]
    },
    "secondary": {
      "title": "Improve Food Service Speed",
      "items": [
        "<strong>Kitchen optimization:</strong> Review order flow during peak hours.",
        "<strong>Queue system:</strong> Implement visible queue so guests know wait time.",
        "<strong>Staff training:</strong> Emphasize speed during peak hours.",
        "<strong>Menu simplification:</strong> Consider reducing complexity during peaks."
      ]
    },
    "maintain": {
      "title": "Protect Recommendation Intent",
      "items": [
        "<strong>Satisfaction tracking:</strong> Continue monitoring LTR scores.",
        "<strong>Staff recognition:</strong> Reward responsive staff behaviors.",
        "<strong>Experience consistency:</strong> Protect overall quality.",
        "<strong>Feedback loop:</strong> Share positive feedback with staff."
      ]
    }
  }
}
```

---

## How to Use These Skills

### For Report Generation (Automatic)

The skills are automatically used by the AI analysis pipeline:

```bash
cd python
python generate_all_reports.py ../example-data/your_file.csv
```

The `ai_analysis.py` script loads `.claude/single-venue-report/synthesis.md`, which references all four skills.

### For Tuning/Editing

To change how a section is written, edit the corresponding skill:

1. **Want different overview tone?** → Edit `venue-overview-skill/SKILL.md`
2. **Want different ups/downs selection?** → Edit `ups-downs-skill/SKILL.md`
3. **Want different impact explanation?** → Edit `impact-drivers-skill/SKILL.md`
4. **Want different recommendations structure?** → Edit `recommendations-skill/SKILL.md`

Then clear the AI analysis cache to regenerate:

```bash
cd python
python ai_analysis.py --clear-cache
python generate_ai_analysis.py venue_data.json
```

### For Understanding the Output

Each skill includes:
- **Purpose** - What this section does
- **Input** - What data it receives
- **Output** - What it produces
- **Rules** - Hard requirements
- **Examples** - Real output samples
- **Strategy** - How to approach the task

---

## Key Concepts

### Combined Ranking

All skills work from a single merged ranking of metrics + comment themes, sorted by magnitude (highest first). This ensures:
- ✅ Consistent prioritization across all sections
- ✅ No conflicting findings
- ✅ Data-driven recommendations

### Magnitude Score

Each entry in the combined ranking has a magnitude (0-100) representing how much it affects overall guest satisfaction:
- **High magnitude (70+)** = affects many guests or affects them strongly
- **Medium magnitude (40-69)** = notable but not dominant
- **Low magnitude (<40)** = minor concern

### Polarity

Each entry is either:
- **Positive** (something working well)
- **Negative** (something that needs fixing)

### Traceability

Every claim in the report must be traceable back to either:
- A metric (with a number)
- A comment theme (with mention count)

No invented or untraced claims.

---

## Related Documentation

- `AGENTS.md` - Overall project workflow
- `.claude/single-venue-report/synthesis.md` - The actual AI prompt that uses these skills
- `ASSESSMENT_DESIGN_RATIONALE.md` - Why the Overall Assessment is rule-based (not AI-generated)
- `COMPARISON_ASSESSMENT_APPROACHES.md` - Comparison of rule-based vs AI-generated approaches

---

## Questions?

Each skill file includes detailed guidance, examples, and strategy sections. Start with the skill you want to understand, then reference the related documentation.
