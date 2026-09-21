# Project Structure & Workflow

## Python Scripts Location
All Python scripts have been moved to the `python/` directory for better organization.

### Scripts in `python/` folder:

#### Report Generation (Main Entry Points)
- **generate_report.py** - **Unified entry point** for all report types (recommended). Single command to generate any report: single-venue snapshot, single-venue comparison, multi-venue snapshot, or multi-venue comparison. Supports interactive prompts or command-line arguments for all parameters (report type, venue, dates, format).
- **generate_venue_reports.py** - Legacy master orchestrator for single-venue reports (CSV-based). Processes data → generates metrics → runs AI analysis once → generates report formats. After processing the data, it asks which report format(s) to generate - HTML, Markdown, PDF, or All - or takes `--format` to skip the prompt.

#### Data Processing
- **generate_venue_data.py** - Loads survey data (defaults to all venues from texas_venues, can filter by venue) → generates JSON metrics

#### AI Analysis
- **analyze_venues.py** - Core module implementing the 3-stage AI analysis pipeline (metrics_analysis → comment_analysis → synthesis)
- **run_analyze_venues.py** - Orchestrator that runs AI analysis for all venues and caches results to JSON. Called by `generate_venue_reports.py` to avoid re-running expensive API calls for each report format.

#### Report Builder Scripts
**Snapshot Reports (single period):**
- **create_single_venue_snapshot_report.py** - Unified builder for single-venue snapshots. Generates HTML, Markdown, and/or PDF formats from venue_data.json. Supports `--format html|markdown|pdf|all` to choose which formats to generate.
- **create_multi_venue_snapshot_report.py** - Multi-venue snapshot (HTML, Markdown, PDF)

**Comparison Reports (two periods):**
- **create_single_venue_comparison_report.py** - Single venue period comparison (HTML, Markdown, PDF). Shows deltas, percent changes, and trend indicators.
- **create_multi_venue_comparison_report.py** - Multi-venue period comparison (HTML, Markdown, PDF). Shows ranking changes and trends.

#### Shared Utilities
- **report_content.py** - Shared, format-agnostic analysis/context logic used by all report builders
- **report_engine.py** - Metrics registry and assessment logic
- **check_venues.py** - Utility to check venues in CSV files (deprecated)
- **test_csv.py** - Utility to test CSV parsing (deprecated)

### Running Scripts

**Data Loader Abstraction:**
All scripts use the `api.data_loader` module to load survey data. The module defaults to loading all data from `texas_venues.csv` (the complete dataset) and supports filtering by venue. This abstraction allows easy transition to a real API when available without changing script code.

**Available Datasets & Venues:**
- `texas_venues` - Multi-venue data (Austin, Dallas, El Paso, Ft Worth, Grand Prairie, San Antonio, The Colony) - **DEFAULT**
- `Grand_Prairie` - Single venue data (Grand Prairie only) - for backward compatibility

List available datasets:
```bash
cd python
python generate_venue_data.py --list
```

List available venues in texas_venues:
```bash
cd python
python generate_venue_data.py --venues
```

**Load All Venues (from texas_venues):**
```bash
cd python
python generate_venue_data.py
# Press Enter when prompted to load all venues
```

**Load Single Venue (from texas_venues):**
```bash
cd python
python generate_venue_data.py "Grand Prairie"
# Or select from interactive menu
```

**Load from Specific Dataset (backward compatible):**
```bash
cd python
python generate_venue_data.py --dataset Grand_Prairie
```

**Unified Report Generator (Recommended - All Report Types):**
```bash
cd python
# Interactive mode - prompts for report type, venue, dates, and format
python generate_report.py

# Or specify parameters directly
# Single-venue snapshot for Grand Prairie
python generate_report.py --report-type snapshot --venue "Grand Prairie" --format all

# Single-venue comparison between two periods
python generate_report.py --report-type comparison --venue "Grand Prairie" --start-date 2026-01-01 --end-date 2026-01-31 --prev-start 2025-12-01 --prev-end 2025-12-31 --format html

# Multi-venue snapshot for a period
python generate_report.py --report-type multi-snapshot --start-date 2026-01-01 --end-date 2026-01-31 --format all

# Multi-venue comparison between two periods
python generate_report.py --report-type multi-comparison --start-date 2026-01-01 --end-date 2026-01-31 --prev-start 2025-12-01 --prev-end 2025-12-31 --format pdf
```

