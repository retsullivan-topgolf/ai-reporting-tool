## Why

Current reporting is limited to single-venue snapshots. Users need to understand performance across multiple venues and track trends over time (monthly and quarterly). This requires new aggregation capabilities, period comparison logic, and composite scoring to rank venue performance.

## What Changes

- **New Report Type 1: Venue Period Comparison** - Compare a single venue's metrics against its previous month/quarter with trend indicators
- **New Report Type 2: Multi-Venue Single Period** - Aggregate metrics across all venues for a given period, ranked by composite performance score
- **New Report Type 3: Multi-Venue Period Comparison** - Compare aggregated multi-venue metrics across two periods (month-to-month or quarter-to-quarter) with trend analysis
- **Enhanced API** - New functions in `venue_processor.py` for period aggregation and comparison
- **New Templates** - Three new Jinja2 templates for the three report types (HTML, Markdown, PDF variants)
- **New Report Scripts** - Three new Python scripts to orchestrate each report type
- **Period-Level AI Analysis** - Extend `ai_analysis.py` to synthesize insights across multiple venues for Reports 2 and 3

## Capabilities

### New Capabilities

- `venue-period-comparison`: Compare a single venue's performance in current period vs. previous period (month or quarter) with trend indicators (±0.5 point threshold)
- `multi-venue-aggregation`: Aggregate metrics across all venues in a CSV for a given time period, calculate composite ranking score (weighted: LTR + Fun + F&B avg + Issue Resolution)
- `period-comparison-analysis`: Compare aggregated multi-venue metrics across two time periods with delta calculations and trend visualization
- `composite-venue-ranking`: Calculate composite performance score for venues using weighted metrics (LTR, Fun, F&B average, Issue Resolution)
- `period-level-ai-synthesis`: Run AI analysis on aggregated period data to identify themes across venues and comment patterns (current period only)

### Modified Capabilities

- `csv-data-processing`: Extend to support filtering by date range and time period (month/quarter) for multi-period analysis

## Impact

**Code Changes:**
- `api/venue_processor.py` - Add period aggregation and comparison functions
- `api/csv_parser.py` - Add date range filtering utilities
- `ai_analysis.py` - Add period-level analysis pipeline
- `python/` - Add three new report generation scripts

**New Files:**
- `templates/venue-comparison-*.html/pdf/md.j2` - Templates for Report 1
- `templates/multi-venue-snapshot-*.html/pdf/md.j2` - Templates for Report 2
- `templates/multi-venue-comparison-*.html/pdf/md.j2` - Templates for Report 3
- `python/create_venue_period_comparison_report.py` - Report 1 orchestrator
- `python/create_multi_venue_period_report.py` - Report 2 orchestrator
- `python/create_period_comparison_report.py` - Report 3 orchestrator

**API Changes:**
- New functions: `calculate_period_summary()`, `compare_periods()`, `calculate_composite_score()`
- New AI analysis: Period-level synthesis pipeline

**Data Flow:**
- Reports 1 & 3 require filtering CSV by two date ranges (current and previous period)
- Report 2 requires filtering CSV by single date range and aggregating across venues
- All reports use composite scoring for venue ranking
