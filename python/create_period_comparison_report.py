#!/usr/bin/env python3
"""
Generate a multi-venue period comparison report comparing aggregated metrics
across two time periods (current vs. previous month/quarter).

This report shows:
- Aggregated metrics for both periods with deltas and percent changes
- Venue ranking comparison with ranking changes
- Trend indicators for significant changes (±0.5 threshold)
- Response count comparison with warnings for ±20% differences
- Comment themes from current period only
- Period-level AI analysis with comparison context

Usage:
    python create_period_comparison_report.py <csv_file> <current_start> <current_end> <previous_start> <previous_end> [--format html|markdown|pdf|all]

Example:
    python create_period_comparison_report.py ../example-data/survey.csv 2026-01-01 2026-01-31 2025-12-01 2025-12-31
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import csv_parser, venue_processor
import report_engine
import report_content
from jinja2 import Environment, FileSystemLoader


def filter_rows_by_date_range(rows, start_date, end_date):
    """Filter CSV rows to those within the date range (inclusive).
    
    Args:
        rows: List of CSV rows
        start_date: Start date as string (YYYY-MM-DD)
        end_date: End date as string (YYYY-MM-DD)
        
    Returns:
        List of filtered rows
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError as e:
        raise ValueError(f"Invalid date format. Expected YYYY-MM-DD: {e}")
    
    filtered = []
    for row in rows:
        row_date_str = row.get('Visit Date (+00:00 GMT)') or row.get('Visit Date') or row.get('VisitDate') or ''
        if not row_date_str:
            continue

        try:
            # Try common date formats
            for fmt in ['%m/%d/%Y', '%Y-%m-%d', '%m/%d/%y']:
                try:
                    row_date = datetime.strptime(row_date_str.split(' ')[0], fmt).date()
                    if start <= row_date <= end:
                        filtered.append(row)
                    break
                except ValueError:
                    continue
        except:
            continue

    return filtered


