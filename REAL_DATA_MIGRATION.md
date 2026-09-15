# Real Data Migration - Complete Guide

## Status Update

✅ **No backward compatibility needed** - Simplifies everything
✅ **Minimal template changes** - Preserve layout, add rows/sections
✅ **Focused implementation** - 11-17 hours (1.5-2 days)

---

## What We're Doing

Updating the AI Reporting Tool to work with **real Qualtrics survey data** (Grand_Prarie.csv) instead of POC synthetic data (DALLAS.csv).

**Real data has:**
- 5 core metrics (LTR, Fun, Helpful, Issues, Resolution)
- 6 F&B metrics (food/beverage value, speed, quality)
- 2 customer intent metrics (return likelihood, price value)
- Operational data (email, bay #, bay host, time)

**Total: 13 metrics** (vs 5 in POC)

---

## The Plan: 6 Phases (11-17 hours)

### Phase 1: CSV Parsing & Metrics (2-3 hours)
**File:** `python/generate_reports.py`

Add schema detection and metrics calculation:
- Detect POC vs Real schema
- Map field names
- Calculate all 13 metrics
- Update venue_data.json

**Result:** venue_data.json with all metrics

---

### Phase 2: Metrics Registry (1-2 hours)
**File:** `python/report_engine.py`

Add new metrics to the registry:
- F&B metrics (6)
- Customer intent metrics (2)
- Assessment thresholds
- Status class mappings

**Result:** Metrics properly assessed

---

### Phase 3: Report Content (1-2 hours)
**File:** `python/report_content.py`

Update the metrics context builder:
- Add new metrics to context dict
- Add formatting functions
- Add conditional logic

**Result:** Context includes all metrics

---

### Phase 4: Templates (2-3 hours)
**Files:** HTML, Markdown, PDF templates

**Minimal layout changes:**
- Add Return Likelihood + Price Value to Performance Summary (2 rows)
- Add Food & Beverage subsection to Experience Metrics (new table)
- Keep existing layout intact

**See:** TEMPLATE_CHANGES_DETAILED.md for exact changes

**Result:** Reports show new metrics

---

### Phase 5: AI Analysis (3-4 hours)
**Files:** Claude skill docs, `python/ai_analysis.py`

Update AI analysis to consider F&B:
- Update metrics_analysis.md (include F&B metrics)
- Update comment_analysis.md (consider F&B themes)
- Update synthesis.md (add F&B recommendations)
- Update payload builders

**Result:** AI analysis includes F&B insights

---

### Phase 6: Testing (2-3 hours)
**Files:** New test files

Comprehensive testing:
- Schema detection
- Metrics calculation
- Template rendering
- AI analysis
- End-to-end pipeline

**Result:** All tests pass

---

## Key Documents

### For Understanding the Plan
- **SIMPLIFIED_PLAN.md** - This simplified 6-phase plan (read this!)
- **TEMPLATE_CHANGES_DETAILED.md** - Exact template changes (read before Phase 4)

### For Implementation Details
- **PHASE1_CODE_EXAMPLES.md** - Code examples for Phase 1
- **QUICK_REFERENCE.md** - Field mappings, metrics, checklists

### For Reference
- **SCHEMA_ANALYSIS.md** - Detailed field comparison
- **SCHEMA_MIGRATION_PLAN.md** - Original comprehensive plan

---

## Template Changes (Minimal)

### Markdown Template

**Performance Summary:** Add 2 rows
```markdown
| Return Likelihood | {{ return_likelihood_avg_display }} / 5 | {{ return_likelihood_assessment }} |
| Price Value | {{ price_value_avg_display }} / 5 | {{ price_value_assessment }} |
```

**New subsection:** Add F&B table
```markdown
### Food & Beverage Experience

| Attribute | Score | Assessment |
|---|---:|---|
| Food Value | {{ food_value_avg_display }} / 5 | {{ food_value_assessment }} |
| Food Speed | {{ food_speed_avg_display }} / 5 | {{ food_speed_assessment }} |
| Food Quality | {{ food_quality_avg_display }} / 5 | {{ food_quality_assessment }} |
| Beverage Value | {{ beverage_value_avg_display }} / 5 | {{ beverage_value_assessment }} |
| Beverage Speed | {{ beverage_speed_avg_display }} / 5 | {{ beverage_speed_assessment }} |
| Beverage Quality | {{ beverage_quality_avg_display }} / 5 | {{ beverage_quality_assessment }} |
```

### HTML Template

**Metric cards:** Add 2 cards
```html
<div class="metric-card">
    <h3>Return Likelihood</h3>
    <p class="metric-value">{{ return_likelihood_avg_display }}</p>
    <p class="metric-status">{{ return_likelihood_assessment }}</p>
</div>

<div class="metric-card">
    <h3>Price Value</h3>
    <p class="metric-value">{{ price_value_avg_display }}</p>
    <p class="metric-status">{{ price_value_assessment }}</p>
</div>
```

**New subsection:** Add F&B table
```html
<h3 class="section-subtitle">Food & Beverage Experience</h3>
<table class="metrics-table">
    <thead>
        <tr>
            <th>Attribute</th>
            <th>Score</th>
            <th>Assessment</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Food Value</td>
            <td class="status-{{ food_value_status }}">{{ food_value_avg_display }} / 5</td>
            <td>{{ food_value_assessment }}</td>
        </tr>
        <!-- 5 more F&B rows -->
    </tbody>
</table>
```

**See:** TEMPLATE_CHANGES_DETAILED.md for complete changes

---

## Field Mapping

### Core Metrics (Both Schemas)

```
POC                          Real Data                    Normalized
─────────────────────────────────────────────────────────────────────
Q1_LTR (1-10)           →    Combined NPS (0-10)      →   ltr
Q2_FUN (text)           →    Fun (1-5)                →   fun
Q3_HELPFUL (text)       →    Helpfulness (1-5)        →   helpful
Q4_ISSUES (Yes/No)      →    Issues During Visit      →   issues
Q5_ISSUE_RESOLUTION     →    Issue Resolution Sat     →   resolution
Q6_COMMENT              →    Open Comment             →   comment
VisitDate (YYYY-MM-DD)  →    Visit Date (M/D/YYYY)   →   visit_date
Venue                   →    Venue                    →   venue
```

### New Metrics (Real Data Only)

```
Real Data Field                                          Normalized
──────────────────────────────────────────────────────────────────
F&B Matrix_1 - Value for food                        →   food_value
F&B Matrix_2 - Speed of food service                 →   food_speed
F&B Matrix_3 - Food quality                          →   food_quality
F&B Matrix_4 - Value for beverages                   →   beverage_value
F&B Matrix_5 - Speed of beverage service             →   beverage_speed
F&B Matrix_6 - Beverage quality                      →   beverage_quality
Likelihood to Return                                 →   return_likelihood
Price Value                                          →   price_value
```

---

## Metrics Overview

### Core Metrics (5)
- **LTR** (0-10 scale) - Likelihood to Recommend
- **Fun** (1-5 scale) - How much fun did you have
- **Helpful** (1-5 scale) - Helpfulness of staff
- **Issues** (%) - Percentage experiencing issues
- **Resolution** (1-5 scale) - Satisfaction with issue resolution

### Customer Intent Metrics (2)
- **Return Likelihood** (1-5 scale) - Likelihood to return
- **Price Value** (1-5 scale) - Value perception

### F&B Metrics (6)
- **Food Value** (1-5) - Value for price of food
- **Food Speed** (1-5) - Speed of food service
- **Food Quality** (1-5) - Food quality
- **Beverage Value** (1-5) - Value for price of beverages
- **Beverage Speed** (1-5) - Speed of beverage service
- **Beverage Quality** (1-5) - Beverage quality

**Total: 13 metrics**

---

## Assessment Thresholds

### 1-5 Scale Metrics (8 metrics)
```
4.5-5.0   = Excellent
3.5-4.4   = Good
2.5-3.4   = Fair
0.0-2.4   = Poor
```

### LTR (0-10 Scale)
```
8-10      = Excellent
6-7       = Good
4-5       = Fair
0-3       = Poor
```

### Issues (Percentage)
```
0-10%     = Excellent
10-20%    = Good
20-30%    = Fair
30%+      = Poor
```

---

## Implementation Checklist

### Phase 1: CSV Parsing & Metrics
- [ ] Add detect_schema() function
- [ ] Add field mapping logic
- [ ] Add metrics calculation for new fields
- [ ] Update venue_data.json structure
- [ ] Test with Grand_Prarie.csv

### Phase 2: Metrics Registry
- [ ] Add F&B metrics to registry
- [ ] Add customer intent metrics to registry
- [ ] Add assessment thresholds
- [ ] Add status class mappings
- [ ] Test metrics assessment

### Phase 3: Report Content
- [ ] Update build_metrics_context()
- [ ] Add new metrics to context dict
- [ ] Add formatting functions
- [ ] Add conditional logic
- [ ] Test context generation

### Phase 4: Templates
- [ ] Update Markdown template (Performance Summary + F&B section)
- [ ] Update HTML template (metric cards + F&B section)
- [ ] Update PDF template (same as HTML)
- [ ] Test template rendering
- [ ] Verify layout

### Phase 5: AI Analysis
- [ ] Update metrics_analysis.md
- [ ] Update comment_analysis.md
- [ ] Update synthesis.md
- [ ] Update payload builders in ai_analysis.py
- [ ] Test AI analysis

### Phase 6: Testing
- [ ] Create schema detection tests
- [ ] Create metrics calculation tests
- [ ] Create template rendering tests
- [ ] Create AI analysis tests
- [ ] Create end-to-end tests
- [ ] Run all tests

---

## Timeline

| Phase | Effort | Time | Cumulative |
|-------|--------|------|-----------|
| 1 | Low | 2-3h | 2-3h |
| 2 | Low | 1-2h | 3-5h |
| 3 | Low | 1-2h | 4-7h |
| 4 | Medium | 2-3h | 6-10h |
| 5 | Medium | 3-4h | 9-14h |
| 6 | Medium | 2-3h | 11-17h |

**Total: 11-17 hours (1.5-2 days)**

---

## Success Criteria

✅ Grand_Prarie.csv parses correctly
✅ All 13 metrics calculated
✅ Templates render without errors
✅ F&B section appears in reports
✅ AI analysis includes F&B insights
✅ All tests pass
✅ Layout unchanged (minimal visual impact)

---

## Next Steps

### Today
1. Read SIMPLIFIED_PLAN.md
2. Read TEMPLATE_CHANGES_DETAILED.md
3. Confirm the approach

### This Week
1. Implement Phase 1 (CSV parsing)
2. Test with Grand_Prarie.csv
3. Implement Phase 2 (metrics registry)
4. Implement Phase 3 (report content)

### Next Week
1. Implement Phase 5 (AI analysis)
2. Implement Phase 4 (templates)
3. Implement Phase 6 (testing)
4. Verify everything works

---

## Questions?

**"What are the exact template changes?"**
→ See TEMPLATE_CHANGES_DETAILED.md

**"What's the field mapping?"**
→ See QUICK_REFERENCE.md or SCHEMA_ANALYSIS.md

**"How do I implement Phase 1?"**
→ See PHASE1_CODE_EXAMPLES.md

**"What are the metrics?"**
→ See this document (Metrics Overview section)

---

## Key Takeaways

1. **No backward compatibility** - Simplifies everything
2. **Minimal template changes** - Just add rows and a subsection
3. **11-17 hours total** - 1.5-2 days of work
4. **6 sequential phases** - Clear implementation path
5. **13 metrics total** - 5 core + 2 intent + 6 F&B

---

## Ready to Start?

1. ✅ Review SIMPLIFIED_PLAN.md
2. ✅ Review TEMPLATE_CHANGES_DETAILED.md
3. → Begin Phase 1 (CSV parsing)

Let's build this! 🚀

