## Context

The current reporting system generates single-venue, single-period reports using a three-stage AI analysis pipeline. Users need to understand performance across multiple venues and track trends over time. This requires:

1. **Period-based data filtering** - Extract records for specific months/quarters
2. **Aggregation logic** - Combine metrics across venues
3. **Composite scoring** - Rank venues by weighted performance (LTR + Fun + F&B avg + Issue Resolution)
4. **Comparison calculations** - Calculate deltas and percent changes between periods
5. **Period-level AI synthesis** - Analyze aggregated data and comment themes across venues

The system will support three distinct report types, each with different data flows and AI requirements.

## Goals / Non-Goals

**Goals:**
- Enable venue-to-venue performance comparison within a period
- Enable period-to-period trend analysis for single venues
- Enable period-to-period trend analysis across all venues
- Provide composite ranking that balances multiple metrics
- Keep AI analysis costs reasonable (no comment analysis for multi-period comparisons)
- Maintain backward compatibility with existing single-venue reports
- Support both month and quarter time periods

**Non-Goals:**
- Real-time reporting or streaming data
- Custom time period selection (only month/quarter)
- Venue-to-venue comparison across different time periods
- Predictive analytics or forecasting
- Historical data archival or data warehouse functionality

## Decisions

### Decision 1: Period Filtering Strategy
**Choice:** Filter CSV by date range at data load time, treating CSV as a database

**Rationale:** 
- Simplest implementation - no external database needed
- CSV is already the source of truth
- Allows "API-like" behavior by filtering the same CSV differently for each period
- Scales adequately for typical venue datasets (hundreds to thousands of records)

**Alternatives Considered:**
- Load entire CSV into SQLite: More complex, overkill for current scale
- Require pre-filtered CSVs: Shifts burden to users, error-prone

### Decision 2: Composite Scoring Formula
**Choice:** Weighted average of four metrics: LTR (40%) + Fun (20%) + F&B Avg (20%) + Issue Resolution (20%)

**Rationale:**
- LTR is primary driver of business value (40%)
- Fun and F&B are equally important experience factors (20% each)
- Issue Resolution reflects operational excellence (20%)
- Weights are intuitive and can be adjusted later if needed
- Handles missing F&B data gracefully (average only non-null metrics)

**Alternatives Considered:**
- Simple average of all metrics: Doesn't reflect business priority
- LTR-only ranking: Ignores important experience dimensions
- Machine learning-based scoring: Overkill without historical data

### Decision 3: Trend Threshold
**Choice:** ±0.5 points triggers visual highlighting as "significant change"

**Rationale:**
- On a 1-10 scale (LTR), 0.5 is ~5% change - meaningful but not noise
- On a 1-5 scale (Fun, F&B), 0.5 is 10% change - noticeable improvement/decline
- Consistent across all metric types
- Prevents alert fatigue from minor fluctuations

**Alternatives Considered:**
- ±0.25 points: Too sensitive, highlights noise
- ±1.0 points: Too insensitive, misses real trends
- Percentage-based (±5%): Inconsistent across different scales

### Decision 4: AI Analysis Scope by Report Type
**Choice:**
- **Report 1 (Venue Period Comparison):** Venue-level analysis (existing pipeline), with comparison context
- **Report 2 (Multi-Venue Single Period):** Period-level synthesis across venues, includes aggregated comment themes
- **Report 3 (Multi-Venue Period Comparison):** Period-level synthesis + trend analysis, current period comments only

**Rationale:**
- Report 1 reuses existing AI pipeline (low cost)
- Report 2 needs cross-venue synthesis to identify patterns
- Report 3 limits comment analysis to current period to control costs
- Keeps AI analysis focused and actionable

**Alternatives Considered:**
- No AI analysis for Reports 2 & 3: Loses valuable insights
- Full comment analysis for Report 3: Doubles AI costs unnecessarily
- Single unified AI pipeline: Doesn't fit different data shapes

### Decision 5: Data Flow Architecture
**Choice:** Three separate report generation scripts, each with its own data pipeline

**Rationale:**
- Clear separation of concerns
- Each script handles its specific filtering/aggregation logic
- Easy to test and debug independently
- Can be called individually or orchestrated together

**Alternatives Considered:**
- Single unified script with conditional logic: Would be complex and hard to maintain
- Shared base class with inheritance: Overkill for three distinct flows

### Decision 6: Template Organization
**Choice:** Separate template files for each report type (not variants of a single template)

**Rationale:**
- Each report has distinct sections and data structures
- Easier to maintain and evolve independently
- Clearer intent (no hidden conditional logic)
- Follows existing pattern (separate browser/PDF templates)

**Alternatives Considered:**
- Single template with extensive conditional logic: Hard to read and maintain
- Template inheritance: Jinja2 doesn't support this well

### Decision 7: Comment Scope for AI Analysis
**Choice:** Current period only (no historical comment comparison)

**Rationale:**
- Keeps AI analysis focused on actionable feedback
- Reduces API costs for multi-period reports
- Comments are most relevant when recent
- Prevents stale feedback from skewing analysis

**Alternatives Considered:**
- Include comments from both periods: Doubles AI cost, less actionable
- No comments at all: Loses qualitative insights

## Risks / Trade-offs

**[Risk] CSV-based filtering may be slow for very large datasets**
→ Mitigation: Current venue datasets are manageable (hundreds to thousands of records). If this becomes a bottleneck, migrate to SQLite with proper indexing.

**[Risk] Composite scoring weights may not reflect actual business priorities**
→ Mitigation: Weights are configurable constants in code. Can be adjusted based on user feedback. Consider adding admin UI later if needed.

**[Risk] Period-level AI analysis may produce generic insights across diverse venues**
→ Mitigation: Design prompts to identify venue-specific patterns and outliers. Include venue names in comment themes.

**[Risk] Comparing periods with different numbers of responses may skew trends**
→ Mitigation: Always show response counts in reports. Highlight when response counts differ significantly (±20%).

**[Risk] Missing F&B data in some venues breaks composite scoring**
→ Mitigation: Score calculation handles null values gracefully - averages only non-null metrics. Document this behavior.

**[Risk] AI analysis costs scale with number of venues in Report 2 & 3**
→ Mitigation: Limit comment analysis to current period only. Consider caching period-level analysis results.

## Migration Plan

1. **Phase 1:** Implement API extensions (`venue_processor.py` changes) - no breaking changes
2. **Phase 2:** Create Report 1 (Venue Period Comparison) - uses existing AI pipeline
3. **Phase 3:** Create Report 2 (Multi-Venue Single Period) - new period-level AI synthesis
4. **Phase 4:** Create Report 3 (Multi-Venue Period Comparison) - extends Report 2 logic
5. **Phase 5:** Update documentation and AGENTS.md with new report workflows

All changes are additive - existing single-venue reports continue to work unchanged.

## Open Questions

1. **Composite Score Weighting** - Are the proposed weights (40/20/20/20) correct, or should they be adjusted?
2. **F&B Data Handling** - Should venues without F&B data be ranked lower, or should scoring ignore missing F&B?
3. **Comment Theme Aggregation** - For Report 2, how many top themes should we extract? (e.g., top 5, top 10?)
4. **Venue Filtering** - Should Report 2 allow filtering to a subset of venues, or always include all venues in the CSV?
5. **Response Count Threshold** - Should we warn if a period has very few responses (e.g., <10)?
