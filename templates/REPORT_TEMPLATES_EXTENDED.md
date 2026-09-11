# Topgolf Venue Report - EXTENDED Template

**Purpose:** Comprehensive analysis for operations teams and strategic planning  
**Length:** 5-8 pages when printed  
**Audience:** Operations managers, regional directors, strategic planners  
**Format:** Markdown (for detailed analysis and documentation)

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

**Length:** 3-4 sentences  
**Purpose:** Detailed characterization of venue performance  
**Data Source:** Quantitative summary + qualitative themes + context

**Template:**
```
[Venue] is a [characterization] Topgolf venue that [primary strength] but [primary challenge]. 
The venue shows a clear pattern: [key insight about what drives satisfaction]. 
[Assessment of capability vs. execution]. [Context about venue positioning or trajectory].
```

**Example:**
```
Myrtle Beach is a high-traffic Topgolf venue that delivers strong entertainment value but 
faces consistent challenges with equipment reliability and response time. The venue shows a 
clear pattern: guests enjoy the experience when things work smoothly, but equipment issues 
create significant friction that impacts satisfaction and recommendation intent.
```

---

### 3. Performance Summary

**Length:** 1 table + 2-3 sentence assessment  
**Purpose:** Detailed metrics overview with context  
**Data Source:** Aggregated CSV metrics

**Table Structure:**

| Metric | Score | Surveys | Assessment |
|---|---:|---:|---|
| Likelihood to Recommend (LTR) | [AVG(Q1_LTR)] | [COUNT(Q1_LTR)] | [Assessment] |
| Fun | [AVG(Q2_FUN_NUMERIC)] | [COUNT(Q2_FUN)] | [Assessment] |
| Helpfulness | [AVG(Q3_HELPFUL_NUMERIC)] | [COUNT(Q3_HELPFUL)] | [Assessment] |
| Issues Reported | [PERCENT(Q4_ISSUES="Yes")] | [COUNT(Q4_ISSUES)] | [Assessment] |
| Issue Resolution | [AVG(Q5_ISSUE_RESOLUTION_NUMERIC)] | [COUNT(Q5_ISSUE_RESOLUTION)] | [Assessment] |

**Overall Assessment:** 2-3 sentences synthesizing metrics

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

| Attribute | Score | Benchmark | Status |
|---|---:|---|---|
| Likelihood to Recommend | [VENUE_AVG] / 10 | [NETWORK_AVG] (network avg) | [Status] |
| Fun | [VENUE_AVG] / 5 | [NETWORK_AVG] (network avg) | [Status] |
| Helpfulness | [VENUE_AVG] / 5 | [NETWORK_AVG] (network avg) | [Status] |
| Issues Reported | [VENUE_PERCENT]% | [NETWORK_PERCENT]% (network avg) | [Status] |
| Issue Resolution | [VENUE_AVG] / 5 | [NETWORK_AVG] (network avg) | [Status] |

---

### 5. What Made Overall Scores Go Up

**Length:** 3 subsections with detailed explanations  
**Purpose:** Identify and explain positive drivers  
**Data Source:** High-scoring responses + positive comments

**Format:**
```
### [Theme Name]

[Detailed explanation of the theme, including:]
- What guests said in comments
- How this theme manifests in the data
- Why this matters for the venue
- Implications for operations
```

**How to Derive:**
1. Filter for Q1_LTR ≥ 8 or Q2_FUN = "5 - Extremely fun"
2. Read Q6_COMMENT for these responses
3. Identify 3 most common positive themes
4. For each theme, write 3-4 sentences explaining it

**Example:**
```
### Strong entertainment value despite operational challenges

All four guests rated the experience as "Very fun" or "Extremely fun," indicating that the 
core entertainment offering is working well. Even guests who experienced equipment issues 
still found the games themselves enjoyable, suggesting that the venue's game selection and 
setup are solid.
```

---

### 6. What Made Overall Scores Go Down

**Length:** 3 subsections with detailed explanations  
**Purpose:** Identify and explain negative drivers  
**Data Source:** Low-scoring responses + negative comments

**Format:**
```
### [Theme Name]

[Detailed explanation of the theme, including:]
- What guests said in comments
- How this theme manifests in the data
- Why this is a problem
- Impact on other metrics
- Root cause assessment
```

**How to Derive:**
1. Filter for Q1_LTR ≤ 6 or Q2_FUN ≤ 2
2. Filter for Q4_ISSUES = "Yes"
3. Read Q6_COMMENT for these responses
4. Identify 3 most common negative themes
5. For each theme, write 4-6 sentences explaining it

