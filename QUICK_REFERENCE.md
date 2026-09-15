# Quick Reference: Schema Migration

## Field Mapping at a Glance

### Core Metrics (Both Schemas)

```
POC                          Real Data                    Normalized Name
─────────────────────────────────────────────────────────────────────────
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
Real Data Field                                          Normalized Name
──────────────────────────────────────────────────────────────────────
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

## Data Type Conversions

### Fun & Helpful (POC Only)

```
POC Text                    →    Numeric
────────────────────────────────────────
5 - Extremely fun           →    5
4 - Very fun                →    4
3 - Moderately fun          →    3
2 - Slightly fun            →    2
1 - Not at all fun          →    1

5 - Extremely helpful       →    5
4 - Very helpful            →    4
3 - Moderately helpful      →    3
2 - Slightly helpful        →    2
1 - Not at all helpful      →    1
```

### Date Format

```
POC Format          →    Real Format       →    Normalized
──────────────────────────────────────────────────────────
2026-08-01          →    8/1/2026          →    2026-08-01
2026-06-21          →    6/21/2026         →    2026-06-21
```

---

## Metrics Calculation

### Core Metrics (Both Schemas)

```
Metric              Calculation                     Scale
──────────────────────────────────────────────────────────
ltr_avg             Average of LTR scores           0-10
fun_avg             Average of Fun scores           1-5
helpful_avg         Average of Helpful scores       1-5
issues_pct          (Count of Yes) / Total * 100    0-100%
resolution_avg      Average of Resolution scores    1-5
                    (only when issues=Yes)
```

### F&B Metrics (Real Data Only)

```
Metric                  Calculation                     Scale
─────────────────────────────────────────────────────────────
food_value_avg          Average of Food Value scores    1-5
food_speed_avg          Average of Food Speed scores    1-5
food_quality_avg        Average of Food Quality scores  1-5
beverage_value_avg      Average of Beverage Value       1-5
beverage_speed_avg      Average of Beverage Speed       1-5
beverage_quality_avg    Average of Beverage Quality     1-5
return_likelihood_avg   Average of Return Likelihood    1-5
price_value_avg         Average of Price Value          1-5
```

---

## Schema Detection Logic

```python
def detect_schema(csv_file):
    if 'Combined NPS' in headers:
        return 'real'
    elif 'Q1_LTR' in headers:
        return 'poc'
    else:
        raise ValueError("Unknown schema")
```

---

## Venue Data JSON Structure

### POC Data Output

```json
{
  "venue": "Dallas",
  "responses": 30,
  "date_range": ["2026-08-01", "2026-08-31"],
  "ltr_avg": 8.5,
  "fun_avg": 4.2,
  "helpful_avg": 4.1,
  "issues_pct": 20.0,
  "resolution_avg": 4.5,
  "comments": ["Great experience!", "..."],
  "high_ltr_comments": ["..."],
  "low_ltr_comments": ["..."]
}
```

### Real Data Output

```json
{
  "venue": "Grand Prairie",
  "responses": 45,
  "date_range": ["2026-01-16", "2026-06-21"],
  "ltr_avg": 7.8,
  "fun_avg": 4.0,
  "helpful_avg": 3.9,
  "issues_pct": 15.0,
  "resolution_avg": 3.0,
  "food_value_avg": 3.8,
  "food_speed_avg": 3.5,
  "food_quality_avg": 3.9,
  "beverage_value_avg": 3.7,
  "beverage_speed_avg": 3.6,
  "beverage_quality_avg": 4.0,
  "return_likelihood_avg": 3.8,
  "price_value_avg": 3.2,
  "comments": ["Very clean!", "..."],
  "high_ltr_comments": ["..."],
  "low_ltr_comments": ["..."]
}
```

---

## Phase 1 Implementation Checklist

- [ ] Add `detect_schema()` function
- [ ] Add `FIELD_MAPPINGS` dict
- [ ] Add `get_field_value()` function
- [ ] Add `parse_date()` function
- [ ] Add `convert_fun_to_numeric()` function
- [ ] Add `convert_helpful_to_numeric()` function
- [ ] Add `normalize_row()` function
- [ ] Update `process_venue_data()` to use normalization
- [ ] Test with DALLAS.csv
- [ ] Test with Grand_Prarie.csv
- [ ] Verify metrics match expected values

---

## Phase 2 Implementation Checklist

- [ ] Add F&B metrics calculation in `process_venue_data()`
- [ ] Add customer intent metrics calculation
- [ ] Update `venue_data.json` structure
- [ ] Add metrics to `report_engine.py` registry
- [ ] Add assessment thresholds for new metrics
- [ ] Test metrics calculation with real data
- [ ] Verify optional metrics skip gracefully if missing

---

## Phase 3 Implementation Checklist

- [ ] Add F&B subsection to HTML template
- [ ] Add F&B subsection to PDF template
- [ ] Add F&B subsection to Markdown template
- [ ] Add Return Likelihood to Performance Summary
- [ ] Add Price Value to Performance Summary
- [ ] Update `build_metrics_context()` in report_content.py
- [ ] Test template rendering with real data
- [ ] Verify POC data reports unchanged

---

## Phase 4 Implementation Checklist

- [ ] Update `metrics_analysis.md` to include F&B metrics
- [ ] Update `comment_analysis.md` to consider F&B themes
- [ ] Update `synthesis.md` to add F&B recommendations
- [ ] Update `_build_metrics_payload()` in ai_analysis.py
- [ ] Update `_build_comment_payload()` in ai_analysis.py
- [ ] Test metrics_analysis with F&B metrics
- [ ] Test comment_analysis with real data
- [ ] Test synthesis with F&B insights

---

## Phase 5 Implementation Checklist

- [ ] Verify `create_html_reports.py` works with new metrics
- [ ] Verify `create_markdown_reports.py` works with new metrics
- [ ] Verify `create_pdf_reports.py` works with new metrics
- [ ] Verify `generate_all_reports.py` works with both schemas
- [ ] Test end-to-end with POC data
- [ ] Test end-to-end with real data

---

## Phase 6 Implementation Checklist

- [ ] Create test_schema_detection.py
- [ ] Create test_field_mapping.py
- [ ] Create test_metrics_calculation.py
- [ ] Create test_ai_analysis.py
- [ ] Create test_reports.py
- [ ] Run all tests with POC data
- [ ] Run all tests with real data
- [ ] Verify backward compatibility
- [ ] Verify no regressions

---

## Common Issues & Solutions

### Issue: "Unknown schema"
**Cause:** CSV doesn't have expected key fields
**Solution:** Check field names match exactly (case-sensitive)

### Issue: Fun/Helpful values are None
**Cause:** POC text labels not matching conversion map
**Solution:** Verify exact text in CSV (e.g., "5 - Extremely fun" vs "5-Extremely fun")

### Issue: Date parsing fails
**Cause:** Date format not recognized
**Solution:** Check date format (YYYY-MM-DD for POC, M/D/YYYY for real)

### Issue: F&B metrics are empty
**Cause:** Real data missing F&B fields
**Solution:** This is OK - optional metrics gracefully skip if missing

### Issue: AI analysis doesn't mention F&B
**Cause:** Claude skills not updated with F&B metrics
**Solution:** Update metrics_analysis.md, comment_analysis.md, synthesis.md

---

## Testing Commands

```bash
# Test Phase 1: Schema Detection
cd python
python -c "
from generate_reports import detect_schema
print(detect_schema('../example-data/topgolf_qualtrics_30_responses - DALLAS.csv'))
print(detect_schema('../qualtrics/Grand_Prarie.csv'))
"

