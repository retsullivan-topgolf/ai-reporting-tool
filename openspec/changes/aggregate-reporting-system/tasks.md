## 1. API Extensions - Venue Processor

- [x] 1.1 Add `filter_by_date_range()` function to `csv_parser.py` to extract records within date range
- [x] 1.2 Add `calculate_period_summary()` function to `venue_processor.py` to aggregate metrics across venues
- [x] 1.3 Add `calculate_composite_score()` function to `venue_processor.py` for venue ranking
- [x] 1.4 Add `compare_periods()` function to `venue_processor.py` to calculate deltas and percent changes
- [x] 1.5 Add `get_period_type()` function to determine if period is month or quarter from date range
- [x] 1.6 Add unit tests for all new venue_processor functions
- [x] 1.7 Add unit tests for date filtering and edge cases (empty periods, missing data, etc.)

## 2. Report 1: Venue Period Comparison - API & Data

- [x] 2.1 Create `python/create_venue_period_comparison_report.py` script
- [x] 2.2 Implement CSV filtering for current and previous periods
- [x] 2.3 Implement delta and percent change calculations
- [x] 2.4 Implement trend threshold logic (±0.5 points)
- [x] 2.5 Integrate with existing `ai_analysis.py` for venue-level analysis
- [x] 2.6 Add comparison context to AI analysis prompts
- [ ] 2.7 Test with sample data (single venue, month and quarter comparisons)

## 3. Report 1: Venue Period Comparison - Templates

- [x] 3.1 Create `templates/venue-comparison-browser.html` template
- [x] 3.2 Create `templates/venue-comparison-pdf.html` template
- [x] 3.3 Create `templates/venue-comparison-report.md.j2` template
- [x] 3.4 Add CSS styling for trend indicators (↑ ↓ →) and comparison columns
- [x] 3.5 Add delta and percent change display in metric cards
- [ ] 3.6 Test template rendering with sample data

## 4. Report 2: Multi-Venue Single Period - API & Data

- [x] 4.1 Create `python/create_multi_venue_period_report.py` script
- [x] 4.2 Implement period summary calculation using `calculate_period_summary()`
- [x] 4.3 Implement composite score calculation for all venues
- [x] 4.4 Implement venue ranking by composite score
- [x] 4.5 Extract and aggregate comment themes from current period
- [ ] 4.6 Implement period-level AI analysis pipeline (adapt existing 3-stage pipeline)
- [ ] 4.7 Test with sample data (multiple venues, single period)

## 5. Report 2: Multi-Venue Single Period - Templates

- [x] 5.1 Create `templates/multi-venue-snapshot-browser.html` template
- [x] 5.2 Create `templates/multi-venue-snapshot-pdf.html` template
- [x] 5.3 Create `templates/multi-venue-snapshot-report.md.j2` template
- [x] 5.4 Add CSS styling for venue ranking table and composite score display
- [x] 5.5 Add metric cards showing aggregated metrics
- [x] 5.6 Add venue ranking section with composite scores and component breakdown
- [x] 5.7 Add comment themes section with frequency counts and venue attribution
- [ ] 5.8 Test template rendering with sample data

## 6. Report 3: Multi-Venue Period Comparison - API & Data

- [x] 6.1 Create `python/create_period_comparison_report.py` script
- [x] 6.2 Implement dual period filtering (current and previous)
- [x] 6.3 Implement period summary calculation for both periods
- [x] 6.4 Implement composite score calculation for both periods
- [x] 6.5 Implement venue ranking comparison and change detection
- [x] 6.6 Implement delta calculations for aggregated metrics
- [x] 6.7 Implement ranking change identification (movers, new top 3, etc.)
- [x] 6.8 Extract and aggregate comment themes from current period only
- [ ] 6.9 Implement period-level AI analysis with comparison context
- [ ] 6.10 Test with sample data (multiple venues, two periods)

## 7. Report 3: Multi-Venue Period Comparison - Templates

- [x] 7.1 Create `templates/multi-venue-comparison-browser.html` template
- [x] 7.2 Create `templates/multi-venue-comparison-pdf.html` template
- [x] 7.3 Create `templates/multi-venue-comparison-report.md.j2` template
- [x] 7.4 Add CSS styling for comparison columns (Current | Previous | Change | % Change | Trend)
- [x] 7.5 Add metric cards showing aggregated metrics with deltas
- [x] 7.6 Add venue ranking comparison section with ranking changes
- [x] 7.7 Add trend indicators for significant changes (±0.5 threshold)
- [x] 7.8 Add response count comparison and warning for ±20% differences
- [ ] 7.9 Test template rendering with sample data

## 8. AI Analysis Extensions

- [ ] 8.1 Create period-level metrics analysis prompt (adapt existing metrics_analysis.md)
- [ ] 8.2 Create period-level comment analysis prompt (adapt existing comment_analysis.md)
- [ ] 8.3 Create period-level synthesis prompt (adapt existing synthesis prompts)
- [x] 8.4 Implement `get_period_ai_analysis()` function in `ai_analysis.py`
- [ ] 8.5 Implement caching for period-level analysis results
- [ ] 8.6 Test AI analysis with sample multi-venue data
- [ ] 8.7 Verify comment analysis is limited to current period only

## 9. Integration & Testing

- [ ] 9.1 Create test CSV files with sample data (multiple venues, multiple periods)
- [ ] 9.2 Test Report 1 generation (venue period comparison)
- [ ] 9.3 Test Report 2 generation (multi-venue single period)
- [ ] 9.4 Test Report 3 generation (multi-venue period comparison)
- [ ] 9.5 Test all three report formats (HTML, Markdown, PDF) for each report type
- [ ] 9.6 Test edge cases: empty periods, missing data, single venue, tied scores
- [ ] 9.7 Test trend threshold logic (±0.5 points)
- [ ] 9.8 Test composite score calculation with missing F&B data
- [ ] 9.9 Test date filtering for month and quarter periods
- [ ] 9.10 Test AI analysis with and without comments

## 10. Documentation & Deployment

- [ ] 10.1 Update `AGENTS.md` with new report types and usage instructions
- [ ] 10.2 Update `API_QUICK_REFERENCE.md` with new API functions
- [ ] 10.3 Create usage examples for each report type
- [ ] 10.4 Document composite score calculation and weighting
- [ ] 10.5 Document date filtering and period type detection
- [ ] 10.6 Document trend threshold and visual indicators
- [ ] 10.7 Create troubleshooting guide for common issues
- [ ] 10.8 Update project README with new capabilities
- [ ] 10.9 Review and test all documentation
- [ ] 10.10 Deploy to production and verify all reports generate correctly

## 11. Optional Enhancements (Post-MVP)

- [ ] 11.1 Add configurable composite score weights via config file
- [ ] 11.2 Add venue filtering option (generate report for subset of venues)
- [ ] 11.3 Add custom time period support (beyond month/quarter)
- [ ] 11.4 Add trend visualization charts (line graphs for metric trends)
- [ ] 11.5 Add response count threshold warnings
- [ ] 11.6 Add venue-to-venue comparison within a period
- [ ] 11.7 Add historical data archival and multi-year trend analysis
