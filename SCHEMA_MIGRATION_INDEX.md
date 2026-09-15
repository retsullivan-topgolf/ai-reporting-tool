# Schema Migration Documentation Index

## Overview

This folder contains a complete plan to update the AI Reporting Tool to work with real Qualtrics data (Grand_Prarie.csv) while maintaining backward compatibility with POC data (DALLAS.csv).

**Status:** Plan complete, ready for implementation
**Total Effort:** 15-21 hours (2-3 days)
**Phases:** 6 sequential phases

---

## Documents

### 1. **PLAN_SUMMARY.md** ⭐ START HERE
**What:** High-level overview of the entire plan
**For:** Quick understanding of what needs to be done
**Read Time:** 10 minutes

**Contains:**
- What we're doing and why
- Key differences between schemas
- 6-phase implementation plan
- Timeline and success criteria
- Next steps

**👉 Read this first to understand the big picture**

---

### 2. **QUICK_REFERENCE.md** ⭐ KEEP HANDY
**What:** Quick lookup reference for field mappings and metrics
**For:** During implementation as a quick reference
**Read Time:** 5 minutes (reference)

**Contains:**
- Field mapping at a glance
- Data type conversions
- Metrics calculation formulas
- Implementation checklists for each phase
- Common issues & solutions
- Testing commands

**👉 Keep this open while implementing**

---

### 3. **SCHEMA_ANALYSIS.md**
**What:** Detailed field-by-field comparison of both schemas
**For:** Understanding the data structure differences
**Read Time:** 15 minutes

**Contains:**
- Complete field comparison table
- POC vs Real data overview
- Detailed field mapping
- Impact on analysis
- Data quality notes
- Implementation complexity assessment

**👉 Read this to understand the data**

---

### 4. **SCHEMA_MIGRATION_PLAN.md**
**What:** Complete implementation plan with rationale
**For:** Understanding the approach and why each phase exists
**Read Time:** 20 minutes

**Contains:**
- Detailed schema comparison
- Key differences summary
- 6-phase implementation plan with details
- Field mapping specification
- Implementation sequence rationale
- Backward compatibility strategy
- File changes required

**👉 Read this for the complete plan**

---

### 5. **IMPLEMENTATION_ROADMAP.md**
**What:** Data flow diagrams and phase breakdown
**For:** Understanding how data flows through the system
**Read Time:** 25 minutes

**Contains:**
- Data flow architecture diagram
- Detailed phase breakdown (1-6)
- What each phase does
- Inputs and outputs for each phase
- Implementation checklist
- Timeline estimate

**👉 Read this to understand the architecture**

---

### 6. **PHASE1_CODE_EXAMPLES.md** ⭐ FOR IMPLEMENTATION
**What:** Concrete code examples for Phase 1
**For:** Implementing Phase 1 (schema detection & field mapping)
**Read Time:** 30 minutes

**Contains:**
- Function 1: Schema detection
- Function 2: Field mapping
- Function 3: Row normalization
- Function 4: Updated process_venue_data
- Integration into main script
- Testing examples

**👉 Use this to implement Phase 1**

---

## Reading Guide

### If you have 10 minutes:
1. Read **PLAN_SUMMARY.md**
2. Skim **QUICK_REFERENCE.md**

### If you have 30 minutes:
1. Read **PLAN_SUMMARY.md**
2. Read **SCHEMA_ANALYSIS.md**
3. Skim **QUICK_REFERENCE.md**

### If you have 1 hour:
1. Read **PLAN_SUMMARY.md**
2. Read **SCHEMA_ANALYSIS.md**
3. Read **IMPLEMENTATION_ROADMAP.md** (skim data flow)
4. Skim **QUICK_REFERENCE.md**

### If you have 2 hours:
1. Read **PLAN_SUMMARY.md**
2. Read **SCHEMA_ANALYSIS.md**
3. Read **SCHEMA_MIGRATION_PLAN.md**
4. Read **IMPLEMENTATION_ROADMAP.md**
5. Skim **PHASE1_CODE_EXAMPLES.md**
6. Skim **QUICK_REFERENCE.md**

### If you're implementing Phase 1:
1. Read **PLAN_SUMMARY.md** (Phase 1 section)
2. Read **PHASE1_CODE_EXAMPLES.md** (all of it)
3. Keep **QUICK_REFERENCE.md** open
4. Reference **SCHEMA_ANALYSIS.md** as needed

---

## Implementation Phases

### Phase 1: Schema Detection & Field Mapping
**Status:** Ready to implement
**Effort:** Low (2-3 hours)
**File:** `python/generate_reports.py`
**Code Examples:** PHASE1_CODE_EXAMPLES.md

**What:** Add functions to auto-detect schema and normalize rows
- `detect_schema()` - Determine if POC or Real
- `normalize_row()` - Convert any row to standard format
- `process_venue_data()` - Calculate metrics with schema awareness

**Result:** Both schemas parse correctly, metrics calculated

---

### Phase 2: Metrics Calculation
**Status:** Ready to implement (after Phase 1)
**Effort:** Medium (2-3 hours)
**Files:** `python/generate_reports.py`, `python/report_engine.py`

**What:** Add F&B and customer intent metrics
- Food Value, Food Speed, Food Quality
- Beverage Value, Beverage Speed, Beverage Quality
- Return Likelihood
- Price Value

**Result:** venue_data.json includes all 13 metrics

---

### Phase 3: Templates & Display
**Status:** Ready to implement (after Phase 2)
**Effort:** Medium (3-4 hours)
**Files:** HTML, Markdown, PDF templates, `report_content.py`

