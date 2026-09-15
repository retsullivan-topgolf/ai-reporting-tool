# Real Data Migration - Implementation Guide

## Overview

This guide covers updating the AI Reporting Tool to work with real Qualtrics survey data (Grand_Prarie.csv) instead of POC data.

**Scope:** 11-17 hours (1.5-2 days)
**Phases:** 6 sequential phases
**Status:** Ready to implement

---

## Quick Start

### 1. Understand the Plan (30 minutes)
Read in this order:
1. **REAL_DATA_MIGRATION.md** - Complete overview (10 min)
2. **TEMPLATE_CHANGES_DETAILED.md** - Template changes (15 min)
3. **SIMPLIFIED_PLAN.md** - Quick reference (5 min)

### 2. Start Implementation (2-3 hours)
1. Read **PHASE1_CODE_EXAMPLES.md**
2. Implement Phase 1 (CSV parsing & metrics)
3. Test with Grand_Prarie.csv

### 3. Continue Phases 2-6
Follow the implementation sequence in SIMPLIFIED_PLAN.md

---

## The Plan: 6 Phases

### Phase 1: CSV Parsing & Metrics (2-3 hours)
**File:** `python/generate_reports.py`
- Schema detection (POC vs Real)
- Field mapping
- Metrics calculation (13 total)
- Update venue_data.json

### Phase 2: Metrics Registry (1-2 hours)
**File:** `python/report_engine.py`
- Add F&B metrics to registry
- Add assessment thresholds
- Add status mappings

### Phase 3: Report Content (1-2 hours)
**File:** `python/report_content.py`
- Update build_metrics_context()
- Add new metrics to context
- Add formatting functions

### Phase 4: Templates (2-3 hours)
**Files:** HTML, Markdown, PDF templates
- Add Return Likelihood + Price Value to Performance Summary
- Add Food & Beverage subsection
- Minimal layout changes

### Phase 5: AI Analysis (3-4 hours)
**Files:** Claude skill docs, `python/ai_analysis.py`
- Update metrics_analysis.md
- Update comment_analysis.md
- Update synthesis.md
- Update payload builders

### Phase 6: Testing (2-3 hours)
**Files:** New test files
- Schema detection tests
- Metrics calculation tests
- Template rendering tests
- AI analysis tests

---

## New Metrics (13 Total)

### Core (5)
- LTR (0-10)
- Fun (1-5)
- Helpful (1-5)
- Issues (%)
- Resolution (1-5)

### Customer Intent (2)
- Return Likelihood (1-5)
- Price Value (1-5)

### F&B (6)
- Food Value, Food Speed, Food Quality
- Beverage Value, Beverage Speed, Beverage Quality

---

## Documents

### Main Implementation Docs
- **REAL_DATA_MIGRATION.md** - Complete guide with all details
- **SIMPLIFIED_PLAN.md** - 6-phase plan overview
- **TEMPLATE_CHANGES_DETAILED.md** - Exact template changes with code examples

### Code Implementation
- **PHASE1_CODE_EXAMPLES.md** - Concrete code for Phase 1
- **QUICK_REFERENCE.md** - Field mappings, metrics, checklists

### Navigation
- **NEXT_STEPS.md** - What to do next
- **IMPLEMENTATION_GUIDE.md** - This file

---

## Timeline

| Phase | Time | Cumulative |
|-------|------|-----------|
| 1 | 2-3h | 2-3h |
| 2 | 1-2h | 3-5h |
| 3 | 1-2h | 4-7h |
| 4 | 2-3h | 6-10h |
| 5 | 3-4h | 9-14h |
| 6 | 2-3h | 11-17h |

**Total: 11-17 hours (1.5-2 days)**

---

## Success Criteria

✅ Grand_Prarie.csv parses correctly
✅ All 13 metrics calculated
✅ Templates render without errors
✅ F&B section appears in reports
✅ AI analysis includes F&B insights
✅ All tests pass

---

## Next Steps

1. Read **REAL_DATA_MIGRATION.md** (10 min)
2. Read **TEMPLATE_CHANGES_DETAILED.md** (15 min)
3. Confirm the approach
4. Start Phase 1 with **PHASE1_CODE_EXAMPLES.md**

---

## Questions?

- **"What are the template changes?"** → TEMPLATE_CHANGES_DETAILED.md
- **"How do I implement Phase 1?"** → PHASE1_CODE_EXAMPLES.md
- **"What's the field mapping?"** → QUICK_REFERENCE.md
- **"What are the metrics?"** → REAL_DATA_MIGRATION.md

---

Ready to start? Open **REAL_DATA_MIGRATION.md** now!