def extract_comment_themes(venue_data_list, max_themes=10):
    """Extract and aggregate comment themes from all venues.
    
    Args:
        venue_data_list: List of processed venue data dicts
        max_themes: Maximum number of themes to extract
        
    Returns:
        List of (theme, count, venues) tuples sorted by frequency
    """
    # Collect all comments with venue attribution
    all_comments = []
    for venue_data in venue_data_list:
        venue_name = venue_data.get('venue', 'Unknown')
        for comment_obj in venue_data.get('comments', []):
            if isinstance(comment_obj, dict):
                text = comment_obj.get('text', '')
            else:
                text = str(comment_obj)
            
            if text:
                all_comments.append({
                    'text': text,
                    'venue': venue_name
                })
    
    # For now, return raw comments grouped by venue
    # In a full implementation, this would use NLP to extract themes
    theme_map = {}
    for comment in all_comments:
        # Simple theme extraction: use first 50 chars as theme
        theme = comment['text'][:50].strip()
        if theme not in theme_map:
            theme_map[theme] = {'count': 0, 'venues': set()}
        theme_map[theme]['count'] += 1
        theme_map[theme]['venues'].add(comment['venue'])
    
    # Sort by frequency and return top N
    sorted_themes = sorted(
        [(theme, data['count'], list(data['venues'])) for theme, data in theme_map.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    return sorted_themes[:max_themes]


def get_trend_indicator(delta):
    """Get trend indicator based on delta value (±0.5 threshold).
    
    Args:
        delta: Metric delta (float or None)
        
    Returns:
        Tuple of (indicator, css_class) where:
        - indicator: '↑', '↓', or '→'
        - css_class: 'up', 'down', or 'neutral'
    """
    if delta is None:
        return '—', 'unavailable'
    
    if delta >= 0.5:
        return '↑', 'up'
    elif delta <= -0.5:
        return '↓', 'down'
    else:
        return '→', 'neutral'


def main():
    """Main entry point."""
    # Parse arguments
    if len(sys.argv) < 6:
        print(__doc__)
        sys.exit(1)
    
    csv_file = sys.argv[1]
    current_start = sys.argv[2]
    current_end = sys.argv[3]
    previous_start = sys.argv[4]
    previous_end = sys.argv[5]
    
    # Optional format argument
    report_format = 'all'
    if len(sys.argv) > 6:
        if sys.argv[6] == '--format':
            report_format = sys.argv[7] if len(sys.argv) > 7 else 'all'
    
    # Validate CSV file
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found: {csv_file}")
        sys.exit(1)
    
    print(f"Processing multi-venue period comparison report...")
    print(f"  Current period: {current_start} to {current_end}")
    print(f"  Previous period: {previous_start} to {previous_end}")
    
    # Parse CSV
    try:
        rows, fieldnames = csv_parser.parse_csv(csv_file)
        schema_type = csv_parser.detect_schema(fieldnames)
        print(f"  Schema detected: {schema_type}")
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        sys.exit(1)
    
    # Filter by date ranges
    current_rows = filter_rows_by_date_range(rows, current_start, current_end)
    previous_rows = filter_rows_by_date_range(rows, previous_start, previous_end)
    
    if not current_rows:
        print(f"Error: No data found for current period ({current_start} to {current_end})")
        sys.exit(1)
    
    if not previous_rows:
        print(f"Warning: No data found for previous period ({previous_start} to {previous_end})")
    
    print(f"  Current period responses: {len(current_rows)}")
    print(f"  Previous period responses: {len(previous_rows)}")
    
    # Calculate period summaries
    current_summary = venue_processor.calculate_period_summary(current_rows, schema_type, current_start, current_end)
    previous_summary = venue_processor.calculate_period_summary(previous_rows, schema_type, previous_start, previous_end) if previous_rows else None
    
    if current_summary['venues_count'] == 0:
        print(f"Error: No venues found in current period data")
        sys.exit(1)
    
    print(f"  Current venues: {current_summary['venues_count']}")
    if previous_summary:
        print(f"  Previous venues: {previous_summary['venues_count']}")
    
    # Compare periods
    comparison = venue_processor.compare_periods(current_summary, previous_summary) if previous_summary else {}
    
    # Extract comment themes from current period only
    current_venue_data_list = [
        venue_processor.process_venue_data(
            [r for r in current_rows if r.get('Venue', '').strip() == venue['venue']],
            schema_type
        )
        for venue in current_summary['venues_ranked']
    ]
    
    comment_themes = extract_comment_themes(current_venue_data_list)
    
    # Build report data
    report_data = {
        'current_period': current_summary['period'],
        'current_period_type': current_summary['period_type'],
        'current_date_range': current_summary['date_range'],
        'current_total_responses': current_summary['total_responses'],
        'current_venues_count': current_summary['venues_count'],
        'current_metrics_avg': current_summary['metrics_avg'],
        'current_venues_ranked': current_summary['venues_ranked'],
        'previous_period': previous_summary['period'] if previous_summary else None,
        'previous_period_type': previous_summary['period_type'] if previous_summary else None,
        'previous_date_range': previous_summary['date_range'] if previous_summary else None,
        'previous_total_responses': previous_summary['total_responses'] if previous_summary else None,
        'previous_venues_count': previous_summary['venues_count'] if previous_summary else None,
        'previous_metrics_avg': previous_summary['metrics_avg'] if previous_summary else None,
        'previous_venues_ranked': previous_summary['venues_ranked'] if previous_summary else None,
        'comparison': comparison,
        'comment_themes': comment_themes,
        'metrics_registry': report_engine.load_metrics_registry()
    }
    
    # TODO: Add period-level AI analysis when implemented
    # For now, mark as unavailable
    report_data['analysis'] = {
        'ai_available': False,
        'unavailable_reason': 'Period-level AI analysis not yet implemented'
    }
    
    # Load Jinja2 environment
    TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
    jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=False)
    
    # Generate reports
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    period_safe = f"{current_summary['period']}_vs_{previous_summary['period'] if previous_summary else 'baseline'}".replace(' ', '_').replace('/', '_')
    
    # HTML report
    if report_format in ['html', 'all']:
        try:
            template = jinja_env.get_template('period-comparison-browser.html')
            html = template.render(**report_data)
            html_file = os.path.join(reports_dir, f"Topgolf_Period_Comparison_{period_safe}_{timestamp}_1PAGE.html")
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"[OK] HTML report: {html_file}")
        except Exception as e:
            print(f"[ERROR] HTML report failed: {e}")
    
    # Markdown report
    if report_format in ['markdown', 'all']:
        try:
            template = jinja_env.get_template('period-comparison-report.md.j2')
            markdown = template.render(**report_data)
            md_file = os.path.join(reports_dir, f"Topgolf_Period_Comparison_{period_safe}_{timestamp}_1PAGE.md")
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"[OK] Markdown report: {md_file}")
        except Exception as e:
            print(f"[ERROR] Markdown report failed: {e}")
    
    # PDF report
    if report_format in ['pdf', 'all']:
        try:
            from playwright.sync_api import sync_playwright
            
            template = jinja_env.get_template('period-comparison-pdf.html')
            html = template.render(**report_data)
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                # Force print CSS and ensure background colors/gradients render
                page.emulate_media(media="print")
                # Wait for content to fully load before rendering PDF
                page.set_content(html, wait_until="load")
                pdf_file = os.path.join(reports_dir, f"Topgolf_Period_Comparison_{period_safe}_{timestamp}_1PAGE.pdf")
                page.pdf(
                    path=pdf_file,
                    format="Letter",
                    print_background=True,
                    margin={"top": "0.4in", "bottom": "0.4in", "left": "0.4in", "right": "0.4in"},
                )
                page.close()
                browser.close()
            print(f"[OK] PDF report: {pdf_file}")
        except ImportError:
            print(f"[ERROR] PDF report skipped: playwright not installed. Run: pip install playwright && playwright install chromium")
        except Exception as e:
            print(f"[ERROR] PDF report failed: {e}")
    
    print(f"\nReport generation complete!")


if __name__ == '__main__':
    main()