# Test Phase 2: Metrics Calculation
python generate_reports.py ../example-data/topgolf_qualtrics_30_responses\ -\ DALLAS.csv
python generate_reports.py ../qualtrics/Grand_Prarie.csv

# Test Phase 3: Report Generation
python create_html_reports.py venue_data.json
python create_markdown_reports.py venue_data.json
python create_pdf_reports.py venue_data.json

# Test Phase 4: AI Analysis
python generate_ai_analysis.py venue_data.json

# Test Phase 5: Full Pipeline
python generate_all_reports.py ../example-data/topgolf_qualtrics_30_responses\ -\ DALLAS.csv --format all
python generate_all_reports.py ../qualtrics/Grand_Prarie.csv --format all
```

---

## Files to Modify

### Phase 1
- `python/generate_reports.py` - Add schema detection, field mapping, normalization

### Phase 2
- `python/generate_reports.py` - Add F&B metrics calculation
- `python/report_engine.py` - Add F&B metrics to registry

### Phase 3
- `templates/venue-1page-browser.html` - Add F&B section
- `templates/venue-1page-pdf.html` - Add F&B section
- `templates/venue-1page-report.md.j2` - Add F&B section
- `python/report_content.py` - Update metrics context

### Phase 4
- `.claude/single-venue-report/metrics_analysis.md` - Include F&B metrics
- `.claude/single-venue-report/comment_analysis.md` - Consider F&B themes
- `.claude/single-venue-report/synthesis.md` - Add F&B recommendations
- `python/ai_analysis.py` - Update payload builders

### Phase 5
- `python/create_html_reports.py` - Verify compatibility
- `python/create_markdown_reports.py` - Verify compatibility
- `python/create_pdf_reports.py` - Verify compatibility
- `python/generate_all_reports.py` - Verify compatibility

### Phase 6
- Create new test files in `python/tests/`

---

## Key Metrics Thresholds

### Core Metrics (Existing)
```
LTR:        8-10 = Excellent, 6-7 = Good, 4-5 = Fair, 0-3 = Poor
Fun:        4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Helpful:    4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Issues:     0-10% = Excellent, 10-20% = Good, 20-30% = Fair, 30%+ = Poor
Resolution: 4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
```

### F&B Metrics (New)
```
Food Value:         4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Food Speed:         4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Food Quality:       4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Beverage Value:     4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Beverage Speed:     4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Beverage Quality:   4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Return Likelihood:  4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Price Value:        4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
```

---

## Summary

**Total Effort:** 15-21 hours
**Phases:** 6 (sequential)
**Backward Compatibility:** ✅ Full
**New Features:** ✅ F&B analysis, Return likelihood, Price value

Ready to start Phase 1? See PHASE1_CODE_EXAMPLES.md for concrete code.