**Or run individual scripts (advanced):**
```bash
cd python
# Single-venue snapshot - manual steps
python generate_venue_data.py "Grand Prairie"
python run_analyze_venues.py venue_data.json
python create_single_venue_snapshot_report.py venue_data.json --format all --analysis ai_analysis_results.json

# Single-venue comparison
python create_single_venue_comparison_report.py texas_venues "Grand Prairie" 2026-01-01 2026-01-31 2025-12-01 2025-12-31 --format all

# Multi-venue snapshot
python create_multi_venue_snapshot_report.py texas_venues 2026-01-01 2026-01-31 --format all

# Multi-venue comparison
python create_multi_venue_comparison_report.py texas_venues 2026-01-01 2026-01-31 2025-12-01 2025-12-31 --format all
```

### File Paths
- Input CSVs: `api/qualtrics/` (managed by data_loader)
- JSON metrics: `venue_data.json` (python folder)
- AI analysis cache: `ai_analysis_results.json` (python folder)
- Output HTML: `../reports/Topgolf_Venue_Report_*_YYYYMMDD_HHMMSS_1PAGE.html`
- Output Markdown: `../reports/Topgolf_Venue_Report_*_YYYYMMDD_HHMMSS_1PAGE.md`
- Output PDF: `../reports/Topgolf_Venue_Report_*_YYYYMMDD_HHMMSS_1PAGE.pdf`

## Report Generation Workflow

**Unified approach (recommended for all report types):**
```bash
cd python
python generate_report.py
```
This interactive script guides you through:
1. Selecting report type (snapshot, comparison, multi-snapshot, multi-comparison)
2. Entering required parameters (venue name, date ranges)
3. Choosing output format (HTML, Markdown, PDF, or All)
4. Automatically running all necessary steps

**Or use command-line arguments to skip prompts:**
```bash
cd python
python generate_report.py --report-type snapshot --venue "Grand Prairie" --format all
```

**For single-venue snapshots specifically:**
The `generate_report.py` script with `--report-type snapshot` automatically:
1. Runs `generate_venue_data.py` to create `venue_data.json`
2. Runs `run_analyze_venues.py` to create `ai_analysis_results.json` (AI analysis runs once)
3. Runs `create_single_venue_snapshot_report.py` with precomputed analysis to generate reports in all selected formats

## Report Features
- Color-coded status pills in Experience Metrics table
- Performance summary with metric cards
- **Overall Assessment synthesizes WEAK metrics** - If any performance metric is rated WEAK/Poor/Critical, the Overall Assessment text automatically includes a synthesized explanation of what that weakness means for the business (e.g., "customers are frequently very unsatisfied with how issues are resolved during their visit" instead of just "Issue Resolution")
- **Venue overview narrative** - Tells the story without redundantly repeating metric numbers; uses descriptive language like "over half" or "most guests" instead of exact percentages/scores that are already in the Performance Summary cards
- Ups/Downs analysis
- Impact drivers ranking
- Actionable recommendations

## Period-Based Reports (NEW)

Three new report types enable period analysis and multi-venue aggregation:

### Report Type 1: Venue Period Comparison
Compare a single venue's performance between two time periods (current vs. previous month/quarter).

**Usage:**
```bash
cd python
# Load from texas_venues (default) and filter by venue
python create_single_venue_comparison_report.py "Grand Prairie" "Grand Prairie" 2026-01-01 2026-01-31 2025-12-01 2025-12-31 --format all

# Or load from specific dataset (backward compatible)
python create_single_venue_comparison_report.py Grand_Prairie "Grand Prairie" 2026-01-01 2026-01-31 2025-12-01 2025-12-31 --format all
```

