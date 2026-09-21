# Python Scripts for Topgolf Venue Reports

This directory contains all Python scripts for generating venue reports from survey data.

## Quick Start

Generate all reports with a single command:

```bash
cd python
python generate_venue_reports.py ../example-data/your_file.csv
```

This will:
1. Process your CSV file and create `venue_data.json`
2. Run AI analysis and create `ai_analysis_results.json`
3. Generate HTML, Markdown, and/or PDF reports in the `reports/` directory

## Scripts

### 0. `generate_venue_reports.py` (Recommended)
Master orchestrator that runs the complete workflow: data generation, AI analysis, and report creation in one command.

**Usage:**
```bash
cd python
python generate_venue_reports.py ../example-data/your_file.csv
python generate_venue_reports.py ../example-data/your_file.csv --format all
python generate_venue_reports.py ../example-data/your_file.csv --format html,pdf
```

**Output:**
- Creates `venue_data.json` in the python folder
- Creates `ai_analysis_results.json` in the python folder
- Creates report files in `../reports/`: `Topgolf_Venue_Report_[VenueName]_YYYYMMDD_HHMMSS_1PAGE.{html,md,pdf}`

---

### 1. `generate_venue_data.py`
Processes CSV survey data and generates a JSON file with aggregated venue metrics.

**Usage:**
```bash
cd python
python generate_venue_data.py ../example-data/your_file.csv
```

**Output:**
- Creates `venue_data.json` in the python folder with aggregated metrics for each venue

---

### 2. `run_analyze_venues.py`
Runs the AI analysis pipeline for all venues and caches results to JSON.

**Usage:**
```bash
cd python
python run_analyze_venues.py venue_data.json
```

**Output:**
- Creates `ai_analysis_results.json` in the python folder

---

### 3. `create_single_venue_snapshot_report.py`
Generates single-venue snapshot reports (HTML, Markdown, and/or PDF) from venue data.

**Usage:**
```bash
cd python
python create_single_venue_snapshot_report.py venue_data.json --format all --analysis ai_analysis_results.json
python create_single_venue_snapshot_report.py venue_data.json --format html
python create_single_venue_snapshot_report.py venue_data.json --format markdown,pdf
```

**Output:**
- Creates report files in `../reports/`: `Topgolf_Venue_Report_[VenueName]_1PAGE.{html,md,pdf}`

### 4. `generate_period_reports.py`
Unified orchestrator for period-based reports with interactive menu. Supports single-venue period comparison, multi-venue snapshots, and multi-venue period comparison.

**Usage:**
```bash
cd python
python generate_period_reports.py ../example-data/your_file.csv
```

---

### 5. `check_venues.py` (Deprecated)
Utility script to check venues in a CSV file.

### 6. `test_csv.py` (Deprecated)
Utility script to test CSV parsing and display venue information.

## Workflow

**Recommended (One Command):**
```bash
python generate_venue_reports.py ../example-data/your_file.csv
```

**Manual Steps:**
1. Run `generate_venue_data.py` with your CSV file to create `venue_data.json`
2. Run `run_analyze_venues.py` to create `ai_analysis_results.json`
3. Run `create_single_venue_snapshot_report.py` to generate reports

## File Paths

Scripts reference files as follows:
- Input CSV files: `../example-data/` (parent directory)
- JSON data file: `venue_data.json` (in python folder)
- AI analysis cache: `ai_analysis_results.json` (in python folder)
- Output reports: `../reports/Topgolf_Venue_Report_*.{html,md,pdf}`
