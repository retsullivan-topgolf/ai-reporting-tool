## ADDED Requirements

### Requirement: Calculate composite performance score for venues

The system SHALL compute a weighted composite score for each venue using four metrics: LTR (40%), Fun (20%), F&B Average (20%), and Issue Resolution (20%).

#### Scenario: Complete metric data
- **WHEN** venue has all four metric types available
- **THEN** composite score = (LTR × 0.4) + (Fun × 0.2) + (F&B_avg × 0.2) + (Resolution × 0.2)
- **AND** score is normalized to 0-10 scale
- **AND** score is rounded to 2 decimal places

#### Scenario: Missing F&B data
- **WHEN** venue lacks F&B metrics but has LTR, Fun, and Resolution
- **THEN** composite score = (LTR × 0.4) + (Fun × 0.2) + (Resolution × 0.2) ÷ 0.8
- **AND** missing weight is redistributed proportionally
- **AND** score is still on 0-10 scale

#### Scenario: Missing Resolution data
- **WHEN** venue has no issue resolution data (no issues reported)
- **THEN** composite score = (LTR × 0.4) + (Fun × 0.2) + (F&B_avg × 0.2) ÷ 0.8
- **AND** missing weight is redistributed
- **AND** score reflects available data accurately

#### Scenario: Partial F&B data
- **WHEN** venue has food metrics but no beverage metrics
- **THEN** F&B average = (food_value + food_speed + food_quality) / 3
- **AND** composite score uses this partial F&B average
- **AND** no penalty is applied for missing beverage data

### Requirement: Normalize metrics to common scale

The system SHALL normalize all metrics to a 0-10 scale before calculating composite score.

#### Scenario: LTR normalization
- **WHEN** LTR is already on 1-10 scale
- **THEN** no normalization needed, use value as-is

#### Scenario: Fun metric normalization
- **WHEN** Fun is on 1-5 scale with value 4.2
- **THEN** normalized value = (4.2 - 1) / (5 - 1) × 10 = 8.0

#### Scenario: F&B average normalization
- **WHEN** F&B average is on 1-5 scale with value 3.8
- **THEN** normalized value = (3.8 - 1) / (5 - 1) × 10 = 7.0

#### Scenario: Resolution normalization
- **WHEN** Resolution is on 1-5 scale with value 4.5
- **THEN** normalized value = (4.5 - 1) / (5 - 1) × 10 = 8.75

#### Scenario: Issues percentage normalization
- **WHEN** Issues % is 15% (15 out of 100 responses)
- **THEN** normalized value = (100 - 15) / 100 × 10 = 8.5
- **AND** higher percentage of satisfied customers = higher score

### Requirement: Rank venues by composite score

The system SHALL sort venues in descending order by composite score and assign ranking numbers.

#### Scenario: Standard ranking
- **WHEN** 5 venues have composite scores: 7.2, 6.8, 6.5, 6.2, 5.9
- **THEN** venues are ranked 1st through 5th in descending order
- **AND** ranking is displayed in report

#### Scenario: Tied scores
- **WHEN** two venues have identical composite scores (6.8)
- **THEN** both venues are assigned the same rank number
- **AND** next venue is ranked with gap (e.g., both 2nd, next is 4th)
- **AND** tie is noted with "Tied for Xth" label

#### Scenario: Score-based sorting
- **WHEN** ranking is applied
- **THEN** venue with highest composite score is ranked 1st
- **AND** venue with lowest composite score is ranked last
- **AND** no venues are skipped in ranking

#### Scenario: Secondary sort for ties
- **WHEN** two venues have identical composite scores
- **THEN** secondary sort by LTR (highest first) breaks the tie
- **AND** tertiary sort by response count (highest first) if LTR also tied
- **AND** ranking is deterministic and reproducible

### Requirement: Handle edge cases in scoring

The system SHALL gracefully handle missing data, zero values, and edge cases in composite scoring.

#### Scenario: All metrics missing
- **WHEN** venue has no valid metric data
- **THEN** composite score is marked as "N/A"
- **AND** venue is excluded from ranking
- **AND** error is logged for investigation

#### Scenario: Single metric available
- **WHEN** venue has only LTR data (no other metrics)
- **THEN** composite score = LTR (no weighting applied)
- **AND** venue is still ranked
- **AND** note indicates limited data

#### Scenario: Zero responses
- **WHEN** venue has zero responses in period
- **THEN** composite score is "N/A"
- **AND** venue is excluded from ranking
- **AND** user is informed of empty venue

#### Scenario: Very low response count
- **WHEN** venue has only 1-2 responses in period
- **THEN** composite score is calculated normally
- **AND** warning is displayed that score may not be representative
- **AND** response count is shown for transparency

### Requirement: Provide scoring transparency

The system SHALL display component scores and weighting in reports for transparency.

#### Scenario: Score breakdown display
- **WHEN** venue ranking is shown in report
- **THEN** each venue displays:
  - Composite score (overall ranking metric)
  - Component scores: LTR, Fun, F&B avg, Resolution
  - Weighting percentages (40%, 20%, 20%, 20%)
  - Response count

#### Scenario: Scoring methodology documentation
- **WHEN** report is generated
- **THEN** report includes a section explaining composite score calculation
- **AND** weighting rationale is documented
- **AND** users understand how ranking is determined
