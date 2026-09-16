## ADDED Requirements

### Requirement: Compare single venue across two time periods

The system SHALL generate a report comparing a single venue's performance metrics between a current period and a previous period (month or quarter), displaying actual values, deltas, and percent changes with trend indicators.

#### Scenario: Monthly comparison with improvement
- **WHEN** user generates a report for venue "Grand Prairie" for January 2026 vs December 2025
- **THEN** report displays metrics for both periods with columns: Current | Previous | Change | % Change | Trend
- **AND** metrics showing improvement (delta ≥ +0.5) display an up arrow (↑)
- **AND** metrics showing decline (delta ≤ -0.5) display a down arrow (↓)
- **AND** metrics with minor changes (-0.5 to +0.5) display a dash (→)

#### Scenario: Quarterly comparison with mixed results
- **WHEN** user generates a report for venue "Chicago" for Q1 2026 vs Q4 2025
- **THEN** report includes LTR, Fun, Helpful, Issues, Resolution, and F&B metrics (if available)
- **AND** each metric shows current value, previous value, absolute delta, and percent change
- **AND** trend indicators are calculated based on ±0.5 point threshold

#### Scenario: Comments from current period only
- **WHEN** report is generated with AI analysis enabled
- **THEN** comments included in analysis are from the current period only
- **AND** previous period comments are not analyzed or displayed
- **AND** comment count is displayed for transparency

#### Scenario: Venue with no previous period data
- **WHEN** user requests comparison for a venue with no data in the previous period
- **THEN** report displays current period metrics normally
- **AND** previous period columns show "N/A" or are hidden
- **AND** trend indicators show "—" (no comparison available)

### Requirement: Calculate metric deltas and percent changes

The system SHALL calculate the difference and percent change between current and previous period metrics, handling edge cases like zero values and missing data.

#### Scenario: Positive delta calculation
- **WHEN** current LTR is 8.5 and previous LTR is 8.0
- **THEN** delta is 0.5 and percent change is +6.25%

#### Scenario: Negative delta calculation
- **WHEN** current Issues % is 15% and previous Issues % is 20%
- **THEN** delta is -5 percentage points and percent change is -25%

#### Scenario: Zero previous value
- **WHEN** previous period has no data (0 responses)
- **THEN** delta and percent change are marked as "N/A"
- **AND** no division-by-zero errors occur

#### Scenario: Missing metric in previous period
- **WHEN** previous period lacks F&B data but current period has it
- **THEN** F&B metrics show current value with "N/A" for previous
- **AND** delta and percent change are "N/A"

### Requirement: Apply trend threshold for visual highlighting

The system SHALL highlight metrics with significant changes (±0.5 points or greater) with visual indicators.

#### Scenario: Significant improvement
- **WHEN** metric delta is +0.6 or greater
- **THEN** display up arrow (↑) and highlight in green

#### Scenario: Significant decline
- **WHEN** metric delta is -0.6 or less
- **THEN** display down arrow (↓) and highlight in red

#### Scenario: Minor fluctuation
- **WHEN** metric delta is between -0.5 and +0.5
- **THEN** display dash (→) with neutral styling

#### Scenario: Threshold boundary
- **WHEN** metric delta is exactly ±0.5
- **THEN** treat as significant change and apply highlighting

### Requirement: Include AI analysis with comparison context

The system SHALL run the existing venue-level AI analysis pipeline on the current period, incorporating comparison context into the narrative.

#### Scenario: AI analysis with previous period context
- **WHEN** AI analysis is enabled for venue period comparison
- **THEN** analysis pipeline receives both current and previous period metrics
- **AND** synthesis stage incorporates trend information into overview and recommendations
- **AND** recommendations address areas of decline or leverage areas of improvement

#### Scenario: AI analysis unavailable
- **WHEN** AI analysis fails or is disabled
- **THEN** report displays metrics and trends without narrative analysis
- **AND** user is informed that AI analysis is unavailable
