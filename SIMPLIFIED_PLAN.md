# Simplified Implementation Plan (No Backward Compatibility)

## Key Changes from Original Plan

✅ **No backward compatibility needed** - We can fully update the schema
✅ **Minimal template changes** - Preserve existing layout, just add rows/sections
✅ **Focused scope** - Only implement what's needed for real data

---

## Updated 6-Phase Plan

### Phase 1: CSV Parsing & Metrics (2-3 hours)
**Files:** `python/generate_reports.py`

**What:**
- Add schema detection (POC vs Real)
- Add field mapping for both schemas
- Add metrics calculation for new fields
- Update venue_data.json structure

**No backward compatibility needed:**
- Can fully update field names
- Can require new fields
- Can change data structures

**Result:** venue_data.json with all 13 metrics

---

### Phase 2: Metrics Registry (1-2 hours)
**Files:** `python/report_engine.py`

**What:**
- Add F&B metrics to METRICS_REGISTRY
- Add assessment thresholds for new metrics
- Add status class mappings

**Result:** Metrics properly assessed and displayed

---

### Phase 3: Report Content (1-2 hours)
**Files:** `python/report_content.py`

**What:**
- Update `build_metrics_context()` to include new metrics
- Add conditional logic for optional metrics
- Add formatting functions

**Result:** Context dict includes all metrics

---

### Phase 4: Templates (2-3 hours)
**Files:** HTML, Markdown, PDF templates

**What:**
- Add Return Likelihood + Price Value to Performance Summary
- Add Food & Beverage subsection to Experience Metrics
- Add conditional rendering for F&B section
- **Minimal layout changes** (see TEMPLATE_CHANGES_DETAILED.md)

**Result:** Reports show new metrics without major redesign

---

### Phase 5: AI Analysis (3-4 hours)
**Files:** Claude skill docs, `python/ai_analysis.py`

**What:**
- Update `metrics_analysis.md` to include F&B metrics
- Update `comment_analysis.md` to consider F&B themes
- Update `synthesis.md` to add F&B recommendations
- Update payload builders in `ai_analysis.py`

**Result:** AI analysis includes F&B insights

---

### Phase 6: Testing (2-3 hours)
**Files:** New test files in `python/tests/`

**What:**
- Test schema detection
- Test metrics calculation
- Test template rendering
- Test AI analysis
- Test end-to-end pipeline

**Result:** All tests pass

---

## Total Effort: 11-17 hours (1.5-2 days)

**Breakdown:**
- Phase 1: 2-3h (CSV parsing)
- Phase 2: 1-2h (Metrics registry)
- Phase 3: 1-2h (Report content)
- Phase 4: 2-3h (Templates)
- Phase 5: 3-4h (AI analysis)
- Phase 6: 2-3h (Testing)

---

## What's Different from Original Plan

| Original | Simplified |
|----------|-----------|
| 15-21 hours | 11-17 hours |
| Backward compatibility | No backward compatibility |
| Complex field mapping | Simple field mapping |
| Optional metrics handling | Direct metrics |
| 6 phases | 6 phases (simpler) |

---

## Key Simplifications

### 1. No Backward Compatibility
- Don't need to support POC schema
- Can fully update field names
- Can require new fields
- Simpler code

### 2. Minimal Template Changes
- Keep existing layout
- Just add rows to tables
- Just add subsection for F&B
- No major redesign

### 3. Direct Metrics
- All metrics always present (if data has them)
- No complex optional logic
- Simpler conditional rendering

### 4. Focused Scope
- Only implement what's needed
- Don't over-engineer
- Keep it simple

---

## Implementation Sequence

```
Phase 1: CSV Parsing & Metrics
    ↓
Phase 2: Metrics Registry
    ↓
Phase 3: Report Content
    ↓
Phase 5: AI Analysis (do before templates)
    ↓
Phase 4: Templates
    ↓
Phase 6: Testing
```

**Why Phase 5 before Phase 4?**
- Templates need to know what AI analysis will produce
- AI analysis defines the data structure
- Easier to template after AI is updated

---

## File Changes Summary

### Phase 1
- `python/generate_reports.py` - Schema detection, field mapping, metrics calculation

### Phase 2
- `python/report_engine.py` - Add new metrics to registry

### Phase 3
- `python/report_content.py` - Update build_metrics_context()

### Phase 4
- `templates/venue-1page-browser.html` - Add new metrics, F&B section
- `templates/venue-1page-pdf.html` - Add new metrics, F&B section
- `templates/venue-1page-report.md.j2` - Add new metrics, F&B section

### Phase 5
- `.claude/single-venue-report/metrics_analysis.md` - Include F&B metrics
- `.claude/single-venue-report/comment_analysis.md` - Consider F&B themes
- `.claude/single-venue-report/synthesis.md` - Add F&B recommendations
- `python/ai_analysis.py` - Update payload builders

### Phase 6
- Create test files in `python/tests/`

---

## Data Structure

### venue_data.json

**Current structure:**
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
  "comments": ["..."],
  "high_ltr_comments": ["..."],
  "low_ltr_comments": ["..."]
}
```

**New structure:**
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
  "return_likelihood_avg": 3.8,
  "price_value_avg": 3.2,
  "food_value_avg": 3.8,
  "food_speed_avg": 3.5,
  "food_quality_avg": 3.9,
  "beverage_value_avg": 3.7,
  "beverage_speed_avg": 3.6,
  "beverage_quality_avg": 4.0,
  "comments": ["..."],
  "high_ltr_comments": ["..."],
  "low_ltr_comments": ["..."]
}
```

---

## Template Changes (Minimal)

### Markdown Template

**Add to Performance Summary:**
```markdown
| Return Likelihood | {{ return_likelihood_avg_display }} / 5 | {{ return_likelihood_assessment }} |
| Price Value | {{ price_value_avg_display }} / 5 | {{ price_value_assessment }} |
```

**Add new subsection:**
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

**Add to metric cards:**
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

**Add new subsection:**
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

---

## Assessment Thresholds

### All 1-5 Scale Metrics
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

## Next Steps

1. **Review TEMPLATE_CHANGES_DETAILED.md** - Understand the layout strategy
2. **Confirm approach** - Any adjustments needed?
3. **Start Phase 1** - CSV parsing and metrics
4. **Test incrementally** - After each phase
5. **Verify layout** - Make sure templates look good

---

## Questions to Consider

1. **CSV Schema:** Should we auto-detect POC vs Real, or just assume Real?
2. **Optional metrics:** Should F&B always be present, or conditionally rendered?
3. **AI Analysis:** Should we update Claude skills to mention F&B, or keep them generic?
4. **Testing:** Should we test with both DALLAS.csv and Grand_Prarie.csv?

---

## Success Criteria

✅ Grand_Prarie.csv parses correctly
✅ All 13 metrics calculated
✅ Templates render without errors
✅ F&B section appears in reports
✅ AI analysis includes F&B insights
✅ All tests pass

---

## Ready to Start?

1. Review TEMPLATE_CHANGES_DETAILED.md
2. Confirm the layout strategy
3. Begin Phase 1 (CSV parsing)
4. Follow the implementation sequence

Let's build this! 🚀

