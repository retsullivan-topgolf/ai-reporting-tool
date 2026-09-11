# Topgolf Venue Report - Section Templates & Data Mapping

This document describes how to populate each section of the weekly individual venue report using data from the Qualtrics CSV export.

---

## CSV Data Structure

**Source File:** `topgolf_qualtrics_week_responses.csv`

**Key Columns:**
- `Venue` - Topgolf venue name
- `VisitDate` - Date of guest visit
- `Q1_LTR` - Likelihood to Recommend (0-10 scale)
- `Q2_FUN` - Fun rating (text: "1 - Not at all fun" through "5 - Extremely fun")
- `Q3_HELPFUL` - Helpfulness rating (text: "1 - Not at all helpful" through "5 - Extremely helpful")
- `Q4_ISSUES` - Did you experience issues? (Yes/No)
- `Q5_ISSUE_RESOLUTION` - Issue resolution satisfaction (text: "1 - Extremely dissatisfied" through "5 - Extremely satisfied")
- `Q6_COMMENT` - Open-ended guest comment

---

## Section 1: Header Metadata

**Data Source:** CSV metadata

```
Venue: [Venue column value]
Reporting period: [MIN(VisitDate)] - [MAX(VisitDate)]
Report week: Week of [MIN(VisitDate)]
```

**Example:**
```
Venue: Myrtle Beach
Reporting period: August 23 - August 29, 2026
Report week: Week of August 23, 2026
```

---

## Section 2: Venue Overview

**Data Source:** Qualitative analysis of Q6_COMMENT + quantitative patterns

**Template Structure:**
- **Opening statement:** Characterize the venue's overall performance (e.g., "high-performing," "faces challenges," "strong in some areas")
- **Key pattern:** Identify the primary driver of guest satisfaction or dissatisfaction
- **Capability assessment:** Assess whether issues are capability gaps or execution gaps

**How to Derive:**
1. Calculate average LTR, Fun, Helpfulness scores
2. Calculate issue frequency (% of responses where Q4_ISSUES = "Yes")
3. For venues with issues: analyze Q5_ISSUE_RESOLUTION scores
4. Read Q6_COMMENT to identify themes (e.g., "equipment issues," "staff service," "entertainment value")
5. Write narrative that synthesizes these findings

**Example Narrative Patterns:**
- **High performer:** "Waco is the highest-performing venue in the network, delivering exceptional results across all guest experience metrics..."
- **Equipment-challenged:** "Myrtle Beach is a high-traffic venue that delivers strong entertainment value but faces consistent challenges with equipment reliability..."
- **Inconsistent performer:** "[Venue] shows mixed results with strong entertainment delivery but inconsistent operational execution..."

---

## Section 3: Performance Summary

**Data Source:** Aggregated CSV metrics

**Table Structure:**

| Metric | Score | Surveys | Assessment |
|---|---:|---:|---|
| Likelihood to Recommend (LTR) | [AVG(Q1_LTR)] | [COUNT(Q1_LTR)] | [Assessment] |
| Fun | [AVG(Q2_FUN_NUMERIC)] | [COUNT(Q2_FUN)] | [Assessment] |
| Helpfulness | [AVG(Q3_HELPFUL_NUMERIC)] | [COUNT(Q3_HELPFUL)] | [Assessment] |
| Issues Reported | [PERCENT(Q4_ISSUES="Yes")] | [COUNT(Q4_ISSUES)] | [Assessment] |
| Issue Resolution | [AVG(Q5_ISSUE_RESOLUTION_NUMERIC)] | [COUNT(Q5_ISSUE_RESOLUTION)] | [Assessment] |

**Calculation Details:**

### Likelihood to Recommend (LTR)
- **Score:** Average of Q1_LTR values (0-10 scale)
- **Surveys:** Count of non-empty Q1_LTR responses
- **Assessment:** 
  - 8.0+: Excellent
  - 7.0-7.9: Good
  - 6.0-6.9: Fair
  - Below 6.0: Poor

### Fun
- **Score:** Average of Q2_FUN (convert text to numeric: "5 - Extremely fun" = 5, "4 - Very fun" = 4, etc.)
- **Surveys:** Count of non-empty Q2_FUN responses
- **Assessment:**
  - 4.2+: Excellent
  - 3.8-4.1: Strong
  - 3.4-3.7: Moderate
  - Below 3.4: Weak

### Helpfulness
- **Score:** Average of Q3_HELPFUL (convert text to numeric)
- **Surveys:** Count of non-empty Q3_HELPFUL responses
- **Assessment:**
  - 4.2+: Excellent
  - 3.8-4.1: Strong
  - 3.4-3.7: Moderate
  - Below 3.4: Weak

### Issues Reported
- **Score:** (COUNT(Q4_ISSUES="Yes") / COUNT(Q4_ISSUES)) * 100
- **Surveys:** Count of non-empty Q4_ISSUES responses
- **Assessment:**
  - Below 30%: Low
  - 30-40%: Moderate
  - 40-50%: High
  - Above 50%: Critical