**Features:**
- Side-by-side metric comparison (Current | Previous | Change | % Change | Trend)
- Trend indicators: ↑ (improvement ≥+0.5), ↓ (decline ≤-0.5), → (minor change)
- AI analysis with comparison context
- Comments from current period only

**Output:** `Topgolf_Venue_Period_Comparison_<venue>_<timestamp>_1PAGE.{html,md,pdf}`

### Report Type 2: Multi-Venue Single Period
Aggregate metrics across all venues for a given time period, ranked by composite performance score.

**Usage:**
```bash
cd python
# Load from texas_venues (default) - processes all venues
python create_multi_venue_snapshot_report.py texas_venues 2026-01-01 2026-01-31 --format all

# Or load from specific dataset (backward compatible)
python create_multi_venue_snapshot_report.py Grand_Prairie 2026-01-01 2026-01-31 --format all
```

**Features:**
- Aggregated metrics across all venues (LTR, Fun, Helpful, Issues, Resolution)
- Venue ranking by composite score: LTR (40%) + Fun (20%) + F&B avg (20%) + Resolution (20%)
- Comment themes aggregated from all venues
- Handles missing F&B data gracefully (redistributes weights)

**Output:** `Topgolf_Multi_Venue_Period_<period>_<timestamp>_1PAGE.{html,md,pdf}`

### Report Type 3: Multi-Venue Period Comparison
Compare aggregated metrics across all venues between two time periods with ranking changes.

**Usage:**
```bash
cd python
# Load from texas_venues (default) - processes all venues
python create_multi_venue_comparison_report.py texas_venues 2026-01-01 2026-01-31 2025-12-01 2025-12-31 --format all

# Or load from specific dataset (backward compatible)
python create_multi_venue_comparison_report.py Grand_Prairie 2026-01-01 2026-01-31 2025-12-01 2025-12-31 --format all
```

**Features:**
- Aggregated metrics comparison with deltas and percent changes
- Venue ranking changes (which venues moved up/down)
- Trend indicators for significant changes (±0.5 threshold)
- Response count comparison with warnings for ±20% differences
- Comment themes from current period only

**Output:** `Topgolf_Period_Comparison_<periods>_<timestamp>_1PAGE.{html,md,pdf}`

### Composite Score Calculation

The venue ranking/composite score is the venue's **Combined NPS** (`nps_avg`), used directly rather than blended into a weighted formula. NPS is a Qualtrics-computed metric that's already a composite of underlying satisfaction signals, so folding it into an additional weighted formula alongside Fun/F&B/Resolution would double-count that signal. Only the `real` schema (which includes a Combined NPS field) has a composite score; venues/schemas without NPS data get `None`.

Note: `nps` (Combined NPS, 1-10 scale) and `ltr` (Likelihood to Return, 1-5 scale) are two distinct survey fields - do not conflate them. NPS is a recommend-intent metric; LTR is a retention-intent metric.

### Trend Threshold

Changes ≥ ±0.5 points are highlighted as "significant":
- **↑ Up arrow:** Improvement of 0.5+ points (green)
- **↓ Down arrow:** Decline of 0.5+ points (red)
- **→ Dash:** Minor change between -0.5 and +0.5 (neutral)

## Key Files

### Templates
**Single-Venue Snapshots:**
- `templates/venue-snapshot-browser.html` - HTML template
- `templates/venue-snapshot-pdf.html` - PDF template
- `templates/venue-snapshot-report.md.j2` - Markdown template

**Single-Venue Comparisons:**
- `templates/venue-comparison-browser.html` - HTML template
- `templates/venue-comparison-pdf.html` - PDF template
- `templates/venue-comparison-report.md.j2` - Markdown template