**Example:**
```
### High frequency of equipment issues

**50% of guests reported experiencing an issue—significantly above the network average of 37%.** 
This is the most critical finding. Both guests who experienced issues reported bay tracking 
problems ("screen stopped tracking shots"), indicating a systemic equipment problem rather than 
isolated incidents.

**Key insight:** With a 50% issue rate, Myrtle Beach is experiencing equipment failures in 
half of all visits. This is not a minor friction point—it's a major operational constraint 
that requires immediate attention.
```

---

### 7. What Impacted Overall Scores Most

**Length:** 1 table (5 rows) + explanatory paragraph  
**Purpose:** Rank drivers by impact on LTR  
**Data Source:** Correlation analysis + comment themes

**Table Structure:**

| Relative Rank | Attribute | Evidence |
|---:|---|---|
| 1 | [Top Driver] | [Quantitative or qualitative evidence] |
| 2 | [Second Driver] | [Evidence] |
| 3 | [Third Driver] | [Evidence] |
| 4 | [Fourth Driver] | [Evidence] |
| 5 | [Fifth Driver] | [Evidence] |

**Explanatory Paragraph:**
```
Based on guest comments and survey responses, the relative importance of experience drivers 
at [Venue] appears to be: [brief explanation of ranking methodology and key insights]
```

**Example:**
```
Based on guest comments and survey responses, the relative importance of experience drivers 
at Myrtle Beach appears to be:

| 1 | Equipment Reliability | 50% issue rate; all issues were equipment-related |
| 2 | Response Time | Same issue produced LTR=9 vs LTR=4 based on response speed |
| 3 | Fun (entertainment value) | Consistently strong across all guests |
| 4 | Staff Knowledge | Guests appreciate staff who explain games well |
| 5 | Likelihood to Recommend | Driven primarily by whether issues occurred and were resolved quickly |
```

---

### 8. What to Focus on Most

**Length:** 3 subsections with detailed action plans  
**Purpose:** Provide strategic priorities and tactical actions  
**Data Source:** Gaps + best practices

#### 8a. Critical Priority: [Top Gap]

**Format:**
```
### Critical Priority: [Gap Name]

[1-2 sentence explanation of why this is critical]

- **[Action Name]**: [Detailed description of what to do and why]
  - [Sub-action or consideration]
  - [Sub-action or consideration]

- **[Action Name]**: [Detailed description]
  - [Sub-action or consideration]
  - [Sub-action or consideration]

- **[Action Name]**: [Detailed description]
  - [Sub-action or consideration]
  - [Sub-action or consideration]

- **[Action Name]**: [Detailed description]
  - [Sub-action or consideration]
  - [Sub-action or consideration]
```

**Example:**
```
### Critical Priority: Reduce Equipment Issue Frequency

**Myrtle Beach's 50% issue rate is the single biggest threat to venue performance.** This is 
not a customer-service problem—it's an operational/equipment problem. Recommended actions:

- **Root cause analysis**: Identify why bay tracking systems are failing so frequently
  - Is it a specific equipment model or age?
  - Is it environmental (humidity, temperature)?
  - Is it a configuration or calibration issue?
  - Is it inadequate maintenance?

- **Preventive maintenance audit**: 
  - Review maintenance logs for the past 90 days
  - Identify any patterns (time of day, specific bays, specific equipment types)
  - Assess whether current maintenance schedule is adequate

- **Hardware assessment**:
  - Evaluate whether bay tracking systems need replacement or upgrade
  - Consider whether equipment is aging beyond its useful life
  - Assess whether newer equipment models have better reliability

- **Immediate mitigation**:
  - Implement daily pre-opening equipment checks
  - Establish a "bay health" monitoring system to detect issues before guests encounter them
  - Consider temporarily taking problematic bays offline if they cannot be reliably fixed
```

#### 8b. Secondary Priority: [Second Gap]

**Format:** Same as 8a, with 3-4 actions

#### 8c. Maintain Strengths: [Top Strength]

**Format:** Same as 8a, with 3-4 actions

---

### 9. Comparative Performance

**Length:** 2 subsections with tables and analysis  
**Purpose:** Contextualize venue performance  
**Data Source:** Venue metrics + network/competitor data

#### 9a. vs. Network Average

**Table Structure:**

| Metric | [Venue] | Network Avg | Difference |
|---|---:|---:|---|
| LTR | [VENUE] | [NETWORK] | [DIFF] ↓/↑ |
| Fun | [VENUE] | [NETWORK] | [DIFF] ↓/↑ |
| Helpfulness | [VENUE] | [NETWORK] | [DIFF] ↓/↑ |
| Issues | [VENUE]% | [NETWORK]% | [DIFF]% ↑/↓ |
| Issue Resolution | [VENUE] | [NETWORK] | [DIFF] ↓/↑ |

**Interpretation Paragraph:**
```
[2-3 sentences explaining what the comparison reveals about the venue's relative performance]
```

