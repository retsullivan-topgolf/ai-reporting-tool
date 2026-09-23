# Multi-Venue Overview Comparison Skill

Generate a compelling 2-4 sentence narrative that frames the network's **change** between two periods, explaining what improved, declined, or remained stable, and what that means for network alignment.

## Purpose

The Multi-Venue Overview Comparison is the narrative centerpiece that tells the story of network-wide **change**. Unlike snapshot (which describes current state), this overview answers: "How did the network perform overall between these periods, and did venues move together or diverge?"

## Input

- `metrics_analysis.current` & `.previous`: Network metrics for both periods
- `comment_analysis.current` & `.previous`: Themes for both periods
- `combined_ranking`: Findings ranked by **change magnitude** (deltas)

## Output

A 2-4 sentence narrative that:
- Opens with overall network trajectory (improved/declined/stable)
- Cites the most significant network change
- Acknowledges venue-level variance in that trend
- Explains what the divergence means operationally

## Rules

### Foundation
- MUST start with overall network trajectory: "Network improved/declined/remained stable..."
- MUST cite network-level deltas explicitly (e.g., "NPS improved by 0.3 points")
- MUST acknowledge venue divergence (e.g., "but gains were uneven across venues")
- MUST NOT focus on individual venues (that's ranking skill)
- MUST NOT compare to external benchmarks (only to previous period)

### Change Framing
- **Improvements:** "improved", "recovered", "strengthened", "became more consistent"
- **Declines:** "declined", "worsened", "became more fragmented", "diverged"
- **Stable:** "remained stable", "held steady", "maintained"
- **Divergence:** "uneven gains", "mixed results", "venues moved in different directions"

### Variance Acknowledgment
- MUST note if venues improved together (consensus) or separately (divergence)
- Examples:
  - "NPS improved +0.3 network-wide, with all venues showing gains" (consensus)
  - "NPS improved +0.3 on average, but Grand Prairie gained +0.6 while El Paso declined -0.2" (divergence)

### Narrative Quality
- SHOULD explain what the divergence suggests operationally
- SHOULD cite specific venue names if they diverge from trend
- MUST use descriptive language without exact metric scores
- MUST be 2-4 sentences, single paragraph

## Examples

### ✅ Good Multi-Venue Comparison Overview Examples

**Example 1: Network Improvement with Uneven Gains**
```
"The network improved overall (NPS +0.3), driven by equipment reliability fixes 
that reduced network-average issue rates from 28% to 25%. However, gains were 
uneven: Grand Prairie and Austin improved significantly (+0.6 each), while El Paso 
declined (-0.2), suggesting venue-specific operational factors influence whether 
venues benefit from network-wide initiatives."
```

**Why this works:**
- Opens with network trend (improved, +0.3)
- Cites what drove it (equipment fixes, 28%→25%)
- Acknowledges uneven gains (Grand Prairie/Austin up, El Paso down)
- Explains operational meaning (venue-specific factors matter)

---

**Example 2: Network Stability with Emerging Variance**
```
"The network remained stable on overall satisfaction (NPS flat at 8.2), but 
operational consistency diverged. Equipment reliability improved at most venues 
(Grand Prairie, Austin, Dallas all up 0.4-0.6 points), while El Paso faced new 
challenges (issues up from 32% to 36%). This suggests the network is improving 
in some locations but not others, creating a divergence opportunity."
```

**Why this works:**
- Notes overall stability (NPS flat)
- Shows divergence (most venues up, El Paso down)
- Cites specific deltas (0.4-0.6 up, 32%→36%)
- Explains implication (divergence = opportunity)

---

**Example 3: Network Decline with Outliers**
```
"Performance declined network-wide (NPS -0.2), driven by F&B service speed 
concerns that worsened across all venues. However, Grand Prairie bucked the trend 
(maintained 8.8 NPS), while El Paso fell further (down to 7.0). This divergence 
suggests Grand Prairie's operational approach could be modeled to halt the network's 
overall decline."
```

**Why this works:**
- Opens with network decline (NPS -0.2)
- Cites root cause (F&B speed, worsened across all)
- Notes outliers (Grand Prairie stable, El Paso fell)
- Explains strategic meaning (Grand Prairie = model)

---

### ❌ What NOT to Do

**Bad: Individual venue focus instead of network**
```
"Grand Prairie improved from 8.6 to 8.8 NPS. Austin improved from 8.2 to 8.4. 
El Paso declined from 7.2 to 7.1."
```
**Why this fails:** That's individual venue stories, not network trend. Ranking skill covers venue movement.

---

**Bad: Missing divergence context**
```
"The network improved slightly with some venues performing better than others."
```
**Why this fails:** Too vague. What's the network delta? Which venues? How much divergence?

---

**Bad: Absolute framing instead of change**
```
"The network shows strong NPS (8.2) with solid equipment reliability (25% issues)."
```
**Why this fails:** Snapshot language, not comparison. Should cite deltas and changes.

---

## Variance Patterns to Highlight

### Consensus Trend (All Venues Move Together)
Venues align on improvement or decline:
- "Network improved +0.3 NPS, with all venues showing gains of 0.2-0.6"
- "The network faced consistent headwinds across all locations"

### Diverging Trend (Venues Move in Different Directions)
Venues split on improvement/decline:
- "Network improved +0.3 on average, but gains were uneven (Grand Prairie +0.6, El Paso -0.2)"
- "While most venues improved, El Paso diverged with new challenges"

### Outlier Trend (One or Two Venues Differ)
Most follow pattern; one or two stand apart:
- "Most venues improved consistently; Grand Prairie led the gains"
- "Equipment reliability worsened network-wide except at Grand Prairie"

---

## Related Skills

- See `multi-venue-ranking-comparison-skill.md` for ranking movement detail
- See `multi-venue-impact-drivers-comparison-skill.md` for what drove the trend
- See `multi-venue-ups-downs-comparison-skill.md` for network patterns that changed

## Resources

- `README.md` - Integration guide for multi-venue comparison reports
- `synthesis_template.md` - The actual prompt that implements this skill