**Multi-Venue Snapshots:**
- `templates/multi-venue-snapshot-browser.html` - HTML template
- `templates/multi-venue-snapshot-pdf.html` - PDF template
- `templates/multi-venue-snapshot-report.md.j2` - Markdown template

**Multi-Venue Comparisons:**
- `templates/multi-venue-comparison-browser.html` - HTML template
- `templates/multi-venue-comparison-pdf.html` - PDF template
- `templates/multi-venue-comparison-report.md.j2` - Markdown template

### Directories
- `python/` - All Python processing scripts
- `example-data/` - Sample CSV survey data
- `reports/` - Generated reports (created automatically)

### Generated Reports
- Single-venue: `Topgolf_Venue_Report_*_1PAGE.{html,md,pdf}`
- Venue period comparison: `Topgolf_Venue_Period_Comparison_*_1PAGE.{html,md,pdf}`
- Multi-venue single period: `Topgolf_Multi_Venue_Period_*_1PAGE.{html,md,pdf}`
- Multi-venue period comparison: `Topgolf_Period_Comparison_*_1PAGE.{html,md,pdf}`

---

## AI Analysis Architecture

### Overview
The report generation pipeline now uses a **3-stage AI analysis pipeline** that runs once and is reused across all report formats (HTML, Markdown, PDF). This avoids redundant API calls and ensures consistency.

### Pipeline Flow
1. **generate_venue_reports.py** (orchestrator)
   - Step 1: Runs `generate_venue_data.py` → creates `venue_data.json`
   - Step 2: Runs `run_analyze_venues.py` → creates `ai_analysis_results.json` (AI analysis runs once here)
   - Step 3: Runs `create_single_venue_snapshot_report.py` with `--analysis ai_analysis_results.json`

2. **run_analyze_venues.py** (orchestrator script)
   - Loads all venues from `venue_data.json`
   - Calls `ai_analysis.get_ai_analysis()` for each venue
   - Saves results to `ai_analysis_results.json` with structure:
     ```json
     {
       "venue_key": {
         "ai_available": true/false,
         "analysis": {...},  // or "unavailable_reason": "..."
       }
     }
     ```

3. **ai_analysis.py** (3-stage pipeline)
   - **Stage 1: metrics_analysis** - Analyzes 5 aggregate metrics, produces concern flags
   - **Stage 2: comment_analysis** - Analyzes guest comments + metric flags, identifies themes
   - **Stage 3: synthesis** - Produces final overview/ups/downs/impact/recommendations (see related skills below)
   - Each stage is cached independently and reusable

4. **report_content.py** (updated)
   - `get_analysis(data, precomputed_analysis=None)` - Accepts precomputed analysis
   - `render_html_report(..., precomputed_analysis=None)` - Passes analysis to template rendering
   - Falls back to on-the-fly analysis if precomputed not provided (backward compatible)

5. **Report builder scripts** (create_single_venue_snapshot_report.py, create_single_venue_comparison_report.py, etc.)
   - Accept `--analysis <file>` parameter
   - Load precomputed analysis and pass to report generation
   - Support `--format` parameter to choose HTML, Markdown, PDF, or all

### Benefits
✅ **Single AI analysis run** - Expensive API calls happen once, not 3 times
✅ **Consistent analysis** - All report formats use identical analysis data
✅ **Backward compatible** - Scripts work without `--analysis` parameter (slower, but functional)
✅ **Cacheable** - AI analysis results cached by `ai_analysis.py` (metrics, comments, synthesis stages)
✅ **Debuggable** - Analysis results saved to JSON file for inspection/debugging

### Synthesis Skills

The Stage 3 synthesis prompt is guided by four modular skill documents in `.claude/single-venue-report/`:

1. **venue-overview-skill.md**
   - Writes 2-4 sentence narrative summary
   - Key rule: Avoid redundant metric numbers; use descriptive language ("over half", "most guests")
   - Example: "This venue is performing well overall, driven by strong satisfaction with the experience. However, equipment reliability issues are creating friction..."

