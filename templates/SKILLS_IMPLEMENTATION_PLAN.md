# Skills Implementation Plan: Multi-Venue & Comparison Reports

**Date:** 2026-09-21  
**Status:** Planning Phase  
**Objective:** Create new Claude skills for comparison and multi-venue report analysis

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current State](#current-state)
3. [Architecture Decisions](#architecture-decisions) (incl. Decision 5: synthesis composition mechanism)
4. [Detailed Implementation Plan](#detailed-implementation-plan)
5. [Phase 1: Comparison Report Skills](#phase-1-comparison-report-skills)
6. [Phase 2: Multi-Venue Report Skills](#phase-2-multi-venue-report-skills)
7. [Phase 2b: Multi-Venue Comparison Skills](#phase-2b-multi-venue-comparison-skills)
8. [Phase 3: Python Integration](#phase-3-python-integration)
9. [File Creation Checklist](#file-creation-checklist)
10. [Key Design Decisions](#key-design-decisions)
11. [Open Questions & Answers](#open-questions--answers)
12. [Success Criteria](#success-criteria)
13. [Next Steps](#next-steps)

---

## Executive Summary

The current AI analysis pipeline supports **single-venue snapshot reports** using skills in `.claude/single-venue-report/`. We need to extend this to support:

1. **Single-venue comparison reports** (two periods)
2. **Multi-venue snapshot reports** (all venues, one period)
3. **Multi-venue comparison reports** (all venues, two periods)

**Approach:**
- Create new skill directories alongside existing `.claude/single-venue-report/` (flat siblings, not nested - see Decision 2)
- Reuse Stages 1-2 (metrics + comment analysis) where possible; run them twice (once per period) for comparison report types
- Convert `synthesis.md` into a `synthesis_template.md` with placeholders, and compose the actual Stage 3 prompt at runtime from the template + the relevant variant's section-skill files (see Decision 5) - this is a **necessary mechanism change**, not just new files, since today the four section-skill files (`venue-overview-skill.md` etc.) aren't actually loaded by any Python code
- Fully rewrite all section skills for both comparison variants (single-venue and multi-venue), not just add one "context" file for multi-venue
- Update Python routing logic to load correct skills by report type, and fix two report builders that currently silently skip AI analysis for the previous period / multi-venue data entirely

**Effort:** ~20 new skill files + 2 synthesis templates + Python integration updates across 5 files
**Timeline:** Can be done in 2-3 focused sessions
**Risk:** Low-medium (backward compatible by design, but the template-extraction step changes the literal prompt text sent to Claude for existing snapshot reports and needs a regression check)

---

## Current State

### Existing Architecture

```
.claude/single-venue-report/
├── metrics_analysis.md          (Stage 1: Analyze metrics)
├── comment_analysis.md          (Stage 2: Analyze comments)
├── synthesis.md                 (Stage 3: Merge + synthesize)
│
├── venue-overview-skill.md      (Skill: Write overview)
├── ups-downs-skill.md           (Skill: Select ups/downs)
├── impact-drivers-skill.md      (Skill: Rank top 3 drivers)
├── recommendations-skill.md     (Skill: Generate actions)
│
├── overview-metrics-guidance.md (Reference: Metrics handling)
└── README.md                    (Architecture guide)
```

### Python Pipeline

```
analyze_venues.py
├── SKILLS_DIR = '.../single-venue-report'  (hardcoded)
├── get_ai_analysis()                        (Single-venue only)
└── get_period_ai_analysis()                 (NOT YET IMPLEMENTED - placeholder)

report_content.py
└── get_analysis()                           (Fetches analysis, formats for templates)
```

### Hardcoded References

- `python/analyze_venues.py` line 78: `SKILLS_DIR = '.../single-venue-report'`
- `python/evals/*.py` (3 files): Comments reference `.claude/single-venue-report/`
- `README.md` (13 references)
- `AGENTS.md` (6 references)
- `.claude/single-venue-report/synthesis.md` (4 self-references)

**Total:** 26+ hardcoded references

---

## Architecture Decisions

### Decision 1: Skill Variants vs. New Skills

**Question:** Should we create separate skill files for each variant, or use parameterized skills?

**Decision:** **Separate skill files** (one per variant)

**Rationale:**
- Each variant has distinct rules and examples
- Easier to maintain and debug
- Claude can focus on one context at a time
- Skill files are lightweight (no performance cost)
- Mirrors the existing modular approach

### Decision 2: Directory Organization

**Question:** Should we rename `single-venue-report/` or create new directories, and should comparison variants live nested inside their base family or as flat siblings?

**Decision:** **Keep `single-venue-report/` and `multi-venue-report/` as the two base families (one per axis-A variant: single-venue vs. multi-venue). Comparison variants are flat sibling folders alongside them** (`comparison-report/` for single-venue, `multi-venue-comparison-report/` for multi-venue) rather than nested subdirectories.

**Rationale:**
- The variation across the 4 report types is genuinely two-dimensional:
  - **Axis A (single-venue vs. multi-venue)** changes Stage 1/2 payload shape and aggregation logic entirely, and changes Stage 3's output envelope (multi-venue adds `venue_ranking` / `venue_specific` fields).
  - **Axis B (snapshot vs. comparison)** only changes *framing* in Stage 3's section skills (absolute vs. delta language) - it doesn't change Stage 1/2's payload shape or Stage 3's output envelope.
- Because of that, a "one folder per report type" (4 folders) layout would duplicate Stage 1, Stage 2, and the synthesis template twice per axis-A family, which contradicts Decision 3's reuse goal and creates a hand-sync burden.
- Flat siblings (rather than nesting `comparison/` inside each base folder) keep the Python loader's path-joining a single `os.path.join('.claude', variant_dir, filename)` with no extra nesting logic, and keep folder names unique and `grep`/glob-friendly for anyone (human or agent) navigating to "the multi-venue comparison overview skill" - runtime skill loading is unaffected either way since Claude never browses the directory itself; Python always loads specific file paths and composes them into the prompt text before Claude ever sees it (see Decision 5).
- Zero breaking changes to existing code; existing eval scripts continue to work
- Backward compatible

**Final directory structure:**

```
.claude/
├── single-venue-report/            (Existing base family: snapshot)
├── comparison-report/              (Overlay: single-venue comparison - full rewrite of all 4 section skills)
├── multi-venue-report/             (NEW base family: multi-venue snapshot)
└── multi-venue-comparison-report/  (Overlay: multi-venue comparison - full rewrite of all 5 section skills)
```

**Cost:** ~5 minutes (just add routing logic to `analyze_venues.py`)

### Decision 3: Stage 1 & 2 Reuse

**Question:** Should multi-venue reports reuse existing metrics/comment analysis or create new ones?

**Decision:** **Create new Stage 1 & 2 for multi-venue** (reuse for single-venue comparison)

**Rationale:**
- Single-venue snapshot/comparison: reuse existing `metrics_analysis.md` + `comment_analysis.md` (same per-venue input format)
- Multi-venue snapshot/comparison: create new `metrics_analysis.md` + `comment_analysis.md` (different aggregation logic), shared by both multi-venue variants
- Aggregation logic is fundamentally different from single-venue analysis
- Cleaner separation of concerns
- **Comparison-specific nuance:** for both single-venue and multi-venue comparison reports, Stage 1 and Stage 2 must be run **twice** - once for the current period and once for the previous period - since the comparison synthesis stage needs both periods' `metrics_analysis`/`comment_analysis` output to compute deltas. This is a real gap in the current implementation: `create_single_venue_comparison_report.py` today only runs the pipeline once, on `current_data`, and never analyzes the previous period at all, despite its docstring claiming "AI analysis with comparison context." Phase 1 and Phase 3 must fix this, not just add new skill files.

### Decision 4: Backward Compatibility

**Question:** Should existing snapshot reports continue to work unchanged?

**Decision:** **Yes, 100% backward compatible**

**Implementation:**
- Existing single-venue snapshot reports continue to work unchanged
- Existing `get_ai_analysis()` defaults to snapshot behavior
- New report types opt-in to new skills via `report_type` parameter
- No changes to the *content* of existing section-skill files (they become the default "snapshot" composition inputs - see Decision 5)

### Decision 5: Synthesis Composition Mechanism (runtime template + section skills)

**Question:** How do the four (or five) per-section skill files (`venue-overview-skill.md`, `ups-downs-skill.md`, etc.) actually influence the Stage 3 output?

**Important finding:** As of today, they don't. `analyze_venues.py` only loads three files into the prompt sent to Claude - `metrics_analysis.md`, `comment_analysis.md`, and `synthesis.md` - via `_load_skill()`. The four per-section skill files are **never read by any Python code** (verified by grepping `python/` for their filenames - zero matches). `synthesis.md` is fully self-contained: it already embeds all four sections' rules inline (see its "## Overview Section", "## Impact Section", etc. headings), and its "Related Skills" footer referencing the four files is documentation for human maintainers only, not a runtime dependency.

This matters because the original plan assumed these files were swappable inputs to the pipeline - they aren't, yet. Simply adding `comparison-report/venue-overview-comparison-skill.md` etc. would have **zero effect on generated output** without also wiring up a composition mechanism.

**Decision:** Convert `synthesis.md` into a **template with placeholders**, and compose the actual Stage 3 prompt at runtime from the template plus the relevant variant's section-skill files, before hashing for the cache key.

**Implementation:**
- Rename/restructure `single-venue-report/synthesis.md` into `single-venue-report/synthesis_template.md`: keep only the genuinely shared parts (Purpose, Inputs, Context, Workflow, the master Output JSON envelope, and cross-cutting rules like Combined Ranking and Formatting/traceability), with placeholder markers where the four per-section rule blocks currently sit inline, e.g. `<!-- SKILL:venue-overview -->`, `<!-- SKILL:ups-downs -->`, `<!-- SKILL:impact-drivers -->`, `<!-- SKILL:recommendations -->`.
- The existing four section-skill files become the literal text substituted into those placeholders - no content changes needed for the snapshot variant; they already contain the right Purpose/Rules/Output shape per section.
- `analyze_venues.py` composes the final `synthesis` skill text at runtime:
  ```python
  SECTION_SKILLS = ["venue-overview", "ups-downs", "impact-drivers", "recommendations"]

  def _compose_synthesis_skill(report_type):
      template = _load_skill("single-venue-report/synthesis_template.md")
      variant_dir, suffix = {
          "snapshot": ("single-venue-report", "-skill.md"),
          "comparison": ("comparison-report", "-comparison-skill.md"),
      }[report_type]
      for name in SECTION_SKILLS:
          section_text = _load_skill_variant(variant_dir, f"{name}{suffix}")
          template = template.replace(f"<!-- SKILL:{name} -->", section_text)
      return template
  ```
- The composed string is what's passed into `_run_stage("synthesis", composed_skill, payload, ...)`. `_stage_cache_key` already hashes `skill_text + payload`, so caching keeps working unchanged - editing any one section-skill file naturally changes the composed text and busts only that cache entry.
- Multi-venue needs its **own** template (`multi-venue-report/synthesis_template.md`), not a shared one, because its Output envelope genuinely differs (adds `venue_ranking`, `venue_specific` recommendations) - it isn't just a framing change.
- **Migration check:** for `report_type='snapshot'`, composing `synthesis_template.md` + the existing (unchanged) four skill files should produce a prompt equivalent in substance to today's monolithic `synthesis.md`. Diff the two prompt strings once during migration and re-run a known venue through the pipeline to confirm the output validator still passes and quality doesn't regress, since the literal text sent to Claude does change even though intent doesn't.

---

## Detailed Implementation Plan

### Directory Structure (Final State)

```
.claude/
├── single-venue-report/            (Base family: Stage 1/2/template + snapshot's 4 section skills)
│   ├── metrics_analysis.md
│   ├── comment_analysis.md
│   ├── synthesis_template.md       (RENAMED from synthesis.md - now a template with placeholders, see Decision 5)
│   ├── venue-overview-skill.md
│   ├── ups-downs-skill.md
│   ├── impact-drivers-skill.md
│   ├── recommendations-skill.md
│   ├── overview-metrics-guidance.md
│   └── README.md
│
├── comparison-report/              (Overlay: single-venue comparison - full rewrite, all 4 section skills)
│   ├── venue-overview-comparison-skill.md
│   ├── ups-downs-comparison-skill.md
│   ├── impact-drivers-comparison-skill.md
│   ├── recommendations-comparison-skill.md
│   └── README.md
│
├── multi-venue-report/             (NEW base family: Stage 1/2/template + multi-snapshot's 5 section skills)
│   ├── metrics_analysis.md         (NEW: aggregated metrics)
│   ├── comment_analysis.md         (NEW: aggregated comments)
│   ├── synthesis_template.md       (NEW: multi-venue synthesis template with placeholders)
│   ├── multi-venue-overview-skill.md
│   ├── multi-venue-ranking-skill.md
│   ├── multi-venue-ups-downs-skill.md
│   ├── multi-venue-impact-drivers-skill.md
│   ├── multi-venue-recommendations-skill.md
│   └── README.md
│
└── multi-venue-comparison-report/  (NEW overlay: multi-venue comparison - full rewrite, all 5 section skills)
    ├── multi-venue-overview-comparison-skill.md
    ├── multi-venue-ranking-comparison-skill.md
    ├── multi-venue-ups-downs-comparison-skill.md
    ├── multi-venue-impact-drivers-comparison-skill.md
    ├── multi-venue-recommendations-comparison-skill.md
    └── README.md
```

### Report Type Routing

```
Report Type              | Stages 1-2 run          | Stage 3 template          | Section skills loaded from
─────────────────────────┼────────────────────────┼───────────────────────────┼────────────────────────────────
snapshot                 | single-venue/*, x1      | single-venue-report/*     | single-venue-report/ (existing)
comparison               | single-venue/*, x2      | single-venue-report/*     | comparison-report/
multi-snapshot           | multi-venue/*, x1       | multi-venue-report/*      | multi-venue-report/
multi-comparison         | multi-venue/*, x2       | multi-venue-report/*      | multi-venue-comparison-report/
```

"x1"/"x2" = number of times Stage 1 + Stage 2 must run (once per period for comparison reports - see Decision 3's comparison nuance). Stage 3's template (structural skeleton + Output envelope) is shared within an axis-A family regardless of snapshot/comparison; only the injected section-skill content differs.

---

## Phase 1: Comparison Report Skills

### Overview

These adapt existing single-venue skills for **two-period comparison** context.

**Key principle:** Comparison skills focus on **change magnitude** and **direction**, not absolute magnitude.

### Files to Create

#### 1. `.claude/comparison-report/venue-overview-comparison-skill.md`

**Purpose:** Write 2-4 sentence narrative comparing two periods

**Key Changes from Single-Venue:**
- Frame as "improved/declined/stable"
- Cite deltas and directions
- Acknowledge trends and reversals
- Use comparison language: "improved by X points," "declined from Y to Z"

**Example output:**
```
"Performance improved significantly from Q1 to Q2, driven by equipment 
reliability fixes that reduced complaint frequency from 14 to 8 mentions. 
Staff responsiveness remained strong throughout. However, F&B service speed 
declined slightly, suggesting new operational challenges emerged."
```

**Key rules:**
- MUST cite deltas (e.g., "improved by 0.8 points")
- MUST acknowledge direction (↑ improvement, ↓ decline, → stable)
- MUST NOT just repeat period 1 and period 2 separately
- MUST frame as a story of change, not two separate snapshots

#### 2. `.claude/comparison-report/ups-downs-comparison-skill.md`

**Purpose:** Select findings that changed between periods

**Key Changes from Single-Venue:**
- Frame as "improved," "declined," "remained strong," "worsened"
- Include delta alongside magnitude
- Highlight reversals (was weak, now strong)
- Show trend direction

**Example output:**
```json
{
  "ups": [
    "<strong>Equipment reliability improved:</strong> Complaint frequency dropped from 14 to 8 mentions, indicating fixes are working. Screen tracking failures are now resolved within 2 minutes consistently.",
    "<strong>Staff responsiveness remained strong:</strong> Maintained 8+ positive mentions across both periods, showing consistent excellence."
  ],
  "downs": [
    "<strong>F&B service speed declined:</strong> Average wait time increased from 8 to 12 minutes, with 5 new complaints in Q2 vs. 2 in Q1.",
    "<strong>Pricing concerns emerged:</strong> New theme in Q2 with 3 mentions, suggesting value perception shifted negatively."
  ]
}
```

**Key rules:**
- MUST frame as change (improved/declined/stable), not absolute state
- MUST cite deltas (e.g., "dropped from 14 to 8")
- MUST include direction indicators
- MUST highlight new issues (emerged in Q2) and resolved issues (no longer mentioned)

#### 3. `.claude/comparison-report/impact-drivers-comparison-skill.md`

**Purpose:** Rank by **change magnitude**, not absolute magnitude

**Key Changes from Single-Venue:**
- Sort by delta, not absolute value
- Explain "what changed most"
- Include direction (↑/↓)
- Show baseline and current state

**Example output:**
```json
{
  "impact": [
    {
      "title": "Equipment Reliability",
      "description": "Improved most significantly (+0.8 points), with complaint frequency dropping from 14 to 8 mentions. This is the primary positive trend driving overall satisfaction gains."
    },
    {
      "title": "F&B Service Speed",
      "description": "Declined by 0.4 points, with average wait times increasing from 8 to 12 minutes. This emerging issue is the primary concern offsetting equipment improvements."
    },
    {
      "title": "Staff Responsiveness",
      "description": "Remained stable with consistent positive mentions (8 in both periods), showing this strength is being maintained."
    }
  ]
}
```

**Key rules:**
- MUST rank by **change magnitude** (delta), not absolute magnitude
- MUST explain "what changed most" not "what matters most"
- MUST include both positive and negative changes
- MUST cite baseline and current values
- MUST NOT reorder based on absolute importance (follow the delta ranking)

#### 4. `.claude/comparison-report/recommendations-comparison-skill.md`

**Purpose:** Generate actions for sustaining/addressing changes

**Key Changes from Single-Venue:**
- "Sustain momentum" for improvements
- "Address emerging issues" for declines
- Reference baseline period for context
- Acknowledge what's working and shouldn't change

**Example output:**
```json
{
  "recommendations": {
    "critical": {
      "title": "Sustain Equipment Reliability Improvements",
      "items": [
        "<strong>Maintain daily calibration schedule:</strong> The 0.8-point improvement came from implementing daily screen checks. Continue this regimen to prevent regression.",
        "<strong>Document the fix process:</strong> Capture what worked so it can be replicated if issues resurface.",
        "<strong>Monitor for regression:</strong> Track screen failures weekly to catch any uptick early."
      ]
    },
    "secondary": {
      "title": "Address F&B Service Speed Decline",
      "items": [
        "<strong>Investigate root cause:</strong> Determine why wait times increased from 8 to 12 minutes (staffing, menu complexity, volume).",
        "<strong>Implement targeted fix:</strong> Based on root cause, adjust staffing, menu, or workflow.",
        "<strong>Set speed targets:</strong> Establish 8-minute target to return to Q1 baseline."
      ]
    },
    "maintain": {
      "title": "Protect Staff Responsiveness",
      "items": [
        "<strong>Continue current practices:</strong> Staff responsiveness remained stable at 8 mentions both periods—maintain current training and recognition programs.",
        "<strong>Recognize staff:</strong> Acknowledge the team for maintaining service quality despite operational changes."
      ]
    }
  }
}
```

**Key rules:**
- `critical`: Address #1 **change** (biggest improvement or biggest decline)
- `secondary`: Address #2 **change**
- `maintain`: Reinforce what's **stable and strong** (not regressing)
- MUST reference baseline period ("Q1 baseline was 8 minutes")
- MUST frame as "sustain" or "address" not just "fix" or "improve"
- MUST acknowledge what's working and shouldn't change

### Phase 1 Deliverables

- [ ] `.claude/single-venue-report/synthesis_template.md` - **prerequisite**: extract from the current monolithic `synthesis.md`, replacing the inline "## Overview Section" / "## Ups and Downs Sections" / "## Impact Section" / "## Recommendations Section" rule blocks with `<!-- SKILL:venue-overview -->` / `<!-- SKILL:ups-downs -->` / `<!-- SKILL:impact-drivers -->` / `<!-- SKILL:recommendations -->` placeholders (see Decision 5). Verify snapshot output is unaffected before moving on.
- [ ] `.claude/comparison-report/README.md` (architecture guide)
- [ ] `.claude/comparison-report/venue-overview-comparison-skill.md`
- [ ] `.claude/comparison-report/ups-downs-comparison-skill.md`
- [ ] `.claude/comparison-report/impact-drivers-comparison-skill.md`
- [ ] `.claude/comparison-report/recommendations-comparison-skill.md`

**Dependencies:**
- Reuse existing `.claude/single-venue-report/metrics_analysis.md` (Stage 1) - run once per period (current and previous)
- Reuse existing `.claude/single-venue-report/comment_analysis.md` (Stage 2) - run once per period (current and previous)
- Reuse `.claude/single-venue-report/synthesis_template.md` (Stage 3 structural skeleton + Output envelope) - unchanged from snapshot, only the injected section skills differ

**Integration point:** `analyze_venues.py` - for `report_type='comparison'`:
1. Run Stage 1 + Stage 2 for `current_data` and again for `previous_data` (four calls total, each independently cached)
2. Compose the Stage 3 synthesis prompt via `_compose_synthesis_skill('comparison')`, injecting `comparison-report/*-comparison-skill.md` content into `synthesis_template.md`
3. Feed both periods' Stage 1/2 results into the Stage 3 payload so deltas can be computed
4. Update `create_single_venue_comparison_report.py` to actually pass `previous_data` through (today it silently ignores it, per Decision 3)

---

## Phase 2: Multi-Venue Report Skills

### Overview

These create **new** skills for aggregated multi-venue analysis. This is more complex because:
- Input data is aggregated across multiple venues
- Metrics are network-wide averages + per-venue values
- Comments are from all venues, with venue attribution
- Themes are network-wide patterns + venue-specific outliers

### Files to Create

#### 1. `.claude/multi-venue-report/metrics_analysis.md` (NEW Stage 1)

**Purpose:** Aggregate metrics across all venues

**Key Differences from Single-Venue:**
- Input: list of venue metrics (not single venue)
- Output: network-wide characterization + per-venue flags
- Handle missing data (some venues may lack F&B)
- Compute network averages and ranges
- Identify outliers (best/worst performers)

**Input format:**
```json
{
  "venues": [
    {
      "venue": "Grand Prairie",
      "responses": 45,
      "metrics": {
        "ltr_avg": 4.2,
        "fun_avg": 4.1,
        "helpful_avg": 3.8,
        "issues_pct": 22,
        "resolution_avg": 3.9,
        "nps_avg": 8.8,
        "fb_average": 3.5
      }
    },
    {
      "venue": "Austin",
      "responses": 38,
      "metrics": {
        "ltr_avg": 4.0,
        "fun_avg": 3.9,
        "helpful_avg": 3.6,
        "issues_pct": 28,
        "resolution_avg": 3.7,
        "nps_avg": 8.4,
        "fb_average": 3.2
      }
    },
    ...
  ],
  "assessment_tiers": {...}
}
```

**Output format:**
```json
{
  "characterization": "The venue network shows strong overall satisfaction (8.2 NPS average), but performance varies significantly by location. Grand Prairie leads (8.8 NPS), while El Paso lags (7.1 NPS). Equipment reliability is the primary network-wide concern, though venues vary in severity.",
  "network_metrics": [
    {
      "metric": "nps",
      "polarity": "positive",
      "magnitude": 82,
      "network_avg": 8.2,
      "range": "7.1 - 8.8",
      "note": "Strong network-wide NPS (8.2/10 average), ranging from 7.1 (El Paso) to 8.8 (Grand Prairie)"
    },
    {
      "metric": "issues",
      "polarity": "negative",
      "magnitude": 65,
      "network_avg": 28,
      "range": "18% - 35%",
      "note": "Issue frequency varies significantly (18% at Grand Prairie vs. 35% at El Paso)"
    }
  ],
  "venue_outliers": [
    {
      "venue": "Grand Prairie",
      "rank": 1,
      "nps": 8.8,
      "note": "Best performer—strong across all metrics"
    },
    {
      "venue": "El Paso",
      "rank": 7,
      "nps": 7.1,
      "note": "Needs support—high issue rate (35%) and low resolution satisfaction"
    }
  ]
}
```

**Key rules:**
- MUST compute network averages for each metric
- MUST identify range (min/max) for each metric
- MUST flag metrics where variance is high (>0.5 points)
- MUST identify outliers (best/worst performers)
- MUST handle missing data gracefully (note which venues lack F&B, etc.)
- MUST NOT rank venues by absolute performance (that's done in ranking skill)
- Characterization MUST focus on network patterns, not individual venues

#### 2. `.claude/multi-venue-report/comment_analysis.md` (NEW Stage 2)

**Purpose:** Aggregate comment themes across all venues

**Key Differences from Single-Venue:**
- Input: comments from all venues (with venue attribution)
- Output: network-wide themes + venue-specific themes
- Track which venues mention each theme
- Adjust magnitude for network-wide relevance
- Identify venue-specific outliers (e.g., "Equipment reliability is only a problem at El Paso")

**Input format:**
```json
{
  "venues": [
    {
      "venue": "Grand Prairie",
      "responses": 45,
      "comments": [
        {
          "text": "Screen tracking worked great, no issues.",
          "ltr": 5,
          "fun": 5
        },
        ...
      ]
    },
    {
      "venue": "Austin",
      "responses": 38,
      "comments": [
        {
          "text": "Screen stopped tracking mid-game, but staff fixed it quickly.",
          "ltr": 4,
          "fun": 4
        },
        ...
      ]
    },
    ...
  ],
  "metric_flags": [...]
}
```

**Output format:**
```json
{
  "themes": [
    {
      "label": "Equipment reliability",
      "polarity": "negative",
      "mention_count": 18,
      "magnitude": 68,
      "network_summary": "Screen tracking failures are the dominant complaint across the network, mentioned in 18 comments (12% of all comments). Severity varies by venue.",
      "venue_breakdown": [
        {
          "venue": "El Paso",
          "mentions": 8,
          "severity": "high",
          "representative_detail": "\"Screen stopped tracking constantly, really frustrating.\""
        },
        {
          "venue": "Austin",
          "mentions": 6,
          "severity": "medium",
          "representative_detail": "\"Screen stopped tracking mid-game, but staff fixed it quickly.\""
        },
        {
          "venue": "Grand Prairie",
          "mentions": 2,
          "severity": "low",
          "representative_detail": "\"Occasional tracking issue, quickly resolved.\""
        },
        {
          "venue": "Dallas",
          "mentions": 2,
          "severity": "low",
          "representative_detail": "\"One screen glitch, but staff was on it.\""
        }
      ],
      "representative_detail": "\"Screen stopped tracking constantly, really frustrating.\" (El Paso)"
    },
    {
      "label": "Staff responsiveness",
      "polarity": "positive",
      "mention_count": 16,
      "magnitude": 62,
      "network_summary": "Staff responsiveness is consistently praised across all venues, mentioned in 16 comments. Guests appreciate quick problem resolution.",
      "venue_breakdown": [
        {
          "venue": "Grand Prairie",
          "mentions": 5,
          "severity": "high",
          "representative_detail": "\"Staff was amazing, fixed our bay issue right away.\""
        },
        {
          "venue": "Austin",
          "mentions": 4,
          "severity": "high",
          "representative_detail": "\"Someone came over quickly to fix the screen.\""
        },
        {
          "venue": "Dallas",
          "mentions": 4,
          "severity": "medium",
          "representative_detail": "\"Staff helped us pretty quickly.\""
        },
        {
          "venue": "El Paso",
          "mentions": 3,
          "severity": "medium",
          "representative_detail": "\"Staff tried to help but took a while.\""
        }
      ],
      "representative_detail": "\"Staff was amazing, fixed our bay issue right away.\" (Grand Prairie)"
    }
  ]
}
```

**Key rules:**
- MUST compute network-wide mention count and magnitude
- MUST track which venues mention each theme and how often
- MUST identify venue-specific outliers (e.g., "El Paso has 8 mentions, others have 2-4")
- MUST adjust magnitude based on network-wide prevalence, not just total mentions
- MUST include venue breakdown in output
- MUST NOT aggregate away venue-specific context
- Themes MUST be network-wide patterns (not venue-specific)

#### 3. `.claude/multi-venue-report/synthesis.md` (NEW Stage 3)

**Purpose:** Merge aggregated metrics + comments into unified analysis

**Key Differences from Single-Venue:**
- Input: aggregated metrics + comments (not single venue)
- Output: network-wide overview/ups/downs/impact/recommendations
- Load multi-venue skill variants (not single-venue)
- Handle venue-specific context in recommendations

**Workflow:**
1. Load aggregated metrics from Stage 1
2. Load aggregated comments from Stage 2
3. Create combined ranking (network-wide magnitude)
4. Load multi-venue skill variants (overview, ranking, ups/downs, impact, recommendations)
5. Call Claude with combined ranking + skill variants
6. Return network-wide analysis

**Key rules:**
- MUST use network-wide magnitude for combined ranking
- MUST load multi-venue skill variants (not single-venue)
- MUST pass venue breakdown data to recommendation skills
- MUST NOT rank venues in synthesis (that's done in ranking skill)

#### 4. `.claude/multi-venue-report/multi-venue-overview-skill.md`

**Purpose:** Write 2-4 sentence network narrative

**Key Differences from Single-Venue:**
- Frame as network-wide patterns
- Acknowledge venue variance
- Highlight outliers (best/worst performers)
- Use aggregate language ("across venues," "on average")

**Example output:**
```
"The venue network shows strong overall satisfaction (8.2 NPS average), 
driven by consistent staff responsiveness and solid game experiences. 
However, equipment reliability varies significantly by location, with 
Grand Prairie performing well (8.8 NPS) while El Paso faces challenges 
(7.1 NPS). Addressing venue-specific operational issues could unlock 
significant network-wide gains."
```

**Key rules:**
- MUST start with network-wide characterization
- MUST acknowledge venue variance explicitly
- MUST highlight outliers (best/worst performers)
- MUST use aggregate language ("across venues," "on average," "most locations")
- MUST NOT focus on individual venues (that's done in ranking skill)
- MUST be 2-4 sentences
- MUST avoid redundant metric numbers

#### 5. `.claude/multi-venue-report/multi-venue-ranking-skill.md`

**Purpose:** Rank venues by composite score and explain ranking

**Key Differences from Single-Venue:**
- Sort venues by NPS or composite metric
- Explain ranking differences
- Show tier groupings (top/middle/bottom)
- For comparisons: show ranking movement

**Example output:**
```json
{
  "venue_ranking": [
    {
      "rank": 1,
      "venue": "Grand Prairie",
      "nps": 8.8,
      "composite_score": 8.8,
      "tier": "top_performer",
      "summary": "Best performer across all metrics. Strong NPS (8.8), low issue rate (18%), and excellent staff responsiveness. Model for network."
    },
    {
      "rank": 2,
      "venue": "Austin",
      "nps": 8.4,
      "composite_score": 8.4,
      "tier": "top_performer",
      "summary": "Strong performance with solid NPS (8.4) and good staff responsiveness. Equipment reliability slightly below network average."
    },
    {
      "rank": 3,
      "venue": "Dallas",
      "nps": 8.1,
      "composite_score": 8.1,
      "tier": "middle_performer",
      "summary": "Solid performance with NPS (8.1) near network average. Balanced across metrics."
    },
    {
      "rank": 4,
      "venue": "El Paso",
      "nps": 7.1,
      "composite_score": 7.1,
      "tier": "needs_support",
      "summary": "Needs targeted support. High issue rate (35%), low resolution satisfaction, and equipment reliability concerns. Opportunity for significant improvement."
    }
  ]
}
```

**Key rules:**
- MUST rank by NPS (or composite score if NPS unavailable)
- MUST explain ranking differences (why is venue X ranked higher than Y?)
- MUST show tier groupings (top/middle/bottom performers)
- MUST include summary for each venue
- For comparisons: MUST show ranking movement (moved up/down X spots)
- MUST NOT mix ranking with recommendations (that's done in recommendations skill)

#### 6. `.claude/multi-venue-report/multi-venue-ups-downs-skill.md`

**Purpose:** Select network-wide strengths and weaknesses

**Key Differences from Single-Venue:**
- Focus on **network patterns**, not individual venues
- Highlight **consistency** vs **variance**
- Call out **outliers** (venues that differ from trend)
- Use aggregate language

**Example output:**
```json
{
  "ups": [
    "<strong>Consistent staff responsiveness:</strong> Praised across all venues (16 mentions total), with Grand Prairie and Austin leading. This is a network-wide strength worth protecting.",
    "<strong>Strong NPS at top venues:</strong> Grand Prairie (8.8) and Austin (8.4) demonstrate that 8.5+ NPS is achievable. Model their practices network-wide."
  ],
  "downs": [
    "<strong>Equipment reliability varies significantly:</strong> While Grand Prairie has minimal issues (18%), El Paso faces challenges (35%). This variance suggests venue-specific factors (maintenance, staffing, equipment age) are at play.",
    "<strong>F&B service speed is a network-wide concern:</strong> Average 3.2/5 across all venues, with no venue exceeding 3.5. This is a systemic issue affecting all locations."
  ]
}
```

**Key rules:**
- MUST focus on **network patterns**, not individual venues
- MUST highlight **consistency** (what's strong everywhere?) vs **variance** (what varies by venue?)
- MUST call out **outliers** (venues that differ from network trend)
- MUST use aggregate language ("across venues," "on average," "most locations")
- MUST NOT focus on individual venues (that's done in ranking skill)
- MUST include 2-3 ups and 2-3 downs

#### 7. `.claude/multi-venue-report/multi-venue-impact-drivers-skill.md`

**Purpose:** Explain top 3 factors affecting network performance

**Key Differences from Single-Venue:**
- Rank by **network-wide magnitude**
- Acknowledge **venue variance** in each driver
- Cite **network averages** and **range** (min/max)
- Explain what variance means operationally

**Example output:**
```json
{
  "impact": [
    {
      "title": "NPS (Network Average: 8.2)",
      "description": "Strong overall satisfaction drives network performance, ranging from 7.1 (El Paso) to 8.8 (Grand Prairie). The 1.7-point spread suggests venue-specific operational factors significantly impact satisfaction."
    },
    {
      "title": "Equipment Reliability",
      "description": "Issue frequency varies significantly (18% at Grand Prairie vs. 35% at El Paso), with 18 comments mentioning equipment problems. This is the primary operational lever for network improvement."
    },
    {
      "title": "Staff Responsiveness",
      "description": "Consistently praised across all venues (16 mentions), with no venue falling below 3.5/5. This is a network-wide strength that's being maintained uniformly."
    }
  ]
}
```

**Key rules:**
- MUST rank by **network-wide magnitude** (not individual venue)
- MUST acknowledge **venue variance** in each driver
- MUST cite **network averages** and **range** (min/max)
- MUST explain what variance means operationally
- MUST include exactly 3 drivers
- MUST use 1-2 sentences per driver

#### 8. `.claude/multi-venue-report/multi-venue-recommendations-skill.md`

**Purpose:** Generate network-wide and venue-specific actions

**Key Differences from Single-Venue:**
- Separate **network-wide actions** from **venue-specific actions**
- Network actions focus on **standardization** and **best practice sharing**
- Venue actions reference **venue name** and **specific issue**
- Acknowledge **best performers** and recommend they mentor others

**Example output:**
```json
{
  "recommendations": {
    "critical": {
      "title": "Standardize Equipment Maintenance Across Network",
      "items": [
        "<strong>Share Grand Prairie's maintenance playbook:</strong> Grand Prairie achieves 18% issue rate vs. network average 28%. Document their daily calibration and maintenance schedule and roll out network-wide.",
        "<strong>Audit El Paso's equipment:</strong> 35% issue rate suggests equipment age, maintenance gaps, or staffing issues. Conduct on-site assessment and develop venue-specific remediation plan.",
        "<strong>Implement daily equipment checks:</strong> Establish network-wide standard for pre-opening equipment verification to catch issues before guests arrive."
      ]
    },
    "secondary": {
      "title": "Improve F&B Service Speed Network-Wide",
      "items": [
        "<strong>Benchmark best practices:</strong> No venue exceeds 3.5/5 on F&B speed. Research industry standards and identify process improvements (menu simplification, staffing, workflow).",
        "<strong>Pilot workflow optimization:</strong> Test changes at one venue (suggest Austin as test site) before rolling out network-wide.",
        "<strong>Set network target:</strong> Establish 4.0/5 target for F&B speed and track progress monthly."
      ]
    },
    "maintain": {
      "title": "Protect Staff Responsiveness Across Network",
      "items": [
        "<strong>Document staff training practices:</strong> Staff responsiveness is consistent across all venues (16 mentions). Capture what's working and standardize training.",
        "<strong>Share best practices:</strong> Grand Prairie leads with 5 positive mentions. Have their team mentor other venues on rapid problem resolution.",
        "<strong>Recognize and reward:</strong> Acknowledge staff across all venues for maintaining service quality despite operational challenges."
      ]
    },
    "venue_specific": [
      {
        "venue": "Grand Prairie",
        "priority": "maintain",
        "action": "Continue current practices—you're the network leader. Share your equipment maintenance playbook with other venues."
      },
      {
        "venue": "Austin",
        "priority": "secondary",
        "action": "Address equipment reliability (6 mentions). Implement Grand Prairie's maintenance schedule and monitor for improvement."
      },
      {
        "venue": "El Paso",
        "priority": "critical",
        "action": "High issue rate (35%) requires urgent attention. Conduct equipment audit, assess staffing, and implement Grand Prairie's maintenance practices."
      }
    ]
  }
}
```

**Key rules:**
- `critical`: Address #1 network-wide issue (e.g., "Standardize equipment maintenance")
- `secondary`: Address #2 network-wide issue
- `maintain`: Reinforce #1 network-wide strength
- `venue_specific`: Include 1-2 sentence action for each venue
- MUST reference **venue names** in venue-specific actions
- MUST acknowledge **best performers** and recommend they mentor others
- MUST separate **network-wide actions** from **venue-specific actions**
- Network actions focus on **standardization** and **best practice sharing**

### Phase 2 Deliverables

- [ ] `.claude/multi-venue-report/README.md` (architecture guide)
- [ ] `.claude/multi-venue-report/metrics_analysis.md` (Stage 1)
- [ ] `.claude/multi-venue-report/comment_analysis.md` (Stage 2)
- [ ] `.claude/multi-venue-report/synthesis_template.md` (Stage 3 - own template, not shared with single-venue; see Decision 5)
- [ ] `.claude/multi-venue-report/multi-venue-overview-skill.md`
- [ ] `.claude/multi-venue-report/multi-venue-ranking-skill.md`
- [ ] `.claude/multi-venue-report/multi-venue-ups-downs-skill.md`
- [ ] `.claude/multi-venue-report/multi-venue-impact-drivers-skill.md`
- [ ] `.claude/multi-venue-report/multi-venue-recommendations-skill.md`

**Dependencies:**
- New Stage 1: `.claude/multi-venue-report/metrics_analysis.md`
- New Stage 2: `.claude/multi-venue-report/comment_analysis.md`
- New Stage 3: `.claude/multi-venue-report/synthesis_template.md`
- New skills: 5 multi-venue-specific section skills

**Integration point:** `analyze_venues.py` - detect `report_type='multi-snapshot'` and compose the synthesis prompt via `_compose_synthesis_skill('multi-snapshot')`, injecting `multi-venue-report/*-skill.md` content into `multi-venue-report/synthesis_template.md`

---

## Phase 2b: Multi-Venue Comparison Skills

### Overview

Per Decision 2, multi-venue comparison gets the **same full-rewrite treatment** as single-venue comparison (Phase 1) - not a single bonus "context" file layered on top of the snapshot skills. Multi-venue comparison reports need every section (overview, ranking, ups/downs, impact, recommendations) reframed around **change** (network trend + per-venue variance in that trend), exactly as Phase 1 did for single-venue's four sections.

**Key principle:** Same as Phase 1 - focus on **change magnitude** and **direction**, but at the network level: highlight the network-wide trend, then show which venues diverge from it.

### Files to Create

All five files live in `.claude/multi-venue-comparison-report/` and overlay `multi-venue-report/`'s Stage 1/2/template (run twice - once per period - same as single-venue comparison in Phase 1).

#### 1. `multi-venue-overview-comparison-skill.md`

**Purpose:** Write 2-4 sentence network narrative framed as change, not two separate snapshots.

**Example output:**
```
"The network improved overall (NPS +0.3), but gains were uneven. Grand Prairie
and Austin improved significantly (+0.6 each), while El Paso declined (-0.2).
This suggests venue-specific factors are more influential than network-wide
initiatives. Equipment reliability improvements at Grand Prairie and Austin
drove their gains, while El Paso's equipment challenges worsened."
```

**Key rules:**
- MUST highlight the **network trend** (up/down/stable) first
- MUST show **venue-level variance** in that trend, not just the network average
- MUST call out **concerning divergence** (venues moving opposite directions)
- MUST be 2-4 sentences; use aggregate language ("across venues," "on average")

#### 2. `multi-venue-ranking-comparison-skill.md`

**Purpose:** Rank venues by current absolute performance (per Q2 decision in Open Questions), with ranking movement shown as secondary context.

**Key rules:**
- MUST rank by current-period NPS/composite score (absolute), same primary ordering as the snapshot ranking skill
- MUST show rank movement vs. the previous period for each venue (e.g., "moved up 2 spots")
- MUST call out venues whose rank changed most, and explain why (tie back to their biggest metric/theme delta)

#### 3. `multi-venue-ups-downs-comparison-skill.md`

**Purpose:** Select network-wide patterns that changed between periods.

**Key rules:**
- MUST frame each item as change (improved/declined/stable network-wide), not absolute state
- MUST distinguish "improved everywhere" from "improved on average but worsened at specific venues"
- MUST include 2-3 ups and 2-3 downs

#### 4. `multi-venue-impact-drivers-comparison-skill.md`

**Purpose:** Rank the top 3 network-wide factors by **change magnitude**, not absolute magnitude.

**Key rules:**
- MUST rank by network-wide delta, not absolute value
- MUST cite baseline and current network average plus the range of per-venue deltas
- MUST include exactly 3 drivers, 1-2 sentences each

#### 5. `multi-venue-recommendations-comparison-skill.md`

**Purpose:** Generate network-wide and venue-specific actions for sustaining improvements or addressing declines.

**Key rules:**
- `critical`/`secondary`/`maintain`: same tier semantics as the snapshot ranking skill, but addressing the #1/#2 **network-wide decline** and reinforcing the #1 **network-wide improvement**, respectively
- `venue_specific`: MUST call out venues that diverged from the network trend (improved while network declined, or vice versa) with a 1-2 sentence action referencing their specific delta
- MUST reference baseline period values, same as Phase 1's single-venue recommendations skill

### Phase 2b Deliverables

- [ ] `.claude/multi-venue-comparison-report/README.md` (architecture guide)
- [ ] `.claude/multi-venue-comparison-report/multi-venue-overview-comparison-skill.md`
- [ ] `.claude/multi-venue-comparison-report/multi-venue-ranking-comparison-skill.md`
- [ ] `.claude/multi-venue-comparison-report/multi-venue-ups-downs-comparison-skill.md`
- [ ] `.claude/multi-venue-comparison-report/multi-venue-impact-drivers-comparison-skill.md`
- [ ] `.claude/multi-venue-comparison-report/multi-venue-recommendations-comparison-skill.md`

**Dependencies:**
- Reuse `.claude/multi-venue-report/metrics_analysis.md` (Stage 1) - run once per period
- Reuse `.claude/multi-venue-report/comment_analysis.md` (Stage 2) - run once per period
- Reuse `.claude/multi-venue-report/synthesis_template.md` (Stage 3 structural skeleton) - only the injected section skills differ

**Integration point:** `analyze_venues.py` - detect `report_type='multi-comparison'`, run Stage 1+2 for both periods, and compose the synthesis prompt via `_compose_synthesis_skill('multi-comparison')`, injecting `multi-venue-comparison-report/*-comparison-skill.md` content into `multi-venue-report/synthesis_template.md`

---

## Phase 3: Python Integration

### Overview

Update Python code to route report types to correct skill sets.

### Files to Modify

#### 1. `python/analyze_venues.py`

**Current state:**
```python
SKILLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.claude', 'single-venue-report')

def get_ai_analysis(data, use_cache=True):
    """Run AI analysis on a single venue."""
    # Loads skills from SKILLS_DIR
    # Runs 3-stage pipeline
    # Returns analysis

def get_period_ai_analysis(period_data, use_cache=True):
    """Placeholder for period-level analysis."""
    return None, "Period-level AI analysis not yet implemented"
```

**Changes needed** (see Decision 5 for the composition mechanism this relies on):

1. Add a generic skill-variant loader and the template composition function:
```python
def _load_skill_variant(variant_dir, filename):
    """Load a skill file from a specific .claude/<variant_dir>/ folder."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.claude', variant_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


# One entry per report_type: (template_source_dir, section_skill_dir, section_filename_suffix)
_SYNTHESIS_CONFIG = {
    'snapshot':         ('single-venue-report', 'single-venue-report', '-skill.md'),
    'comparison':       ('single-venue-report', 'comparison-report', '-comparison-skill.md'),
    'multi-snapshot':   ('multi-venue-report', 'multi-venue-report', '-skill.md'),
    'multi-comparison': ('multi-venue-report', 'multi-venue-comparison-report', '-comparison-skill.md'),
}
_SECTION_NAMES = {
    'snapshot':   ['venue-overview', 'ups-downs', 'impact-drivers', 'recommendations'],
    'comparison': ['venue-overview', 'ups-downs', 'impact-drivers', 'recommendations'],
    'multi-snapshot':   ['multi-venue-overview', 'multi-venue-ranking', 'multi-venue-ups-downs', 'multi-venue-impact-drivers', 'multi-venue-recommendations'],
    'multi-comparison': ['multi-venue-overview', 'multi-venue-ranking', 'multi-venue-ups-downs', 'multi-venue-impact-drivers', 'multi-venue-recommendations'],
}
_PLACEHOLDER_KEYS = {
    'venue-overview': 'venue-overview', 'ups-downs': 'ups-downs',
    'impact-drivers': 'impact-drivers', 'recommendations': 'recommendations',
    'multi-venue-overview': 'venue-overview', 'multi-venue-ranking': 'ranking',
    'multi-venue-ups-downs': 'ups-downs', 'multi-venue-impact-drivers': 'impact-drivers',
    'multi-venue-recommendations': 'recommendations',
}


def _compose_synthesis_skill(report_type):
    """Build the Stage 3 prompt text by substituting each <!-- SKILL:x --> placeholder
    in the family's synthesis_template.md with that report_type's section-skill content.
    Cache keys are computed on this composed string, so editing any one section skill
    naturally invalidates only the affected cache entries (see _stage_cache_key)."""
    template_dir, section_dir, suffix = _SYNTHESIS_CONFIG[report_type]
    template = _load_skill_variant(template_dir, 'synthesis_template.md')
    for name in _SECTION_NAMES[report_type]:
        section_text = _load_skill_variant(section_dir, f"{name}{suffix}")
        template = template.replace(f"<!-- SKILL:{_PLACEHOLDER_KEYS[name]} -->", section_text)
    return template
```

2. Add `report_type` to `get_ai_analysis()`, and make it run Stage 1+2 once per period (twice total for comparison):
```python
def get_ai_analysis(data, report_type='snapshot', previous_data=None, use_cache=True):
    """
    Run AI analysis on venue data.

    Args:
        data: Current-period venue data
        report_type: 'snapshot' or 'comparison'
        previous_data: Required when report_type='comparison' - previous period's venue data
        use_cache: Whether to use cached results

    Returns:
        (analysis, None) on success, or (None, reason) if unavailable
    """
    if report_type == 'comparison' and previous_data is None:
        return None, "report_type='comparison' requires previous_data"

    metrics_current, error = _run_stage('metrics_analysis', METRICS_ANALYSIS_SKILL, _build_metrics_payload(data), ...)
    comment_current, error = _run_stage('comment_analysis', COMMENT_ANALYSIS_SKILL, _build_comment_payload(data, metrics_current['metric_flags']), ...)

    synthesis_payload = {"venue": data["venue"], "responses": data["responses"],
                          "metrics_analysis": metrics_current, "comment_analysis": comment_current}

    if report_type == 'comparison':
        metrics_previous, error = _run_stage('metrics_analysis', METRICS_ANALYSIS_SKILL, _build_metrics_payload(previous_data), ...)
        comment_previous, error = _run_stage('comment_analysis', COMMENT_ANALYSIS_SKILL, _build_comment_payload(previous_data, metrics_previous['metric_flags']), ...)
        synthesis_payload["previous"] = {"metrics_analysis": metrics_previous, "comment_analysis": comment_previous}

    synthesis_skill = _compose_synthesis_skill(report_type)
    return _run_stage('synthesis', synthesis_skill, synthesis_payload, _validate_synthesis, data["venue"], use_cache, force_refresh)
```

3. Implement `get_aggregated_ai_analysis()` (rename from `get_period_ai_analysis()`), mirroring the same pattern for `multi-snapshot`/`multi-comparison`, with its own `_build_multi_venue_metrics_payload()`/`_build_multi_venue_comment_payload()` (Phase 2's new aggregation logic) instead of the single-venue builders.

4. `_run_stage()` itself needs no changes - it already just takes whatever `skill_content` string it's given and hashes it for the cache key; `_compose_synthesis_skill()` is what changed what gets passed in.

#### 2. `python/report_content.py`

**Current state:**
```python
def get_analysis(data, precomputed_analysis=None):
    """Get analysis for a venue."""
    if precomputed_analysis is not None:
        # Use precomputed analysis
    else:
        # Call get_ai_analysis()
```

**Changes needed:**

1. Add `report_type` and `previous_data` parameters:
```python
def get_analysis(data, report_type='snapshot', previous_data=None, precomputed_analysis=None):
    """
    Get analysis for venue data.

    Args:
        data: Current-period venue data
        report_type: 'snapshot' or 'comparison'
        previous_data: Required when report_type='comparison'
        precomputed_analysis: Optional precomputed analysis

    Returns:
        Analysis dict
    """
    if precomputed_analysis is not None:
        # Use precomputed analysis
    else:
        # Call get_ai_analysis(data, report_type=report_type, previous_data=previous_data)
```

2. Pass `report_type`/`previous_data` through:
```python
analysis, error = get_ai_analysis(data, report_type=report_type, previous_data=previous_data, use_cache=True)
```

3. **Fix `create_single_venue_comparison_report.py`**: today it calls `report_content.get_analysis(current_data)` with no `previous_data` at all (verified in the current codebase) despite its docstring claiming "AI analysis with comparison context." Update the call site to pass `report_type='comparison'` and the already-loaded `previous_data`.

### Phase 3 Deliverables

- [ ] Update `python/analyze_venues.py` - Add `_load_skill_variant()`, `_compose_synthesis_skill()`, `report_type`/`previous_data` routing, two-period Stage 1/2 orchestration for comparison report types
- [ ] Update `python/report_content.py` - Pass `report_type`/`previous_data` through pipeline
- [ ] Update `create_single_venue_comparison_report.py` - actually pass `previous_data` and `report_type='comparison'` (currently silently analyzes only the current period)
- [ ] Update `create_multi_venue_snapshot_report.py` / `create_multi_venue_comparison_report.py` - call `get_aggregated_ai_analysis()` instead of hardcoding `ai_available: False`; remove the naive `extract_comment_themes()` first-50-characters placeholder in favor of the real Stage 2 comment analysis
- [ ] Update `python/evals/*.py` - Update comments to reference new skill directories (optional)

**Testing:**
- [ ] Test snapshot report (composed synthesis prompt should be substantively equivalent to today's monolithic `synthesis.md` - diff and re-run a known venue to confirm no regression)
- [ ] Test comparison report (should run Stage 1+2 twice, use `comparison-report/` skills, and actually reflect `previous_data` in the output - not just re-run the snapshot narrative on current data)
- [ ] Test multi-snapshot report (should use `multi-venue-report/` skills instead of the `ai_available: False` stub)
- [ ] Test multi-comparison report (should use `multi-venue-comparison-report/` skills, run Stage 1+2 twice)

---

## File Creation Checklist

### Phase 0: Template Extraction (prerequisite, 1 file)

- [ ] `.claude/single-venue-report/synthesis_template.md` - extracted from current `synthesis.md`, with `<!-- SKILL:x -->` placeholders (see Decision 5). Verify snapshot output is unaffected before Phase 1.

### Phase 1: Comparison Skills (5 files)

- [ ] `.claude/comparison-report/README.md`
- [ ] `.claude/comparison-report/venue-overview-comparison-skill.md`
- [ ] `.claude/comparison-report/ups-downs-comparison-skill.md`
- [ ] `.claude/comparison-report/impact-drivers-comparison-skill.md`
- [ ] `.claude/comparison-report/recommendations-comparison-skill.md`

### Phase 2: Multi-Venue Skills (9 files)

- [ ] `.claude/multi-venue-report/README.md`
- [ ] `.claude/multi-venue-report/metrics_analysis.md`
- [ ] `.claude/multi-venue-report/comment_analysis.md`
- [ ] `.claude/multi-venue-report/synthesis_template.md`
- [ ] `.claude/multi-venue-report/multi-venue-overview-skill.md`
- [ ] `.claude/multi-venue-report/multi-venue-ranking-skill.md`
- [ ] `.claude/multi-venue-report/multi-venue-ups-downs-skill.md`
- [ ] `.claude/multi-venue-report/multi-venue-impact-drivers-skill.md`
- [ ] `.claude/multi-venue-report/multi-venue-recommendations-skill.md`

### Phase 2b: Multi-Venue Comparison Skills (6 files)

- [ ] `.claude/multi-venue-comparison-report/README.md`
- [ ] `.claude/multi-venue-comparison-report/multi-venue-overview-comparison-skill.md`
- [ ] `.claude/multi-venue-comparison-report/multi-venue-ranking-comparison-skill.md`
- [ ] `.claude/multi-venue-comparison-report/multi-venue-ups-downs-comparison-skill.md`
- [ ] `.claude/multi-venue-comparison-report/multi-venue-impact-drivers-comparison-skill.md`
- [ ] `.claude/multi-venue-comparison-report/multi-venue-recommendations-comparison-skill.md`

### Phase 3: Python Integration (4 files)

- [ ] `python/analyze_venues.py` - Add `_load_skill_variant()`, `_compose_synthesis_skill()`, report_type/previous_data routing, two-period Stage 1/2 orchestration
- [ ] `python/report_content.py` - Update with report_type/previous_data parameters
- [ ] `python/create_single_venue_comparison_report.py` - fix the missing `previous_data` pass-through
- [ ] `python/create_multi_venue_snapshot_report.py` / `create_multi_venue_comparison_report.py` - wire up `get_aggregated_ai_analysis()`, remove the naive comment-theme placeholder

**Total:** 25 new/modified files

---

## Key Design Decisions

See [Architecture Decisions](#architecture-decisions) near the top of this document for the full, current set (Decisions 1-5, including the runtime synthesis composition mechanism and the two-period Stage 1/2 orchestration needed for comparison reports).

---

## Open Questions & Answers

### Q1: How do we handle venue-specific themes in multi-venue reports?

**Options:**
- Option A: Aggregate themes across all venues (lose venue context)
- Option B: Track which venues mention each theme (preserve context)

**Decision:** Option B - include venue attribution in theme summaries

**Implementation:**
- In `multi-venue-report/comment_analysis.md`, include `venue_breakdown` field
- Track mention count per venue
- Include representative detail from each venue
- Use venue breakdown in recommendations to identify venue-specific issues

**Example:**
```json
{
  "label": "Equipment reliability",
  "mention_count": 18,
  "venue_breakdown": [
    {"venue": "El Paso", "mentions": 8, "severity": "high"},
    {"venue": "Austin", "mentions": 6, "severity": "medium"},
    {"venue": "Grand Prairie", "mentions": 2, "severity": "low"}
  ]
}
```

### Q2: For multi-venue comparisons, should we rank venues by absolute performance or by improvement?

**Options:**
- Option A: Rank by absolute performance (who's best now?)
- Option B: Rank by improvement (who improved most?)

**Decision:** Option A (absolute) for primary ranking, with improvement delta as secondary signal

**Implementation:**
- Primary ranking: by NPS (or composite score)
- Secondary ranking: by NPS improvement (for comparison reports)
- Show both in output: "Rank 1: Grand Prairie (NPS 8.8, +0.2 from Q1)"

### Q3: Should multi-venue recommendations include venue-specific actions or only network-wide actions?

**Options:**
- Option A: Network-wide only (simpler, less actionable)
- Option B: Network-wide + venue-specific (more actionable, more complex)

**Decision:** Option B - include both tiers

**Implementation:**
- `critical` tier: Network-wide action (e.g., "Standardize equipment maintenance")
- `secondary` tier: Network-wide action (e.g., "Improve F&B speed")
- `maintain` tier: Network-wide action (e.g., "Protect staff responsiveness")
- `venue_specific` tier: 1-2 sentence action for each venue

### Q4: How do we handle missing data in multi-venue aggregation?

**Example:** Some venues have F&B metrics, others don't

**Decision:** Document in `multi-venue-report/metrics_analysis.md` how to handle missing data

**Implementation:**
- Compute averages only for venues that have data
- Note which venues lack F&B data
- Don't include F&B in composite score if <50% of venues have data
- Flag missing data in output: "F&B metrics available for 5/7 venues"

**Example:**
```json
{
  "metric": "fb_average",
  "network_avg": 3.2,
  "venues_with_data": 5,
  "venues_total": 7,
  "note": "F&B metrics available for 5/7 venues. Average computed from available data only."
}
```

### Q5: How do we cache multi-venue analysis?

**Question:** Should we cache by venue list, or by aggregated data hash?

**Decision:** Cache by aggregated data hash

**Implementation:**
- Compute hash of aggregated metrics + comments
- Use hash as cache key
- If same venues + same periods, reuse cached analysis
- If venues or periods change, recompute

---

## Success Criteria

- [ ] All 20 new skill files (+ 2 synthesis templates) created and documented
- [ ] Each skill has clear purpose, rules, examples, and related skills
- [ ] `synthesis_template.md` composition mechanism verified to produce output equivalent to today's monolithic `synthesis.md` for snapshot reports (no regression)
- [ ] Python integration routes report types to correct skills via `_compose_synthesis_skill()`
- [ ] Comparison reports run Stage 1+2 twice (current + previous period) and actually reflect `previous_data` - not just the current period's snapshot narrative
- [ ] Comparison reports use comparison skills (not snapshot skills)
- [ ] Multi-venue reports use multi-venue skills (not single-venue skills), replacing the current `ai_available: False` stub
- [ ] Multi-venue comment aggregation uses real Stage 2 analysis, not the naive first-50-characters placeholder in `extract_comment_themes()`
- [ ] Backward compatibility maintained (snapshot reports unchanged)
- [ ] All skills follow existing documentation patterns
- [ ] README files explain architecture and integration points
- [ ] End-to-end testing passes for all 4 report types:
  - [ ] Single-venue snapshot
  - [ ] Single-venue comparison
  - [ ] Multi-venue snapshot
  - [ ] Multi-venue comparison

---

## Next Steps

### Immediate (This Session)

1. ✅ Review this plan - architecture validated against the actual codebase
2. ✅ Clarify open questions - Q1-Q5 below, plus the synthesis composition mechanism (Decision 5) and folder layout (Decision 2)
3. ✅ Approve directory structure - `single-venue-report/`, `comparison-report/`, `multi-venue-report/`, `multi-venue-comparison-report/` as flat siblings under `.claude/`

### Phase 0: Template Extraction (Next Session, prerequisite for everything else)

1. Extract `.claude/single-venue-report/synthesis_template.md` from the current `synthesis.md`, replacing inline section rules with `<!-- SKILL:x -->` placeholders
2. Implement `_load_skill_variant()` / `_compose_synthesis_skill()` in `analyze_venues.py`, wired to `report_type='snapshot'` only for now
3. Diff old vs. new composed prompt text and re-run a known venue to confirm no regression before touching anything else

### Phase 1: Comparison Skills (Session After)

1. Create `.claude/comparison-report/README.md`
2. Create `.claude/comparison-report/venue-overview-comparison-skill.md`
3. Create `.claude/comparison-report/ups-downs-comparison-skill.md`
4. Create `.claude/comparison-report/impact-drivers-comparison-skill.md`
5. Create `.claude/comparison-report/recommendations-comparison-skill.md`
6. Add two-period Stage 1+2 orchestration to `get_ai_analysis()` and fix `create_single_venue_comparison_report.py`'s missing `previous_data` pass-through

### Phase 2: Multi-Venue Skills (Session After)

1. Create `.claude/multi-venue-report/README.md`
2. Create `.claude/multi-venue-report/metrics_analysis.md`
3. Create `.claude/multi-venue-report/comment_analysis.md`
4. Create `.claude/multi-venue-report/synthesis_template.md`
5. Create `.claude/multi-venue-report/multi-venue-overview-skill.md`
6. Create `.claude/multi-venue-report/multi-venue-ranking-skill.md`
7. Create `.claude/multi-venue-report/multi-venue-ups-downs-skill.md`
8. Create `.claude/multi-venue-report/multi-venue-impact-drivers-skill.md`
9. Create `.claude/multi-venue-report/multi-venue-recommendations-skill.md`

### Phase 2b: Multi-Venue Comparison Skills (Session After)

1. Create `.claude/multi-venue-comparison-report/README.md`
2. Create `.claude/multi-venue-comparison-report/multi-venue-overview-comparison-skill.md`
3. Create `.claude/multi-venue-comparison-report/multi-venue-ranking-comparison-skill.md`
4. Create `.claude/multi-venue-comparison-report/multi-venue-ups-downs-comparison-skill.md`
5. Create `.claude/multi-venue-comparison-report/multi-venue-impact-drivers-comparison-skill.md`
6. Create `.claude/multi-venue-comparison-report/multi-venue-recommendations-comparison-skill.md`

### Phase 3: Python Integration (Final Session)

1. Update `python/analyze_venues.py` - full report_type routing, `get_aggregated_ai_analysis()`
2. Update `python/report_content.py` - pass report_type/previous_data through pipeline
3. Update `create_single_venue_comparison_report.py`, `create_multi_venue_snapshot_report.py`, `create_multi_venue_comparison_report.py` to use the new AI analysis functions instead of stubs
4. Test end-to-end for all 4 report types

---

## Appendix: Report Type Matrix

| Report Type | Stages 1-2 (per period) | Stage 3 template | Section skills | Input | Output |
|---|---|---|---|---|---|
| **snapshot** | single-venue-report/*, x1 | single-venue-report/synthesis_template.md | single-venue-report/ (existing) | Single venue, one period | Single-venue snapshot report |
| **comparison** | single-venue-report/*, x2 | single-venue-report/synthesis_template.md | comparison-report/ (NEW) | Single venue, two periods | Single-venue comparison report |
| **multi-snapshot** | multi-venue-report/*, x1 | multi-venue-report/synthesis_template.md | multi-venue-report/ (NEW) | All venues, one period | Multi-venue snapshot report |
| **multi-comparison** | multi-venue-report/*, x2 | multi-venue-report/synthesis_template.md | multi-venue-comparison-report/ (NEW) | All venues, two periods | Multi-venue comparison report |

---

## Appendix: Skill File Dependencies

```
Single-Venue Snapshot:
├── .claude/single-venue-report/metrics_analysis.md          (x1)
├── .claude/single-venue-report/comment_analysis.md          (x1)
├── .claude/single-venue-report/synthesis_template.md         (composed with:)
├── .claude/single-venue-report/venue-overview-skill.md
├── .claude/single-venue-report/ups-downs-skill.md
├── .claude/single-venue-report/impact-drivers-skill.md
└── .claude/single-venue-report/recommendations-skill.md

Single-Venue Comparison:
├── .claude/single-venue-report/metrics_analysis.md          (x2: current + previous)
├── .claude/single-venue-report/comment_analysis.md          (x2: current + previous)
├── .claude/single-venue-report/synthesis_template.md         (composed with:)
├── .claude/comparison-report/venue-overview-comparison-skill.md
├── .claude/comparison-report/ups-downs-comparison-skill.md
├── .claude/comparison-report/impact-drivers-comparison-skill.md
└── .claude/comparison-report/recommendations-comparison-skill.md

Multi-Venue Snapshot:
├── .claude/multi-venue-report/metrics_analysis.md            (x1)
├── .claude/multi-venue-report/comment_analysis.md            (x1)
├── .claude/multi-venue-report/synthesis_template.md           (composed with:)
├── .claude/multi-venue-report/multi-venue-overview-skill.md
├── .claude/multi-venue-report/multi-venue-ranking-skill.md
├── .claude/multi-venue-report/multi-venue-ups-downs-skill.md
├── .claude/multi-venue-report/multi-venue-impact-drivers-skill.md
└── .claude/multi-venue-report/multi-venue-recommendations-skill.md

Multi-Venue Comparison:
├── .claude/multi-venue-report/metrics_analysis.md            (x2: current + previous)
├── .claude/multi-venue-report/comment_analysis.md            (x2: current + previous)
├── .claude/multi-venue-report/synthesis_template.md           (composed with:)
├── .claude/multi-venue-comparison-report/multi-venue-overview-comparison-skill.md
├── .claude/multi-venue-comparison-report/multi-venue-ranking-comparison-skill.md
├── .claude/multi-venue-comparison-report/multi-venue-ups-downs-comparison-skill.md
├── .claude/multi-venue-comparison-report/multi-venue-impact-drivers-comparison-skill.md
└── .claude/multi-venue-comparison-report/multi-venue-recommendations-comparison-skill.md
```

---

## Document Metadata

- **Created:** 2026-09-21
- **Last Updated:** 2026-09-21 (revised after codebase review: added Decision 5 synthesis composition mechanism, split multi-venue comparison into its own full-rewrite phase, added two-period Stage 1/2 orchestration for comparison report types, restructured directories as 4 flat sibling folders)
- **Status:** Ready for Implementation (Phase 0 template extraction must land first)
- **Next Review:** After Phase 0 completion
- **Owner:** AI Reporting Tool Team
