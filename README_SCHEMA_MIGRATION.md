# Schema Migration: POC → Real Data

## 📋 What We're Doing

You have two CSV data sources:
- **POC Data** (DALLAS.csv) - Synthetic demo with 5 core metrics
- **Real Data** (Grand_Prarie.csv) - Real customer data with 5 core metrics + 8 new metrics

**Goal:** Update the analysis tool to work with BOTH schemas seamlessly, adding F&B and customer intent analysis for real data while maintaining backward compatibility.

---

## 📊 The Difference

```
                POC Data              Real Data
                ────────              ─────────
LTR Field       Q1_LTR (1-10)    →    Combined NPS (0-10)
Fun Field       Q2_FUN (text)    →    Fun (1-5 numeric)
Helpful Field   Q3_HELPFUL (text)→    Helpfulness (1-5 numeric)
Comment Field   Q6_COMMENT       →    Open Comment
F&B Metrics     ❌ None          →    ✅ 6 new fields
Return Likely   ❌ None          →    ✅ New field
Price Value     ❌ None          →    ✅ New field
```

---

## 📚 Documentation

We've created 7 comprehensive documents to guide implementation:

### Quick Start (10-15 minutes)
1. **[PLAN_SUMMARY.md](PLAN_SUMMARY.md)** ⭐ **START HERE**
   - High-level overview
   - 6-phase plan
   - Timeline and success criteria

2. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** ⭐ **KEEP HANDY**
   - Field mappings at a glance
   - Metrics calculations
   - Implementation checklists
   - Common issues & solutions

### Deep Dive (30-60 minutes)
3. **[SCHEMA_ANALYSIS.md](SCHEMA_ANALYSIS.md)**
   - Detailed field-by-field comparison
   - Data quality notes
   - Impact on analysis

4. **[SCHEMA_MIGRATION_PLAN.md](SCHEMA_MIGRATION_PLAN.md)**
   - Complete implementation plan
   - Field mapping specification
   - Backward compatibility strategy

5. **[IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)**
   - Data flow diagrams
   - Phase breakdown with details
   - Timeline estimate

### For Implementation (30 minutes)
6. **[PHASE1_CODE_EXAMPLES.md](PHASE1_CODE_EXAMPLES.md)** ⭐ **FOR CODING**
   - Concrete code examples
   - Function signatures
   - Usage examples
   - Testing code

### Navigation
7. **[SCHEMA_MIGRATION_INDEX.md](SCHEMA_MIGRATION_INDEX.md)**
   - Document index
   - Reading guide
   - Quick start paths

---

## 🚀 Implementation Plan

### Phase 1: Schema Detection & Field Mapping (2-3 hours)
**File:** `python/generate_reports.py`
- Add `detect_schema()` - Auto-detect POC vs Real
- Add `normalize_row()` - Convert to standard format
- Update `process_venue_data()` - Schema-aware processing

**Result:** Both schemas parse correctly ✅

### Phase 2: Metrics Calculation (2-3 hours)
**Files:** `python/generate_reports.py`, `python/report_engine.py`
- Add F&B metrics (6 fields)
- Add customer intent metrics (2 fields)
- Update metrics registry

**Result:** All 13 metrics calculated ✅

### Phase 3: Templates & Display (3-4 hours)
**Files:** HTML, Markdown, PDF templates, `report_content.py`
- Add F&B section to reports
- Add new metrics to Performance Summary
- Conditional rendering for optional metrics

**Result:** Reports show F&B section ✅

### Phase 4: AI Analysis Pipeline (4-5 hours)
**Files:** Claude skill docs, `ai_analysis.py`
- Update `metrics_analysis.md` - Include F&B
- Update `comment_analysis.md` - Consider F&B themes
- Update `synthesis.md` - Add F&B recommendations

**Result:** AI analysis includes F&B insights ✅

### Phase 5: Report Scripts (1-2 hours)
**Files:** `create_html_reports.py`, `create_markdown_reports.py`, `create_pdf_reports.py`
- Verify compatibility with new metrics
- Test with both schemas

**Result:** All report formats work ✅

### Phase 6: Testing & Validation (3-4 hours)
**Files:** New test files in `python/tests/`
- Schema detection tests
- Field mapping tests
- Metrics calculation tests
- AI analysis tests
- Report generation tests

**Result:** All tests pass ✅

---

## ⏱️ Timeline

| Phase | Effort | Time |
|-------|--------|------|
| 1 | Low | 2-3h |
| 2 | Medium | 2-3h |
| 3 | Medium | 3-4h |
| 4 | Medium-High | 4-5h |
| 5 | Low | 1-2h |
| 6 | Medium | 3-4h |
| **Total** | **Medium** | **15-21h** |

**Realistic estimate:** 2-3 days for experienced developer

---

## ✅ Success Criteria

- ✅ POC data works exactly as before (backward compatible)
- ✅ Real data parses correctly
- ✅ All 13 metrics calculated for real data
- ✅ F&B section appears in real data reports
- ✅ AI analysis includes F&B insights
- ✅ All report formats generate successfully
- ✅ All tests pass

---

## 🎯 Getting Started

### Option 1: Quick Understanding (15 minutes)
```
1. Read PLAN_SUMMARY.md
2. Skim QUICK_REFERENCE.md
3. You understand the plan!
```

### Option 2: Full Understanding (1 hour)
```
1. Read PLAN_SUMMARY.md
2. Read SCHEMA_ANALYSIS.md
3. Read IMPLEMENTATION_ROADMAP.md
4. Skim QUICK_REFERENCE.md
5. You're ready to implement!
```