2. **ups-downs-skill.md**
   - Identifies 2-3 positive and 2-3 negative findings
   - Key rule: Don't limit to top 3; include lower-magnitude items with distinct operational value
   - Example: Strong recommendation intent, Responsive staff, Equipment reliability issues, Food service speed

3. **impact-drivers-skill.md**
   - Explains the top 3 factors affecting performance
   - Key rule: Follow magnitude ranking strictly; cite numbers
   - Example: Recommendation Intent (87% LTR), Equipment Reliability (14 comments), Staff Responsiveness (8 mentions)

4. **recommendations-skill.md**
   - Generates actionable next steps in three tiers
   - Key rule: Critical addresses #1 negative, Secondary addresses #2 negative, Maintain reinforces #1 positive
   - Example: Critical: Fix Equipment Reliability (4 actions), Secondary: Improve Food Service Speed (4 actions), Maintain: Protect Recommendation Intent (4 actions)

All skills work from the same **combined ranking** of metrics + comment themes, sorted by magnitude (highest first). This ensures consistent prioritization across all sections.

**For detailed guidance on the synthesis pipeline and skills**, see `.claude/single-venue-report/README.md`.

**For detailed guidance on metrics handling in the overview**, see `.claude/single-venue-report/overview-metrics-guidance.md`.

---

---

## API Module Architecture

### Overview

The `api/` module provides clean separation between CSV parsing logic and report generation. It handles:
- **Schema detection** - Automatically identifies POC vs Real survey formats
- **CSV parsing** - Reads and validates Qualtrics CSV files
- **Venue data aggregation** - Calculates metrics and groups by venue
- **Optional REST wrapper** - Flask app for future web-based usage

### Module Structure

```
api/
├── __init__.py              # Package initialization
├── schemas.py              # JSON Schema definitions (POC & Real)
├── csv_parser.py           # CSV reading, validation, field extraction
├── venue_processor.py      # Venue grouping and metrics calculation
└── app.py                  # Optional Flask REST API (future use)
```

### Using the API in Python

```python
from api import csv_parser, venue_processor

# Step 1: Parse CSV file
rows, fieldnames = csv_parser.parse_csv('../qualtrics/Grand_Prarie.csv')

# Step 2: Detect schema type
schema_type = csv_parser.detect_schema(fieldnames)  # Returns 'poc' or 'real'

# Step 3: Build venue data
venue_data = venue_processor.build_venue_data_dict(rows, schema_type)

# Result: {
#   "grand_prairie": {
#     "venue": "Grand Prairie",
#     "responses": 475,
#     "ltr_avg": 8.3,
#     "fun_avg": 4.4,
#     ...
#   }
# }
```

### API Functions

#### csv_parser module

- **`parse_csv(file_path)`** - Read CSV and return (rows, fieldnames)
  - Handles Qualtrics format with header rows
  - Returns list of dicts and column names
  - Raises `CSVParseError` on failure

- **`detect_schema(fieldnames)`** - Identify schema type
  - Returns 'poc' or 'real'
  - Raises `SchemaDetectionError` if ambiguous
  - Checks for schema-specific field patterns

- **`get_field(row, field_name, schema_name)`** - Extract field from row
  - Uses schema mapping to find CSV column
  - Returns trimmed string value
  - Safe: returns empty string if not found

- **`convert_field_value(value, field_name, schema_name)`** - Convert to proper type
  - Handles categorical→numeric mapping
  - Converts text booleans to bool
  - Parses integers and floats
  - Returns None if conversion fails

- **`validate_row(row, schema_name)`** - Validate row against schema
  - Returns (is_valid, error_message)
  - Checks required fields
  - Validates field types

#### venue_processor module

- **`group_by_venue(rows)`** - Group rows by venue
  - Returns dict: venue_name → list of rows

- **`process_venue_data(rows, schema_name)`** - Calculate metrics for one venue
  - Aggregates scores (LTR, Fun, Helpful, etc.)
  - Calculates averages and percentages
  - Extracts comments
  - Returns dict with all metrics

