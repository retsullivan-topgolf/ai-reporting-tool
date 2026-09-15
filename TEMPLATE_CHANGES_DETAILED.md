# Template Changes - Detailed Analysis

## Current Situation

✅ **No backward compatibility needed** - We can update the schema fully
✅ **Minimal layout changes** - We want to preserve the existing design
✅ **Real data has new metrics** - F&B, Return Likelihood, Price Value

---

## Current Template Structure

### Markdown Template (venue-1page-report.md.j2)

**Current sections:**
1. Header (Venue, Reporting period, Report week)
2. Venue Overview (AI-generated narrative)
3. Performance Summary (5 metrics in table)
4. Experience Metrics (5 metrics in table)
5. Ups/Downs/Impact/Recommendations (AI-generated)

**Current metrics shown:**
- Likelihood to Recommend (LTR)
- Fun
- Helpfulness
- Issues Reported
- Issue Resolution (only if issues=Yes)

### HTML Template (venue-1page-browser.html)

**Current sections:**
1. Header (Venue, Reporting period, Report week)
2. Main content area with:
   - Venue Overview (AI-generated narrative)
   - Performance Summary (metric cards)
   - Experience Metrics (table)
   - Ups/Downs/Impact/Recommendations (AI-generated)

**Current metrics shown:**
- Likelihood to Recommend (LTR)
- Fun
- Helpfulness
- Issues Reported
- Issue Resolution (only if issues=Yes)

---

## New Metrics to Add

### From Real Data Schema

**F&B Metrics (6 fields):**
- Food Value (1-5)
- Food Speed (1-5)
- Food Quality (1-5)
- Beverage Value (1-5)
- Beverage Speed (1-5)
- Beverage Quality (1-5)

**Customer Intent Metrics (2 fields):**
- Return Likelihood (1-5)
- Price Value (1-5)

**Total new metrics: 8**

---

## Design Strategy: Minimal Layout Changes

### Key Principle
**Keep the same visual structure, just add rows to tables and cards to grids.**

### Approach

#### 1. Performance Summary Section
**Current:** 4 metrics in a simple table
**New:** Add 3 rows for key new metrics (Return Likelihood, Value, + 1 F&B AVERAGE metric)

**Why this works:**
- Table naturally extends 
- No layout disruption
- Easy to scan

**Proposed additions:**
- Return Likelihood (shows customer loyalty)
- Price Value (shows value perception)
- Food Quality (represents F&B category)

#### 2. Experience Metrics Section
**Current:** 5 metrics in detailed table
**New:** Add F&B subsection with 6 metrics in a sub-table

**Why this works:**
- Subsection keeps F&B grouped logically
- Doesn't disrupt existing metrics
- Clear visual separation

**Structure:**
```
## Experience Metrics - Current Period

[Existing 5 metrics table]

### Food & Beverage Experience

[New 6 F&B metrics table]
```

#### 3. Metric Cards (HTML only)
**Current:** 5 metric cards in grid
**New:** Add F&B subsection with 6 cards below

**Why this works:**
- Cards naturally wrap
- Subsection keeps F&B grouped
- No disruption to existing cards

---

## Detailed Changes by Template

### Markdown Template (venue-1page-report.md.j2)

#### Change 1: Performance Summary Section

**Current:**
```markdown
## Performance Summary

| Metric | Score | Assessment |
|---|---:|---|
| Likelihood to Recommend (LTR) | {{ ltr_avg_display }} / 10 | {{ ltr_assessment }} |
| Fun | {{ fun_avg_display }} / 5 | {{ fun_assessment }} |
| Helpfulness | {{ helpful_avg_display }} / 5 | {{ helpful_assessment }} |
| Issues Reported | {{ issues_pct_card_display }} | {{ issues_assessment }} |

**Overall Assessment:** {{ overall_assessment }}
```

**New:**
```markdown
## Performance Summary

| Metric | Score | Assessment |
|---|---:|---|
| Likelihood to Recommend (LTR) | {{ ltr_avg_display }} / 10 | {{ ltr_assessment }} |
| Fun | {{ fun_avg_display }} / 5 | {{ fun_assessment }} |
| Helpfulness | {{ helpful_avg_display }} / 5 | {{ helpful_assessment }} |
| Issues Reported | {{ issues_pct_card_display }} | {{ issues_assessment }} |
| Return Likelihood | {{ return_likelihood_avg_display }} / 5 | {{ return_likelihood_assessment }} |
| Price Value | {{ price_value_avg_display }} / 5 | {{ price_value_assessment }} |

**Overall Assessment:** {{ overall_assessment }}
```

**Impact:** 2 additional rows in table (minimal)

---

#### Change 2: Experience Metrics Section

