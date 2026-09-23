#!/usr/bin/env python3
"""
Generate a multi-venue single period report aggregating metrics across all venues
for a given time period and ranking them by composite performance score.

This report shows:
- Aggregated metrics across all venues
- Venue ranking by composite score (Combined NPS)
- Comment themes aggregated from current period
- Period-level AI analysis synthesizing insights across venues

Usage:
    python create_multi_venue_report.py <data_identifier> <start_date> <end_date> [--format html|markdown|pdf|all]

Example:
    python create_multi_venue_report.py Grand_Prairie 2026-01-01 2026-01-31
    python create_multi_venue_report.py texas_venues 2026-01-01 2026-01-31
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from collections import Counter

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import csv_parser, venue_processor, data_loader
import report_engine
import report_content
import analyze_venues
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
    
    data_identifier = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    
    # Optional format argument
    report_format = 'all'
    if len(sys.argv) > 4:
        if sys.argv[4] == '--format':
            report_format = sys.argv[5] if len(sys.argv) > 5 else 'all'
    
    print(f"Processing multi-venue period report...")
    print(f"  Data: {data_identifier}")
    print(f"  Period: {start_date} to {end_date}")
    
    # Load survey data
    try:
        # Determine if data_identifier is a dataset name or venue name
        # If it's a known dataset, use it; otherwise treat as venue name
        available_datasets = data_loader.list_available_datasets()
        if data_identifier in available_datasets:
            # Use the specified dataset
            rows, fieldnames = data_loader.load_survey_data(dataset=data_identifier)
        else:
            # Assume it's a venue name, load from texas_venues
            rows, fieldnames = data_loader.load_survey_data(venue=data_identifier)
        
        schema_type = csv_parser.detect_schema(fieldnames)
        print(f"  Schema detected: {schema_type}")
    except data_loader.DataLoaderError as e:
        print(f"Error loading data: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing data: {e}")
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
    print(f"  Aggregated NPS: {period_summary['metrics_avg'].get('nps_avg', 'N/A')}")
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
    
    # Run multi-venue AI analysis
    print(f"  Running multi-venue AI analysis...")
    aggregated_data = {
        'venues': [{
            'venue': venue_data['venue'],
            'responses': venue_data['responses'],
            'metrics': {k: v for k, v in venue_data.items() if k not in ['venue', 'responses', 'comments']},
            'comments': venue_data.get('comments', [])
        } for venue_data in venue_data_list]
    }

    ai_result, error = analyze_venues.get_aggregated_ai_analysis(aggregated_data)
    if ai_result is not None:
        print(f"  [OK] AI analysis completed")
        report_data['analysis'] = report_content._format_analysis_as_html(ai_result)
        report_data['analysis']['ai_available'] = True
    else:
        print(f"  [WARNING] AI analysis unavailable: {error}")
        report_data['analysis'] = {
            'ai_available': False,
            'unavailable_reason': error or 'Unknown error'
        }
    
    # Load Jinja2 environment
    TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
    jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=False)

    # Register strftime filter for date formatting in templates
    def strftime_filter(value, format_str):
        if isinstance(value, str) and value.lower() == 'now':
            return datetime.now().strftime(format_str)
        elif isinstance(value, datetime):
            return value.strftime(format_str)
        return str(value)

    jinja_env.filters['strftime'] = strftime_filter
    
    # Generate reports
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    period_safe = period_summary['period'].replace(' ', '_').replace('/', '_')
    
    # HTML report
    if report_format in ['html', 'all']:
        try:
            template = jinja_env.get_template('multi-venue-snapshot-browser.html')
            html = template.render(**report_data)
            html_file = os.path.join(reports_dir, f"Topgolf_Multi_Venue_Period_{period_safe}_{timestamp}.html")
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"[OK] HTML report: {html_file}")
        except Exception as e:
            print(f"[ERROR] HTML report failed: {e}")
    
    # Markdown report
    if report_format in ['markdown', 'all']:
        try:
            template = jinja_env.get_template('multi-venue-snapshot-report.md.j2')
            markdown = template.render(**report_data)
            md_file = os.path.join(reports_dir, f"Topgolf_Multi_Venue_Period_{period_safe}_{timestamp}.md")
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"[OK] Markdown report: {md_file}")
        except Exception as e:
            print(f"[ERROR] Markdown report failed: {e}")
    
    # PDF report
    if report_format in ['pdf', 'all']:
        try:
            from playwright.sync_api import sync_playwright
            
            template = jinja_env.get_template('multi-venue-snapshot-pdf.html')
            html = template.render(**report_data)
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                # Force print CSS and ensure background colors/gradients render
                page.emulate_media(media="print")
                # Wait for content to fully load before rendering PDF
                page.set_content(html, wait_until="load")
                pdf_file = os.path.join(reports_dir, f"Topgolf_Multi_Venue_Period_{period_safe}_{timestamp}.pdf")
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