- **`build_venue_data_dict(rows, schema_name)`** - Process all venues
  - Groups rows by venue
  - Processes each venue
  - Returns final venue_data structure

### Schema Definitions

#### POC Schema (Original)
- Fields: Venue, VisitDate, Q1_LTR, Q2_FUN, Q3_HELPFUL, Q4_ISSUES, Q5_ISSUE_RESOLUTION, Q6_COMMENT
- LTR: 1-10 scale
- Fun/Helpful: 5-point categorical ("5 - Extremely fun", etc.)

#### Real Schema (Production)
- Fields: Venue, Visit Date, Combined NPS, Fun, Helpful, Issues, Issue Resolution, Open Comment
- Plus F&B metrics: Food/Beverage Value, Speed, Quality (1-5 scales)
- Plus Return Likelihood, Price Value (1-5 scales)
- LTR: 1-10 scale (called "Combined NPS")
- All metrics: numeric 1-5 scales

### Optional REST API

To run the Flask REST API server:

```bash
cd api
python app.py                    # http://localhost:5000
python app.py --port 8080        # Custom port
python app.py --host 0.0.0.0     # Listen on all interfaces
```

Available endpoints:

- **GET /api/health** - Health check
  ```json
  { "status": "ok", "service": "Topgolf Reporting API", "version": "1.0.0" }
  ```

- **GET /api/schemas** - List available schemas
  ```json
  {
    "schemas": [
      {
        "name": "poc",
        "description": "Proof of Concept survey format",
        "fields": ["venue", "visit_date", "ltr", ...]
      },
      ...
    ]
  }
  ```

- **POST /api/parse-csv** - Parse CSV and return venue data
  - Request: multipart form with `file` field, OR JSON with `csv_path`
  - Response: `{ "success": true, "schema": "real", "venues": {...} }`

- **POST /api/validate-row** - Validate a single row
  - Request: `{ "schema": "real", "row": {...} }`
  - Response: `{ "valid": true, "error": null }`

### Integration with Report Generation

The `python/generate_reports.py` script now uses the API:

```python
from api import csv_parser, venue_processor

# Parse and process
rows, fieldnames = csv_parser.parse_csv(csv_file)
schema_type = csv_parser.detect_schema(fieldnames)
venue_data_dict = venue_processor.build_venue_data_dict(rows, schema_type)

# Save to JSON
with open('venue_data.json', 'w') as f:
    json.dump(venue_data_dict, f, indent=2)
```

No changes needed to `generate_all_reports.py` - it calls `generate_reports.py` which now uses the API internally.

### Adding Support for New Schemas

To add a new survey format:

1. **Add schema definition** in `api/schemas.py`:
   ```python
   NEW_SCHEMA = {
       "name": "new_format",
       "description": "New survey format",
       "fields": {
           "venue": { "csv_column": "...", "type": "string", ... },
           ...
       },
       "detection_rule": "Checks for specific columns"
   }
   SCHEMAS["new_format"] = NEW_SCHEMA
   ```

2. **Update detection logic** in `csv_parser.detect_schema()`:
   ```python
   has_new_fields = any('NewField' in field for field in fieldnames)
   if has_new_fields and ...:
       return 'new_format'
   ```

3. **Update venue processor** if needed in `venue_processor.py`:
   - Add new metric calculations if schema has new fields
   - Ensure `process_venue_data()` handles new metrics

---

## For Developers

### How the AI Analysis Pipeline Works

The `python/ai_analysis.py` script implements the 3-stage pipeline:

