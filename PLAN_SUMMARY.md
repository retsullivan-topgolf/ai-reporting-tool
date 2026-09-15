# Plan Summary: POC → Real Data Migration

## What We're Doing

You have two CSV schemas:
1. **POC Data** (DALLAS.csv) - Synthetic demo data with 5 core metrics
2. **Real Data** (Grand_Prarie.csv) - Real customer data with 5 core metrics + 8 new metrics (F&B, Return, Price)

**Goal:** Update the analysis tool to work with BOTH schemas seamlessly, adding F&B and customer intent analysis for real data while maintaining backward compatibility with POC data.

---

## Key Differences at a Glance

| Aspect | POC | Real Data |
|--------|-----|-----------|
| **LTR Field** | Q1_LTR (1-10) | Combined NPS (0-10) |
| **Fun Field** | Q2_FUN (text labels) | Fun (numeric 1-5) |
| **Helpful Field** | Q3_HELPFUL (text labels) | Helpfulness (numeric 1-5) |
| **Comment Field** | Q6_COMMENT | Open Comment |
| **F&B Metrics** | ❌ None | ✅ 6 new fields |
| **Return Likelihood** | ❌ None | ✅ New field |
| **Price Value** | ❌ None | ✅ New field |

---

## The Plan (6 Phases)

### Phase 1: Schema Detection & Field Mapping ⭐ START HERE
**File:** `python/generate_reports.py`
**Effort:** Low (2-3 hours)
**What:** Add functions to auto-detect schema and normalize rows

**Key Functions:**
- `detect_schema()` - Determine if POC or Real
- `normalize_row()` - Convert any row to standard format
- `process_venue_data()` - Calculate metrics with schema awareness

**Result:** Both schemas parse correctly, metrics calculated

---

### Phase 2: Metrics Calculation
**Files:** `python/generate_reports.py` + `python/report_engine.py`
**Effort:** Medium (2-3 hours)
**What:** Add F&B and customer intent metrics

**New Metrics:**
- Food Value, Food Speed, Food Quality
- Beverage Value, Beverage Speed, Beverage Quality
- Return Likelihood
- Price Value

**Result:** venue_data.json includes all 13 metrics (5 core + 8 new)

---

### Phase 3: Templates & Display
**Files:** HTML, Markdown, PDF templates + `report_content.py`
**Effort:** Medium (3-4 hours)
**What:** Add F&B section to reports, display new metrics

**Changes:**
- Add F&B subsection to Experience Metrics table
- Add Return Likelihood to Performance Summary
- Add Price Value to Performance Summary
- Conditional rendering (only show F&B if data present)

**Result:** Reports show F&B section for real data, unchanged for POC

---

### Phase 4: AI Analysis Pipeline ⭐ CRITICAL
**Files:** Claude skill docs + `ai_analysis.py`
**Effort:** Medium-High (4-5 hours)
**What:** Update AI analysis to consider F&B metrics and comments

**Changes:**
- `metrics_analysis.md` - Include F&B metrics in payload
- `comment_analysis.md` - Consider F&B themes in comments
- `synthesis.md` - Add F&B-specific recommendations
- `ai_analysis.py` - Update payload builders for new fields

**Result:** AI analysis includes F&B insights, recommendations consider food/beverage quality

---

### Phase 5: Report Generation Scripts
**Files:** `create_html_reports.py`, `create_markdown_reports.py`, `create_pdf_reports.py`
**Effort:** Low (1-2 hours)
**What:** Verify scripts work with new metrics

**Changes:** Minimal - these already use venue_data.json

**Result:** All report formats generate successfully with new metrics

---

### Phase 6: Testing & Validation
**Effort:** Medium (3-4 hours)
**What:** Comprehensive testing of both schemas

**Test Cases:**
- POC data works as before (backward compatibility)
- Real data parses and calculates all metrics
- F&B section appears in real data reports
- AI analysis includes F&B insights
- Optional metrics gracefully skip if missing

**Result:** All tests pass, zero regressions

---

## Implementation Sequence

```
Phase 1 (Schema Detection)
    ↓
Phase 2 (Metrics Calculation)
    ↓
Phase 4 (AI Analysis) ← Do this before templates
    ↓
Phase 3 (Templates & Display)
    ↓
Phase 5 (Report Scripts)
    ↓
Phase 6 (Testing & Validation)
```

**Why this order?**
- Phase 1 is foundation for everything
- Phase 2 creates the data structure
- Phase 4 before Phase 3 because templates need to know what analysis will produce
- Phase 5 is integration (uses Phases 1-4)
- Phase 6 validates everything

---

## What You Get

### For POC Data (DALLAS.csv)
✅ Works exactly as before
✅ No changes to output
✅ Same 5 metrics
✅ Same analysis

### For Real Data (Grand_Prarie.csv)
✅ Automatic schema detection
✅ All 13 metrics calculated
✅ F&B section in reports
✅ AI analysis includes F&B insights
✅ Return likelihood analysis
✅ Price value analysis

