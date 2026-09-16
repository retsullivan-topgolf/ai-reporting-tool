## ADDED Requirements

### Requirement: Run period-level AI analysis on aggregated data

The system SHALL execute a multi-stage AI analysis pipeline on aggregated multi-venue period data to synthesize insights and identify patterns.

#### Scenario: Period-level analysis for multi-venue report
- **WHEN** user generates a multi-venue period report for January 2026
- **THEN** system runs AI analysis on:
  - Aggregated metrics (LTR avg, Fun avg, Helpful avg, Issues %, Resolution avg, F&B metrics)
  - Aggregated comment themes from current period only
  - Venue rankings and composite scores
- **AND** analysis produces period overview, key themes, and recommendations
- **AND** analysis completes without errors

#### Scenario: Analysis with comment themes
- **WHEN** period-level analysis runs
- **THEN** system extracts top comment themes across all venues
- **AND** themes are tagged with venue names for context
- **AND** frequency counts are provided for each theme
- **AND** themes are sorted by frequency (most common first)

#### Scenario: Analysis with venue performance context
- **WHEN** period-level analysis runs
- **THEN** system includes venue rankings in analysis context
- **AND** top performers and bottom performers are identified
- **AND** analysis highlights outliers (venues significantly above/below average)
- **AND** recommendations address both high and low performers

#### Scenario: Analysis unavailable
- **WHEN** AI analysis fails or is disabled
- **THEN** report displays metrics and rankings without narrative analysis
- **AND** user is informed that AI analysis is unavailable
- **AND** report remains complete with all data-driven sections

### Requirement: Limit comment analysis to current period

The system SHALL restrict comment analysis to the current period only, excluding historical comments from previous periods.

#### Scenario: Current period comments only
- **WHEN** period-level analysis runs for January 2026
- **THEN** only comments from January 2026 are included in analysis
- **AND** comments from December 2025 or earlier are excluded
- **AND** comment count reflects only current period

#### Scenario: Comment filtering by date
- **WHEN** CSV contains responses from multiple months
- **THEN** system filters comments to those within the current period date range
- **AND** filtering is applied before AI analysis
- **AND** excluded comments are not processed

#### Scenario: No comments in current period
- **WHEN** current period has zero comments
- **THEN** analysis proceeds without comment themes
- **AND** report indicates "No guest comments available for this period"
- **AND** analysis focuses on metric trends and venue performance

#### Scenario: Mixed period data
- **WHEN** CSV spans multiple periods and user requests January 2026 analysis
- **THEN** only January 2026 comments are analyzed
- **AND** metrics are aggregated for January 2026 only
- **AND** previous period data is not included in analysis

### Requirement: Generate period-level synthesis

The system SHALL produce a comprehensive synthesis combining metrics, rankings, themes, and actionable insights.

#### Scenario: Period overview synthesis
- **WHEN** analysis completes
- **THEN** system generates 2-4 sentence overview describing:
  - Overall period performance (strong, stable, declining)
  - Key drivers of performance
  - Notable venue performance variations
  - Significant changes from previous period (if comparison available)

#### Scenario: Theme identification and ranking
- **WHEN** comment analysis runs
- **THEN** system identifies top 3-5 themes across all venues
- **AND** each theme includes:
  - Theme name/category
  - Frequency count
  - Venues where theme appears
  - Representative comment excerpts
- **AND** themes are ranked by frequency

#### Scenario: Venue performance insights
- **WHEN** analysis includes venue rankings
- **THEN** system identifies:
  - Top 3 performing venues and their strengths
  - Bottom 3 performing venues and their challenges
  - Venues with largest composite score improvements (if comparison available)
  - Outliers (venues significantly above/below average)

#### Scenario: Actionable recommendations
- **WHEN** analysis completes
- **THEN** system generates recommendations addressing:
  - Top venue strengths to maintain across all venues
  - Bottom venue challenges to address system-wide
  - Venue-specific recommendations for bottom performers
  - Best practices from top performers to share

### Requirement: Handle aggregated data in AI analysis

The system SHALL adapt the AI analysis pipeline to work with aggregated metrics rather than individual venue data.

#### Scenario: Metrics analysis stage
- **WHEN** metrics analysis stage runs on aggregated data
- **THEN** system analyzes:
  - Overall period metrics (LTR avg, Fun avg, etc.)
  - Metric health status (good/moderate/poor)
  - Metric trends vs. previous period (if available)
  - Variance across venues (which venues drive the aggregate)

#### Scenario: Comment analysis stage
- **WHEN** comment analysis stage runs
- **THEN** system processes comments from all venues combined
- **AND** themes are extracted across all venues
- **AND** venue context is preserved (which venues mention each theme)
- **AND** high-frequency themes are prioritized

#### Scenario: Synthesis stage with multi-venue context
- **WHEN** synthesis stage runs
- **THEN** system produces:
  - Period overview (aggregate performance narrative)
  - Venue performance ranking summary
  - Key themes and patterns across venues
  - Recommendations for period-wide improvements
  - Venue-specific insights for outliers

#### Scenario: Caching and reuse
- **WHEN** period-level analysis completes
- **THEN** results are cached to `ai_analysis_results.json`
- **AND** cached results can be reused for multiple report formats
- **AND** cache is keyed by period identifier (e.g., "2026-01")

### Requirement: Include venue context in analysis

The system SHALL ensure AI analysis recognizes and references specific venues in synthesis.

#### Scenario: Venue-specific theme attribution
- **WHEN** comment theme is identified
- **THEN** analysis includes which venues contributed to the theme
- **AND** theme description includes venue names
- **AND** venue-specific examples are provided

#### Scenario: Top/bottom performer identification
- **WHEN** venue rankings are analyzed
- **THEN** analysis explicitly names top 3 and bottom 3 venues
- **AND** their composite scores are cited
- **AND** their strengths/weaknesses are described

#### Scenario: Outlier detection
- **WHEN** analysis identifies venues significantly above/below average
- **THEN** outliers are named and their composite scores highlighted
- **AND** analysis explains what makes them outliers
- **AND** recommendations address outlier-specific issues
