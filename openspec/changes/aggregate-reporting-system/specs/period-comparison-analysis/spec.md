## ADDED Requirements

### Requirement: Compare aggregated metrics across two time periods

The system SHALL calculate deltas and percent changes between two period summaries (current vs. previous month/quarter) for all aggregated metrics.

#### Scenario: Month-to-month comparison
- **WHEN** user compares January 2026 (current) vs December 2025 (previous)
- **THEN** system calculates delta for each metric: LTR, Fun, Helpful, Issues %, Resolution, F&B avg
- **AND** percent change is calculated for each metric
- **AND** trend indicators (↑ ↓ →) are assigned based on ±0.5 threshold

#### Scenario: Quarter-to-quarter comparison
- **WHEN** user compares Q1 2026 (current) vs Q4 2025 (previous)
- **THEN** system calculates deltas across all metrics
- **AND** response counts are compared to identify if periods have similar sample sizes
- **AND** warning is displayed if response count differs by ±20% or more

#### Scenario: Venue ranking changes
- **WHEN** comparing two periods
- **THEN** system identifies which venues improved ranking and which declined
- **AND** ranking changes are highlighted in the report
- **AND** venues entering/exiting top 3 are noted

#### Scenario: Missing data in previous period
- **WHEN** previous period has no data
- **THEN** comparison shows current metrics with "N/A" for previous
- **AND** deltas and percent changes are marked "N/A"
- **AND** trend indicators show "—"

### Requirement: Calculate metric deltas for aggregated data

The system SHALL compute the difference between current and previous period metrics with proper handling of edge cases.

#### Scenario: Positive aggregate delta
- **WHEN** current period LTR avg is 8.2 and previous is 8.0
- **THEN** delta is +0.2 and percent change is +2.5%

#### Scenario: Negative aggregate delta
- **WHEN** current period Issues % is 12% and previous is 15%
- **THEN** delta is -3 percentage points and percent change is -20%

#### Scenario: F&B average delta
- **WHEN** current period F&B avg is 4.1 and previous is 3.9
- **THEN** delta is +0.2 and percent change is +5.1%

#### Scenario: Response count comparison
- **WHEN** current period has 500 responses and previous has 480
- **THEN** percent difference is +4.2%
- **AND** note is added if difference exceeds ±20%

### Requirement: Identify venue ranking changes

The system SHALL compare venue rankings between periods and identify movers (improved/declined).

#### Scenario: Venue improves ranking
- **WHEN** venue "Grand Prairie" ranked 3rd in previous period and 1st in current
- **THEN** report shows ranking change: "3rd → 1st" with up arrow
- **AND** composite score change is displayed

#### Scenario: Venue declines ranking
- **WHEN** venue "Chicago" ranked 1st in previous period and 2nd in current
- **THEN** report shows ranking change: "1st → 2nd" with down arrow
- **AND** composite score change is displayed

#### Scenario: Venue enters top 3
- **WHEN** venue "Dallas" was ranked 5th previously and is now 2nd
- **THEN** report highlights this as "Notable Improvement"
- **AND** composite score improvement is emphasized

#### Scenario: Venue exits top 3
- **WHEN** venue "Austin" was ranked 2nd previously and is now 4th
- **THEN** report highlights this as "Notable Decline"
- **AND** composite score decline is emphasized

### Requirement: Apply trend threshold to period comparisons

The system SHALL highlight significant changes (±0.5 points) with visual indicators at the period level.

#### Scenario: Significant period improvement
- **WHEN** aggregated metric delta is +0.6 or greater
- **THEN** display up arrow (↑) and highlight in green

#### Scenario: Significant period decline
- **WHEN** aggregated metric delta is -0.6 or less
- **THEN** display down arrow (↓) and highlight in red

#### Scenario: Minor period fluctuation
- **WHEN** aggregated metric delta is between -0.5 and +0.5
- **THEN** display dash (→) with neutral styling

#### Scenario: Threshold boundary
- **WHEN** aggregated metric delta is exactly ±0.5
- **THEN** treat as significant change and apply highlighting

### Requirement: Generate period comparison summary

The system SHALL produce a structured comparison containing both period summaries, deltas, and ranking changes.

#### Scenario: Comparison output structure
- **WHEN** period comparison completes
- **THEN** system outputs JSON with structure:
  ```
  {
    "current_period": { ...period_summary... },
    "previous_period": { ...period_summary... },
    "comparison": {
      "metrics_deltas": {
        "ltr_delta": 0.2,
        "ltr_percent_change": 2.5,
        "fun_delta": 0.1,
        "fun_percent_change": 2.4,
        ...
      },
      "response_count_change": {
        "current": 500,
        "previous": 480,
        "delta": 20,
        "percent_change": 4.2
      },
      "ranking_changes": [
        {
          "venue": "Grand Prairie",
          "previous_rank": 3,
          "current_rank": 1,
          "change": "↑ 2 positions",
          "composite_score_delta": 0.3
        },
        ...
      ]
    }
  }
  ```

#### Scenario: Comparison metadata
- **WHEN** comparison is generated
- **THEN** both period summaries are included in full
- **AND** all deltas and percent changes are calculated
- **AND** ranking changes are identified and sorted by magnitude
- **AND** timestamp of comparison generation is included
