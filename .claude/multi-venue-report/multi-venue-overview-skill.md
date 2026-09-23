# Multi-Venue Overview Skill

Generate a compelling 2-4 sentence narrative summary that describes the venue network's overall performance, acknowledges venue variance explicitly, and highlights outliers without focusing on individual venues.

## Purpose

The Multi-Venue Overview is the narrative centerpiece that tells the story of network-wide performance while acknowledging that venues are not uniform. It should answer: "How is the network performing overall, and where do venues differ?"

Unlike snapshot overview (which describes a single venue's performance), this overview frames findings at the network level: aggregates, variance, and outliers.

## Input

- `metrics_analysis`: Characterization + network_metrics + venue_outliers from Stage 1
- `comment_analysis`: Themes with venue breakdown from Stage 2
- `combined_ranking`: Merged and sorted by magnitude

## Output

A 2-4 sentence narrative paragraph that:
- Describes network-wide performance (strong/moderate/weak)
- Acknowledges venue variance explicitly
- Highlights outliers (best/worst performers)
- Uses aggregate language ("across venues", "on average", "most locations")
- Avoids focusing on individual venues (that's done in ranking skill)

## Rules

### Foundation
- MUST start with network-wide characterization
- MUST acknowledge venue variance explicitly ("varies significantly", "ranges from X to Y")
- MUST highlight outliers by name and differential ("Grand Prairie leading at 8.8, El Paso lagging at 7.1")
- MUST use aggregate language ("across venues", "on average", "network-wide")
- MUST NOT focus on individual venues (save that for ranking skill)

### Language Guidelines
- **Network framing:** "The network shows...", "Across venues...", "On average..."
- **Variance acknowledgment:** "varies significantly", "ranges from...to", "one location to the next"
- **Outlier calling:** Name the top and bottom performers
- **Aggregate metrics:** "8.2 NPS average", "ranging from 7.1 to 8.8"
- **NOT individual:** Don't explain "why Grand Prairie is strong" (ranking skill does that)

### Narrative Quality
- SHOULD explain what the variance means operationally
- SHOULD use specific numbers for context (network average + range)
- SHOULD avoid redundancy with metrics cards (cite themes instead)
- MUST NOT introduce numbers or claims not traceable to input stages
- MUST be clear, concise, easy to read
- MUST be 2-4 sentences (typically 3)
- MUST be a single paragraph

### Formatting
- MUST use inline HTML limited to `<strong>` tags only
- MUST avoid generic language ("needs improvement", "good performance")
- MUST ground all claims in numbers from input
- MUST NOT state or imply comparisons to other periods or networks

## Examples

### ✅ Good Multi-Venue Overview Examples

**Example 1: Strong Network with Variance**
```
"The venue network shows strong overall satisfaction (8.2 NPS average), 
driven by consistent staff responsiveness and solid game experiences. However, 
equipment reliability varies significantly by location, with Grand Prairie 
performing well (8.8 NPS) while El Paso faces challenges (7.1 NPS, 35% issue rate). 
This venue-specific variance suggests operational differences offer a clear 
improvement lever for the network."
```

**Why this works:**
- Opens with network performance (strong, 8.2 NPS)
- Acknowledges variance (varies significantly, 8.8 to 7.1)
- Names best and worst performers explicitly
- Explains why variance matters (operational lever)
- Uses aggregate language (network, venue-specific, overall)

---

**Example 2: Mixed Network Performance**
```
"Performance across venues is moderate overall, with strong satisfaction metrics 
(4.2/5 LTR average) offset by operational concerns. While Grand Prairie and Austin 
maintain consistent excellence (4.4 and 4.0 LTR), Dallas and El Paso lag behind 
(3.8 and 3.7). Equipment reliability is the primary variance driver, with issue 
rates ranging from 18% at top venues to 35% at bottom venues."
```

**Why this works:**
- Frames as network-wide (across venues, overall)
- Cites specific range (4.4 down to 3.7)
- Names multiple tiers (Grand Prairie/Austin vs. Dallas/El Paso)
- Explains what drives variance (equipment reliability)
- Uses network-level analysis

---

**Example 3: Consistent Network with One Outlier**
```
"The network maintains solid performance across nearly all venues (8.1 NPS average), 
with strong staff responsiveness and game satisfaction. However, El Paso consistently 
underperforms across all metrics (7.1 NPS, 35% issues), suggesting venue-specific 
challenges that diverge sharply from the network norm (which shows 8.8 NPS at best). 
Addressing El Paso's operational issues could unlock significant network-wide gains."
```

**Why this works:**
- Establishes baseline (solid, 8.1 average)
- Identifies outlier (El Paso)
- Shows why it's an outlier (7.1 vs. 8.8 network spread)
- Frames as opportunity (unlock gains)
- Network-focused language (venue-specific challenges)

---

### ❌ What NOT to Do

**Bad: Individual venue focus instead of network**
```
"Grand Prairie is doing great with 8.8 NPS and low equipment issues. 
Austin is doing well with 8.4 NPS. El Paso is struggling with 7.1 NPS..."
```
**Why this fails:** Reads like individual venue descriptions, not a network overview. That's the ranking skill's job.

---

**Bad: Missing variance acknowledgment**
```
"The network shows strong satisfaction (8.2 NPS) with good equipment reliability 
and responsive staff."
```
**Why this fails:** Ignores that El Paso has 35% issues while Grand Prairie has 18%. Variance is critical.

---

**Bad: Too detailed on individual examples**
```
"Grand Prairie excels because they have great maintenance and excellent staff 
training. Austin does well because of their team. El Paso struggles with old 
equipment and staffing challenges."
```
**Why this fails:** Individual venue explanations are ranking skill territory. Overview stays at network level.

---

## Variance-Acknowledging Language

Use these phrases to acknowledge that venues differ:

| Magnitude | Phrasing |
|---|---|
| **Large variance** | "varies significantly", "ranges widely", "one location to the next", "marked differences" |
| **Moderate variance** | "shows some variance", "ranges from X to Y", "with some venue-to-venue differences" |
| **Consistent** | "consistently", "across all venues", "uniformly", "holding steady" |
| **One outlier** | "except at venue X", "with venue X diverging", "venue X stands apart" |

---

## Network Metrics in Overview

When citing network metrics, use:
- **Network average:** "8.2 NPS average"
- **Range:** "ranging from 7.1 to 8.8"
- **Aggregate:** "across venues", "on average", "across the network"
- **NOT:** Individual scores unless highlighting outliers (top/bottom)

---

## Related Skills

- See `multi-venue-ranking-skill.md` for how to rank and explain venues in detail
- See `multi-venue-ups-downs-skill.md` for network patterns and variance findings
- See `multi-venue-impact-drivers-skill.md` for explaining what drives the variance

## Resources

- `README.md` - Integration guide for multi-venue reports
- `synthesis_template.md` - The actual prompt that implements this skill