```python
# Stage 1: Load metrics_analysis.md and analyze metrics
METRICS_ANALYSIS_SKILL = _load_skill('metrics_analysis.md')
metrics_result, error = _run_stage(
    'metrics_analysis', 
    METRICS_ANALYSIS_SKILL, 
    _build_metrics_payload(data),
    _validate_metrics_analysis, 
    venue, 
    use_cache=True
)
# Output: characterization + metric_flags

# Stage 2: Load comment_analysis.md and analyze comments
COMMENT_ANALYSIS_SKILL = _load_skill('comment_analysis.md')
comment_result, error = _run_stage(
    'comment_analysis', 
    COMMENT_ANALYSIS_SKILL,
    _build_comment_payload(data, metrics_result['metric_flags']),
    _validate_comment_analysis, 
    venue, 
    use_cache=True
)
# Output: themes with magnitude and summary

# Stage 3: Load synthesis.md and all skill guides, then synthesize
SYNTHESIS_SKILL = _load_skill('synthesis.md')
synthesis_payload = {
    'venue': venue,
    'responses': data['responses'],
    'metrics_analysis': metrics_result,
    'comment_analysis': comment_result,
}
synthesis_result, error = _run_stage(
    'synthesis', 
    SYNTHESIS_SKILL, 
    synthesis_payload,
    _validate_synthesis, 
    venue, 
    use_cache=True
)
# Output: overview, ups, downs, impact, recommendations
```

### Caching

Each stage is cached independently:

```python
def _stage_cache_key(stage, skill_text, payload):
    """Hash of (stage guideline doc + that stage's input payload)"""
    fingerprint = skill_text + "\n" + json.dumps(payload, sort_keys=True)
    return hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()
```

This means:
- Editing `venue-overview-skill.md` only invalidates the synthesis stage cache
- Editing `metrics_analysis.md` only invalidates the metrics_analysis stage cache
- Running with new data automatically invalidates all affected caches

### Adding a New Skill or Modifying the Pipeline

To add a new section or modify how synthesis works:

1. **Edit the skill file** in `.claude/single-venue-report/`
   - Add or modify the guidance
   - Update examples and rules
   - Update the output schema if needed

2. **Update `synthesis.md`** if the output structure changes
   - Update the Output section
   - Update the validation rules
   - Update the example

3. **Update `_validate_synthesis()`** in `ai_analysis.py` if the output schema changes
   - Add new required fields
   - Update validation logic

4. **Clear the cache** to force regeneration:
   ```bash
   python ai_analysis.py --clear-cache
   ```

5. **Test with sample data**:
   ```bash
   python generate_ai_analysis.py venue_data.json
   ```

### Skill File Locations

All skill files are in `.claude/single-venue-report/`:

```
.claude/single-venue-report/
├── README.md                      (This guide)
├── metrics_analysis.md            (Stage 1 prompt)
├── comment_analysis.md            (Stage 2 prompt)
├── synthesis.md                   (Stage 3 prompt)
├── venue-overview-skill.md        (Skill: overview writing)
├── ups-downs-skill.md             (Skill: findings selection)
├── impact-drivers-skill.md        (Skill: impact explanation)
├── recommendations-skill.md       (Skill: action generation)
└── overview-metrics-guidance.md   (Reference: metrics handling)
```

### Performance Considerations

- **3 API calls per venue** (one per stage)
- **Caching**: Subsequent runs with same data are instant
- **Timeout**: 600 seconds per stage (5 minutes)
- **Batch processing**: All venues processed sequentially

To optimize for large batches:
- Run `generate_ai_analysis.py` once to cache all results
- Reuse cached results across multiple report formats
- Clear cache only when data or prompts change

### Debugging

To debug the AI analysis:

1. **Check the cache**:
   ```bash
   ls -la python/.cache/ai_analysis/
   ```

2. **Clear cache and re-run**:
   ```bash
   python ai_analysis.py --clear-cache
   python generate_ai_analysis.py venue_data.json
   ```

3. **Inspect the output**:
   ```bash
   cat python/ai_analysis_results.json | jq '.["venue_name"]'
   ```

4. **Check for errors**:
   - Look for `"ai_available": false` in the results
   - Check the `unavailable_reason` field for error details
   - Verify Claude CLI is logged in: `claude auth status`
