# Claude Single-Venue Report Analysis

This directory contains the AI analysis pipeline for generating venue reports. It consists of three stages that work together to produce comprehensive, data-driven insights.

## Directory Contents

### Core Pipeline Files

1. **metrics_analysis.md** (Stage 1)
   - Analyzes 5 aggregate metrics (LTR, Fun, Helpfulness, Issues, Resolution)
   - Produces a characterization of what the numbers say together
   - Flags each metric with a magnitude score (0-100)
   - Input: Raw metrics from survey data
   - Output: Characterization + metric_flags

2. **comment_analysis.md** (Stage 2)
   - Analyzes 100+ guest comments
   - Identifies themes (positive and negative)
   - Assigns magnitude scores to each theme
   - Input: Guest comments + metric_flags from Stage 1
   - Output: Themes with magnitude and summary

3. **synthesis.md** (Stage 3)
   - Merges metric flags + comment themes into a combined ranking
   - Produces final report sections: overview, ups/downs, impact, recommendations
   - Uses four modular skill guides (see below)
   - Input: metrics_analysis output + comment_analysis output
   - Output: Complete analysis (overview/ups/downs/impact/recommendations)

### Synthesis Skill Guides

These files guide how each section of the synthesis output should be written:

4. **venue-overview-skill.md**
   - Purpose: Write 2-4 sentence narrative summary
   - Key Rule: Avoid redundant metric numbers; use descriptive language
   - Output: Narrative paragraph explaining what's happening at the venue
   - See also: `overview-metrics-guidance.md` for detailed metrics handling

5. **ups-downs-skill.md**
   - Purpose: Identify 2-3 positive and 2-3 negative findings
   - Key Rule: Don't limit to top 3; include lower-magnitude items with distinct value
   - Output: 2-3 ups + 2-3 downs with explanations

6. **impact-drivers-skill.md**
   - Purpose: Explain the top 3 factors affecting performance
   - Key Rule: Follow magnitude ranking strictly; cite numbers
   - Output: 3 drivers with 1-2 sentence explanations

7. **recommendations-skill.md**
   - Purpose: Generate actionable next steps
   - Key Rule: Critical addresses #1 negative, Secondary addresses #2 negative, Maintain reinforces #1 positive
   - Output: 3 tiers × 3-4 actions each

### Supporting Documentation

8. **overview-metrics-guidance.md**
   - Detailed guidance on how to handle metrics in the overview narrative
   - Explains what metric numbers to avoid (redundancy)
   - Explains what descriptive language to use instead
   - Examples of good vs bad overview text

---

## How They Work Together

### The Combined Ranking

All skills work from the same **combined ranking** of metrics + comment themes, sorted by magnitude (highest first):

```
1. LTR (positive, 82)
2. Equipment reliability (negative, 71)
3. Staff responsiveness (positive, 65)
4. Food service speed (negative, 45)
5. Game selection (positive, 38)
...
```

### Each Skill Uses the Ranking Differently

| Skill | Uses | How |
|-------|------|-----|
| **overview** | Top findings | Explains why #1-3 matter; tells the story |
| **ups/downs** | Top 2-3 of each polarity | Selects notable positive/negative findings |
| **impact** | Top 3 (any polarity) | Explains why these 3 are most impactful |
| **recommendations** | #1 and #2 negatives + #1 positive | Generates actions for critical/secondary/maintain |

---

## Pipeline Flow

```
CSV Survey Data
    ↓
generate_venue_data.py (Python)
    ↓ (creates venue_data.json)
run_analyze_venues.py (Python)
    ↓
analyze_venues.py (Python) loads this directory
    ├─ Stage 1: Loads metrics_analysis.md
    │           Calls Claude with metrics payload
    │           Gets: characterization + metric_flags
    │
    ├─ Stage 2: Loads comment_analysis.md
    │           Calls Claude with comments + metric_flags
    │           Gets: themes with magnitude
    │
    └─ Stage 3: Loads synthesis.md
               Loads all four skill guides (venue-overview-skill.md, etc.)
               Calls Claude with combined ranking
               Gets: overview/ups/downs/impact/recommendations
    ↓
ai_analysis_results.json (cached)
    ↓
create_single_venue_snapshot_report.py (Python)
    ↓
Reports (HTML/Markdown/PDF)
```

---

## Key Concepts

### Magnitude (0-100)

Each entry in the combined ranking has a magnitude representing how much it affects guest satisfaction:

- **70+**: High impact (affects many guests or affects them strongly)
- **40-69**: Medium impact (notable but not dominant)
- **<40**: Low impact (minor concern)

### Polarity

Each entry is either:
- **Positive**: Something working well
- **Negative**: Something that needs fixing

### Traceability

