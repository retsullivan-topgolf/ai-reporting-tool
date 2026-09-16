## ADDED Requirements

### Requirement: Aggregate metrics across all venues in a period

The system SHALL combine survey responses from all venues in a CSV for a given time period and calculate aggregate metrics (averages, percentages, response counts).

#### Scenario: Aggregate metrics for single month
- **WHEN** user processes a CSV with 5 venues and 500 total responses for January 2026
- **THEN** system calculates aggregated metrics: LTR avg, Fun avg, Helpful avg, Issues %, Resolution avg, F&B metrics avg
- **AND** total response count is 500
- **AND** date range is "Jan 1 - Jan 31, 2026"

#### Scenario: Aggregate with missing F&B data
- **WHEN** some venues in the CSV have F&B metrics and others don't
- **THEN** F&B averages are calculated only from venues that have F&B data
- **AND** missing data is not treated as zero
- **AND** response count for F&B metrics reflects venues with data

#### Scenario: Single venue in period
- **WHEN** CSV contains only one venue for a given period
- **THEN** aggregated metrics equal that venue's metrics
- **AND** venue is still ranked (composite score calculated)

#### Scenario: Empty period
- **WHEN** date range filter returns zero responses
- **THEN** system returns error or empty report
- **AND** user is informed that no data exists for the period

### Requirement: Rank venues by composite performance score

The system SHALL calculate a weighted composite score for each venue and rank them from highest to lowest performance.

#### Scenario: Composite score calculation
- **WHEN** venue has LTR=8.0, Fun=4.2, F&B avg=4.0, Resolution=4.5
- **THEN** composite score = (8.0 × 0.4) + (4.2 × 0.2) + (4.0 × 0.2) + (4.5 × 0.2) = 6.36
- **AND** score is rounded to 2 decimal places

#### Scenario: Ranking with missing F&B data
- **WHEN** venue has LTR=8.0, Fun=4.2, Resolution=4.5, but no F&B data
- **THEN** composite score = (8.0 × 0.4) + (4.2 × 0.2) + (4.5 × 0.2) ÷ 0.8 = 6.63
- **AND** missing metric weight is redistributed to remaining metrics

#### Scenario: Venues ranked best to worst
- **WHEN** aggregation includes 5 venues with varying scores
- **THEN** venues are sorted by composite score in descending order
- **AND** ranking numbers (1st, 2nd, 3rd, etc.) are assigned
- **AND** top performers and bottom performers are clearly identified

#### Scenario: Tied composite scores
- **WHEN** two venues have identical composite scores
- **THEN** venues are sorted by secondary metric (LTR) to break tie
- **AND** both venues show the same rank number with notation (e.g., "Tied for 3rd")

### Requirement: Calculate composite score weights

The system SHALL apply consistent weighting to metrics: LTR (40%) + Fun (20%) + F&B Average (20%) + Issue Resolution (20%).

#### Scenario: Weight distribution
- **WHEN** composite score is calculated
- **THEN** LTR contributes 40% of the score
- **AND** Fun contributes 20%
- **AND** F&B Average (food_value + food_speed + food_quality + beverage_value + beverage_speed + beverage_quality) / 6 contributes 20%
- **AND** Issue Resolution contributes 20%

#### Scenario: F&B average calculation
- **WHEN** venue has food_value=4.0, food_speed=3.8, food_quality=4.2, beverage_value=4.1, beverage_speed=3.9, beverage_quality=4.0
- **THEN** F&B average = (4.0 + 3.8 + 4.2 + 4.1 + 3.9 + 4.0) / 6 = 4.0

#### Scenario: Partial F&B data
- **WHEN** venue has only food metrics (no beverage metrics)
- **THEN** F&B average = (food_value + food_speed + food_quality) / 3
- **AND** missing beverage metrics do not reduce the score

### Requirement: Generate period summary data structure

The system SHALL produce a structured summary containing aggregated metrics, venue rankings, and metadata.

#### Scenario: Period summary output
- **WHEN** aggregation completes
- **THEN** system outputs JSON with structure:
  ```
  {
    "period": "January 2026",
    "period_type": "month",
    "date_range": ["2026-01-01", "2026-01-31"],
    "total_responses": 500,
    "venues_count": 5,
    "metrics_avg": {
      "ltr_avg": 8.1,
      "fun_avg": 4.2,
      "helpful_avg": 4.3,
      "issues_pct": 12.5,
      "resolution_avg": 4.4,
      "f&b_avg": 4.0
    },
    "venues_ranked": [
      {
        "rank": 1,
        "venue": "Grand Prairie",
        "composite_score": 6.8,
        "ltr_avg": 8.5,
        "fun_avg": 4.5,
        "f&b_avg": 4.2,
        "resolution_avg": 4.6,
        "responses": 120
      },
      ...
    ]
  }
  ```

#### Scenario: Metadata accuracy
- **WHEN** period summary is generated
- **THEN** total_responses equals sum of all venue responses
- **AND** venues_count equals number of unique venues
- **AND** date_range reflects earliest and latest response dates
- **AND** period_type is either "month" or "quarter"
