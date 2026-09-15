# Implementation Roadmap: POC → Real Data

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CSV INPUT (Either Schema)                        │
├─────────────────────────────────────────────────────────────────────────┤
│  POC (DALLAS.csv)              │  Real Data (Grand_Prarie.csv)          │
│  - Q1_LTR (1-10)               │  - Combined NPS (0-10)                 │
│  - Q2_FUN (text)               │  - Fun (1-5 numeric)                   │
│  - Q3_HELPFUL (text)           │  - Helpfulness (1-5 numeric)           │
│  - Q4_ISSUES (Yes/No)          │  - Issues During Visit (Yes/No)        │
│  - Q5_ISSUE_RESOLUTION (1-5)   │  - Issue Resolution Sat (1-5)          │
│  - Q6_COMMENT (text)           │  - Open Comment (text)                 │
│                                │  - F&B Matrix_1-6 (NEW)                │
│                                │  - Likelihood to Return (NEW)          │
│                                │  - Price Value (NEW)                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
                    ┌───────────────────────────────┐
                    │  PHASE 1: Schema Detection    │
                    │  & Field Mapping              │
                    │  (generate_reports.py)        │
                    └───────────────────────────────┘
                                    ↓
                    ┌───────────────────────────────┐
                    │  PHASE 2: Metrics             │
                    │  Calculation                  │
                    │  (generate_reports.py)        │
                    └───────────────────────────────┘
                                    ↓
                    ┌───────────────────────────────┐
                    │  venue_data.json              │
                    │  (normalized metrics)         │
                    └───────────────────────────────┘
                                    ↓
                    ┌───────────────────────────────┐
                    │  PHASE 4: AI Analysis         │
                    │  (ai_analysis.py)             │
                    │  - metrics_analysis.md        │
                    │  - comment_analysis.md        │
                    │  - synthesis.md               │
                    └───────────────────────────────┘
                                    ↓
                    ┌───────────────────────────────┐
                    │  ai_analysis_results.json     │
                    │  (precomputed analysis)       │
                    └───────────────────────────────┘
                                    ↓
        ┌───────────────────────────┴───────────────────────────┐
        ↓                           ↓                           ↓
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  PHASE 3:        │      │  PHASE 3:        │      │  PHASE 3:        │
│  HTML Reports    │      │  Markdown        │      │  PDF Reports     │
│  (create_html_   │      │  Reports         │      │  (create_pdf_    │
│   reports.py)    │      │  (create_        │      │   reports.py)    │
│                  │      │   markdown_      │      │                  │
│  + Templates     │      │   reports.py)    │      │  + Templates     │
│  + F&B Section   │      │                  │      │  + F&B Section   │
│  + New Metrics   │      │  + Templates     │      │  + New Metrics   │
└──────────────────┘      │  + F&B Section   │      └──────────────────┘
        ↓                 │  + New Metrics   │              ↓
        └─────────────────┴──────────────────┴──────────────┘
                                    ↓
                    ┌───────────────────────────────┐
                    │  reports/ folder              │
                    │  - HTML files                 │
                    │  - Markdown files             │
                    │  - PDF files                  │
                    └───────────────────────────────┘
```

---

## Phase Breakdown

### PHASE 1: Schema Detection & Field Mapping
**File:** `python/generate_reports.py`
**Complexity:** Low
**Time:** 2-3 hours

**What it does:**
```python
def detect_schema(csv_file):
    """Auto-detect which schema is being used"""
    # Check for key fields to determine schema
    # Return: 'poc' or 'real'

def normalize_row(row, schema):
    """Convert row to normalized format regardless of schema"""
    # Map field names
    # Convert data types
    # Return: normalized_row

def process_venue_data(rows, schema):
    """Process rows with schema awareness"""
    # Use normalized rows
    # Calculate metrics based on schema
    # Return: venue_data
```

**Inputs:**
- CSV file (either schema)

**Outputs:**
- Normalized venue data dict with metrics

**Testing:**
- Test with DALLAS.csv (POC)
- Test with Grand_Prarie.csv (Real)
- Verify both produce correct metrics

---

### PHASE 2: Metrics Calculation
**File:** `python/generate_reports.py` + `python/report_engine.py`
**Complexity:** Medium
**Time:** 2-3 hours

**What it does:**
```python
# In generate_reports.py:
def calculate_metrics(rows, schema):
    """Calculate all metrics from normalized rows"""
    metrics = {
        # Core metrics (always present)
        'ltr_avg': ...,
        'fun_avg': ...,
        'helpful_avg': ...,
        'issues_pct': ...,
        'resolution_avg': ...,
        
        # F&B metrics (optional, only if fields present)
        'food_value_avg': ...,
        'food_speed_avg': ...,
        'food_quality_avg': ...,
        'beverage_value_avg': ...,
        'beverage_speed_avg': ...,
        'beverage_quality_avg': ...,
        
        # Customer intent (optional, only if fields present)
        'return_likelihood_avg': ...,
        'price_value_avg': ...,
    }
    return metrics

