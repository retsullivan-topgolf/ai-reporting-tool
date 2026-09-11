# Topgolf Venue Report - 1-PAGE Template

**Purpose:** Quick, executive-level summary for venue managers and regional leadership  
**Length:** ~2-3 pages when printed  
**Audience:** Decision-makers who need key insights quickly  
**Format:** Can be HTML (browser/email) or Markdown

---

## Section Structure & Data Mapping

### 1. Header Metadata

**Data Source:** CSV metadata

```
Venue: [Venue column value]
Reporting period: [MIN(VisitDate)] - [MAX(VisitDate)]
Report week: Week of [MIN(VisitDate)]
```

---

### 2. Venue Overview

**Length:** 2-3 sentences  
**Purpose:** Immediate characterization of venue performance  
**Data Source:** Quantitative summary + qualitative themes

**Template:**
```
[Venue] is a [characterization] venue that [primary strength] but [primary challenge]. 
The venue shows a clear pattern: [key insight about what drives satisfaction]. 
[Assessment of whether issues are capability gaps or execution gaps].
```

**Characterization Options:**
- "high-performing" (LTR ≥ 8.0)
- "strong" (LTR 7.0-7.9)
- "moderate" (LTR 6.0-6.9)
- "challenged" (LTR < 6.0)

**Example:**
```
Myrtle Beach is a high-traffic venue that delivers strong entertainment value but faces 
consistent challenges with equipment reliability and response time. The venue shows a clear 
pattern: guests enjoy the experience when things work smoothly, but equipment issues create 
significant friction that impacts satisfaction and recommendation intent. The venue has 
demonstrated the capability to resolve issues quickly, suggesting that the problem is not a 
lack of capability but rather inconsistent execution or inadequate preventive maintenance.
```

---

### 3. Performance Summary

**Length:** 4 metric cards + 1-2 sentence assessment  
**Purpose:** At-a-glance metrics overview  
**Data Source:** Aggregated CSV metrics

**Metric Cards (displayed as grid):**

| Metric | Value | Assessment |
|---|---:|---|
| Likelihood to Recommend (LTR) | [AVG(Q1_LTR)] / 10 | [Assessment] |
| Fun | [AVG(Q2_FUN_NUMERIC)] / 5 | [Assessment] |
| Helpfulness | [AVG(Q3_HELPFUL_NUMERIC)] / 5 | [Assessment] |
| Issues Reported | [PERCENT(Q4_ISSUES="Yes")]% | [Assessment] |

**Assessment Thresholds:**

| Metric | Excellent | Strong | Moderate | Weak |
|---|---|---|---|---|
| LTR | 8.0+ | 7.0-7.9 | 6.0-6.9 | <6.0 |
| Fun | 4.2+ | 3.8-4.1 | 3.4-3.7 | <3.4 |
| Helpfulness | 4.2+ | 3.8-4.1 | 3.4-3.7 | <3.4 |
| Issues | <30% | 30-40% | 40-50% | >50% |

**Overall Assessment:** 1-2 sentence summary

**Example:**
```
Overall Assessment: Myrtle Beach demonstrates strong entertainment delivery but is 
significantly hampered by equipment issues that occur in half of guest visits. The venue's 
challenge is not entertainment or staff friendliness, but rather operational reliability and 
the speed of problem resolution.
```

---

### 4. Experience Metrics - Current Period

**Length:** 1 table  
**Purpose:** Show how venue compares to network average  
**Data Source:** Venue metrics + network benchmarks

**Table Structure:**

|| Attribute | Score | Benchmark | Status |
||---|---:|---|---|
|| Likelihood to Recommend | [VENUE_AVG] / 10 | [NETWORK_AVG] (network avg) | [Status] |
|| Fun | [VENUE_AVG] / 5 | [NETWORK_AVG] (network avg) | [Status] |
|| Helpfulness | [VENUE_AVG] / 5 | [NETWORK_AVG] (network avg) | [Status] |
|| Issues Reported | [VENUE_PERCENT]% | [NETWORK_PERCENT]% (network avg) | [Status] |
|| Issue Resolution | [VENUE_AVG] / 5 | [NETWORK_AVG] (network avg) | [Status] |

