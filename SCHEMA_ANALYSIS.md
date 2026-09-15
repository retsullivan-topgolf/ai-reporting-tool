# Schema Analysis: POC vs Real Data

## Quick Overview

### POC Data (DALLAS.csv)
- **Venue:** Dallas
- **Responses:** 30
- **Metrics:** 5 core metrics (LTR, Fun, Helpful, Issues, Resolution)
- **Comments:** Single free-text field
- **Scale:** LTR is 1-10, Fun/Helpful are text labels (converted to 1-5)

### Real Data (Grand_Prarie.csv)
- **Venue:** Grand Prairie
- **Responses:** Multiple
- **Metrics:** 5 core metrics + 8 new metrics (F&B, Return, Price)
- **Comments:** Single free-text field
- **Scale:** All numeric (1-5 or 0-10), no text conversion needed
- **Operational Data:** Email, Bay #, Bay Host, Time of visit

---

## Detailed Field Comparison

### ✅ COMPATIBLE FIELDS (Direct Mapping)

| POC Field | Real Data Field | Type | Scale | Notes |
|-----------|-----------------|------|-------|-------|
| `Q1_LTR` | `Combined NPS` | Numeric | 1-10 / 0-10 | Scales compatible; just rename |
| `Q4_ISSUES` | `Issues During Visit` | Yes/No | Boolean | Same logic |
| `Q5_ISSUE_RESOLUTION` | `Issue Resolution Sat` | Numeric | 1-5 | Same scale |
| `Q6_COMMENT` | `Open Comment` | Text | Free-text | Same logic |

### ⚠️ FIELDS NEEDING CONVERSION

| POC Field | Real Data Field | POC Format | Real Data Format | Conversion |
|-----------|-----------------|-----------|------------------|-----------|
| `Q2_FUN` | `Fun` | Text labels ("5 - Extremely fun") | Numeric (1-5) | **SIMPLER!** No conversion needed in real data |
| `Q3_HELPFUL` | `Helpfulness` | Text labels ("5 - Extremely helpful") | Numeric (1-5) | **SIMPLER!** No conversion needed in real data |
| `VisitDate` | `Visit Date (+00:00 GMT)` | YYYY-MM-DD | M/D/YYYY | Date format conversion |

### 🆕 NEW FIELDS (Real Data Only)

#### F&B Metrics (6 fields)
```
F&B Matrix_1 - Value for the price you paid for food         → food_value_avg
F&B Matrix_2 - Speed of food service                         → food_speed_avg
F&B Matrix_3 - Food quality                                  → food_quality_avg
F&B Matrix_4 - Value for the price you paid for beverages    → beverage_value_avg
F&B Matrix_5 - Speed of beverage service                     → beverage_speed_avg
F&B Matrix_6 - Beverage quality                              → beverage_quality_avg
```
All 1-5 numeric scale

#### Customer Intent Metrics (2 fields)
```
Likelihood to Return - How likely are you to return...?      → return_likelihood_avg (1-5)
Price Value - How would you rate Topgolf's price...?         → price_value_avg (1-5)
```

#### Operational Data (4 fields)
```
Email Address          → respondent_email (not analyzed, but available)
Hour ID               → visit_hour (operational insight)
Bay Number            → bay_number (operational insight)
Bayhost               → bay_host_name (operational insight)
```

---

## Impact on Analysis

### Metrics Calculation
**POC:** 5 metrics
```
- ltr_avg (1-10)
- fun_avg (1-5)
- helpful_avg (1-5)
- issues_pct (0-100%)
- resolution_avg (1-5)
```

**Real Data:** 13 metrics
```
Core (5):
- ltr_avg (0-10)
- fun_avg (1-5)
- helpful_avg (1-5)
- issues_pct (0-100%)
- resolution_avg (1-5)

F&B (6):
- food_value_avg (1-5)
- food_speed_avg (1-5)
- food_quality_avg (1-5)
- beverage_value_avg (1-5)
- beverage_speed_avg (1-5)
- beverage_quality_avg (1-5)

Customer Intent (2):
- return_likelihood_avg (1-5)
- price_value_avg (1-5)
```

