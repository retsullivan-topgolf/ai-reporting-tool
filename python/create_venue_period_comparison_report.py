#!/usr/bin/env python3
"""
Generate a venue period comparison report comparing a single venue's performance
between two time periods (current vs. previous month/quarter).

This report shows:
- Metrics for both periods (current | previous | change | % change | trend)
- Trend indicators (↑ for improvement, ↓ for decline, → for minor changes)
- AI analysis with comparison context
- Comments from current period only

Usage:
    python create_venue_period_comparison_report.py <csv_file> <venue_name> <current_start> <current_end> <previous_start> <previous_end> [--format html|markdown|pdf|all]

Example:
    python create_venue_period_comparison_report.py ../example-data/survey.csv "Grand Prairie" 2026-01-01 2026-01-31 2025-12-01 2025-12-31
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


def calculate_metric_delta(current_val, previous_val):
    """Calculate delta and percent change between two metric values.
    
    Args:
        current_val: Current period value (float or None)
        previous_val: Previous period value (float or None)
        
    Returns:
        Tuple of (delta, percent_change) or (None, None) if values unavailable
    """
    if current_val is None or previous_val is None:
        return None, None
    
    delta = round(current_val - previous_val, 2)
    
    if previous_val != 0:
        pct_change = round((delta / abs(previous_val)) * 100, 1)
    else:
        pct_change = None
    
    return delta, pct_change


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


def build_comparison_data(current_venue_data, previous_venue_data):
    """Build comparison data structure with deltas and trend indicators.
    
    Args:
        current_venue_data: Current period venue metrics dict
        previous_venue_data: Previous period venue metrics dict (or None)
        
    Returns:
        Dict with comparison metrics and trend indicators
    """
    if not previous_venue_data:
        # No previous data available
        return {
            'current': current_venue_data,
            'previous': None,
            'metrics_comparison': {
                'ltr': {
                    'current': current_venue_data.get('ltr_avg'),
                    'previous': None,
                    'delta': None,
                    'percent_change': None,
                    'trend': '—',
                    'trend_class': 'unavailable'
                },
                'fun': {
                    'current': current_venue_data.get('fun_avg'),
                    'previous': None,
                    'delta': None,
                    'percent_change': None,
                    'trend': '—',
                    'trend_class': 'unavailable'
                },
                'helpful': {
                    'current': current_venue_data.get('helpful_avg'),
                    'previous': None,
                    'delta': None,
                    'percent_change': None,
                    'trend': '—',
                    'trend_class': 'unavailable'
                },
                'issues': {
                    'current': current_venue_data.get('issues_pct'),
                    'previous': None,
                    'delta': None,
                    'percent_change': None,
                    'trend': '—',
                    'trend_class': 'unavailable'
                },
                'resolution': {
                    'current': current_venue_data.get('resolution_avg'),
                    'previous': None,
                    'delta': None,
                    'percent_change': None,
                    'trend': '—',
                    'trend_class': 'unavailable'
                }
            }
        }
    
    # Build comparison with previous data
    comparison = {
        'current': current_venue_data,
        'previous': previous_venue_data,
        'metrics_comparison': {}
    }
    
    # Compare each metric
    metrics_to_compare = [
        ('ltr', 'ltr_avg'),
        ('fun', 'fun_avg'),
        ('helpful', 'helpful_avg'),
        ('issues', 'issues_pct'),
        ('resolution', 'resolution_avg')
    ]
    
    for metric_key, data_key in metrics_to_compare:
        current_val = current_venue_data.get(data_key)
        previous_val = previous_venue_data.get(data_key)
        
        delta, pct_change = calculate_metric_delta(current_val, previous_val)
        trend, trend_class = get_trend_indicator(delta)
        
        comparison['metrics_comparison'][metric_key] = {
            'current': current_val,
            'previous': previous_val,
            'delta': delta,
            'percent_change': pct_change,
            'trend': trend,
            'trend_class': trend_class
        }
    
    # Add F&B metrics if available (real schema)
    fb_metrics = [
        ('food_value', 'food_value_avg'),
        ('food_speed', 'food_speed_avg'),
        ('food_quality', 'food_quality_avg'),
        ('beverage_value', 'beverage_value_avg'),
        ('beverage_speed', 'beverage_speed_avg'),
        ('beverage_quality', 'beverage_quality_avg')
    ]
    
    for metric_key, data_key in fb_metrics:
        current_val = current_venue_data.get(data_key)
        previous_val = previous_venue_data.get(data_key)
        
        if current_val is not None or previous_val is not None:
            delta, pct_change = calculate_metric_delta(current_val, previous_val)
            trend, trend_class = get_trend_indicator(delta)
            
            comparison['metrics_comparison'][metric_key] = {
                'current': current_val,
                'previous': previous_val,
                'delta': delta,
                'percent_change': pct_change,
                'trend': trend,
                'trend_class': trend_class
            }
    
    return comparison


def main():
    """Main entry point."""
    # Parse arguments
    if len(sys.argv) < 7:
        print(__doc__)
        sys.exit(1)
    
    csv_file = sys.argv[1]
    venue_name = sys.argv[2]
    current_start = sys.argv[3]
    current_end = sys.argv[4]
    previous_start = sys.argv[5]
    previous_end = sys.argv[6]
    
    # Optional format argument
    report_format = 'all'
    if len(sys.argv) > 7:
        if sys.argv[7] == '--format':
            report_format = sys.argv[8] if len(sys.argv) > 8 else 'all'
    
    # Validate CSV file
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found: {csv_file}")
        sys.exit(1)
    
    print(f"Processing venue period comparison report...")
    print(f"  Venue: {venue_name}")
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
    
    # Filter by venue
    venue_rows = [r for r in rows if r.get('Venue', '').strip() == venue_name]
    if not venue_rows:
        print(f"Error: No data found for venue '{venue_name}'")
        sys.exit(1)
    
    # Filter by date ranges
    current_rows = filter_rows_by_date_range(venue_rows, current_start, current_end)
    previous_rows = filter_rows_by_date_range(venue_rows, previous_start, previous_end)
    
    if not current_rows:
        print(f"Error: No data found for current period ({current_start} to {current_end})")
        sys.exit(1)
    
    print(f"  Current period responses: {len(current_rows)}")
    print(f"  Previous period responses: {len(previous_rows)}")
    
    # Process venue data for both periods
    current_data = venue_processor.process_venue_data(current_rows, schema_type)
    previous_data = venue_processor.process_venue_data(previous_rows, schema_type) if previous_rows else None
    
    if not current_data:
        print(f"Error: Could not process current period data")
        sys.exit(1)
    
    # Build comparison data
    comparison_data = build_comparison_data(current_data, previous_data)
    
    # Get AI analysis for current period (with comparison context)
    print(f"  Running AI analysis...")
    ai_analysis = report_content.get_analysis(current_data)
    
    if not ai_analysis.get('ai_available'):
        print(f"  Warning: AI analysis unavailable: {ai_analysis.get('unavailable_reason')}")
    
    # Build report data
    report_data = {
        'venue': venue_name,
        'generated_date': datetime.now().strftime("%B %d, %Y at %I:%M %p"),
        'current_period': {
            'start': current_start,
            'end': current_end,
            'period_type': venue_processor.get_period_type(current_start, current_end),
            'responses': len(current_rows)
        },
        'previous_period': {
            'start': previous_start,
            'end': previous_end,
            'period_type': venue_processor.get_period_type(previous_start, previous_end),
            'responses': len(previous_rows)
        } if previous_rows else None,
        'comparison': comparison_data,
        'analysis': ai_analysis,
        'metrics_registry': report_engine.load_metrics_registry()
    }
    
    # Load Jinja2 environment
    TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
    jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=False)
    
    # Generate reports
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    venue_safe = venue_name.replace(' ', '_')
    
    # HTML report
    if report_format in ['html', 'all']:
        try:
            template = jinja_env.get_template('period-venue-comparison-browser.html')
            html = template.render(**report_data)
            html_file = os.path.join(reports_dir, f"Topgolf_Venue_Period_Comparison_{venue_safe}_{timestamp}_1PAGE.html")
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"[OK] HTML report: {html_file}")
        except Exception as e:
            print(f"[ERROR] HTML report failed: {e}")
    
    # Markdown report
    if report_format in ['markdown', 'all']:
        try:
            template = jinja_env.get_template('period-venue-comparison-report.md.j2')
            markdown = template.render(**report_data)
            md_file = os.path.join(reports_dir, f"Topgolf_Venue_Period_Comparison_{venue_safe}_{timestamp}_1PAGE.md")
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"[OK] Markdown report: {md_file}")
        except Exception as e:
            print(f"[ERROR] Markdown report failed: {e}")
    
    # PDF report
    if report_format in ['pdf', 'all']:
        try:
            from playwright.sync_api import sync_playwright
            
            template = jinja_env.get_template('period-venue-comparison-pdf.html')
            html = template.render(**report_data)
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                # Force print CSS and ensure background colors/gradients render
                page.emulate_media(media="print")
                # Wait for content to fully load before rendering PDF
                page.set_content(html, wait_until="load")
                pdf_file = os.path.join(reports_dir, f"Topgolf_Venue_Period_Comparison_{venue_safe}_{timestamp}_1PAGE.pdf")
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
