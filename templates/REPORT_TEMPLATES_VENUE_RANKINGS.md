# Topgolf Venue Rankings - Weekly Report Template

**Purpose:** Network-wide comparison of guest experience performance across all venues  
**Length:** 2-5 pages (summary + detailed rankings)  
**Audience:** Corporate leadership, regional directors, operations teams  
**Format:** Markdown (summary) + HTML (interactive rankings table)  
**Frequency:** Weekly

---

## Report Purpose & Structure

The Weekly Guest Experience Venue Rankings report answers three primary questions:

1. **How is each venue performing relative to other venues?**
2. **Which aspects of the guest experience are driving strong or weak performance?**
3. **Is each venue's relative performance improving, declining, or remaining stable?**

---

## Section 1: Executive Summary

**Length:** 2-3 paragraphs  
**Purpose:** High-level overview of network performance  
**Data Source:** Composite ranks + key metrics

**Template:**

```
This week's guest experience rankings show [overall network trend]. 

[Top performers]: [List top 3 venues with composite ranks and key strengths]

[Areas of concern]: [List bottom 3 venues with composite ranks and key challenges]

[Notable trends]: [Highlight significant rank movements, emerging patterns, or network-wide changes]
```

**Example:**
```
This week's guest experience rankings show strong overall performance with clear leaders 
emerging. Waco continues to dominate with a Composite Rank of 1, supported by exceptional 
scores across all dimensions (LTR 92.3%, Fun 92.3%, Helpfulness 92.3%). Rogers (Rank 2) 
and Buford (Rank 3) also demonstrate strong performance.

Areas of concern include Houston-Katy (Rank 8) with elevated issues (20.6%) and weak issue 
resolution (15.0%), and Bryan (Rank 9) with a small sample size (16 surveys) that limits 
confidence in results.

Notable trends: Myrtle Beach shows strong Fun performance (Rank 2) but weak LTR (Rank 23), 
suggesting that entertainment value is high but recommendation intent is constrained by 
operational issues.
```

---

## Section 2: Overall Rankings Table

**Length:** 1 comprehensive table  
**Purpose:** Display all venues with composite and metric rankings  
**Data Source:** Aggregated survey data

**Table Structure:**