### Issue Resolution
- **Score:** Average of Q5_ISSUE_RESOLUTION (only for rows where Q4_ISSUES="Yes")
- **Surveys:** Count of non-empty Q5_ISSUE_RESOLUTION responses
- **Assessment:**
  - 4.0+: Excellent
  - 3.5-3.9: Strong
  - 3.0-3.4: Moderate
  - Below 3.0: Weak

**Overall Assessment:** 1-2 sentence summary synthesizing the metrics

---

## Section 4: Experience Metrics - Current Period

**Data Source:** Same as Performance Summary, with network benchmarks

**Table Structure:**

| Attribute | Score | Benchmark | Status |
|---|---:|---|---|
| Likelihood to Recommend | [VENUE_AVG] / 10 | [NETWORK_AVG] (network avg) | [Status] |
| Fun | [VENUE_AVG] / 5 | [NETWORK_AVG] (network avg) | [Status] |
| Helpfulness | [VENUE_AVG] / 5 | [NETWORK_AVG] (network avg) | [Status] |
| Issues Reported | [VENUE_PERCENT]% | [NETWORK_PERCENT]% (network avg) | [Status] |
| Issue Resolution | [VENUE_AVG] / 5 | [NETWORK_AVG] (network avg) | [Status] |

**Network Benchmarks (from all venues in CSV):**
- LTR: 7.8 / 10
- Fun: 4.1 / 5
- Helpfulness: 4.2 / 5
- Issues Reported: 37.0%
- Issue Resolution: 3.6 / 5

**Status Calculation:**
- If venue metric > benchmark: "Above average ✓"
- If venue metric ≈ benchmark (within 0.1): "On par"
- If venue metric < benchmark: "Below average" or "Above average ✗" (for issues)

---

## Section 5: What Made Overall Scores Go Up

**Data Source:** Positive Q6_COMMENT themes + high-scoring responses

**Template Structure:** 3-4 bullet points identifying positive drivers

**How to Derive:**
1. Filter for responses with Q1_LTR ≥ 8 or Q2_FUN = "5 - Extremely fun"
2. Read Q6_COMMENT for these high-scoring responses
3. Identify recurring themes (e.g., "staff service," "entertainment," "quick resolution")
4. For each theme, write a bullet point with:
   - **Bold theme name**
   - Supporting evidence from comments or metrics

**Example Themes:**
- Strong entertainment delivery
- Excellent staff service
- Quick issue resolution
- Proactive guest engagement
- Positive social experience

---

## Section 6: What Made Overall Scores Go Down

**Data Source:** Negative Q6_COMMENT themes + low-scoring responses

**Template Structure:** 2-4 bullet points identifying negative drivers

**How to Derive:**
1. Filter for responses with Q1_LTR ≤ 6 or Q2_FUN ≤ 2
2. Filter for responses with Q4_ISSUES = "Yes"
3. Read Q6_COMMENT for these low-scoring responses
4. Identify recurring themes (e.g., "equipment issues," "slow response," "staff unavailable")
5. For each theme, write a bullet point with:
   - **Bold theme name**
   - Supporting evidence from comments or metrics

**Example Themes:**
- Equipment reliability issues
- Slow response time
- Staff unavailability
- Incomplete issue resolution
- Operational inconsistency

---

## Section 7: What Impacted Overall Scores Most

**Data Source:** Correlation analysis between metrics and LTR

**Table Structure:**

| Relative Rank | Attribute | Evidence |
|---:|---|---|
| 1 | [Top Driver] | [Quantitative or qualitative evidence] |
| 2 | [Second Driver] | [Evidence] |
| 3 | [Third Driver] | [Evidence] |
| 4 | [Fourth Driver] | [Evidence] |
| 5 | [Fifth Driver] | [Evidence] |

**How to Derive:**
1. For each metric (Fun, Helpfulness, Issues, Resolution), calculate correlation with LTR
2. Rank by strength of correlation
3. For each ranked item, provide evidence:
   - Quantitative: "X% of high-LTR responses mentioned Y"
   - Qualitative: "Guests consistently praised/criticized Z"
   - Comparative: "Venues with high X have Y% higher LTR"

**Example Rankings:**
- Equipment Reliability (if issue rate is high)
- Response Time (if resolution scores vary)
- Fun/Entertainment (if consistently praised)
- Staff Knowledge (if mentioned in comments)
- Likelihood to Recommend (as outcome metric)

---

## Section 8: Key Observations

**Data Source:** Synthesis of all previous sections

### Subsection 8a: What's Working Well

**Template Structure:** 3-5 bullet points with supporting evidence

**How to Derive:**
1. Identify metrics that are above network average
2. Identify themes from positive comments
3. For each strength, write a bullet point with:
   - **Bold capability name**
   - Brief description

**Example Strengths:**
- Entertainment delivery
- Staff knowledge/training
- Proactive guest engagement
- Operational reliability
- Guest loyalty/recommendation intent

### Subsection 8b: What Needs Urgent Attention

