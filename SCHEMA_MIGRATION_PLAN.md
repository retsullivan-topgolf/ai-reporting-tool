# Schema Migration Plan: POC → Real Data

## 1. SCHEMA COMPARISON

### Current POC Schema (example-data/topgolf_qualtrics_30_responses - DALLAS.csv)

**Key Fields:**
- `Venue` - Venue name (e.g., "Dallas")
- `VisitDate` - Date of visit (YYYY-MM-DD format)
- `Q1_LTR` - Likelihood to Recommend (1-10 numeric scale)
- `Q2_FUN` - Fun level (text: "5 - Extremely fun", "4 - Very fun", etc.)
- `Q3_HELPFUL` - Helpfulness (text: "5 - Extremely helpful", "4 - Very helpful", etc.)
- `Q4_ISSUES` - Did you experience issues? (Yes/No)
- `Q5_ISSUE_RESOLUTION` - Issue resolution satisfaction (1-5 numeric scale, only if Q4=Yes)
- `Q6_COMMENT` - Free-text guest comment

**Metadata Fields (not used in analysis):**
- StartDate, EndDate, Status, IPAddress, Progress, Duration, Finished, RecordedDate, ResponseId, DistributionChannel, UserLanguage

**Analysis Metrics:**
- LTR (Likelihood to Recommend): 1-10 scale
- Fun: 5-point scale (text-to-numeric conversion)
- Helpful: 5-point scale (text-to-numeric conversion)
- Issues: Yes/No → percentage
- Resolution: 1-5 scale (when issues=Yes)
- Comments: Free-text field

---

### Real Data Schema (qualtrics/Grand_Prarie.csv)

**Key Fields:**
- `Email Address` - Respondent email
- `Venue` - Venue name (e.g., "Grand Prairie")
- `Visit Date (+00:00 GMT)` - Date of visit (M/D/YYYY format)
- `Hour ID` - Time of visit (HH:MM format)
- `Bay Number` - Bay/lane number
- `Bayhost` - Bay host name
- `Helpfulness - How satisfied were you with the overall helpfulness of our staff?` - 1-5 numeric scale
- `Fun - How much fun did you have during your visit at Topgolf [Field-Venue_Name]?` - 1-5 numeric scale
- **F&B Matrix Fields (NEW):**
  - `F&B Matrix_1 - Value for the price you paid for food` - 1-5 scale
  - `F&B Matrix_4 - Value for the price you paid for beverages` - 1-5 scale
  - `F&B Matrix_2 - Speed of food service` - 1-5 scale
  - `F&B Matrix_5 - Speed of beverage service` - 1-5 scale
  - `F&B Matrix_3 - Food quality` - 1-5 scale
  - `F&B Matrix_6 - Beverage quality` - 1-5 scale
- `Issues During Visit` - Yes/No
- `Issue Resolution Sat` - 1-5 numeric scale (when Issues=Yes)
- `Combined NPS` - 0-10 numeric scale (replaces Q1_LTR)
- `Likelihood to Return - How likely are you to return to this or another Topgolf venue?` - 1-5 numeric scale (NEW)
- `Price Value - How would you rate Topgolf's price compared to the value of your experience...?` - 1-5 numeric scale (NEW)
- `Open Comment` - Free-text guest comment

---

## 2. KEY DIFFERENCES SUMMARY

| Aspect | POC | Real Data | Impact |
|--------|-----|-----------|--------|
| **LTR Scale** | 1-10 (Q1_LTR) | 0-10 (Combined NPS) | Field name changes; scale compatible |
| **Fun Scale** | Text labels → 1-5 (Q2_FUN) | Direct 1-5 numeric (Fun) | Simpler parsing; no text conversion needed |
| **Helpful Scale** | Text labels → 1-5 (Q3_HELPFUL) | Direct 1-5 numeric (Helpfulness) | Simpler parsing; no text conversion needed |
| **Issues** | Yes/No (Q4_ISSUES) | Yes/No (Issues During Visit) | Field name changes; logic same |
| **Resolution** | 1-5 when issues=Yes (Q5_ISSUE_RESOLUTION) | 1-5 when issues=Yes (Issue Resolution Sat) | Field name changes; logic same |
| **Comments** | Single field (Q6_COMMENT) | Single field (Open Comment) | Field name changes; logic same |
| **F&B Metrics** | ❌ Not present | ✅ 6 new fields | **NEW: Food/Beverage analysis** |
| **Return Likelihood** | ❌ Not present | ✅ New field | **NEW: Can measure repeat visit intent** |
| **Price Value** | ❌ Not present | ✅ New field | **NEW: Can measure value perception** |
| **Additional Data** | Limited | Email, Bay #, Bay Host, Hour ID | Better operational insights |