Every claim in the report must be traceable back to either:
- A metric (with a number)
- A comment theme (with mention count)

No invented or untraced claims.

---

## How to Use These Files

### For Understanding the Pipeline

1. Read this README (you are here)
2. Read `metrics_analysis.md` to understand Stage 1
3. Read `comment_analysis.md` to understand Stage 2
4. Read `synthesis.md` to understand Stage 3
5. Read the skill guides to understand how each section is written

### For Tuning/Customizing Output

To change how a section is written:

1. **Want different overview tone?** → Edit `venue-overview-skill.md`
2. **Want different ups/downs selection?** → Edit `ups-downs-skill.md`
3. **Want different impact explanation?** → Edit `impact-drivers-skill.md`
4. **Want different recommendations structure?** → Edit `recommendations-skill.md`

Then clear the cache and regenerate:

```bash
cd python
python ai_analysis.py --clear-cache
python generate_ai_analysis.py venue_data.json
```

### For Developers

The Python code (`ai_analysis.py`) loads these files as follows:

```python
# Stage 1
METRICS_ANALYSIS_SKILL = _load_skill('metrics_analysis.md')
result1, error = _run_stage('metrics_analysis', METRICS_ANALYSIS_SKILL, payload1, ...)

# Stage 2
COMMENT_ANALYSIS_SKILL = _load_skill('comment_analysis.md')
result2, error = _run_stage('comment_analysis', COMMENT_ANALYSIS_SKILL, payload2, ...)

# Stage 3
SYNTHESIS_SKILL = _load_skill('synthesis.md')
result3, error = _run_stage('synthesis', SYNTHESIS_SKILL, payload3, ...)
```

Each stage is cached independently, so editing one skill only invalidates that stage's cache.

---

## Quick Reference

### What Each File Does

| File | Stage | Purpose | Input | Output |
|------|-------|---------|-------|--------|
| metrics_analysis.md | 1 | Analyze metrics | Raw metrics | Characterization + flags |
| comment_analysis.md | 2 | Analyze comments | Comments + flags | Themes with magnitude |
| synthesis.md | 3 | Synthesize findings | Metrics + comments | Overview/ups/downs/impact/recommendations |
| venue-overview-skill.md | 3 | Guide overview writing | Combined ranking | Narrative paragraph |
| ups-downs-skill.md | 3 | Guide findings selection | Combined ranking | 2-3 ups + 2-3 downs |
| impact-drivers-skill.md | 3 | Guide impact explanation | Combined ranking | Top 3 drivers |
| recommendations-skill.md | 3 | Guide action generation | Combined ranking | 3 tiers × 3-4 actions |
| overview-metrics-guidance.md | Reference | Detailed metrics guidance | N/A | Examples and rules |

### Common Tasks

**I want to change how the overview sounds**
→ Edit `venue-overview-skill.md`

**I want to change which ups/downs are selected**
→ Edit `ups-downs-skill.md`

**I want to change the impact explanation style**
→ Edit `impact-drivers-skill.md`

**I want to change the recommendations structure**
→ Edit `recommendations-skill.md`

**I want to understand the whole system**
→ Read this README, then read `synthesis.md`

**I want to see examples of good output**
→ Look at the Examples section in each skill file

**I want to understand the strategy**
→ Look at the Strategy section in each skill file

---

## Architecture Notes

### Why Three Stages?

The previous version sent one giant prompt asking Claude to read every comment, reconcile it with all 5 metrics, and produce the entire report in a single turn. That's a lot of reasoning and a large structured output in one shot, causing timeouts with non-trivial comment counts.

Splitting into 3 focused stages means:
- ✅ Each call does much less work
- ✅ Each stage is separately cacheable
- ✅ Can be tested/timed independently
- ⚠️ Trade-off: 3 subprocess round-trips instead of 1

### Why Modular Skills?

The synthesis stage produces four different sections (overview/ups/downs/impact/recommendations). Rather than embedding all guidance in one monolithic prompt, we split it into four modular skill guides:

- ✅ Each skill is independently editable
- ✅ Clear separation of concerns
- ✅ Can be reused in other contexts
- ✅ Easier to understand and maintain
- ⚠️ Trade-off: More files to manage

### Caching Strategy

Each stage is cached independently, keyed on:
- The stage's guideline doc (e.g., `metrics_analysis.md`)
- That stage's input payload

This means:
- ✅ Re-running report generation for unchanged data is instant
- ✅ Editing one stage's guideline only invalidates that stage's cache
- ✅ Metrics and comments are reused if unchanged
- ⚠️ Cache can grow large over time (use `--clear-cache` to reset)

---

## Related Documentation

- `AGENTS.md` - Project structure and workflow overview
- `README.md` - Quick start and installation guide
- `python/ai_analysis.py` - Python implementation of the pipeline
