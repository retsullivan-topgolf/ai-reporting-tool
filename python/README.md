# Python Scripts for Topgolf Venue Reports

This directory contains all Python scripts for generating venue reports from survey data.

All scripts use the `api.data_loader` module to load survey data by identifier, abstracting away file path management. This makes it easy to transition to a real API when available.

## Quick Start

Generate any report type with a single unified command:

```bash
cd python
python generate_report.py
```

This interactive script lets you:
1. Choose report type (single-venue snapshot, comparison, multi-venue snapshot, or comparison)
2. Enter required parameters (venue name, date ranges)
3. Select output format (HTML, Markdown, PDF, or All)
4. Automatically runs all necessary steps and generates reports in `reports/` directory

**Or skip prompts with command-line arguments:**
```bash
cd python
# Single-venue snapshot
python generate_report.py --report-type snapshot --venue "Grand Prairie" --format all

# Single-venue comparison
python generate_report.py --report-type comparison --venue "Grand Prairie" --start-date 2026-01-01 --end-date 2026-01-31 --prev-start 2025-12-01 --prev-end 2025-12-31 --format all

# Multi-venue snapshot
python generate_report.py --report-type multi-snapshot --start-date 2026-01-01 --end-date 2026-01-31 --format all

# Multi-venue comparison
python generate_report.py --report-type multi-comparison --start-date 2026-01-01 --end-date 2026-01-31 --prev-start 2025-12-01 --prev-end 2025-12-31 --format all
```

## Available Datasets

List available datasets:
```bash
cd python
python generate_venue_data.py --list
```

## Scripts

### 0. `generate_report.py` (Recommended - Unified Entry Point)
Single command to generate any report type: single-venue snapshot, single-venue comparison, multi-venue snapshot, or multi-venue comparison.

**Interactive mode (prompts for all inputs):**
```bash
cd python
python generate_report.py
```

**Command-line mode (skip prompts):**
```bash
cd python
# Single-venue snapshot
python generate_report.py --report-type snapshot --venue "Grand Prairie" --format all

# Single-venue comparison
python generate_report.py --report-type comparison --venue "Grand Prairie" --start-date 2026-01-01 --end-date 2026-01-31 --prev-start 2025-12-01 --prev-end 2025-12-31 --format all

# Multi-venue snapshot
python generate_report.py --report-type multi-snapshot --start-date 2026-01-01 --end-date 2026-01-31 --format all

# Multi-venue comparison
python generate_report.py --report-type multi-comparison --start-date 2026-01-01 --end-date 2026-01-31 --prev-start 2025-12-01 --prev-end 2025-12-31 --format all
```

**Output:**
- For snapshots: Creates `venue_data.json`, `ai_analysis_results.json`, and report files in `../reports/`
- For comparisons: Creates report files directly in `../reports/`

---

### 0b. `generate_venue_reports.py` (Legacy - CSV-based)
Master orchestrator for single-venue reports using CSV files directly (legacy approach).

**Usage:**
```bash
cd python
python generate_venue_reports.py ../example-data/survey.csv
python generate_venue_reports.py ../example-data/survey.csv --format all
```

**Output:**
- Creates `venue_data.json` in the python folder
- Creates `ai_analysis_results.json` in the python folder
- Creates report files in `../reports/`: `Topgolf_Venue_Report_[VenueName]_YYYYMMDD_HHMMSS_1PAGE.{html,md,pdf}`

---

### 1. `generate_venue_data.py`
Loads survey data by identifier and generates a JSON file with aggregated venue metrics.

**Usage:**
```bash
cd python
python generate_venue_data.py Grand_Prairie
python generate_venue_data.py texas_venues
python generate_venue_data.py --list  # Show available datasets
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

### 4. `create_single_venue_comparison_report.py`
Generates single-venue period comparison reports comparing metrics between two time periods.

**Usage:**
```bash
cd python
python create_single_venue_comparison_report.py Grand_Prairie "Grand Prairie" 2026-01-01 2026-01-31 2025-12-01 2025-12-31 --format all
python create_single_venue_comparison_report.py texas_venues "Grand Prairie" 2026-01-01 2026-01-31 2025-12-01 2025-12-31
```

**Output:**
- Creates report files in `../reports/`: `Topgolf_Venue_Period_Comparison_*.{html,md,pdf}`

### 5. `create_multi_venue_snapshot_report.py`
Generates multi-venue aggregated reports for a single time period with venue ranking.

**Usage:**
```bash
cd python
python create_multi_venue_snapshot_report.py Grand_Prairie 2026-01-01 2026-01-31 --format all
python create_multi_venue_snapshot_report.py texas_venues 2026-01-01 2026-01-31
```

**Output:**
- Creates report files in `../reports/`: `Topgolf_Multi_Venue_Period_*.{html,md,pdf}`

### 6. `create_multi_venue_comparison_report.py`
Generates multi-venue period comparison reports comparing aggregated metrics between two time periods.

**Usage:**
```bash
cd python
python create_multi_venue_comparison_report.py Grand_Prairie 2026-01-01 2026-01-31 2025-12-01 2025-12-31 --format all
python create_multi_venue_comparison_report.py texas_venues 2026-01-01 2026-01-31 2025-12-01 2025-12-31
```

**Output:**
- Creates report files in `../reports/`: `Topgolf_Period_Comparison_*.{html,md,pdf}`

---

### 7. `check_venues.py` (Deprecated)
Utility script to check venues in a CSV file.

### 8. `test_csv.py` (Deprecated)
Utility script to test CSV parsing and display venue information.

## Workflow

**Recommended (Unified Entry Point - All Report Types):**
```bash
python generate_report.py
```
Interactive prompts guide you through all options, or use command-line arguments to skip prompts.

**Advanced (Individual Scripts):**
For single-venue snapshots:
1. Run `generate_venue_data.py "Grand Prairie"` to create `venue_data.json`
2. Run `run_analyze_venues.py venue_data.json` to create `ai_analysis_results.json`
3. Run `create_single_venue_snapshot_report.py venue_data.json --format all --analysis ai_analysis_results.json` to generate reports

For comparisons or multi-venue reports, use the individual `create_*_report.py` scripts directly.

## File Paths

Scripts reference files as follows:
- Input survey data: Loaded by `api.data_loader` from `api/qualtrics/` (managed internally)
- JSON data file: `venue_data.json` (in python folder)
- AI analysis cache: `ai_analysis_results.json` (in python folder)
- Output reports: `../reports/Topgolf_Venue_Report_*.{html,md,pdf}`