### Option 3: Start Implementing Phase 1 (2-3 hours)
```
1. Read PHASE1_CODE_EXAMPLES.md
2. Open python/generate_reports.py
3. Add the 4 new functions
4. Test with both CSV files
5. Move to Phase 2
```

---

## 📁 Key Files

### To Modify
- `python/generate_reports.py` - Phase 1, 2
- `python/report_engine.py` - Phase 2
- `templates/venue-1page-browser.html` - Phase 3
- `templates/venue-1page-pdf.html` - Phase 3
- `templates/venue-1page-report.md.j2` - Phase 3
- `python/report_content.py` - Phase 3
- `.claude/single-venue-report/metrics_analysis.md` - Phase 4
- `.claude/single-venue-report/comment_analysis.md` - Phase 4
- `.claude/single-venue-report/synthesis.md` - Phase 4
- `python/ai_analysis.py` - Phase 4

### To Test
- `example-data/topgolf_qualtrics_30_responses - DALLAS.csv` - POC data
- `qualtrics/Grand_Prarie.csv` - Real data

---

## 🔑 Key Concepts

### Schema Detection
```python
if 'Combined NPS' in headers:
    schema = 'real'
elif 'Q1_LTR' in headers:
    schema = 'poc'
```

### Field Mapping
```
POC                Real Data              Normalized
Q1_LTR        →    Combined NPS      →    ltr
Q2_FUN        →    Fun               →    fun
Q3_HELPFUL    →    Helpfulness       →    helpful
Q6_COMMENT    →    Open Comment      →    comment
```

### Optional Metrics
- F&B metrics only in real data
- Gracefully skip if missing
- AI analysis works with or without them

### Backward Compatibility
- Single codebase, two schemas
- POC data unchanged
- Real data gets new features
- No user intervention needed

---

## 📖 Document Guide

| Document | Purpose | Read Time | Best For |
|----------|---------|-----------|----------|
| PLAN_SUMMARY.md | Overview | 10 min | Understanding the plan |
| QUICK_REFERENCE.md | Lookup | 5 min | During implementation |
| SCHEMA_ANALYSIS.md | Details | 15 min | Understanding data |
| SCHEMA_MIGRATION_PLAN.md | Complete plan | 20 min | Full context |
| IMPLEMENTATION_ROADMAP.md | Architecture | 25 min | Understanding flow |
| PHASE1_CODE_EXAMPLES.md | Code | 30 min | Implementing Phase 1 |
| SCHEMA_MIGRATION_INDEX.md | Navigation | 5 min | Finding documents |

---

## 🎓 Learning Path

### Path 1: Quick Overview
```
PLAN_SUMMARY.md (10 min)
    ↓
QUICK_REFERENCE.md (5 min)
    ↓
You understand the plan!
```

### Path 2: Full Understanding
```
PLAN_SUMMARY.md (10 min)
    ↓
SCHEMA_ANALYSIS.md (15 min)
    ↓
IMPLEMENTATION_ROADMAP.md (25 min)
    ↓
QUICK_REFERENCE.md (5 min)
    ↓
You're ready to implement!
```

### Path 3: Implementation
```
PHASE1_CODE_EXAMPLES.md (30 min)
    ↓
Code Phase 1 (2-3 hours)
    ↓
Test with both CSV files
    ↓
Repeat for Phases 2-6
```

---

## 🔍 Common Questions

**Q: Do I need to change the POC data?**
A: No! POC data continues to work exactly as before. Schema detection is automatic.

**Q: How long will this take?**
A: 15-21 hours total (2-3 days for experienced developer). Can be done incrementally.

**Q: Can I do the phases out of order?**
A: No, they're sequential. Phase 1 is foundation for everything else.

**Q: What if real data is missing F&B fields?**
A: Optional metrics gracefully skip. The tool still works.

**Q: Will AI analysis change?**
A: Yes, it will now consider F&B metrics and themes. This is intentional.

**Q: Do I need to update documentation?**
A: Yes, update AGENTS.md with new field mappings and metrics.

---

## 🚦 Status

- ✅ Plan complete
- ✅ Documentation complete
- ✅ Code examples ready
- ⏳ Implementation ready to start

**Next step:** Read PLAN_SUMMARY.md and start Phase 1!

---

## 📞 Need Help?

1. **Understanding the plan?** → Read PLAN_SUMMARY.md
2. **Understanding the data?** → Read SCHEMA_ANALYSIS.md
3. **Understanding the flow?** → Read IMPLEMENTATION_ROADMAP.md
4. **Implementing Phase 1?** → Read PHASE1_CODE_EXAMPLES.md
5. **Quick lookup?** → Use QUICK_REFERENCE.md
6. **Finding documents?** → Use SCHEMA_MIGRATION_INDEX.md

---

## 📝 Files in This Migration

```
C:\ai-reporting-tool\
├── README_SCHEMA_MIGRATION.md          ← You are here
├── PLAN_SUMMARY.md                     ← Start here
├── QUICK_REFERENCE.md                  ← Keep handy
├── SCHEMA_ANALYSIS.md
├── SCHEMA_MIGRATION_PLAN.md
├── IMPLEMENTATION_ROADMAP.md
├── PHASE1_CODE_EXAMPLES.md
└── SCHEMA_MIGRATION_INDEX.md
```

---

## 🎉 Ready?

**Let's get started!**

1. Open [PLAN_SUMMARY.md](PLAN_SUMMARY.md)
2. Understand the 6-phase plan
3. Review [PHASE1_CODE_EXAMPLES.md](PHASE1_CODE_EXAMPLES.md)
4. Start implementing Phase 1
5. Test with both CSV files
6. Proceed through phases 2-6

**You've got this! 🚀**

