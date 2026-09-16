# Report Configuration Files

These JSON configuration files define report parameters and can be used to run reports non-interactively via the command line or API.

## Usage

Run any report using its config file:

```bash
cd python
python generate_all_period_reports.py --config ../configs/venue_period_comparison.json
```

## Available Configs

### 1. `venue_period_comparison.json`
Compare a single venue's metrics between two time periods.

**Parameters:**
- `venue` - The venue name to analyze
- `current_period` - Start and end dates for the current period
- `previous_period` - Start and end dates for the previous period

**Example use case:** Compare Grand Prairie's performance in August vs July

### 2. `multi_venue_single_period.json`
Aggregate metrics across all venues for one time period with venue ranking and trends.

**Parameters:**
- `period` - Start and end dates for the analysis period

**Example use case:** Rank all Texas venues for August performance

### 3. `multi_venue_period_comparison.json`
Compare aggregated metrics across all venues between two time periods.

**Parameters:**
- `current_period` - Start and end dates for the current period
- `previous_period` - Start and end dates for the previous period

**Example use case:** See how all Texas venues performed in August vs July

### 4. `single_venue_all.json`
Generate single-venue reports for all venues in the CSV file (existing functionality).

**Parameters:**
- None required (generates for all venues)

**Example use case:** Generate detailed reports for each venue

## Config File Structure

All configs have this basic structure:

```json
{
  "report_type": "venue_period_comparison",
  "csv_file": "../qualtrics/Grand_Prarie.csv",
  "output_format": "all",
  "venue": "Grand Prairie",
  "current_period": {
    "start_date": "2026-08-01",
    "end_date": "2026-08-31"
  },
  "previous_period": {
    "start_date": "2026-07-01",
    "end_date": "2026-07-31"
  }
}
```

### Common Fields

- `report_type` - One of: `single_venue`, `venue_period_comparison`, `multi_venue_single_period`, `multi_venue_period_comparison`
- `csv_file` - Path to the Qualtrics CSV file
- `output_format` - One of: `html`, `markdown`, `pdf`, `all`

### Type-Specific Fields

**venue_period_comparison & multi_venue_period_comparison:**
- `current_period.start_date` - YYYY-MM-DD format
- `current_period.end_date` - YYYY-MM-DD format
- `previous_period.start_date` - YYYY-MM-DD format
- `previous_period.end_date` - YYYY-MM-DD format

**multi_venue_single_period:**
- `period.start_date` - YYYY-MM-DD format
- `period.end_date` - YYYY-MM-DD format

**venue_period_comparison:**
- `venue` - Name of the venue to analyze

## Creating Custom Configs

Copy one of the example configs and modify the parameters:

1. Choose the report type you want
2. Update the CSV file path
3. Set the date ranges
4. Add venue name if needed
5. Set output format (html, markdown, pdf, or all)

Example for custom venue comparison:

```json
{
  "report_type": "venue_period_comparison",
  "csv_file": "../qualtrics/texas_venues.csv",
  "venue": "Dallas",
  "current_period": {
    "start_date": "2026-09-01",
    "end_date": "2026-09-30"
  },
  "previous_period": {
    "start_date": "2026-08-01",
    "end_date": "2026-08-31"
  },
  "output_format": "pdf"
}
```

## Future: Web UI Integration

These configs will become the contract between a future web UI and the Python report generation system:

1. Web UI generates a config file based on user selections
2. Calls the Python script with `--config config_file.json`
3. Displays the results to the user

This architecture makes the system flexible and reusable across different interfaces (CLI, web UI, API, etc.).
