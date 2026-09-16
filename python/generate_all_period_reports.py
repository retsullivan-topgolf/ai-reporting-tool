#!/usr/bin/env python3
"""
Unified orchestrator for all report types: single-venue, venue period comparison,
multi-venue aggregation, and multi-venue period comparison.

This script provides an interactive menu to guide users through report generation,
with smart date handling and parameter validation.

Usage:
    python generate_all_period_reports.py <csv_file> [--format html|markdown|pdf|all] [--no-prompt]

Examples:
    python generate_all_period_reports.py ../example-data/survey.csv
    python generate_all_period_reports.py ../example-data/survey.csv --format html --no-prompt
"""

import os
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api import csv_parser


def get_csv_file():
    """Prompt user for CSV file path."""
    while True:
        csv_file = input("\nEnter path to CSV file (or press Enter for ../example-data/survey.csv): ").strip()
        
        if not csv_file:
            csv_file = "../example-data/survey.csv"
        
        if os.path.exists(csv_file):
            return csv_file
        else:
            print(f"Error: File not found: {csv_file}")


def get_venues_from_csv(csv_file):
    """Extract unique venues from CSV file."""
    try:
        rows, fieldnames = csv_parser.parse_csv(csv_file)
        venues = sorted(set(r.get('Venue', '').strip() for r in rows if r.get('Venue', '').strip()))
        return venues
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []


def parse_date_input(prompt):
    """Parse user date input, accepting various formats."""
    while True:
        date_str = input(prompt).strip()
        
        # Try common date formats
        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%m-%d-%Y']:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        print(f"Invalid date format. Please use YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY")


def get_period_dates(period_name="current"):
    """Get date range for a period with smart options."""
    print(f"\n--- {period_name.capitalize()} Period ---")
    print("1) Last month")
    print("2) Last quarter")
    print("3) Custom date range")
    
    choice = input(f"Select {period_name} period (1-3): ").strip()
    
    if choice == "1":
        # Last month
        today = datetime.now()
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        
        start_date = first_day_last_month.strftime('%Y-%m-%d')
        end_date = last_day_last_month.strftime('%Y-%m-%d')
        period_type = "month"
        
        print(f"Using last month: {start_date} to {end_date}")
        return start_date, end_date, period_type
    
    elif choice == "2":
        # Last quarter
        today = datetime.now()
        current_quarter = (today.month - 1) // 3
        
        # Get last quarter
        if current_quarter == 0:
            # Q1, so last quarter is Q4 of previous year
            last_quarter = 3
            year = today.year - 1
        else:
            last_quarter = current_quarter - 1
            year = today.year
        
        # Calculate start and end dates for last quarter
        quarter_start_month = last_quarter * 3 + 1
        quarter_end_month = quarter_start_month + 2
        
        start_date = datetime(year, quarter_start_month, 1).strftime('%Y-%m-%d')
        end_date = datetime(year, quarter_end_month, 1).replace(day=1) - timedelta(days=1)
        end_date = end_date.strftime('%Y-%m-%d')
        period_type = "quarter"
        
        print(f"Using last quarter: {start_date} to {end_date}")
        return start_date, end_date, period_type
    
    elif choice == "3":
        # Custom date range
        start_date = parse_date_input(f"Enter {period_name} period start date (YYYY-MM-DD): ")
        end_date = parse_date_input(f"Enter {period_name} period end date (YYYY-MM-DD): ")
        
        # Determine period type
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        days = (end - start).days + 1
        
        if 25 <= days <= 32:
            period_type = "month"
        elif 88 <= days <= 93:
            period_type = "quarter"
        else:
            period_type = "custom"
        
        print(f"Using custom period: {start_date} to {end_date}")
        return start_date, end_date, period_type
    
    else:
        print("Invalid choice. Using last month.")
        today = datetime.now()
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        
        start_date = first_day_last_month.strftime('%Y-%m-%d')
        end_date = last_day_last_month.strftime('%Y-%m-%d')
        return start_date, end_date, "month"


def get_output_format():
    """Prompt user for output format."""
    print("\nOutput Format:")
    print("1) HTML")
    print("2) Markdown")
    print("3) PDF")
    print("4) All formats")
    
    choice = input("Select format (1-4, or press Enter for all): ").strip()
    
    format_map = {
        "1": "html",
        "2": "markdown",
        "3": "pdf",
        "4": "all",
        "": "all"
    }
    
    return format_map.get(choice, "all")