```
| Rank | Venue | Composite Rank | LTR | Fun | Helpfulness | Issues | Issue Resolution | Survey Count |
|---:|---|---:|---|---|---|---|---|---:|
| 1 | [Venue] | 1 | [Score]% (Rank [#]) | [Score]% (Rank [#]) | [Score]% (Rank [#]) | [Score]% (Rank [#]) | [Score]% (Rank [#]) | [Count] |
| 2 | [Venue] | 2 | [Score]% (Rank [#]) | [Score]% (Rank [#]) | [Score]% (Rank [#]) | [Score]% (Rank [#]) | [Score]% (Rank [#]) | [Count] |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

**Rank Shift Notation:**
- `▲` = Improved from previous period
- `▼` = Declined from previous period
- `--` = No change from previous period

**Example:**

```
| Rank | Venue | Composite | LTR | Fun | Helpfulness | Issues | Resolution | Surveys |
|---:|---|---:|---|---|---|---|---|---:|
| 1 | Waco | 1 | 92.3% (▲ Rank 1) | 92.3% (▲ Rank 1) | 92.3% (-- Rank 1) | 3.8% (-- Rank 1) | 100.0% (▲ Rank 1) | 27 |
| 2 | Rogers | 2 | 88.9% (▼ Rank 2) | 88.9% (▲ Rank 3) | 88.9% (▲ Rank 2) | 5.6% (▼ Rank 2) | 80.0% (-- Rank 2) | 36 |
| 3 | Buford | 3 | 85.7% (▲ Rank 3) | 85.7% (-- Rank 4) | 85.7% (-- Rank 3) | 7.1% (-- Rank 3) | 75.0% (▲ Rank 3) | 28 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 8 | Houston-Katy | 8 | 70.0% (▼ Rank 15) | 75.0% (▼ Rank 12) | 72.5% (▼ Rank 14) | 20.6% (▼ Rank 20) | 15.0% (▼ Rank 23) | 40 |
| 9 | Bryan | 9 | 62.5% (▼ Rank 18) | 68.8% (▼ Rank 16) | 65.0% (▼ Rank 17) | 25.0% (▼ Rank 22) | N/A | 16 |
```

---

## Section 3: Metric Definitions & Interpretation Guide

**Length:** Reference section  
**Purpose:** Ensure consistent interpretation of metrics  
**Data Source:** Report definition document

### 3a. LTR (Likelihood to Recommend)

**Definition:** Percentage-based aggregate of guest responses regarding willingness to recommend Topgolf

**Interpretation:** Higher score = better

**Example:**
- Waco: 92.3% (Rank 1) = Strongest recommendation intent in network
- Houston-Katy: 70.0% (Rank 15) = Below-average recommendation intent

### 3b. Fun

**Definition:** Aggregated survey measure of whether guests found their experience fun/enjoyable

**Interpretation:** Higher score = better

**Example:**
- Waco: 92.3% (Rank 1) = Guests consistently rate experience as very fun
- Bryan: 68.8% (Rank 16) = Lower proportion of guests rating experience as fun

### 3c. Helpfulness

**Definition:** Aggregated guest feedback regarding helpfulness of Topgolf team members

**Interpretation:** Higher score = better

**Example:**
- Waco: 92.3% (Rank 1) = Staff perceived as highly helpful
- Houston-Katy: 72.5% (Rank 14) = Staff helpfulness below network average

### 3d. Issues

**Definition:** Percentage of surveyed guests who reported experiencing an issue during their visit

**Interpretation:** **Lower score = better** (INVERSE from other metrics)

**Example:**
- Waco: 3.8% (Rank 1) = Very few guests report issues (GOOD)
- Houston-Katy: 20.6% (Rank 20) = Substantially higher issue rate (POOR)

### 3e. Issue Resolution

**Definition:** Aggregated result for guests who experienced an issue and provided feedback on its resolution

**Interpretation:** Higher score = better

**Important:** Missing values (N/A) do NOT mean poor performance. Possible reasons:
- No guests reported issues
- Too few responses to calculate
- Reporting rules suppressing metric

**Example:**
- Waco: 100.0% (Rank 1) = Issues that occurred were resolved to guest satisfaction
- Houston-Katy: 15.0% (Rank 23) = Guests with issues were less satisfied with resolution

---

## Section 4: Top Performers Analysis

**Length:** 3-5 subsections (one per top venue)  
**Purpose:** Highlight what top venues are doing well  
**Data Source:** Composite rank + metric scores + rank shifts

**Format for Each Top Performer:**

```
### [Rank]. [Venue Name]

**Composite Rank:** [Rank]  
**Survey Count:** [Count] responses