### For Future Data
✅ Any new schema can be added by updating field mappings
✅ Optional metrics gracefully skip if missing
✅ Single codebase handles all schemas

---

## Backward Compatibility

**Strategy:** Auto-detection + optional metrics

```python
# Schema detection
if 'Combined NPS' in row:
    schema = 'real'
elif 'Q1_LTR' in row:
    schema = 'poc'

# Field mapping
field_name = FIELD_MAPPINGS[schema][field_key]

# Optional metrics
if schema == 'real' and 'F&B Matrix_1' in row:
    calculate_fb_metrics()
```

**Result:** Single codebase, zero user friction

---

## Code Changes Summary

### New Functions
- `detect_schema(csv_file)` - Auto-detect schema
- `normalize_row(row, schema)` - Normalize to standard format
- `parse_date(date_str, schema)` - Handle date formats
- `convert_fun_to_numeric(fun_value, schema)` - Convert text to numeric
- `convert_helpful_to_numeric(helpful_value, schema)` - Convert text to numeric

### Updated Functions
- `process_venue_data(rows, schema)` - Add schema awareness
- `_build_metrics_payload()` in ai_analysis.py - Include F&B metrics
- `_build_comment_payload()` in ai_analysis.py - Use "Open Comment" field
- `build_metrics_context()` in report_content.py - Include new metrics

### New Data Structures
- `FIELD_MAPPINGS` dict - Field name mappings for both schemas
- F&B metrics in venue_data.json
- Customer intent metrics in venue_data.json

### Updated Templates
- Add F&B subsection to Experience Metrics table
- Add Return Likelihood to Performance Summary
- Add Price Value to Performance Summary
- Conditional rendering for optional metrics

### Updated Claude Skills
- metrics_analysis.md - Include F&B metrics
- comment_analysis.md - Consider F&B themes
- synthesis.md - Add F&B recommendations

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

## Success Criteria

✅ **Phase 1:** Both schemas parse correctly
✅ **Phase 2:** All metrics calculated for both schemas
✅ **Phase 3:** Templates render with new metrics
✅ **Phase 4:** AI analysis includes F&B insights
✅ **Phase 5:** All report formats generate successfully
✅ **Phase 6:** All tests pass, backward compatibility verified

---

## Documents Created

1. **SCHEMA_ANALYSIS.md** - Detailed field-by-field comparison
2. **SCHEMA_MIGRATION_PLAN.md** - Complete implementation plan with rationale
3. **IMPLEMENTATION_ROADMAP.md** - Phase breakdown with data flow diagrams
4. **PHASE1_CODE_EXAMPLES.md** - Concrete code examples for Phase 1
5. **PLAN_SUMMARY.md** - This document (quick reference)

---

## Next Steps

### Immediate (Today)
1. ✅ Review this plan
2. ✅ Review SCHEMA_ANALYSIS.md for field details
3. ✅ Review PHASE1_CODE_EXAMPLES.md for code structure

### This Week
1. Implement Phase 1 (schema detection + field mapping)
2. Test with both DALLAS.csv and Grand_Prarie.csv
3. Implement Phase 2 (metrics calculation)
4. Test metrics with both schemas

### Next Week
1. Implement Phase 4 (AI analysis updates)
2. Implement Phase 3 (templates)
3. Implement Phase 5 (report scripts)
4. Implement Phase 6 (testing)

---

## Questions to Consider

1. **Priority:** Should we do all phases at once, or phase them over time?
2. **Testing:** Should we create automated tests, or manual testing?
3. **Rollout:** Should we test with Grand_Prarie.csv first, then DALLAS.csv, or both in parallel?
4. **Documentation:** Should we update AGENTS.md with new field mappings?

---

## Key Insights

### Why This Approach Works
1. **Schema detection is automatic** - No user intervention needed
2. **Field mapping is centralized** - Easy to add new schemas
3. **Optional metrics are graceful** - Missing fields don't break anything
4. **Backward compatible** - POC data continues to work
5. **Modular phases** - Can implement incrementally

### Why F&B Matters
1. **Real customer feedback** - F&B is a significant part of the experience
2. **Actionable insights** - Can recommend specific F&B improvements
3. **Competitive advantage** - Can identify F&B as strength or weakness
4. **Customer intent** - Return likelihood and price value show loyalty/satisfaction

### Why This Matters Now
1. **Real data is here** - Grand_Prarie.csv is production data
2. **POC is working** - DALLAS.csv proves the concept
3. **Scaling opportunity** - Can now analyze multiple real venues
4. **Insights are valuable** - F&B analysis will drive business decisions

---

## Let's Get Started!

Ready to begin Phase 1? Here's what to do:

1. Open `python/generate_reports.py`
2. Review PHASE1_CODE_EXAMPLES.md
3. Add the four new functions (detect_schema, normalize_row, etc.)
4. Update process_venue_data() to use schema awareness
5. Test with both CSV files
6. Verify metrics are calculated correctly

Once Phase 1 is working, Phase 2 follows naturally from the data structure you've created.