**What:** Add F&B section to reports, display new metrics
- Add F&B subsection to Experience Metrics table
- Add Return Likelihood to Performance Summary
- Add Price Value to Performance Summary

**Result:** Reports show F&B section for real data

---

### Phase 4: AI Analysis Pipeline
**Status:** Ready to implement (before Phase 3)
**Effort:** Medium-High (4-5 hours)
**Files:** Claude skill docs, `ai_analysis.py`

**What:** Update AI analysis to consider F&B metrics
- `metrics_analysis.md` - Include F&B metrics
- `comment_analysis.md` - Consider F&B themes
- `synthesis.md` - Add F&B recommendations
- `ai_analysis.py` - Update payload builders

**Result:** AI analysis includes F&B insights

---

### Phase 5: Report Generation Scripts
**Status:** Ready to implement (after Phase 4)
**Effort:** Low (1-2 hours)
**Files:** `create_html_reports.py`, `create_markdown_reports.py`, `create_pdf_reports.py`

**What:** Verify scripts work with new metrics
- Minimal code changes needed
- Test with both schemas

**Result:** All report formats generate successfully

---

### Phase 6: Testing & Validation
**Status:** Ready to implement (after Phase 5)
**Effort:** Medium (3-4 hours)
**Files:** New test files in `python/tests/`

**What:** Comprehensive testing of both schemas
- Schema detection tests
- Field mapping tests
- Metrics calculation tests
- AI analysis tests
- Report generation tests

**Result:** All tests pass, zero regressions

---

## Key Concepts

### Schema Detection
Automatically determine which schema is being used by checking for key fields:
- If `Combined NPS` present → Real Data schema
- If `Q1_LTR` present → POC schema

### Field Mapping
Convert field names from either schema to normalized names:
- `Q1_LTR` / `Combined NPS` → `ltr`
- `Q2_FUN` / `Fun` → `fun`
- `Q6_COMMENT` / `Open Comment` → `comment`

### Data Normalization
Convert data types to standard formats:
- Text labels → Numeric (Fun, Helpful in POC)
- Date formats → YYYY-MM-DD (Visit Date)
- Yes/No → Boolean (Issues)

### Optional Metrics
F&B metrics are optional - gracefully skip if missing:
- If fields present → calculate and include
- If fields missing → skip gracefully
- AI analysis works with or without them

### Backward Compatibility
Single codebase handles both schemas:
- POC data works exactly as before
- Real data gets new features
- No user intervention needed

---

## Quick Start

### To understand the plan (15 minutes):
```
1. Read PLAN_SUMMARY.md
2. Skim QUICK_REFERENCE.md
3. You're ready to discuss!
```

### To implement Phase 1 (2-3 hours):
```
1. Read PHASE1_CODE_EXAMPLES.md
2. Open python/generate_reports.py
3. Add the 4 new functions
4. Test with both CSV files
5. Verify metrics are correct
```

### To implement all phases (15-21 hours):
```
1. Follow the implementation sequence (Phase 1 → 6)
2. Use QUICK_REFERENCE.md as a checklist
3. Reference specific documents as needed
4. Test after each phase
```

---

## Success Criteria

✅ **Phase 1:** Both schemas parse correctly
✅ **Phase 2:** All metrics calculated for both schemas
✅ **Phase 3:** Templates render with new metrics
✅ **Phase 4:** AI analysis includes F&B insights
✅ **Phase 5:** All report formats generate successfully
✅ **Phase 6:** All tests pass, backward compatibility verified

---

## Files to Modify

### Phase 1
- `python/generate_reports.py`

### Phase 2
- `python/generate_reports.py`
- `python/report_engine.py`

### Phase 3
- `templates/venue-1page-browser.html`
- `templates/venue-1page-pdf.html`
- `templates/venue-1page-report.md.j2`
- `python/report_content.py`

### Phase 4
- `.claude/single-venue-report/metrics_analysis.md`
- `.claude/single-venue-report/comment_analysis.md`
- `.claude/single-venue-report/synthesis.md`
- `python/ai_analysis.py`

### Phase 5
- `python/create_html_reports.py` (verify)
- `python/create_markdown_reports.py` (verify)
- `python/create_pdf_reports.py` (verify)
- `python/generate_all_reports.py` (verify)

### Phase 6
- Create new test files in `python/tests/`

---

## Timeline

| Phase | Effort | Time | Cumulative |
|-------|--------|------|-----------|
| 1 | Low | 2-3h | 2-3h |
| 2 | Medium | 2-3h | 4-6h |
| 3 | Medium | 3-4h | 7-10h |
| 4 | Medium-High | 4-5h | 11-15h |
| 5 | Low | 1-2h | 12-17h |
| 6 | Medium | 3-4h | 15-21h |

**Total:** 15-21 hours (2-3 days for experienced developer)

---

## Questions?

Refer to the appropriate document:
- **"What are we doing?"** → PLAN_SUMMARY.md
- **"How do the schemas differ?"** → SCHEMA_ANALYSIS.md
- **"What's the implementation plan?"** → SCHEMA_MIGRATION_PLAN.md
- **"How does data flow?"** → IMPLEMENTATION_ROADMAP.md
- **"How do I implement Phase 1?"** → PHASE1_CODE_EXAMPLES.md
- **"What's the field mapping?"** → QUICK_REFERENCE.md

---

## Next Steps

1. ✅ Review PLAN_SUMMARY.md
2. ✅ Review SCHEMA_ANALYSIS.md
3. ✅ Review PHASE1_CODE_EXAMPLES.md
4. Start implementing Phase 1
5. Test with both DALLAS.csv and Grand_Prarie.csv
6. Proceed through phases 2-6

**Ready to begin? Start with PLAN_SUMMARY.md!**

