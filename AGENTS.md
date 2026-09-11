# Project Structure & Workflow

## Python Scripts Location
All Python scripts have been moved to the `python/` directory for better organization.

### Scripts in `python/` folder:
- **generate_all_reports.py** - Master script: runs both steps below in one command (recommended). After processing the CSV, it asks which report format(s) to generate - HTML, Markdown, PDF, or All - or takes `--format` to skip the prompt.
- **generate_reports.py** - Processes CSV survey data → generates JSON metrics
- **create_html_reports.py** - Generates HTML reports from JSON data
- **create_markdown_reports.py** - Generates Markdown reports from JSON data (same analysis as the HTML report - see `report_content.py`)
- **create_pdf_reports.py** - Generates PDF reports from JSON data by rendering the same HTML through headless Chromium (Playwright), so the PDF matches the HTML report's styling/layout exactly. One-time setup: `pip install playwright` then `playwright install chromium`.
- **report_content.py** - Shared, format-agnostic analysis/context logic used by `create_html_reports.py`, `create_markdown_reports.py`, and `create_pdf_reports.py`
- **check_venues.py** - Utility to check venues in CSV files
- **test_csv.py** - Utility to test CSV parsing

### Running Scripts

**Recommended (single command):**
```bash
cd python
python generate_all_reports.py ../example-data/your_file.csv
# You'll be prompted: 1) HTML  2) Markdown  3) PDF  4) All
# Or skip the prompt:
python generate_all_reports.py ../example-data/your_file.csv --format all
python generate_all_reports.py ../example-data/your_file.csv --format html,pdf
```

**Or run individually:**
```bash
cd python
python generate_reports.py ../example-data/your_file.csv
python create_html_reports.py venue_data.json
python create_markdown_reports.py venue_data.json
python create_pdf_reports.py venue_data.json
```

### File Paths
- Input CSVs: `../example-data/` (parent directory)
- JSON data: `venue_data.json` (python folder)
- Output HTML: `../reports/Topgolf_Venue_Report_*_1PAGE.html`
- Output Markdown: `../reports/Topgolf_Venue_Report_*_1PAGE.md`
- Output PDF: `../reports/Topgolf_Venue_Report_*_1PAGE.pdf`

## Report Generation Workflow

**Quick way (recommended):**
```bash
cd python
python generate_all_reports.py ../example-data/your_file.csv
```
You'll be prompted to choose HTML, Markdown, PDF, or All. Pass `--format` (or `-f`) to choose non-interactively - useful for scripting - with any of: `html`, `markdown`, `pdf`, `both` (html+markdown, legacy alias), `all` (all three), or a comma-separated combo like `html,pdf`. A non-interactive session (piped input, no real terminal) skips the prompt and defaults to all three automatically.

**Manual steps:**
1. Place CSV survey file in `example-data/` folder
2. Run `python/generate_reports.py <csv_file>` to create `python/venue_data.json`
3. Run any of `python/create_html_reports.py venue_data.json`, `python/create_markdown_reports.py venue_data.json`, `python/create_pdf_reports.py venue_data.json` to generate reports in `reports/`

## Report Features
- Color-coded status pills in Experience Metrics table
- Performance summary with metric cards
- Venue overview narrative
- Ups/Downs analysis
- Impact drivers ranking
- Actionable recommendations

## Key Files
- `templates/venue-1page-browser.html` - HTML template for reports
- `templates/venue-1page-pdf.html` - separate template used only for the PDF (different section order/content by request - see its docstring comment)
- `templates/venue-1page-report.md.j2` - Markdown template for reports
- `python/` - All Python processing scripts
- `example-data/` - Sample CSV survey data
- Generated reports appear in `reports/` as `Topgolf_Venue_Report_*_1PAGE.html`, `.md`, and/or `.pdf`

---

## IMPORTANT: Analysis Generation Architecture

### Current Issue
The `create_html_reports.py` script uses **hardcoded logic** to generate:
- Venue Overview narrative
- Ups/Downs drivers
- Impact drivers ranking
- Recommendations

This approach **DOES NOT WORK** because:
1. It only looks at aggregate metrics (LTR, Fun, Helpfulness, Issues %, Resolution)
2. It completely ignores the actual guest comments from Q6_COMMENT field
3. New themes in comments (like parking issues, new game excitement) are never detected
4. Analysis is generic and not specific to actual guest feedback

### Solution Required
**Use an AI/LLM analysis tool to generate summaries** that:
1. Analyzes the actual guest comments from the CSV
2. Identifies themes and patterns in the comments
3. Generates dynamic Ups/Downs/Impact/Recommendations based on real feedback
4. Can mention specific issues like "parking" or "Sonic game" when they appear in comments
5. Balances comment-based insights with metric-based insights

### Implementation Notes
- It's OK to use metrics as a foundation (e.g., "51.7% reported issues")
- But the narrative, drivers, and recommendations MUST be informed by actual comment analysis
- An LLM/AI tool should analyze comments and generate the text for these sections
- Simple keyword matching (like the `analyze_comments()` function) is insufficient
- Need proper NLP/AI to understand context and generate coherent analysis

### Files to Update
- `python/create_html_reports.py` - Replace hardcoded generation functions with AI-based analysis
- Consider adding a new analysis step that calls an LLM API (Claude, GPT, etc.) for comment analysis
- The LLM should receive: venue name, metrics, and all guest comments, then generate analysis text