**Performance Profile:**
- **LTR:** [Score]% (Rank [#]) [Trend]
- **Fun:** [Score]% (Rank [#]) [Trend]
- **Helpfulness:** [Score]% (Rank [#]) [Trend]
- **Issues:** [Score]% (Rank [#]) [Trend]
- **Issue Resolution:** [Score]% (Rank [#]) [Trend]

**Key Strengths:**
- [Strength 1]: [Brief explanation]
- [Strength 2]: [Brief explanation]
- [Strength 3]: [Brief explanation]

**Notable Trends:**
- [Trend 1]: [Brief explanation]
- [Trend 2]: [Brief explanation]

**Assessment:** [1-2 sentence summary of what makes this venue a top performer]
```

**Example:**

```
### 1. Waco

**Composite Rank:** 1  
**Survey Count:** 27 responses

**Performance Profile:**
- **LTR:** 92.3% (Rank 1) -- Stable
- **Fun:** 92.3% (Rank 1) ▲ Improved
- **Helpfulness:** 92.3% (Rank 1) -- Stable
- **Issues:** 3.8% (Rank 1) -- Stable
- **Issue Resolution:** 100.0% (Rank 1) ▲ Improved

**Key Strengths:**
- **Consistent Excellence:** Waco ranks #1 across all five dimensions, demonstrating 
  comprehensive operational excellence
- **Low Issue Rate:** Only 3.8% of guests report issues, indicating strong preventive 
  maintenance and operational reliability
- **Perfect Resolution:** 100% of guests with issues report satisfaction with resolution, 
  showing strong problem-solving capability

**Notable Trends:**
- **Improving:** Fun and Issue Resolution both improved this week, suggesting sustained 
  momentum
- **Stable:** LTR, Helpfulness, and Issues remain unchanged, indicating consistent execution

**Assessment:** Waco is the network's benchmark venue, demonstrating that operational 
excellence, strong entertainment value, and excellent staff service can be achieved 
simultaneously and consistently.
```

---

## Section 5: Venues Requiring Attention

**Length:** 2-4 subsections (one per underperforming venue)  
**Purpose:** Identify venues with challenges  
**Data Source:** Composite rank + metric scores + rank shifts

**Format for Each Underperforming Venue:**

```
### [Rank]. [Venue Name]

**Composite Rank:** [Rank]  
**Survey Count:** [Count] responses [Note if low sample size]

**Performance Profile:**
- **LTR:** [Score]% (Rank [#]) [Trend]
- **Fun:** [Score]% (Rank [#]) [Trend]
- **Helpfulness:** [Score]% (Rank [#]) [Trend]
- **Issues:** [Score]% (Rank [#]) [Trend]
- **Issue Resolution:** [Score]% (Rank [#]) [Trend]

**Key Challenges:**
- [Challenge 1]: [Brief explanation with metric evidence]
- [Challenge 2]: [Brief explanation with metric evidence]
- [Challenge 3]: [Brief explanation with metric evidence]

**Notable Trends:**
- [Trend 1]: [Brief explanation]
- [Trend 2]: [Brief explanation]

**Recommended Focus Areas:**
- [Priority 1]: [Action to address challenge]
- [Priority 2]: [Action to address challenge]

**Assessment:** [1-2 sentence summary of the venue's situation and recommended focus]
```

**Example:**

```
### 8. Houston-Katy

**Composite Rank:** 8  
**Survey Count:** 40 responses

**Performance Profile:**
- **LTR:** 70.0% (Rank 15) ▼ Declined
- **Fun:** 75.0% (Rank 12) ▼ Declined
- **Helpfulness:** 72.5% (Rank 14) ▼ Declined
- **Issues:** 20.6% (Rank 20) ▼ Declined
- **Issue Resolution:** 15.0% (Rank 23) ▼ Declined

**Key Challenges:**
- **High Issue Rate:** 20.6% of guests report issues, significantly above network average 
  (12.0%), indicating operational or equipment reliability problems
- **Weak Issue Resolution:** Only 15.0% satisfaction with issue resolution (Rank 23), 
  suggesting that when problems occur, guests are not satisfied with how they're handled
- **Declining Performance:** All five metrics declined this week, indicating deteriorating 
  guest experience

**Notable Trends:**
- **Downward Trajectory:** Every metric declined this week, suggesting systemic issues 
  rather than isolated problems
- **Compounding Effect:** High issue rate combined with poor resolution creates double 
  negative impact on LTR

**Recommended Focus Areas:**
- **Equipment Reliability:** Conduct root-cause analysis of why 20.6% of guests report issues
- **Response & Resolution:** Implement rapid-response protocols and staff training on issue 
  resolution
- **Preventive Maintenance:** Review maintenance schedules and implement proactive monitoring

**Assessment:** Houston-Katy is experiencing significant performance challenges across all 
dimensions. The combination of high issue frequency and poor resolution suggests operational 
problems that require immediate attention.
```

---

## Section 6: Rank Movement & Trends

**Length:** 1-2 subsections  
**Purpose:** Highlight venues with significant changes  
**Data Source:** Rank shift indicators + metric trends

**Format:**

```
### Venues with Improving Trends

[List venues with ▲ indicators]

- **[Venue]:** [Metric] improved from Rank [X] to Rank [Y], suggesting [implication]
- **[Venue]:** [Metric] improved from Rank [X] to Rank [Y], suggesting [implication]

### Venues with Declining Trends

[List venues with ▼ indicators]

- **[Venue]:** [Metric] declined from Rank [X] to Rank [Y], suggesting [implication]
- **[Venue]:** [Metric] declined from Rank [X] to Rank [Y], suggesting [implication]

### Venues to Watch

[List venues with multiple changes or concerning patterns]

- **[Venue]:** [Pattern description]
- **[Venue]:** [Pattern description]
```

**Example:**

```
### Venues with Improving Trends

- **Waco:** Fun improved to Rank 1, Issue Resolution improved to Rank 1, suggesting 
  sustained momentum in both entertainment and problem-solving
- **Buford:** LTR improved to Rank 3, Issue Resolution improved to Rank 3, indicating 
  strengthening guest advocacy and issue handling

### Venues with Declining Trends

- **Houston-Katy:** All five metrics declined this week, with LTR dropping to Rank 15 and 
  Issue Resolution to Rank 23, indicating systemic performance deterioration
- **Rogers:** LTR declined to Rank 2 and Issues worsened to Rank 2, suggesting emerging 
  operational challenges

### Venues to Watch

- **Bryan:** Small sample size (16 surveys) limits confidence in results; monitor for 
  sustained low performance or sample size increase
- **Myrtle Beach:** Strong Fun (Rank 2) but weak LTR (Rank 23) and Issue Resolution (Rank 23) 
  suggest entertainment is strong but operational issues are constraining recommendation intent
```

---

## Section 7: Network-Wide Insights

**Length:** 2-3 subsections  
**Purpose:** Identify patterns across the network  
**Data Source:** Aggregated metrics across all venues

**Format:**

```
### Overall Network Performance

[Summary of network-wide metrics]

- **Average LTR:** [Network average]
- **Average Fun:** [Network average]
- **Average Helpfulness:** [Network average]
- **Average Issues:** [Network average]
- **Average Issue Resolution:** [Network average]

[Commentary on network health]

### Performance Gaps

[Identify gaps between top and bottom performers]

- **LTR Gap:** [Top performer] vs [Bottom performer] = [Gap]
- **Issues Gap:** [Best performer] vs [Worst performer] = [Gap]

[Commentary on what these gaps suggest]

### Emerging Patterns

[Identify network-wide trends]

- [Pattern 1]: [Description]
- [Pattern 2]: [Description]
- [Pattern 3]: [Description]
```

**Example:**

```
### Overall Network Performance

The network shows solid overall performance with clear leaders and areas requiring attention:

- **Average LTR:** 79.2% (Range: 62.5% to 92.3%)
- **Average Fun:** 81.5% (Range: 68.8% to 92.3%)
- **Average Helpfulness:** 80.1% (Range: 65.0% to 92.3%)
- **Average Issues:** 12.0% (Range: 3.8% to 25.0%)
- **Average Issue Resolution:** 62.5% (Range: 15.0% to 100.0%)

The network demonstrates strong entertainment value (81.5% Fun) and reasonable staff 
helpfulness (80.1%), but recommendation intent (79.2% LTR) is constrained by operational 
issues (12.0% average issue rate).

### Performance Gaps

- **LTR Gap:** Waco (92.3%) vs Bryan (62.5%) = 29.8 percentage points
- **Issues Gap:** Waco (3.8%) vs Bryan (25.0%) = 21.2 percentage points

These gaps suggest that top performers have achieved significantly better operational 
reliability and guest advocacy. The gap is not primarily driven by entertainment value 
(Fun is relatively consistent across venues) but by operational execution.

### Emerging Patterns

- **Equipment Reliability as Key Differentiator:** Venues with low issue rates (Waco, Rogers) 
  also have high LTR, suggesting equipment reliability is a primary driver of recommendation intent
- **Resolution Quality Varies Widely:** Issue Resolution ranges from 15% to 100%, indicating 
  inconsistent problem-solving approaches across venues
- **Entertainment is Consistent:** Fun scores are relatively consistent across venues (68.8% 
  to 92.3%), suggesting that entertainment value is not the primary differentiator
```

---

## Section 8: Data Quality & Confidence Notes

**Length:** 1-2 subsections  
**Purpose:** Provide context for interpreting results  
**Data Source:** Survey count + data completeness

**Format:**

```
### Sample Size Considerations

- **High Confidence (100+ surveys):** [List venues]
- **Moderate Confidence (50-99 surveys):** [List venues]
- **Lower Confidence (<50 surveys):** [List venues]

Venues with fewer than 50 surveys should be interpreted cautiously, as results may be 
influenced by random variation.

### Missing Data

- **Issue Resolution:** [List venues with missing values and explanation]

Missing Issue Resolution values do not indicate poor performance. They may reflect venues 
with no reported issues or too few responses to calculate.

### Reporting Notes

[Any other data quality notes or caveats]
```

**Example:**

```
### Sample Size Considerations

- **High Confidence (100+ surveys):** Myrtle Beach (160), Houston-Katy (40)
- **Moderate Confidence (50-99 surveys):** [None this week]
- **Lower Confidence (<50 surveys):** Waco (27), Rogers (36), Buford (28), Bryan (16)

Bryan's results are based on only 16 surveys and should be interpreted cautiously. The 
low sample size may not be representative of typical venue performance.

### Missing Data

- **Issue Resolution:** Bryan has no Issue Resolution data because no guests reported issues 
  or too few responses were available to calculate. This does not indicate poor performance.

### Reporting Notes

- Composite Rank calculation methodology is not exposed in this report. Rank should be 
  treated as authoritative without attempting to reconstruct the underlying formula.
- Rank Shift indicates direction (improved/declined/unchanged) but not magnitude of change.
```

---

## Section 9: Recommended Actions

**Length:** 1-2 subsections  
**Purpose:** Provide actionable recommendations  
**Data Source:** Venue analysis + best practices

**Format:**

```
### Immediate Priorities

- **[Venue]:** [Specific action based on analysis]
- **[Venue]:** [Specific action based on analysis]

### Short-Term Focus (Next 2-4 Weeks)

- **[Venue]:** [Specific action based on analysis]
- **[Venue]:** [Specific action based on analysis]

### Longer-Term Strategic Initiatives

- **Network-Wide:** [Initiative to address network-wide pattern]
- **Network-Wide:** [Initiative to address network-wide pattern]
```

**Example:**

```
### Immediate Priorities

- **Houston-Katy:** Conduct root-cause analysis of 20.6% issue rate and implement rapid 
  response protocols to improve Issue Resolution (currently 15.0%)
- **Bryan:** Increase survey volume to improve confidence in results; monitor performance 
  trends as sample size increases

### Short-Term Focus (Next 2-4 Weeks)

- **Rogers:** Investigate why LTR declined this week despite stable Fun and Helpfulness; 
  may indicate emerging operational issues
- **Myrtle Beach:** Implement targeted improvements to issue resolution (currently Rank 23) 
  while maintaining strong entertainment value (Rank 2)

### Longer-Term Strategic Initiatives

- **Network-Wide:** Document Waco's best practices in equipment maintenance and staff 
  training; share with venues experiencing higher issue rates
- **Network-Wide:** Implement standardized issue-resolution protocols across all venues to 
  reduce variation in Issue Resolution scores (currently 15% to 100%)
- **Network-Wide:** Establish equipment reliability benchmarks and preventive maintenance 
  standards based on Waco's 3.8% issue rate
```

---

## Section 10: Conclusion

**Length:** 2-3 sentences  
**Purpose:** Synthesize findings and forward outlook  
**Data Source:** All previous sections

**Template:**

```
This week's rankings show [overall network status]. [Top performers] are demonstrating 
[key success factors], while [underperformers] are experiencing [key challenges]. 
[Recommended focus] should be on [priorities] to improve network-wide performance and 
move closer to the benchmark set by [top performer].
```

**Example:**

```
This week's rankings show a network with strong entertainment value but variable operational 
execution. Waco continues to demonstrate that operational excellence, strong entertainment, 
and excellent staff service can be achieved simultaneously, while Houston-Katy and Bryan are 
experiencing significant challenges. Recommended focus should be on equipment reliability and 
issue resolution to improve network-wide performance and move closer to the benchmark set by 
Waco.
```

---

## Data Processing Checklist

- [ ] Aggregate survey data by venue
- [ ] Calculate 5 metrics (LTR, Fun, Helpfulness, Issues %, Resolution)
- [ ] Rank venues for each metric
- [ ] Calculate Composite Rank
- [ ] Determine Rank Shift (▲/▼/--)
- [ ] Count survey responses per venue
- [ ] Identify top 3 performers
- [ ] Identify bottom 3 performers
- [ ] Identify venues with significant rank movements
- [ ] Calculate network-wide averages
- [ ] Identify performance gaps
- [ ] Identify emerging patterns
- [ ] Note data quality issues (low sample sizes, missing values)
- [ ] Write narrative sections

---

## Output Formats

### Markdown (Summary)
- File: `Venue_Rankings_Weekly_[Date]_Summary.md`
- Use for: Email, documentation, version control

### Markdown (Detailed)
- File: `Venue_Rankings_Weekly_[Date]_Detailed.md`
- Use for: Full analysis, strategic planning

### HTML (Interactive)
- File: `venue-rankings-interactive.html`
- Use for: Dashboard, browser viewing, sorting/filtering

---

## Example Reports

See:
- `Venue Rankings Weekly - Report Definition.md` (detailed interpretation guide)
- `Venue Rankings Weekly - Summary.md` (example summary format)

