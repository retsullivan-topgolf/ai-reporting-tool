# Unified Report Orchestrator Guide

## Quick Start

The new unified orchestrator (`generate_all_period_reports.py`) provides an interactive menu for generating all types of reports. It automatically discovers available CSV files - no need to specify a path!

### Basic Usage

```bash
cd python
python generate_all_period_reports.py
```

This will:
1. Show available CSV files in `../example-data/`
2. Let you select a CSV file (or enter a custom path)
3. Show a menu to select report type (1-4)
4. Prompt for required parameters (venue, dates, etc.)
5. Ask for output format (HTML, Markdown, PDF, or All)
6. Generate the report(s)
7. Ask if you want to generate another report

### With a Specific CSV File

```bash
cd python
python generate_all_period_reports.py ../example-data/survey.csv
```

Skips the file selection menu and uses the specified file directly.

### Non-Interactive Mode

```bash
cd python
python generate_all_period_reports.py --format all --no-prompt
```

This:
- Auto-selects the first available CSV file
- Skips all prompts
- Generates all report types with all formats

---

## Report Types

### 1. Single-Venue Reports (Existing)
Generate reports for one or all venues in the CSV file.

**What it does:**
- Creates individual reports for selected venue(s)
- Shows performance for a single time period
- Includes AI analysis for each venue
- Compares venue metrics against assessment thresholds
- Lets you choose: all venues or a specific venue

**When to use:**
- You want to see how each venue is performing
- You need detailed analysis for individual venues
- You want to share venue-specific reports
- You want to focus on one venue's performance

**Venue Selection:**
When you select Report Type 1, the script will:
1. List all available venues from the CSV
2. Ask you to choose:
   - A specific venue (by number)
   - All venues (generates one report per venue)

**Example:**
```
Available venues (3):
  1) Grand Prairie
  2) Chicago
  3) Dallas
  4) All venues

Select venue (1-4): 1

Output: Topgolf_Venue_Report_Grand_Prairie_20260115_143022_1PAGE.html
```

**Or for all venues:**
```
Select venue (1-4): 4

Output:
Topgolf_Venue_Report_Grand_Prairie_20260115_143022_1PAGE.html
Topgolf_Venue_Report_Chicago_20260115_143022_1PAGE.html
Topgolf_Venue_Report_Dallas_20260115_143022_1PAGE.html
```

---

### 2. Venue Period Comparison (New)
Compare one venue's metrics between two time periods.

**What it does:**
- Shows metrics for current and previous period side-by-side
- Calculates deltas and percent changes
- Displays trend indicators (↑ ↓ →)
- Includes AI analysis with comparison context
- Uses comments from current period only

**When to use:**
- You want to see if a specific venue is improving or declining
- You need to track trends for a particular venue
- You want to understand what changed month-over-month or quarter-over-quarter

**Example:**
```
Report Type: 2
Venue: Grand Prairie
Current Period: Last month (Jan 1-31, 2026)
Previous Period: Last month (Dec 1-31, 2025)
Format: HTML

Output: Topgolf_Venue_Period_Comparison_Grand_Prairie_20260115_143022_1PAGE.html
```

---

### 3. Multi-Venue Single Period (New)
Aggregate metrics across all venues for one time period.

**What it does:**
- Combines data from all venues in the CSV
- Calculates aggregated metrics (LTR, Fun, Helpful, Issues, Resolution)
- Ranks venues by composite performance score
- Extracts and aggregates comment themes
- Shows which venues are top performers

**When to use:**
- You want to see overall performance across all venues
- You need to identify top and bottom performers
- You want to understand common themes in guest feedback
- You need a snapshot of the entire portfolio for a period

**Composite Score Formula:**
```
Score = (LTR × 0.4) + (Fun × 0.2) + (F&B Avg × 0.2) + (Resolution × 0.2)
```

