# AI Reporting Tool

Generate professional venue reports from survey data with AI-powered analysis.

## Quick Start

```bash
cd python
python generate_all_reports.py ../example-data/your_file.csv
```

Choose your report format(s): HTML, Markdown, PDF, or All. Reports are generated in the `reports/` directory.

## Features

- **Multi-format reports** - Generate HTML, Markdown, and PDF reports from a single CSV file
- **AI-powered analysis** - 3-stage analysis pipeline (metrics → comments → synthesis) using Claude
- **Performance metrics** - Color-coded status indicators and metric cards
- **Actionable insights** - Ups/downs analysis, impact drivers, and recommendations
- **Efficient processing** - AI analysis runs once and is reused across all report formats

## Installation

1. Ensure Python 3.8+ is installed
2. Install dependencies:
   ```bash
   pip install -r python/requirements.txt
   ```
3. Install and authenticate the Claude CLI:
   ```bash
   # Install Claude CLI (if not already installed)
   npm install -g @anthropic-ai/claude-cli
   
   # Authenticate with your Anthropic API key
   claude login
   ```
4. For PDF support, install Playwright:
   ```bash
   pip install playwright
   playwright install chromium
   ```

## Usage

### One-Command Generation (Recommended)

```bash
cd python
python generate_all_reports.py ../example-data/your_file.csv
# Choose format: 1) HTML  2) Markdown  3) PDF  4) All

# Or skip the prompt:
python generate_all_reports.py ../example-data/your_file.csv --format all
python generate_all_reports.py ../example-data/your_file.csv --format html,pdf
```

### Step-by-Step Generation

```bash
cd python

# Step 1: Process CSV and generate metrics
python generate_reports.py ../example-data/your_file.csv

# Step 2: Run AI analysis (optional but recommended)
python generate_ai_analysis.py venue_data.json

# Step 3: Generate reports
python create_html_reports.py venue_data.json --analysis ai_analysis_results.json
python create_markdown_reports.py venue_data.json --analysis ai_analysis_results.json
python create_pdf_reports.py venue_data.json --analysis ai_analysis_results.json
```

## Project Structure

```
ai-reporting-tool/
├── python/                    # All Python scripts
│   ├── generate_all_reports.py       # Master orchestrator (recommended)
│   ├── generate_reports.py           # CSV → JSON metrics
│   ├── generate_ai_analysis.py       # Runs AI analysis pipeline
│   ├── create_html_reports.py        # Generate HTML reports
│   ├── create_markdown_reports.py    # Generate Markdown reports
│   ├── create_pdf_reports.py         # Generate PDF reports
│   ├── report_content.py             # Shared analysis logic
│   ├── ai_analysis.py                # AI analysis pipeline
│   └── requirements.txt
├── templates/                 # Report templates (HTML, Markdown)
├── example-data/              # Sample CSV files
├── reports/                   # Generated reports (output)
└── AGENTS.md                  # Detailed workflow documentation
```

## File Paths

- **Input**: CSV files in `example-data/`
- **Intermediate**: `python/venue_data.json` (metrics), `python/ai_analysis_results.json` (AI analysis)
- **Output**: Reports in `reports/` as `Topgolf_Venue_Report_*_YYYYMMDD_HHMMSS_1PAGE.{html,md,pdf}`

## Report Contents

Each report includes:

- **Venue Overview** - Summary narrative
- **Performance Metrics** - Color-coded status indicators
- **Ups/Downs Analysis** - Key improvements and concerns
- **Impact Drivers** - Ranked factors affecting performance
- **Actionable Recommendations** - Data-driven suggestions

## Configuration

For detailed workflow documentation and advanced options, see [AGENTS.md](AGENTS.md).

## Requirements

- Python 3.8+
- Node.js (for Claude CLI)
- Claude CLI installed and authenticated (`claude login`)
- Dependencies listed in `python/requirements.txt`
- Playwright (for PDF generation)
- Anthropic API key (for AI analysis)

## License

See LICENSE file for details.