def run_command(cmd, description):
    """Run a command and report status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True
        else:
            print(f"✗ {description} failed with exit code {result.returncode}")
            return False
    except Exception as e:
        print(f"✗ Error running {description}: {e}")
        return False


def report_type_1_single_venue(csv_file, output_format):
    """Generate single-venue reports for all venues in CSV."""
    print("\n" + "="*60)
    print("REPORT TYPE 1: Single-Venue Reports")
    print("="*60)
    print("This will generate one report per venue in the CSV file.")
    print("Each report includes AI analysis for that venue.")
    
    # Run the existing generate_all_reports.py
    format_arg = f"--format {output_format}" if output_format != "all" else ""
    cmd = f"python generate_all_reports.py {csv_file} {format_arg}"
    
    return run_command(cmd, "Single-venue report generation")


def report_type_2_venue_period_comparison(csv_file, output_format):
    """Generate venue period comparison report."""
    print("\n" + "="*60)
    print("REPORT TYPE 2: Venue Period Comparison")
    print("="*60)
    print("Compare a single venue's metrics between two time periods.")
    
    venues = get_venues_from_csv(csv_file)
    if not venues:
        print("Error: No venues found in CSV file")
        return False
    
    print(f"\nAvailable venues: {', '.join(venues)}")
    venue_name = input("Enter venue name: ").strip()
    
    if venue_name not in venues:
        print(f"Error: Venue '{venue_name}' not found in CSV")
        return False
    
    current_start, current_end, _ = get_period_dates("current")
    previous_start, previous_end, _ = get_period_dates("previous")
    
    format_arg = f"--format {output_format}" if output_format != "all" else ""
    cmd = f"python create_venue_period_comparison_report.py {csv_file} \"{venue_name}\" {current_start} {current_end} {previous_start} {previous_end} {format_arg}"
    
    return run_command(cmd, f"Venue period comparison for {venue_name}")


def report_type_3_multi_venue_single_period(csv_file, output_format):
    """Generate multi-venue single period report."""
    print("\n" + "="*60)
    print("REPORT TYPE 3: Multi-Venue Single Period")
    print("="*60)
    print("Aggregate metrics across all venues for one time period.")
    print("Includes venue ranking by composite score and comment themes.")
    
    start_date, end_date, period_type = get_period_dates("period")
    
    format_arg = f"--format {output_format}" if output_format != "all" else ""
    cmd = f"python create_multi_venue_period_report.py {csv_file} {start_date} {end_date} {format_arg}"
    
    return run_command(cmd, f"Multi-venue {period_type} report")


def report_type_4_multi_venue_period_comparison(csv_file, output_format):
    """Generate multi-venue period comparison report."""
    print("\n" + "="*60)
    print("REPORT TYPE 4: Multi-Venue Period Comparison")
    print("="*60)
    print("Compare aggregated metrics across all venues between two time periods.")
    print("Shows ranking changes and trends across all venues.")
    
    current_start, current_end, _ = get_period_dates("current")
    previous_start, previous_end, _ = get_period_dates("previous")
    
    format_arg = f"--format {output_format}" if output_format != "all" else ""
    cmd = f"python create_period_comparison_report.py {csv_file} {current_start} {current_end} {previous_start} {previous_end} {format_arg}"
    
    return run_command(cmd, "Multi-venue period comparison")


def show_report_menu():
    """Display the main report type menu."""
    print("\n" + "="*60)
    print("REPORT TYPE SELECTION")
    print("="*60)
    print("\n1) SINGLE-VENUE REPORTS (Existing)")
    print("   Generate one report per venue in the CSV")
    print("   Shows all venues' performance for a single time period")
    print("   Includes AI analysis for each venue")
    
    print("\n2) VENUE PERIOD COMPARISON (New)")
    print("   Compare one venue's metrics between two time periods")
    print("   Shows trends and changes for that specific venue")
    
    print("\n3) MULTI-VENUE SINGLE PERIOD (New)")
    print("   Aggregate metrics across all venues for one time period")
    print("   Shows venue ranking by composite score")
    print("   Includes comment themes")
    
    print("\n4) MULTI-VENUE PERIOD COMPARISON (New)")
    print("   Compare aggregated metrics across two time periods")
    print("   Shows ranking changes and trends across all venues")
    
    print("\n0) EXIT")
    
    choice = input("\nSelect report type (0-4): ").strip()
    return choice


def main():
    """Main orchestrator function."""
    print("\n" + "="*60)
    print("TOPGOLF REPORT GENERATION ORCHESTRATOR")
    print("="*60)
    
    # Parse command line arguments
    csv_file = None
    output_format = "all"
    no_prompt = False
    
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        
        # Parse optional arguments
        for i in range(2, len(sys.argv)):
            if sys.argv[i] == "--format" and i + 1 < len(sys.argv):
                output_format = sys.argv[i + 1]
            elif sys.argv[i] == "--no-prompt":
                no_prompt = True
    
    # Get CSV file if not provided
    if not csv_file or not os.path.exists(csv_file):
        csv_file = get_csv_file()
    
    print(f"\nUsing CSV file: {csv_file}")
    
    # Get output format if not provided
    if not no_prompt:
        output_format = get_output_format()
    
    print(f"Output format: {output_format}")
    
    # Main loop
    while True:
        choice = show_report_menu()
        
        if choice == "0":
            print("\nExiting...")
            break
        
        elif choice == "1":
            report_type_1_single_venue(csv_file, output_format)
        
        elif choice == "2":
            report_type_2_venue_period_comparison(csv_file, output_format)
        
        elif choice == "3":
            report_type_3_multi_venue_single_period(csv_file, output_format)
        
        elif choice == "4":
            report_type_4_multi_venue_period_comparison(csv_file, output_format)
        
        else:
            print("Invalid choice. Please select 0-4.")
        
        # Ask if user wants to generate another report
        if not no_prompt:
            another = input("\nGenerate another report? (y/n): ").strip().lower()
            if another != "y":
                print("\nExiting...")
                break


if __name__ == "__main__":
    main()