---

## 3. IMPLEMENTATION PLAN

### Phase 1: CSV Parsing & Data Normalization ✅ FOUNDATION
**File:** `python/generate_reports.py`

**Changes:**
1. Add field mapping logic to handle both schemas
2. Create a `normalize_row()` function that:
   - Maps old field names to new field names (or vice versa)
   - Converts Fun/Helpful from text to numeric if needed
   - Handles date format differences (YYYY-MM-DD vs M/D/YYYY)
   - Extracts comments from correct field
3. Update venue filtering to work with both schemas
4. Add schema detection logic (auto-detect which schema is being used)

**Key Functions to Update:**
- `process_venue_data()` - Add field mapping
- Add `detect_schema()` function
- Add `normalize_row()` function

---

### Phase 2: Metrics Calculation Updates ✅ FOUNDATION
**File:** `python/generate_reports.py` & `python/report_engine.py`

**Changes:**
1. Add new metrics for F&B analysis:
   - `food_value_avg` - Average of F&B_1 (food value)
   - `beverage_value_avg` - Average of F&B_4 (beverage value)
   - `food_speed_avg` - Average of F&B_2 (food speed)
   - `beverage_speed_avg` - Average of F&B_5 (beverage speed)
   - `food_quality_avg` - Average of F&B_3 (food quality)
   - `beverage_quality_avg` - Average of F&B_6 (beverage quality)
   - `return_likelihood_avg` - Average of "Likelihood to Return"
   - `price_value_avg` - Average of "Price Value"

2. Update `process_venue_data()` to:
   - Calculate F&B averages (only if fields present)
   - Calculate return likelihood average (only if field present)
   - Calculate price value average (only if field present)
   - Keep existing metrics (LTR, Fun, Helpful, Issues, Resolution)

3. Update `venue_data.json` structure to include new metrics

---

### Phase 3: Report Templates & Display ✅ PRESENTATION
**Files:** 
- `templates/venue-1page-browser.html`
- `templates/venue-1page-pdf.html`
- `templates/venue-1page-report.md.j2`
- `python/report_content.py`

**Changes:**
1. Add F&B section to templates (conditional - only show if data present)
2. Add "Return Likelihood" metric to Performance Summary
3. Add "Price Value" metric to Performance Summary
4. Create F&B subsection in Experience Metrics table with:
   - Food Value
   - Beverage Value
   - Food Speed
   - Beverage Speed
   - Food Quality
   - Beverage Quality
5. Update `build_metrics_context()` in `report_content.py` to include new metrics

---

### Phase 4: AI Analysis Pipeline Updates ✅ CRITICAL
**Files:**
- `.claude/single-venue-report/metrics_analysis.md`
- `.claude/single-venue-report/comment_analysis.md`
- `.claude/single-venue-report/synthesis.md`
- `python/ai_analysis.py`

**Changes:**
1. **metrics_analysis.md:**
   - Add F&B metrics to the metrics payload
   - Add concern flags for food/beverage quality, speed, value
   - Update guidance to consider F&B in overall characterization

2. **comment_analysis.md:**
   - Keep comment parsing logic the same (field name: "Open Comment")
   - Update to consider F&B themes in comments (food quality, service speed, pricing)
   - Metric flags now include F&B concerns

3. **synthesis.md:**
   - Update to synthesize F&B findings into recommendations
   - Consider F&B in "ups" and "downs" sections
   - Add F&B-specific recommendations if relevant

