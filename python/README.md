# Python Scripts for Topgolf Venue Reports

This directory contains all Python scripts for generating venue reports from survey data.

## Quick Start

Generate all reports with a single command:

```bash
cd python
python generate_all_reports.py ../example-data/your_file.csv
```

This will:
1. Process your CSV file and create `venue_data.json`
2. Generate HTML reports in the parent directory

## Scripts

### 0. `generate_all_reports.py` (Recommended)
Master script that runs both data generation and HTML report creation in one command.

**Usage:**
```bash
cd python
python generate_all_reports.py ../example-data/topgolf_qualtrics_week_responses.csv
```

**Output:**
- Creates `venue_data.json` in the python folder
- Creates HTML report files in parent directory: `../Topgolf_Venue_Report_[VenueName]_1PAGE.html`

**Default input:**
- `../example-data/topgolf_qualtrics_week_responses.csv`

---

### 1. `generate_reports.py`
Processes CSV survey data and generates a JSON file with aggregated venue metrics.

**Usage:**
```bash
cd python
python generate_reports.py ../example-data/topgolf_qualtrics_week_responses.csv
```

**Output:**
- Creates `venue_data.json` in the python folder with aggregated metrics for each venue

**Default input:**
- `../example-data/topgolf_qualtrics_week_responses.csv`

### 2. `create_html_reports.py`
Generates HTML reports from the JSON venue data.

**Usage:**
```bash
cd python
python create_html_reports.py venue_data.json
```

**Output:**
- Creates HTML report files in parent directory: `../Topgolf_Venue_Report_[VenueName]_1PAGE.html`

**Default input:**
- `venue_data.json` (in python folder)

### 3. `check_venues.py`
Utility script to check venues in a CSV file.

**Usage:**
```bash
cd python
python check_venues.py
```

### 4. `test_csv.py`
Utility script to test CSV parsing and display venue information.

**Usage:**
```bash
cd python
python test_csv.py
```

## Workflow

1. Run `generate_reports.py` with your CSV file to create `venue_data.json`
2. Run `create_html_reports.py` to generate HTML reports from the JSON data

## File Paths

Scripts reference files as follows:
- Input CSV files: `../example-data/` (parent directory)
- JSON data file: `venue_data.json` (in python folder)
- Output HTML reports: `../Topgolf_Venue_Report_*.html` (parent directory)