**Network Benchmarks:**
- LTR: 7.8 / 10
- Fun: 4.1 / 5
- Helpfulness: 4.2 / 5
- Issues Reported: 37.0%
- Issue Resolution: 3.6 / 5

**Status Calculation:**
```
IF venue_metric > benchmark: "Above average ✓"
IF venue_metric ≈ benchmark (within 0.1): "On par"
IF venue_metric < benchmark: "Below average" [or "Above average ✗" for Issues]
```

---

### 5. Ups & Downs (What Made Scores Go Up/Down)

**Length:** 3 bullet points each (6 total)  
**Purpose:** Identify positive and negative drivers  
**Data Source:** High/low-scoring responses + comments

#### 5a. Ups (What Made Scores Go Up)

**Format:**
```
- **[Theme Name]**: [Evidence from comments or metrics]
- **[Theme Name]**: [Evidence]
- **[Theme Name]**: [Evidence]
```

**How to Derive:**
1. Filter for Q1_LTR ≥ 8 or Q2_FUN = "5 - Extremely fun"
2. Read Q6_COMMENT for these responses
3. Identify 3 most common positive themes
4. Write bullet with theme + supporting evidence

**Example:**
```
- **Strong entertainment value despite operational challenges**: All four guests rated 
  the experience as "Very fun" or "Extremely fun," indicating that the core entertainment 
  offering is working well

- **Staff helpfulness when engaged**: Guests who received prompt assistance reported 
  positive interactions; staff have knowledge and willingness to enhance the guest experience

- **Positive resolution outcomes when issues are addressed**: Guests whose equipment issues 
  were resolved quickly reported satisfaction ratings of 4-5 out of 5
```

#### 5b. Downs (What Made Scores Go Down)

**Format:**
```
- **[Theme Name]**: [Evidence from comments or metrics]
- **[Theme Name]**: [Evidence]
- **[Theme Name]**: [Evidence, if applicable]
```

**How to Derive:**
1. Filter for Q1_LTR ≤ 6 or Q2_FUN ≤ 2
2. Filter for Q4_ISSUES = "Yes"
3. Read Q6_COMMENT for these responses
4. Identify 2-3 most common negative themes
5. Write bullet with theme + supporting evidence

**Example:**
```
- **High frequency of equipment issues**: 50% of guests reported experiencing an issue—
  significantly above the network average of 37%—indicating a systemic equipment problem

- **Inconsistent response time to equipment problems**: Same type of problem (bay equipment 
  failure) produced vastly different outcomes: one guest with quick response gave LTR=9, 
  while another with slow response gave LTR=4

- **Moderate helpfulness ratings**: While staff are friendly and knowledgeable, the 
  helpfulness score of 3.8 is slightly below network average, likely reflecting guest 
  frustration with equipment issues and slow response
```

---

### 6. Impact (What Impacted Overall Scores Most)

**Length:** 1 ranked list (3 items)  
**Purpose:** Rank top 3 drivers by impact on LTR  
**Data Source:** Correlation analysis + comment themes

**List Structure:**

1. **[Top Driver]** - [Quantitative or qualitative evidence]
2. **[Second Driver]** - [Evidence]
3. **[Third Driver]** - [Evidence]

**How to Derive:**
1. For each metric, calculate correlation with LTR
2. Rank by strength of correlation
3. Select top 3 drivers with evidence

**Example:**
```
1. **Equipment Reliability** - 50% issue rate; all issues were equipment-related
2. **Response Time** - Same issue produced LTR=9 vs LTR=4 based on response speed
3. **Fun (entertainment value)** - Consistently strong across all guests
```

---

### 7. Recommendations

**Length:** 3 subsections with 4 bullets each  
**Purpose:** Provide actionable next steps  
**Data Source:** Impact drivers + best practices

#### 7a. 🔴 Critical Priority: [Top Gap]

**Format:**
```
- **[Action Name]**: [Brief description]
- **[Action Name]**: [Brief description]
- **[Action Name]**: [Brief description]
- **[Action Name]**: [Brief description]
```