**Current:**
```markdown
## Experience Metrics - Current Period

| Attribute | Score | Assessment |
|---|---:|---|
| Likelihood to Recommend | {{ ltr_avg_display }} / 10 | {{ ltr_assessment }} |
| Fun | {{ fun_avg_display }} / 5 | {{ fun_assessment }} |
| Helpfulness | {{ helpful_avg_display }} / 5 | {{ helpful_assessment }} |
| Issues Reported | {{ issues_pct_table_display }} | {{ issues_assessment }} |
| Issue Resolution | {{ resolution_avg_display }} | {{ resolution_assessment }} |
```

**New:**
```markdown
## Experience Metrics - Current Period

| Attribute | Score | Assessment |
|---|---:|---|
| Likelihood to Recommend | {{ ltr_avg_display }} / 10 | {{ ltr_assessment }} |
| Fun | {{ fun_avg_display }} / 5 | {{ fun_assessment }} |
| Helpfulness | {{ helpful_avg_display }} / 5 | {{ helpful_assessment }} |
| Issues Reported | {{ issues_pct_table_display }} | {{ issues_assessment }} |
| Issue Resolution | {{ resolution_avg_display }} | {{ resolution_assessment }} |

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

**Impact:** New subsection below existing metrics (minimal disruption)

**Conditional rendering:**
```jinja2
{% if food_value_avg_display %}
### Food & Beverage Experience
[F&B table]
{% endif %}
```

---

### HTML Template (venue-1page-browser.html)

#### Change 1: Performance Summary Metric Cards

**Current structure:**
```html
<div class="metrics-grid">
    <div class="metric-card">
        <h3>Likelihood to Recommend</h3>
        <p class="metric-value">{{ ltr_avg_display }}</p>
        <p class="metric-status">{{ ltr_assessment }}</p>
    </div>
    <!-- 4 more cards -->
</div>
```

**New structure:**
```html
<div class="metrics-grid">
    <!-- Existing 5 cards -->
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
</div>
```

**Impact:** 2 additional cards in grid (wraps naturally)

---

#### Change 2: Experience Metrics Table

**Current structure:**
```html
<table class="metrics-table">
    <thead>
        <tr>
            <th>Attribute</th>
            <th>Score</th>
            <th>Assessment</th>
        </tr>
    </thead>
    <tbody>
        <!-- 5 rows -->
    </tbody>
</table>
```

**New structure:**
```html
<table class="metrics-table">
    <thead>
        <tr>
            <th>Attribute</th>
            <th>Score</th>
            <th>Assessment</th>
        </tr>
    </thead>
    <tbody>
        <!-- Existing 5 rows -->
    </tbody>
</table>

{% if food_value_avg_display %}
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
{% endif %}
```

**Impact:** New subsection table below existing metrics (minimal disruption)

---

## Data Flow Changes

### What needs to be updated in Python

#### 1. report_content.py - build_metrics_context()

**Current output:**
```python
{
    'ltr_avg': 8.5,
    'ltr_avg_display': '8.5',
    'ltr_assessment': 'Excellent',
    'fun_avg': 4.2,
    'fun_avg_display': '4.2',
    'fun_assessment': 'Excellent',
    # ... etc for helpful, issues, resolution
}
```

**New output:**
```python
{
    # Existing metrics
    'ltr_avg': 8.5,
    'ltr_avg_display': '8.5',
    'ltr_assessment': 'Excellent',
    # ... etc
    
    # New metrics (only if present in data)
    'return_likelihood_avg': 3.8,
    'return_likelihood_avg_display': '3.8',
    'return_likelihood_assessment': 'Good',
    'return_likelihood_status': 'good',
    
    'price_value_avg': 3.2,
    'price_value_avg_display': '3.2',
    'price_value_assessment': 'Fair',
    'price_value_status': 'fair',
    
    # F&B metrics (only if present in data)
    'food_value_avg': 3.8,
    'food_value_avg_display': '3.8',
    'food_value_assessment': 'Good',
    'food_value_status': 'good',
    
    # ... etc for all 6 F&B metrics
}
```

**Implementation:**
```python
def build_metrics_context(data, registry):
    """Build metrics context with optional F&B metrics"""
    
    context = {
        # Existing metrics
        'ltr_avg': data.get('ltr_avg'),
        'ltr_avg_display': format_metric(data.get('ltr_avg')),
        'ltr_assessment': get_assessment('ltr', data.get('ltr_avg'), registry),
        # ... etc
    }
    
    # Add optional metrics if present
    if data.get('return_likelihood_avg'):
        context['return_likelihood_avg'] = data['return_likelihood_avg']
        context['return_likelihood_avg_display'] = format_metric(data['return_likelihood_avg'])
        context['return_likelihood_assessment'] = get_assessment('return_likelihood', data['return_likelihood_avg'], registry)
        context['return_likelihood_status'] = get_status_class(context['return_likelihood_assessment'])
    
    # Add F&B metrics if present
    if data.get('food_value_avg'):
        for metric in ['food_value', 'food_speed', 'food_quality', 'beverage_value', 'beverage_speed', 'beverage_quality']:
            context[f'{metric}_avg'] = data.get(f'{metric}_avg')
            context[f'{metric}_avg_display'] = format_metric(data.get(f'{metric}_avg'))
            context[f'{metric}_assessment'] = get_assessment(metric, data.get(f'{metric}_avg'), registry)
            context[f'{metric}_status'] = get_status_class(context[f'{metric}_assessment'])
    
    return context