**Example:**
```
Report Type: 3
Period: Last month (Jan 1-31, 2026)
Format: All (HTML, Markdown, PDF)

Output:
- Topgolf_Multi_Venue_Period_January_2026_20260115_143022_1PAGE.html
- Topgolf_Multi_Venue_Period_January_2026_20260115_143022_1PAGE.md
- Topgolf_Multi_Venue_Period_January_2026_20260115_143022_1PAGE.pdf
```

---

### 4. Multi-Venue Period Comparison (New)
Compare aggregated metrics across all venues between two time periods.

**What it does:**
- Aggregates metrics for current and previous periods
- Shows deltas and percent changes for all metrics
- Identifies ranking changes (which venues moved up/down)
- Displays trend indicators for significant changes
- Compares response counts with warnings for large differences
- Extracts comment themes from current period only

**When to use:**
- You want to see if the overall portfolio is improving or declining
- You need to identify which venues are gaining/losing ground
- You want to understand trends across the entire business
- You need to present period-over-period performance to leadership

**Trend Threshold:**
- ↑ Improvement of 0.5+ points (green)
- ↓ Decline of 0.5+ points (red)
- → Minor change between -0.5 and +0.5 (neutral)

**Example:**
```
Report Type: 4
Current Period: Last month (Jan 1-31, 2026)
Previous Period: Last month (Dec 1-31, 2025)
Format: PDF

Output: Topgolf_Period_Comparison_January_2026_vs_December_2025_20260115_143022_1PAGE.pdf
```

---

## Period Selection

When prompted for a period, you have three options:

### Option 1: Last Month
Automatically calculates the previous calendar month.
- Today: January 15, 2026
- Last month: December 1-31, 2025

### Option 2: Last Quarter
Automatically calculates the previous quarter.
- Today: January 15, 2026 (Q1)
- Last quarter: October 1 - December 31, 2025 (Q4)

### Option 3: Custom Date Range
Enter specific start and end dates.
- Supported formats: YYYY-MM-DD, MM/DD/YYYY, MM/DD/YY
- Example: 2026-01-01 or 01/01/2026

---

## Output Formats

### HTML
- Interactive, styled reports
- Best for viewing in browser
- Includes all formatting and colors
- File: `*_1PAGE.html`

### Markdown
- Plain text format
- Good for documentation and version control
- Can be converted to other formats
- File: `*_1PAGE.md`

### PDF
- Print-ready format
- Professional appearance
- Requires Playwright (one-time setup: `pip install playwright && playwright install chromium`)
- File: `*_1PAGE.pdf`

### All
- Generates all three formats
- Recommended for comprehensive reporting
- Takes longer but provides maximum flexibility

---

## Examples

### Simplest: Just run it!
```bash
cd python
python generate_all_period_reports.py
# Select CSV file from list
# Select report type
# Follow the prompts
```

### Generate single-venue report for a specific venue
```bash
cd python
python generate_all_period_reports.py
# CSV File: 1 (survey.csv) - or select from list
# Report Type: 1 (Single-Venue Reports)
# Venue: 1 (Grand Prairie) - or choose any venue from the list
# Format: 1 (HTML)
```

### Generate single-venue reports for all venues
```bash
cd python
python generate_all_period_reports.py
# CSV File: 1 (survey.csv)
# Report Type: 1 (Single-Venue Reports)
# Venue: 4 (All venues)
# Format: 4 (All formats)
```

### Compare Grand Prairie's performance month-over-month
```bash
cd python
python generate_all_period_reports.py
# CSV File: 1 (survey.csv)
# Report Type: 2 (Venue Period Comparison)
# Venue: Grand Prairie
# Current Period: 1 (Last month)
# Previous Period: 1 (Last month)
# Format: 1 (HTML)
```

### See which venues are top performers this month
```bash
cd python
python generate_all_period_reports.py
# CSV File: 1 (survey.csv)
# Report Type: 3 (Multi-Venue Single Period)
# Period: 1 (Last month)
# Format: 2 (Markdown)
```