**How to Derive:**
1. Identify #1 driver from Section 6 (Impact)
2. If negative, make it critical priority
3. List 4 specific actions to address it

**Example:**
```
- **Root cause analysis**: Identify why bay tracking systems are failing so frequently 
  (equipment model/age, environmental factors, configuration, maintenance adequacy)

- **Preventive maintenance audit**: Review maintenance logs for patterns; assess whether 
  current maintenance schedule is adequate

- **Hardware assessment**: Evaluate whether bay tracking systems need replacement or upgrade

- **Immediate mitigation**: Implement daily pre-opening equipment checks and bay-monitoring 
  system to detect issues before guests encounter them
```

#### 7b. 🟡 Secondary Priority: [Second Gap]

**Format:** Same as 7a, with 3-4 actions

**Example:**
```
- **Establish response-time standard**: Staff respond to equipment issues within 2 minutes

- **Implement bay-monitoring system**: Automated detection of equipment failures alerts staff immediately

- **Staffing analysis**: Ensure adequate staffing during peak hours to enable rapid response

- **Staff training**: Emphasize importance of rapid response and provide clear escalation procedures
```

#### 7c. 🟢 Maintain Strengths: [Top Strength]

**Format:** Same as 7a, with 3-4 actions

**Example:**
```
- **Protect the experience**: Ensure that equipment issues don't undermine the positive aspects of the venue

- **Staff recognition**: Acknowledge staff who provide excellent explanations and service

- **Consistency**: Ensure that the positive service culture is maintained across all shifts
```

---

## Data Processing Checklist

- [ ] Filter CSV by venue and date range
- [ ] Calculate 5 metrics (LTR, Fun, Helpfulness, Issues %, Resolution)
- [ ] Compare to network benchmarks
- [ ] Analyze Q6_COMMENT for themes
- [ ] Identify top 3 positive drivers (Ups)
- [ ] Identify top 2-3 negative drivers (Downs)
- [ ] Rank 3 drivers by impact
- [ ] Define 3 priority levels with 4 actions each
- [ ] Write narrative sections (Overview, Assessment)

---

## Output Formats

All three formats are generated from the same venue_data.json. They share identical analysis/metrics via `python/report_content.py` (see `report_content.render_html_report()`), so they never disagree on the numbers or the narrative - only on layout/markup. Run them via `python/generate_all_reports.py` (which prompts for HTML, Markdown, PDF, or All - or takes `--format` to skip the prompt), or individually.

### HTML (Browser)
- Template: `templates/venue-1page-browser.html` (Jinja2)
- Generator: `python/create_html_reports.py`
- Output: `reports/Topgolf_Venue_Report_[VenueName]_1PAGE.html`
- Use for: Interactive viewing

### PDF
- Template: `templates/venue-1page-pdf.html` (Jinja2) - a layout dedicated to the PDF, deliberately separate from the HTML template above: by request, the PDF omits the "Overall Assessment" box and orders Impact before Ups/Downs, and reordering a *shared* template via print CSS (`order`/flexbox) turned out to conflict with Chromium's print pagination (content unexpectedly spilled onto an extra page). Plain top-to-bottom DOM order in its own file paginates predictably.
- Generator: `python/create_pdf_reports.py` (one-time setup: `pip install playwright` then `playwright install chromium`) - renders that template through headless Chromium and prints it to PDF.
- Output: `reports/Topgolf_Venue_Report_[VenueName]_1PAGE.pdf`
- Use for: Email attachments, printing, sharing outside a browser

### Markdown (1-Page)
- Template: `templates/venue-1page-report.md.j2` (Jinja2)
- Generator: `python/create_markdown_reports.py`
- Output: `reports/Topgolf_Venue_Report_[VenueName]_1PAGE.md`
- Use for: Email, documentation, version control

Note: this project's current single-venue reports deliberately have no network-benchmark column (see `report_engine.py` / `templates/metrics.json`) - the "Benchmark" column shown in the example below is from an earlier iteration and does not reflect the current templates.

---

## Example: Complete 1-Page Report (illustrative only - see note above re: benchmarks)

See: `example-data/Topgolf_Venue_Report_Myrtle_Beach_20260829_1PAGE.md`