# In report_engine.py:
# Add F&B metrics to METRICS_REGISTRY
# Add assessment thresholds for new metrics
```

**Inputs:**
- Normalized venue data

**Outputs:**
- venue_data.json with all metrics

**Testing:**
- Verify POC data produces same metrics as before
- Verify Real data produces all 13 metrics
- Verify optional metrics gracefully skip if missing

---

### PHASE 3: Templates & Display
**Files:** 
- `templates/venue-1page-browser.html`
- `templates/venue-1page-pdf.html`
- `templates/venue-1page-report.md.j2`
- `python/report_content.py`

**Complexity:** Medium
**Time:** 3-4 hours

**What it does:**
1. Add F&B section to Performance Summary
2. Add F&B subsection to Experience Metrics table
3. Add Return Likelihood metric
4. Add Price Value metric
5. Update `build_metrics_context()` to include new metrics

**Template Changes:**
```html
<!-- Add to Performance Summary -->
<div class="metric-card">
    <h4>Food Value</h4>
    <p class="metric-value">{{ metrics.food_value_avg }}</p>
    <p class="metric-status">{{ metrics.food_value_status }}</p>
</div>

<!-- Add F&B section to Experience Metrics -->
<tr>
    <td>Food Value</td>
    <td class="status-{{ metrics.food_value_status }}">
        {{ metrics.food_value_avg }}/5
    </td>
</tr>
```

**Inputs:**
- venue_data.json with metrics

**Outputs:**
- HTML/Markdown/PDF reports with F&B section

**Testing:**
- Verify POC reports look the same (no F&B section)
- Verify Real data reports show F&B section
- Verify status pills color-code correctly

---

### PHASE 4: AI Analysis Pipeline
**Files:**
- `.claude/single-venue-report/metrics_analysis.md`
- `.claude/single-venue-report/comment_analysis.md`
- `.claude/single-venue-report/synthesis.md`
- `python/ai_analysis.py`

**Complexity:** Medium-High
**Time:** 4-5 hours

**What it does:**

#### metrics_analysis.md
```markdown
# Stage 1: Metrics Analysis

You will receive:
- venue name
- response count
- 5 core metrics (ltr, fun, helpful, issues, resolution)
- 6 F&B metrics (food_value, food_speed, food_quality, beverage_value, beverage_speed, beverage_quality)
- 2 customer intent metrics (return_likelihood, price_value)
- assessment tier for each metric

Produce:
- characterization of the venue (2-3 sentences)
- metric_flags for each metric (concern flags on 0-100 scale)
```

#### comment_analysis.md
```markdown
# Stage 2: Comment Analysis

You will receive:
- venue name
- response count
- guest comments (from "Open Comment" field)
- metric_flags from Stage 1

Produce:
- themes (positive and negative)
- magnitude scores (0-100)
- categorization based on metric flags
```

#### synthesis.md
```markdown
# Stage 3: Synthesis

You will receive:
- Stage 1 characterization + metric_flags
- Stage 2 themes

Produce:
- overview (1 paragraph)
- ups (3-5 positive themes)
- downs (3-5 negative themes)
- impact (3-5 key drivers with descriptions)
- recommendations (critical, secondary, maintain tiers)
```

#### ai_analysis.py
```python
def _build_metrics_payload(data):
    """Include F&B metrics in payload"""
    return {
        "venue": data["venue"],
        "responses": data["responses"],
        "metrics": {
            "ltr_avg": data["ltr_avg"],
            "fun_avg": data["fun_avg"],
            "helpful_avg": data["helpful_avg"],
            "issues_pct": data["issues_pct"],
            "resolution_avg": data["resolution_avg"],
            # NEW: F&B metrics
            "food_value_avg": data.get("food_value_avg"),
            "food_speed_avg": data.get("food_speed_avg"),
            "food_quality_avg": data.get("food_quality_avg"),
            "beverage_value_avg": data.get("beverage_value_avg"),
            "beverage_speed_avg": data.get("beverage_speed_avg"),
            "beverage_quality_avg": data.get("beverage_quality_avg"),
            # NEW: Customer intent
            "return_likelihood_avg": data.get("return_likelihood_avg"),
            "price_value_avg": data.get("price_value_avg"),
        },
        "assessment_tiers": {...},
    }

def _build_comment_payload(data, metric_flags):
    """Use "Open Comment" field instead of Q6_COMMENT"""
    return {
        "venue": data["venue"],
        "responses": data["responses"],
        "comments": data.get("comments", []),  # From "Open Comment"
        "metric_flags": metric_flags,
    }