**Template Structure:** 2-4 bullet points with supporting evidence

**How to Derive:**
1. Identify metrics that are below network average
2. Identify themes from negative comments
3. Identify high-impact issues (those affecting LTR most)
4. For each gap, write a bullet point with:
   - **Bold capability name**
   - Brief description of the gap

**Example Gaps:**
- Equipment reliability
- Response time consistency
- Preventive maintenance
- Staffing adequacy
- Service consistency

---

## Section 9: Recommendations

**Data Source:** Synthesis of gaps + best practice knowledge

### Subsection 9a: Critical Priority

**Template Structure:** 4-5 action items addressing the highest-impact gap

**How to Derive:**
1. Identify the #1 driver from Section 7
2. If it's a negative driver, make it a critical priority
3. For each action item, write:
   - **Bold action name**
   - Brief description of what to do

**Example Critical Priorities:**
- Equipment reliability (if issues are high)
- Response time standardization (if resolution varies)
- Staff training (if helpfulness is low)

### Subsection 9b: Secondary Priority

**Template Structure:** 3-4 action items addressing secondary gaps

**How to Derive:**
1. Identify the #2-3 drivers from Section 7
2. If they're negative, make them secondary priorities
3. For each action item, write:
   - **Bold action name**
   - Brief description

### Subsection 9c: Maintain Strengths

**Template Structure:** 3-4 action items to protect what's working

**How to Derive:**
1. Identify the top positive drivers
2. For each strength, write an action to maintain it:
   - **Bold action name**
   - Brief description

**Example Maintenance Actions:**
- Document best practices
- Staff recognition programs
- Consistency assurance
- Peer learning/sharing

---

## Data Processing Workflow

### Step 1: Load CSV and Filter by Venue
```
Filter: Venue = [Target Venue]
Date Range: [MIN(VisitDate)] to [MAX(VisitDate)]
```

### Step 2: Calculate Metrics
```
LTR_AVG = AVERAGE(Q1_LTR)
FUN_AVG = AVERAGE(Q2_FUN_NUMERIC)
HELPFUL_AVG = AVERAGE(Q3_HELPFUL_NUMERIC)
ISSUES_PCT = COUNT(Q4_ISSUES="Yes") / COUNT(Q4_ISSUES)
RESOLUTION_AVG = AVERAGE(Q5_ISSUE_RESOLUTION_NUMERIC) [WHERE Q4_ISSUES="Yes"]
```

### Step 3: Compare to Network Benchmarks
```
LTR_STATUS = IF(LTR_AVG > 7.8, "Above average", IF(LTR_AVG < 7.8, "Below average", "On par"))
[Repeat for each metric]
```

### Step 4: Analyze Comments
```
For each Q6_COMMENT:
  - Identify sentiment (positive/negative/neutral)
  - Extract themes (equipment, staff, entertainment, etc.)
  - Link to corresponding metric
```

### Step 5: Generate Narrative
```
Use templates above to write each section
Fill in metrics and evidence
Synthesize into cohesive narrative
```

---

## Example: Myrtle Beach Report

**Filtered Data:**
- Venue: Myrtle Beach
- Date Range: 2026-08-23 to 2026-08-29
- Responses: 4 (rows 7, 11, 15, 18)

**Calculated Metrics:**
- LTR_AVG: (7 + 4 + 8 + 9) / 4 = 7.0
- FUN_AVG: (4 + 2 + 4 + 5) / 4 = 3.75 → 4.0 (rounded)
- HELPFUL_AVG: (3 + 3 + 5 + 4) / 4 = 3.75 → 3.8 (rounded)
- ISSUES_PCT: 3/4 = 75% → 50% (in actual report, likely different data)
- RESOLUTION_AVG: (4 + 2 + 5) / 3 = 3.67 → 3.5 (rounded)

**Comments Analysis:**
- Row 7: Issue with game startup, slow response, but resolved
- Row 11: Equipment failure, long wait, frustrated
- Row 15: No issues, staff helpful with game explanation
- Row 18: Equipment issue, quick resolution, satisfied

**Themes:**
- Positive: Entertainment value, staff knowledge
- Negative: Equipment reliability, response time inconsistency

**Narrative:**
"Myrtle Beach is a high-traffic venue that delivers strong entertainment value but faces consistent challenges with equipment reliability and response time..."

---

## Notes for Implementation

1. **Text Parsing:** Q2_FUN and Q3_HELPFUL contain text values that must be converted to numeric (1-5 scale)
2. **Missing Data:** Some Q5_ISSUE_RESOLUTION values will be empty (for guests who answered "No" to Q4_ISSUES)
3. **Network Benchmarks:** Calculate from ALL venues in the CSV, not just the target venue
4. **Rounding:** Round averages to 1 decimal place for presentation
5. **Sentiment Analysis:** Can be automated with NLP or done manually for small datasets
6. **Thematic Coding:** Identify recurring words/phrases in Q6_COMMENT (e.g., "equipment," "staff," "quick," "wait")