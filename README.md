# AI Reporting Tool

Generate professional venue reports from survey data with AI-powered analysis.

## Quick Start

```bash
cd python
python generate_venue_reports.py ../example-data/your_file.csv
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
python generate_venue_reports.py ../example-data/your_file.csv
# Choose format: 1) HTML  2) Markdown  3) PDF  4) All

# Or skip the prompt:
python generate_venue_reports.py ../example-data/your_file.csv --format all
python generate_venue_reports.py ../example-data/your_file.csv --format html,pdf
```

### Step-by-Step Generation

```bash
cd python

# Step 1: Process CSV and generate metrics
python generate_venue_data.py ../example-data/your_file.csv

# Step 2: Run AI analysis (optional but recommended)
python run_analyze_venues.py venue_data.json

# Step 3: Generate reports
python create_single_venue_snapshot_report.py venue_data.json --format all --analysis ai_analysis_results.json
```

## Project Structure

```
ai-reporting-tool/
├── python/                    # All Python scripts
│   ├── generate_venue_reports.py            # Master orchestrator (recommended)
│   ├── generate_period_reports.py           # Period-based reports orchestrator
│   ├── generate_venue_data.py               # CSV → JSON metrics
│   ├── run_analyze_venues.py                # Runs AI analysis pipeline
│   ├── analyze_venues.py                    # AI analysis core module
│   ├── create_single_venue_snapshot_report.py    # Single-venue snapshot reports
│   ├── create_single_venue_comparison_report.py  # Single-venue comparison reports
│   ├── create_multi_venue_snapshot_report.py     # Multi-venue snapshot reports
│   ├── create_multi_venue_comparison_report.py   # Multi-venue comparison reports
│   ├── report_content.py                   # Shared analysis logic
│   ├── report_engine.py                    # Metrics registry and assessment
│   └── requirements.txt
├── templates/                 # Report templates (HTML, Markdown, PDF)
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

- **Venue Overview** - 2-4 sentence narrative summary (avoids redundant metric numbers)
- **Performance Metrics** - Color-coded status indicators with metric cards
- **Ups/Downs Analysis** - 2-3 positive and 2-3 negative findings
- **Impact Drivers** - Top 3 factors ranked by importance
- **Actionable Recommendations** - Data-driven suggestions organized by priority (Critical/Secondary/Maintain)

## Customization

### Tuning Report Output

The AI analysis is guided by modular skill documents in `.claude/single-venue-report/`:

- **venue-overview-skill.md** - Change how the narrative is written
- **ups-downs-skill.md** - Change which findings are selected
- **impact-drivers-skill.md** - Change how impact is explained
- **recommendations-skill.md** - Change the recommendation structure

To customize:

1. Edit the skill file you want to change
2. Clear the analysis cache: `python ai_analysis.py --clear-cache`
3. Regenerate reports: `python generate_ai_analysis.py venue_data.json`

For detailed guidance on each skill, see [`.claude/single-venue-report/README.md`](.claude/single-venue-report/README.md).

### Tuning Metrics Assessment

The Overall Assessment text is rule-based and can be customized:

- Edit `templates/metrics.json` to change metric thresholds and weak_explanation text
- The Overall Assessment automatically acknowledges any WEAK metrics
- See `python/report_content.py` for the implementation

## Documentation

For detailed information:

- **[AGENTS.md](AGENTS.md)** - Project structure, workflow, and architecture
- **[.claude/single-venue-report/README.md](.claude/single-venue-report/README.md)** - AI analysis pipeline and skill guides
- **[.claude/single-venue-report/overview-metrics-guidance.md](.claude/single-venue-report/overview-metrics-guidance.md)** - Detailed guidance on metrics handling in the overview

## Requirements

- Python 3.8+
- Node.js (for Claude CLI)
- Claude CLI installed and authenticated (`claude login`)
- Dependencies listed in `python/requirements.txt`
- Playwright (for PDF generation)
- Anthropic API key (for AI analysis)

## For Developers

### Architecture Overview

The report generation pipeline has two main components:

1. **Data Processing (Python)**
   - `generate_reports.py` - CSV → JSON metrics
   - `generate_ai_analysis.py` - Orchestrates AI analysis
   - `create_html_reports.py`, `create_markdown_reports.py`, `create_pdf_reports.py` - Format generation

2. **AI Analysis (Claude CLI)**
   - 3-stage pipeline in `.claude/single-venue-report/`
   - Stage 1: Analyze metrics → characterization + flags
   - Stage 2: Analyze comments → themes with magnitude
   - Stage 3: Synthesize findings → overview/ups/downs/impact/recommendations

### Key Files

**Python Scripts:**
- `python/ai_analysis.py` - Implements the 3-stage pipeline
- `python/report_content.py` - Shared analysis logic
- `python/report_engine.py` - Metric assessment logic

**AI Prompts:**
- `.claude/single-venue-report/metrics_analysis.md` - Stage 1
- `.claude/single-venue-report/comment_analysis.md` - Stage 2
- `.claude/single-venue-report/synthesis.md` - Stage 3

**Skill Guides:**
- `.claude/single-venue-report/venue-overview-skill.md`
- `.claude/single-venue-report/ups-downs-skill.md`
- `.claude/single-venue-report/impact-drivers-skill.md`
- `.claude/single-venue-report/recommendations-skill.md`

### Caching Strategy

Each AI analysis stage is cached independently:

```
Cache key = hash(stage_prompt + input_payload)
```

This means:
- Re-running with same data is instant (cache hit)
- Editing a prompt invalidates only that stage's cache
- New data automatically invalidates affected caches

Clear cache with: `python ai_analysis.py --clear-cache`

### Adding New Metrics

To add a new metric to the analysis:

1. **Add to CSV parsing** in `python/generate_reports.py`
2. **Add to metrics.json** in `templates/metrics.json` with thresholds
3. **Update metrics_analysis.md** to include the new metric
4. **Clear cache** and regenerate

### Modifying the Synthesis Pipeline

To change how the final report is generated:

1. **Edit the skill file** in `.claude/single-venue-report/`
   - `venue-overview-skill.md` - Change overview writing
   - `ups-downs-skill.md` - Change findings selection
   - `impact-drivers-skill.md` - Change impact explanation
   - `recommendations-skill.md` - Change recommendations

2. **Or edit synthesis.md** if changing the overall structure

3. **Update validation** in `python/ai_analysis.py` if output schema changes

4. **Clear cache** and test: `python generate_ai_analysis.py venue_data.json`

### Performance Notes

- **3 API calls per venue** (one per stage)
- **Caching**: Subsequent runs with same data are instant
- **Timeout**: 600 seconds per stage
- **Batch processing**: Sequential (can be parallelized if needed)

For large batches, run `generate_ai_analysis.py` once to cache all results, then reuse across multiple report formats.

### Debugging

**Check Claude CLI status:**
```bash
claude auth status
```

**View cached analysis:**
```bash
cat python/ai_analysis_results.json | jq '.["venue_name"]'
```

**Clear cache and re-run:**
```bash
python ai_analysis.py --clear-cache
python generate_ai_analysis.py venue_data.json
```

**Check for errors:**
- Look for `"ai_available": false` in results
- Check `unavailable_reason` field for details
- Verify Claude CLI is authenticated

## License

See LICENSE file for details.