**Example:**
```
**Interpretation:** Myrtle Beach's underperformance is driven almost entirely by the elevated 
issue rate. The venue's entertainment and staff capabilities are on par with or above network 
average, but the frequency of equipment problems is dragging down all other metrics.
```

#### 9b. vs. Top Performers

**Table Structure:**

| Metric | [Venue] | [Top Performer] | Gap |
|---|---:|---:|---|
| LTR | [VENUE] | [TOP] | [GAP] |
| Fun | [VENUE] | [TOP] | [GAP] |
| Helpfulness | [VENUE] | [TOP] | [GAP] |
| Issues | [VENUE]% | [TOP]% | [GAP]% |
| Issue Resolution | [VENUE] | [TOP] | [GAP] |

**Interpretation Paragraph:**
```
[2-3 sentences explaining what the gap reveals and what the top performer is doing differently]
```

**Example:**
```
**Interpretation:** The gap between Myrtle Beach and Waco is almost entirely explained by 
equipment reliability. Waco's 3.8% issue rate (vs. Myrtle Beach's 50%) indicates that Waco 
has either superior equipment, superior maintenance, or superior preventive practices. This 
is the key area for Myrtle Beach to investigate and improve.
```

---

### 10. Guest Comments Analysis

**Length:** 2 subsections with detailed comment review  
**Purpose:** Provide qualitative context for quantitative findings  
**Data Source:** Q6_COMMENT field

#### 10a. Positive Comments

**Format:**
```
### Positive Comments ([X] of [Y] guests)

1. **"[Direct quote from Q6_COMMENT]"**
   - Highlights: [Key positive aspects mentioned]
   - Implication: [What this tells us about the venue]

2. **"[Direct quote]"**
   - Highlights: [Key positive aspects]
   - Implication: [What this tells us]
```

**Example:**
```
### Positive Comments (2 of 4 guests)

1. **"We had a good time and the staff was especially helpful explaining the games to the 
   newer golfers in our group."**
   - Highlights: Staff knowledge, educational approach, positive social experience
   - Implication: Staff are well-trained and engaged; venue attracts diverse skill levels

2. **"The screen stopped tracking shots for a few minutes, but someone came over quickly and 
   fixed it. Great experience overall."**
   - Highlights: Quick response, effective resolution, positive outcome despite problem
   - Implication: When staff respond quickly, equipment issues don't significantly damage satisfaction
```

#### 10b. Negative Comments

**Format:**
```
### Negative Comments ([X] of [Y] guests)

1. **"[Direct quote]"**
   - **Issue type**: [What went wrong]
   - **Root cause**: [Why it happened]
   - **Outcome**: [Impact on guest experience]
   - **Implication**: [What this tells us about the venue]

2. **"[Direct quote]"**
   - **Issue type**: [What went wrong]
   - **Root cause**: [Why it happened]
   - **Outcome**: [Impact on guest experience]
   - **Implication**: [What this tells us]
```

**Example:**
```
### Negative Comments (2 of 4 guests)

1. **"We waited quite a while for assistance when the bay equipment stopped working. It was 
   eventually fixed, but we lost playing time."**
   - **Issue type**: Equipment failure (bay equipment)
   - **Root cause**: Slow response time
   - **Outcome**: Lost playing time, reduced satisfaction, LTR = 4
   - **Implication**: Slow response compounds the frustration of equipment failure

2. **"We had trouble getting one of the games to start. It took a little while to get help, 
   but the issue was resolved."**
   - **Issue type**: Game startup failure
   - **Root cause**: Slow response time
   - **Outcome**: Delayed start, moderate satisfaction, LTR = 7
   - **Implication**: Even when resolved, slow response reduces satisfaction
```

---

### 11. Key Observations & Recommendations

**Length:** 3 subsections with detailed action plan  
**Purpose:** Synthesize all findings into actionable plan  
**Data Source:** All previous sections

#### 11a. What's Working Well

**Format:**
```
1. **[Strength Name]**: [Detailed description]
2. **[Strength Name]**: [Detailed description]
3. **[Strength Name]**: [Detailed description]
4. **[Strength Name]**: [Detailed description]
```

#### 11b. What Needs Urgent Attention

**Format:**
```
1. **[Gap Name]**: [Detailed description]
2. **[Gap Name]**: [Detailed description]
3. **[Gap Name]**: [Detailed description]
4. **[Gap Name]**: [Detailed description]
```

#### 11c. Recommended Action Plan

**Format:**
```
**This Week (Urgent):**
- [ ] [Action item]
  - [Sub-action]
  - [Sub-action]
- [ ] [Action item]
  - [Sub-action]
  - [Sub-action]

**Next 2-4 Weeks:**
- [ ] [Action item]
  - [Sub-action]
  - [Sub-action]
- [ ] [Action item]
  - [Sub-action]
  - [Sub-action]

**Ongoing:**
- [ ] [Action item]
  - [Sub-action]
  - [Sub-action]
- [ ] [Action item]
  - [Sub-action]
  - [Sub-action]
```