### Track portfolio trends quarter-over-quarter
```bash
cd python
python generate_all_period_reports.py
# CSV File: 1 (survey.csv)
# Report Type: 4 (Multi-Venue Period Comparison)
# Current Period: 2 (Last quarter)
# Previous Period: 2 (Last quarter)
# Format: 3 (PDF)
```

### Use a custom CSV file
```bash
cd python
python generate_all_period_reports.py /path/to/custom/data.csv
# Skips file selection, uses your file directly
# Then follow the report type prompts
```

---

## Troubleshooting

### No CSV files appear in the menu
- Make sure you have CSV files in the `../example-data/` directory
- The script looks for `.csv` files (case-insensitive)
- You can still enter a custom path when prompted

### "File not found" error when entering custom path
- Make sure the CSV file path is correct
- Use absolute path or relative path from the `python/` directory
- Example: `../example-data/survey.csv` or `/full/path/to/file.csv`

### "No venues found" error
- The CSV file doesn't have a "Venue" column
- Check that your CSV has the correct column names
- Use `python check_venues.py <csv_file>` to verify

### PDF generation fails
- Install Playwright: `pip install playwright`
- Install Chromium: `playwright install chromium`
- Try HTML format instead if PDF fails

### AI analysis unavailable
- Make sure Claude Code CLI is installed and logged in
- Run `claude --version` to check
- AI analysis is optional; reports still work without it

---

## Tips

1. **The script automatically lists all venues** - You don't need to know venue names; just pick from the list
2. **Start with Report Type 3 or 4** if you want a quick overview of all venues
3. **Use Report Type 1 with a specific venue** to focus on one location's performance
4. **Use Report Type 2** to see how a specific venue is trending over time
5. **Generate all formats** (HTML, Markdown, PDF) for maximum flexibility
6. **Use "Last month" or "Last quarter"** for quick period selection
7. **Check the reports/ directory** for all generated files
8. **Combine reports** - generate single-venue reports AND a multi-venue comparison for complete visibility
9. **Generate multiple reports in one session** - The script loops, so you can generate different report types without restarting

---

## File Locations

All reports are saved to the `reports/` directory with descriptive filenames:

```
reports/
├── Topgolf_Venue_Report_Grand_Prairie_20260115_143022_1PAGE.html
├── Topgolf_Venue_Report_Chicago_20260115_143022_1PAGE.html
├── Topgolf_Venue_Period_Comparison_Grand_Prairie_20260115_143022_1PAGE.html
├── Topgolf_Multi_Venue_Period_January_2026_20260115_143022_1PAGE.html
├── Topgolf_Multi_Venue_Period_January_2026_20260115_143022_1PAGE.md
├── Topgolf_Multi_Venue_Period_January_2026_20260115_143022_1PAGE.pdf
├── Topgolf_Period_Comparison_January_2026_vs_December_2025_20260115_143022_1PAGE.html
└── ...
```

---

## Advanced Usage

### Scripting with non-interactive mode
```bash
#!/bin/bash
cd python

# Generate all report types with all formats
python generate_all_period_reports.py ../example-data/survey.csv --format all --no-prompt

# Generate only HTML reports
python generate_all_period_reports.py ../example-data/survey.csv --format html --no-prompt

# Generate HTML and PDF only
python generate_all_period_reports.py ../example-data/survey.csv --format html,pdf --no-prompt
```

### Batch processing multiple CSV files
```bash
#!/bin/bash
cd python

for csv_file in ../example-data/*.csv; do
  echo "Processing $csv_file..."
  python generate_all_period_reports.py "$csv_file" --format all --no-prompt
done
```

---

## Questions?

Refer to the main `AGENTS.md` file for detailed technical documentation on:
- API functions and their parameters
- Report generation workflows
- AI analysis architecture
- File paths and naming conventions