```

**Inputs:**
- venue_data.json with all metrics

**Outputs:**
- ai_analysis_results.json with precomputed analysis

**Testing:**
- Test metrics_analysis with POC data
- Test metrics_analysis with Real data (with F&B)
- Test comment_analysis with both
- Test synthesis with both
- Verify F&B themes appear in recommendations when relevant

---

### PHASE 5: Report Generation Scripts
**Files:**
- `python/create_html_reports.py`
- `python/create_markdown_reports.py`
- `python/create_pdf_reports.py`
- `python/generate_all_reports.py`

**Complexity:** Low
**Time:** 1-2 hours

**What it does:**
- Verify these scripts work with new metrics structure
- No code changes needed (they already use venue_data.json)
- Test with both schemas

**Testing:**
- Run with POC data → verify output matches before
- Run with Real data → verify F&B section appears
- Run with both schemas → verify no errors

---

### PHASE 6: Testing & Validation
**Complexity:** Medium
**Time:** 3-4 hours

**Test Suite:**

```python
# test_schema_detection.py
def test_detect_poc_schema():
    """Verify POC schema is detected correctly"""
    
def test_detect_real_schema():
    """Verify Real schema is detected correctly"""

# test_field_mapping.py
def test_poc_field_mapping():
    """Verify POC fields map correctly"""
    
def test_real_field_mapping():
    """Verify Real fields map correctly"""

# test_metrics_calculation.py
def test_poc_metrics():
    """Verify POC metrics calculated correctly"""
    
def test_real_metrics():
    """Verify Real metrics calculated correctly"""
    
def test_optional_metrics():
    """Verify optional metrics gracefully skip if missing"""

# test_ai_analysis.py
def test_metrics_analysis_with_fb():
    """Verify metrics_analysis includes F&B metrics"""
    
def test_comment_analysis_with_real_data():
    """Verify comment_analysis works with 'Open Comment' field"""

# test_reports.py
def test_html_report_with_poc():
    """Verify HTML report works with POC data"""
    
def test_html_report_with_real():
    """Verify HTML report shows F&B section with Real data"""
    
def test_markdown_report_with_real():
    """Verify Markdown report shows F&B section"""
    
def test_pdf_report_with_real():
    """Verify PDF report shows F&B section"""
```

---

## Implementation Checklist

### Phase 1: Schema Detection & Field Mapping
- [ ] Add `detect_schema()` function
- [ ] Add `normalize_row()` function
- [ ] Update `process_venue_data()` to use normalization
- [ ] Test with DALLAS.csv
- [ ] Test with Grand_Prarie.csv

### Phase 2: Metrics Calculation
- [ ] Add F&B metrics calculation
- [ ] Add customer intent metrics calculation
- [ ] Update `venue_data.json` structure
- [ ] Add metrics to `report_engine.py` registry
- [ ] Test metrics calculation

### Phase 3: Templates & Display
- [ ] Update `venue-1page-browser.html`
- [ ] Update `venue-1page-pdf.html`
- [ ] Update `venue-1page-report.md.j2`
- [ ] Update `build_metrics_context()` in `report_content.py`
- [ ] Test template rendering

### Phase 4: AI Analysis
- [ ] Update `metrics_analysis.md`
- [ ] Update `comment_analysis.md`
- [ ] Update `synthesis.md`
- [ ] Update `_build_metrics_payload()` in `ai_analysis.py`
- [ ] Update `_build_comment_payload()` in `ai_analysis.py`
- [ ] Test AI analysis pipeline

### Phase 5: Report Scripts
- [ ] Verify `create_html_reports.py` works
- [ ] Verify `create_markdown_reports.py` works
- [ ] Verify `create_pdf_reports.py` works
- [ ] Verify `generate_all_reports.py` works

### Phase 6: Testing & Validation
- [ ] Create test suite
- [ ] Test with POC data (backward compatibility)
- [ ] Test with Real data (new features)
- [ ] Test with both schemas
- [ ] Verify no regressions

---

## Success Criteria

✅ **Phase 1:** POC and Real data both parse correctly
✅ **Phase 2:** All metrics calculated for both schemas
✅ **Phase 3:** Templates render correctly with new metrics
✅ **Phase 4:** AI analysis includes F&B insights
✅ **Phase 5:** All report formats generate successfully
✅ **Phase 6:** All tests pass, backward compatibility verified

---

## Timeline Estimate

| Phase | Effort | Time |
|-------|--------|------|
| 1 | Low | 2-3 hours |
| 2 | Medium | 2-3 hours |
| 3 | Medium | 3-4 hours |
| 4 | Medium-High | 4-5 hours |
| 5 | Low | 1-2 hours |
| 6 | Medium | 3-4 hours |
| **Total** | **Medium** | **15-21 hours** |

**Realistic estimate:** 2-3 days for experienced developer working full-time