**Example:**
```
**This Week (Urgent):**
- [ ] Conduct root-cause analysis of bay tracking system failures
  - Interview staff about frequency, timing, and patterns
  - Review maintenance logs for the past 30 days
  - Physically inspect bays for signs of wear or misconfiguration
- [ ] Identify which bays are most problematic and prioritize maintenance
- [ ] Implement daily pre-opening equipment checks
- [ ] Brief staff on the importance of rapid response and establish clear escalation procedures

**Next 2-4 Weeks:**
- [ ] Implement automated bay-monitoring system to detect issues before guests encounter them
- [ ] Conduct preventive maintenance on all bays (cleaning, calibration, component replacement as needed)
- [ ] Establish response-time standard and tracking mechanism
- [ ] Review staffing levels during peak hours and adjust if necessary
- [ ] Conduct staff training on rapid troubleshooting and guest communication

**Ongoing:**
- [ ] Track issue rate weekly and trend against network average
- [ ] Monitor response-time compliance
- [ ] Assess whether equipment replacement is needed
- [ ] Maintain strong service culture and staff engagement
- [ ] Share learnings with other venues experiencing similar issues
```

---

### 12. Data Quality Notes

**Length:** 3-4 bullet points  
**Purpose:** Provide context for interpreting results  
**Data Source:** CSV metadata + analysis notes

**Format:**
```
- **[Note Category]**: [Explanation of limitation or context]
- **[Note Category]**: [Explanation]
- **[Note Category]**: [Explanation]
- **[Note Category]**: [Explanation]
```

**Example:**
```
- **Sample size**: 4 survey responses this week. This is a very small sample, so results 
  should be treated as directional.

- **Issue rate stability**: The 50% issue rate is consistent with the broader venue rankings 
  data (September 7), which shows Myrtle Beach at 12.8% issues with 160 responses. The higher 
  rate this week may reflect random variation or a temporary equipment problem.

- **Issue resolution sample**: Only 2 guests reported issues and provided resolution feedback, 
  so the Issue Resolution score is based on a small subset.

- **Broader context**: The venue rankings data shows Myrtle Beach at Rank 6 overall with 
  strong Fun (Rank 2) but weaker LTR (Rank 23), which aligns with this week's findings that 
  entertainment is strong but recommendation intent is constrained by operational issues.
```

---

### 13. Conclusion

**Length:** 3-4 sentences  
**Purpose:** Synthesize findings and provide forward-looking perspective  
**Data Source:** All previous sections

**Template:**
```
[Venue] is a venue with [key strengths], but it is [key constraint]. The venue's [primary 
metric] this week is [assessment] and represents [opportunity or threat]. The good news is 
that [positive capability or finding], suggesting that [implication]. By focusing on 
[critical priority] and [secondary priority], [Venue] can [expected outcome].
```

**Example:**
```
Myrtle Beach is a venue with strong entertainment value and engaged staff, but it is 
significantly constrained by equipment reliability issues. The venue's 50% issue rate this 
week is well above network average and represents the primary opportunity for improvement. 
The good news is that Myrtle Beach has demonstrated the capability to resolve issues quickly 
(as evidenced by the guest who received prompt assistance), suggesting that the problem is 
not a lack of capability but rather inconsistent execution or inadequate preventive 
maintenance. By focusing on equipment reliability and standardizing response time, Myrtle 
Beach can significantly improve its performance and move closer to the network leaders.
```

---

## Data Processing Checklist

- [ ] Filter CSV by venue and date range
- [ ] Calculate 5 metrics (LTR, Fun, Helpfulness, Issues %, Resolution)
- [ ] Compare to network benchmarks
- [ ] Compare to top performer benchmarks
- [ ] Analyze Q6_COMMENT for themes and sentiment
- [ ] Identify top 3 positive drivers with detailed explanations
- [ ] Identify top 3 negative drivers with detailed explanations
- [ ] Rank 5 drivers by impact with evidence
- [ ] Extract and categorize positive comments
- [ ] Extract and categorize negative comments
- [ ] List 4 strengths with detailed descriptions
- [ ] List 4 gaps with detailed descriptions
- [ ] Define 3 priority levels with 4 detailed actions each
- [ ] Create action plan with timeline (This Week, Next 2-4 Weeks, Ongoing)
- [ ] Add data quality notes and limitations
- [ ] Write narrative sections (Overview, Assessment, Interpretation, Conclusion)

---

## Output Format

### Markdown (Extended)
- File: `Topgolf_Venue_Report_[VenueName]_[Date].md`
- Use for: Detailed analysis, documentation, strategic planning, version control

---

## Example: Complete Extended Report

See: `Topgolf_Venue_Report_Myrtle_Beach_20260829.md`