### AI Analysis Impact
**Comment Analysis:** Remains the same
- Field name: `Q6_COMMENT` → `Open Comment`
- Logic: Unchanged
- Themes: Can now identify F&B-related comments (already in prompts)

**Metrics Analysis:** Expands to include F&B
- New concern flags for food/beverage quality, speed, value
- Can identify F&B as a strength or weakness

**Synthesis:** Richer recommendations
- Can recommend F&B improvements if metrics/comments indicate issues
- Can highlight F&B as a differentiator if strong

---

## Data Quality Notes

### POC Data (DALLAS.csv)
- Synthetic/demo data
- Clean, consistent formatting
- Text labels for Fun/Helpful (requires conversion)
- 30 responses

### Real Data (Grand_Prarie.csv)
- Real customer survey responses
- More varied formatting
- Numeric scales (simpler parsing)
- Some fields may be empty (e.g., "N/A" for comments)
- Operational metadata included

---

## Implementation Complexity

### Low Complexity
- ✅ Field name mapping (simple string replacement)
- ✅ Date format conversion (regex or datetime parsing)
- ✅ Comment field mapping (same logic, different field name)
- ✅ Issue resolution logic (same conditional logic)

### Medium Complexity
- ⚠️ Schema detection (check for presence of key fields)
- ⚠️ Optional metrics handling (gracefully skip if fields missing)
- ⚠️ F&B metrics aggregation (new calculation logic)

### Higher Complexity
- 🔧 AI analysis prompt updates (need to consider F&B in recommendations)
- 🔧 Template updates (add F&B section, new metrics display)
- 🔧 Testing (verify both schemas work correctly)

---

## Backward Compatibility Strategy

### Goal
POC data should continue to work without any changes

### Approach
1. **Auto-detection:** Detect schema by checking for key fields
   - If `Combined NPS` present → Real Data schema
   - If `Q1_LTR` present → POC schema
   
2. **Field mapping:** Conditional logic to map fields based on detected schema
   
3. **Optional metrics:** F&B metrics are optional
   - If fields present → calculate and include
   - If fields missing → skip gracefully
   
4. **Fallback logic:** AI analysis works with or without new metrics
   - Core analysis uses 5 core metrics (always present)
   - F&B analysis uses 6 F&B metrics (optional)

### Result
Single codebase, two schemas, zero user friction

---

## File Changes Required

### Phase 1: CSV Parsing
- `python/generate_reports.py` - Add schema detection, field mapping, normalization

### Phase 2: Metrics
- `python/generate_reports.py` - Add F&B metrics calculation
- `python/report_engine.py` - Add F&B metrics to registry

### Phase 3: Templates
- `templates/venue-1page-browser.html` - Add F&B section
- `templates/venue-1page-pdf.html` - Add F&B section
- `templates/venue-1page-report.md.j2` - Add F&B section

### Phase 4: AI Analysis
- `.claude/single-venue-report/metrics_analysis.md` - Include F&B metrics
- `.claude/single-venue-report/comment_analysis.md` - Consider F&B themes
- `.claude/single-venue-report/synthesis.md` - Add F&B recommendations
- `python/ai_analysis.py` - Update payload builders

### Phase 5: Report Scripts
- `python/create_html_reports.py` - Verify compatibility
- `python/create_markdown_reports.py` - Verify compatibility
- `python/create_pdf_reports.py` - Verify compatibility

### Phase 6: Testing
- Create test suite for schema detection
- Create test suite for field mapping
- Create test suite for metrics calculation

---

## Summary

| Aspect | Impact | Effort |
|--------|--------|--------|
| **Core Logic** | Minimal changes | Low |
| **Field Mapping** | Simple string replacement | Low |
| **Metrics** | Add 8 new optional metrics | Medium |
| **AI Analysis** | Expand prompts for F&B | Medium |
| **Templates** | Add F&B section | Medium |
| **Testing** | Comprehensive validation | Medium |
| **Backward Compatibility** | Full support for POC data | Low |

**Total Effort:** Medium (2-3 days for experienced developer)