```

---

## Visual Impact Summary

### Markdown Report
```
Before: 2 tables (Performance Summary + Experience Metrics)
After:  2 tables + 1 optional subsection table (F&B)

Layout: Vertical extension only (no width changes)
```

### HTML Report
```
Before: 5 metric cards + 1 metrics table
After:  7 metric cards (if F&B present) + 2 tables (if F&B present)

Layout: Grid wraps naturally, subsection below
```

### PDF Report
```
Same as HTML (rendered via Playwright)
```

---

## Implementation Checklist

### Phase 1: Data Layer (generate_reports.py)
- [ ] Add F&B metrics calculation to process_venue_data()
- [ ] Add return/price metrics calculation
- [ ] Update venue_data.json structure

### Phase 2: Metrics Registry (report_engine.py)
- [ ] Add F&B metrics to METRICS_REGISTRY
- [ ] Add assessment thresholds for new metrics
- [ ] Add status class mappings

### Phase 3: Report Content (report_content.py)
- [ ] Update build_metrics_context() to include new metrics
- [ ] Add conditional logic for optional metrics
- [ ] Add formatting functions for new metrics

### Phase 4: Markdown Template (venue-1page-report.md.j2)
- [ ] Add Return Likelihood + Price Value to Performance Summary
- [ ] Add Food & Beverage subsection to Experience Metrics
- [ ] Add conditional rendering for F&B section

### Phase 5: HTML Template (venue-1page-browser.html)
- [ ] Add Return Likelihood + Price Value metric cards
- [ ] Add Food & Beverage subsection with table
- [ ] Add conditional rendering for F&B section

### Phase 6: PDF Template (venue-1page-pdf.html)
- [ ] Same changes as HTML template
- [ ] Verify layout in PDF rendering

---

## Conditional Rendering Strategy

### For Optional Metrics

**In Markdown:**
```jinja2
{% if return_likelihood_avg_display %}
| Return Likelihood | {{ return_likelihood_avg_display }} / 5 | {{ return_likelihood_assessment }} |
{% endif %}

{% if food_value_avg_display %}
### Food & Beverage Experience
[F&B table]
{% endif %}
```

**In HTML:**
```html
{% if return_likelihood_avg_display %}
<div class="metric-card">
    <h3>Return Likelihood</h3>
    <p class="metric-value">{{ return_likelihood_avg_display }}</p>
    <p class="metric-status">{{ return_likelihood_assessment }}</p>
</div>
{% endif %}

{% if food_value_avg_display %}
<h3 class="section-subtitle">Food & Beverage Experience</h3>
<table class="metrics-table">
    <!-- F&B table -->
</table>
{% endif %}
```

**Benefit:** POC data (without F&B) renders normally, Real data shows F&B section

---

## Assessment Thresholds

### Existing Metrics (unchanged)
```
LTR:        8-10 = Excellent, 6-7 = Good, 4-5 = Fair, 0-3 = Poor
Fun:        4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Helpful:    4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Issues:     0-10% = Excellent, 10-20% = Good, 20-30% = Fair, 30%+ = Poor
Resolution: 4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
```

### New Metrics (1-5 scale)
```
Return Likelihood:  4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Price Value:        4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Food Value:         4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Food Speed:         4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Food Quality:       4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Beverage Value:     4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Beverage Speed:     4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
Beverage Quality:   4.5-5 = Excellent, 3.5-4.4 = Good, 2.5-3.4 = Fair, 0-2.4 = Poor
```

---

## Summary

### Layout Impact: MINIMAL ✅
- No major restructuring
- Tables extend vertically
- Cards wrap naturally
- Subsections keep F&B grouped

### Visual Impact: CLEAN ✅
- Same color scheme
- Same typography
- Same spacing
- New sections clearly labeled

### User Impact: TRANSPARENT ✅
- POC data unchanged
- Real data enhanced
- Conditional rendering
- No breaking changes

---

## Next Steps

1. **Confirm this approach** - Does this layout strategy work for you?
2. **Review the specific changes** - Any adjustments needed?
3. **Start implementation** - Begin with Phase 1 (data layer)
4. **Test incrementally** - Test after each phase

Ready to proceed? Let me know if you'd like to adjust the layout strategy!

