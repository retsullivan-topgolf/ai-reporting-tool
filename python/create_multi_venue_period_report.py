#!/usr/bin/env python3
"""
Generate a multi-venue single period report aggregating metrics across all venues
for a given time period and ranking them by composite performance score.

This report shows:
- Aggregated metrics across all venues
- Venue ranking by composite score (LTR + Fun + F&B avg + Issue Resolution)
- Comment themes aggregated from current period
- Period-level AI analysis synthesizing insights across venues

Usage:
    python create_multi_venue_period_report.py <csv_file> <start_date> <end_date> [--format html|markdown|pdf|all]

Example:
    python create_multi_venue_period_report.py ../example-data/survey.csv 2026-01-01 2026-01-31
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from collections import Counter

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


def main():
    """Main entry point."""
    # Parse arguments
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    
    csv_file = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    
    # Optional format argument
    report_format = 'all'
    if len(sys.argv) > 4:
        if sys.argv[4] == '--format':
            report_format = sys.argv[5] if len(sys.argv) > 5 else 'all'
    
    # Validate CSV file
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found: {csv_file}")
        sys.exit(1)
    
    print(f"Processing multi-venue period report...")
    print(f"  Period: {start_date} to {end_date}")
    
    # Parse CSV
    try:
        rows, fieldnames = csv_parser.parse_csv(csv_file)
        schema_type = csv_parser.detect_schema(fieldnames)
        print(f"  Schema detected: {schema_type}")
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        sys.exit(1)
    
    # Filter by date range
    period_rows = filter_rows_by_date_range(rows, start_date, end_date)
    
    if not period_rows:
        print(f"Error: No data found for period ({start_date} to {end_date})")
        sys.exit(1)
    
    print(f"  Total responses in period: {len(period_rows)}")
    
    # Calculate period summary (aggregates across all venues)
    period_summary = venue_processor.calculate_period_summary(period_rows, schema_type, start_date, end_date)
    
    if period_summary['venues_count'] == 0:
        print(f"Error: No venues found in period data")
        sys.exit(1)
    
    print(f"  Venues: {period_summary['venues_count']}")
    print(f"  Aggregated LTR: {period_summary['metrics_avg'].get('ltr_avg', 'N/A')}")
    
    # Extract comment themes
    venue_data_list = [
        venue_processor.process_venue_data(
            [r for r in period_rows if r.get('Venue', '').strip() == venue['venue']],
            schema_type
        )
        for venue in period_summary['venues_ranked']
    ]
    
    comment_themes = extract_comment_themes(venue_data_list)
    
    # Build report data
    report_data = {
        'period': period_summary['period'],
        'period_type': period_summary['period_type'],
        'date_range': period_summary['date_range'],
        'total_responses': period_summary['total_responses'],
        'venues_count': period_summary['venues_count'],
        'metrics_avg': period_summary['metrics_avg'],
        'venues_ranked': period_summary['venues_ranked'],
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
    period_safe = period_summary['period'].replace(' ', '_').replace('/', '_')
    
    # HTML report
    if report_format in ['html', 'all']:
        try:
            template = jinja_env.get_template('multi-venue-period-browser.html')
            html = template.render(**report_data)
            html_file = os.path.join(reports_dir, f"Topgolf_Multi_Venue_Period_{period_safe}_{timestamp}_1PAGE.html")
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"[OK] HTML report: {html_file}")
        except Exception as e:
            print(f"[ERROR] HTML report failed: {e}")
    
    # Markdown report
    if report_format in ['markdown', 'all']:
        try:
            template = jinja_env.get_template('multi-venue-period-report.md.j2')
            markdown = template.render(**report_data)
            md_file = os.path.join(reports_dir, f"Topgolf_Multi_Venue_Period_{period_safe}_{timestamp}_1PAGE.md")
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"[OK] Markdown report: {md_file}")
        except Exception as e:
            print(f"[ERROR] Markdown report failed: {e}")
    
    # PDF report
    if report_format in ['pdf', 'all']:
        try:
            from playwright.async_api import async_playwright
            import asyncio
            
            template = jinja_env.get_template('multi-venue-period-pdf.html')
            html = template.render(**report_data)
            
            async def generate_pdf():
                async with async_playwright() as p:
                    browser = await p.chromium.launch()
                    page = await browser.new_page()
                    await page.set_content(html)
                    pdf_file = os.path.join(reports_dir, f"Topgolf_Multi_Venue_Period_{period_safe}_{timestamp}_1PAGE.pdf")
                    await page.pdf(path=pdf_file)
                    await browser.close()
                    return pdf_file
            
            pdf_file = asyncio.run(generate_pdf())
            print(f"[OK] PDF report: {pdf_file}")
        except ImportError:
            print(f"[ERROR] PDF report skipped: playwright not installed. Run: pip install playwright && playwright install chromium")
        except Exception as e:
            print(f"[ERROR] PDF report failed: {e}")
    
    print(f"\nReport generation complete!")


if __name__ == '__main__':
    main()