4. **ai_analysis.py:**
   - Update `_build_metrics_payload()` to include F&B metrics
   - Update `_build_comment_payload()` to use "Open Comment" field
   - No structural changes needed; just field name updates

---

### Phase 5: Report Generation Scripts ✅ INTEGRATION
**Files:**
- `python/create_html_reports.py`
- `python/create_markdown_reports.py`
- `python/create_pdf_reports.py`
- `python/generate_all_reports.py`

**Changes:**
1. No changes needed - these already use the normalized data from `venue_data.json`
2. Verify they work with new metrics structure
3. Test with both old and new schema data

---

### Phase 6: Testing & Validation ✅ VERIFICATION
**Files:**
- Create test suite for schema detection
- Create test suite for field mapping
- Create test suite for metrics calculation
- Test with both POC and real data

**Test Cases:**
1. POC data (DALLAS.csv) - should work as before
2. Real data (Grand_Prarie.csv) - should parse and calculate all metrics
3. Mixed data - should auto-detect schema
4. Missing F&B fields - should gracefully handle (optional fields)
5. Missing return/price fields - should gracefully handle (optional fields)

---

## 4. DETAILED FIELD MAPPING

### POC → Real Data Field Mapping

```python
FIELD_MAPPING = {
    # Core fields (same in both)
    'Venue': 'Venue',
    
    # Date fields (format conversion needed)
    'VisitDate': 'Visit Date (+00:00 GMT)',  # YYYY-MM-DD → M/D/YYYY
    
    # Metrics (direct mapping)
    'Q1_LTR': 'Combined NPS',  # 1-10 → 0-10 (compatible)
    'Q2_FUN': 'Fun',  # Text → 1-5 numeric (already numeric in real data)
    'Q3_HELPFUL': 'Helpfulness',  # Text → 1-5 numeric (already numeric in real data)
    'Q4_ISSUES': 'Issues During Visit',  # Yes/No → Yes/No
    'Q5_ISSUE_RESOLUTION': 'Issue Resolution Sat',  # 1-5 → 1-5
    'Q6_COMMENT': 'Open Comment',  # Free text → Free text
    
    # New fields (real data only)
    'F&B Matrix_1': 'Food Value',
    'F&B Matrix_2': 'Food Speed',
    'F&B Matrix_3': 'Food Quality',
    'F&B Matrix_4': 'Beverage Value',
    'F&B Matrix_5': 'Beverage Speed',
    'F&B Matrix_6': 'Beverage Quality',
    'Likelihood to Return': 'Return Likelihood',
    'Price Value': 'Price Value',
}
```

---

## 5. IMPLEMENTATION SEQUENCE

**Recommended order:**
1. ✅ **Phase 1** - CSV Parsing (foundation for everything else)
2. ✅ **Phase 2** - Metrics Calculation (feeds into AI analysis)
3. ✅ **Phase 4** - AI Analysis Updates (Claude skills)
4. ✅ **Phase 3** - Templates & Display (uses new metrics)
5. ✅ **Phase 5** - Report Scripts (integration)
6. ✅ **Phase 6** - Testing & Validation (verification)

---

## 6. BACKWARD COMPATIBILITY

**Goal:** POC data should continue to work without modification

**Strategy:**
- Schema detection: Automatically detect which schema is being used
- Field mapping: Use conditional logic to map fields based on detected schema
- Optional metrics: F&B and new metrics are optional; gracefully skip if not present
- Fallback logic: If new metrics missing, use only existing metrics in AI analysis

**Result:** Single codebase handles both schemas seamlessly

---

## 7. COMMENT ANALYSIS - NO MAJOR CHANGES

The comment analysis ability will remain largely the same:
- Field name changes from `Q6_COMMENT` → `Open Comment`
- Comment parsing logic stays identical
- AI analysis can now consider F&B themes in comments (already in the prompts)
- No structural changes to the 3-stage pipeline

---

## 8. NEXT STEPS

1. **Review this plan** - Confirm approach and priorities
2. **Start Phase 1** - Implement schema detection and field mapping
3. **Test with Grand_Prarie.csv** - Verify parsing works
4. **Proceed through phases** - Follow implementation sequence
5. **Validate with both datasets** - Ensure backward compatibility

