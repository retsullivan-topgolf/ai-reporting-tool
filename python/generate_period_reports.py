#!/usr/bin/env python3
"""
Unified orchestrator for period-based reports: venue period comparison,
multi-venue aggregation, and multi-venue period comparison.

This script provides an interactive menu to guide users through report generation,
with smart date handling and parameter validation. It automatically discovers
available CSV files in the example-data directory.

Usage:
    python generate_period_reports.py [<csv_file>] [--format html|markdown|pdf|all] [--no-prompt]

Examples:
    python generate_period_reports.py
    # Shows menu to select from available CSV files
    
    python generate_period_reports.py ../example-data/survey.csv
    # Uses specified CSV file
    
    python generate_period_reports.py --format all --no-prompt
    # Auto-selects first CSV, generates all report types with all formats
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import csv_parser


def load_config(config_file):
    """Load report configuration from JSON file."""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Config file not found: {config_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        sys.exit(1)


def validate_config(config):
    """Validate that config has required fields."""
    required_fields = ['csv_file', 'report_type', 'output_format']
    for field in required_fields:
        if field not in config:
            print(f"Error: Missing required config field: {field}")
            sys.exit(1)

    if not os.path.exists(config['csv_file']):
        print(f"Error: CSV file not found: {config['csv_file']}")
        sys.exit(1)


def execute_report_from_config(config):
    """Execute a report based on config file."""
    csv_file = config['csv_file']
    report_type = config['report_type']
    output_format = config['output_format']

    print(f"\n[OK] Using CSV file: {os.path.basename(csv_file)}")
    print(f"Report type: {report_type}")
    print(f"Output format: {output_format}\n")

    if report_type == "single_venue":
        # For single venue, optionally filter to specific venue
        venue = config.get('venue')
        if venue:
            print(f"Generating report for venue: {venue}")
        else:
            print("Generating reports for all venues")

        format_arg = f"--format {output_format}" if output_format != "all" else ""
        cmd = f"python generate_venue_reports.py {csv_file} {format_arg}"
        return run_command(cmd, "Single-venue report generation")

    elif report_type == "venue_period_comparison":
        venue = config.get('venue')
        current_start = config.get('current_period', {}).get('start_date')
        current_end = config.get('current_period', {}).get('end_date')
        previous_start = config.get('previous_period', {}).get('start_date')
        previous_end = config.get('previous_period', {}).get('end_date')

        if not all([venue, current_start, current_end, previous_start, previous_end]):
            print("Error: Missing required config fields for venue_period_comparison")
            print("  Required: venue, current_period.start_date, current_period.end_date,")
            print("           previous_period.start_date, previous_period.end_date")
            sys.exit(1)

        format_arg = f"--format {output_format}" if output_format != "all" else ""
        cmd = f"python create_single_venue_comparison_report.py {csv_file} \"{venue}\" {current_start} {current_end} {previous_start} {previous_end} {format_arg}"
        return run_command(cmd, f"Venue period comparison for {venue}")

    elif report_type == "multi_venue_single_period":
        start_date = config.get('period', {}).get('start_date')
        end_date = config.get('period', {}).get('end_date')

        if not all([start_date, end_date]):
            print("Error: Missing required config fields for multi_venue_single_period")
            print("  Required: period.start_date, period.end_date")
            sys.exit(1)

        format_arg = f"--format {output_format}" if output_format != "all" else ""
        cmd = f"python create_multi_venue_snapshot_report.py {csv_file} {start_date} {end_date} {format_arg}"
        return run_command(cmd, "Multi-venue single period report")

    elif report_type == "multi_venue_period_comparison":
        current_start = config.get('current_period', {}).get('start_date')
        current_end = config.get('current_period', {}).get('end_date')
        previous_start = config.get('previous_period', {}).get('start_date')
        previous_end = config.get('previous_period', {}).get('end_date')

        if not all([current_start, current_end, previous_start, previous_end]):
            print("Error: Missing required config fields for multi_venue_period_comparison")
            print("  Required: current_period.start_date, current_period.end_date,")
            print("           previous_period.start_date, previous_period.end_date")
            sys.exit(1)

        format_arg = f"--format {output_format}" if output_format != "all" else ""
        cmd = f"python create_multi_venue_comparison_report.py {csv_file} {current_start} {current_end} {previous_start} {previous_end} {format_arg}"
        return run_command(cmd, "Multi-venue period comparison")

    else:
        print(f"Error: Unknown report type: {report_type}")
        print("Valid types: single_venue, venue_period_comparison, multi_venue_single_period, multi_venue_period_comparison")
        sys.exit(1)


def find_csv_files():
    """Find all CSV files in the qualtrics directory."""
    example_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'qualtrics')
    
    if not os.path.exists(example_data_dir):
        return []
    
    csv_files = []
    try:
        for file in sorted(os.listdir(example_data_dir)):
            if file.lower().endswith('.csv'):
                full_path = os.path.join(example_data_dir, file)
                csv_files.append((file, full_path))
    except Exception as e:
        print(f"Error scanning for CSV files: {e}")
    
    return csv_files


def get_csv_file():
    """Let user select from available CSV files or enter a custom path."""
    csv_files = find_csv_files()
    
    if csv_files:
        print("\n" + "="*60)
        print("AVAILABLE CSV FILES")
        print("="*60)
        print("\nFound CSV files in ../qualtrics/:")
        for i, (filename, filepath) in enumerate(csv_files, 1):
            print(f"  {i}) {filename}")
        
        print(f"\n  {len(csv_files) + 1}) Enter custom path")
        
        choice = input(f"\nSelect CSV file (1-{len(csv_files) + 1}): ").strip()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(csv_files):
                return csv_files[choice_num - 1][1]
            elif choice_num == len(csv_files) + 1:
                # Custom path
                csv_file = input("Enter path to CSV file: ").strip()
                if os.path.exists(csv_file):
                    return csv_file
                else:
                    print(f"Error: File not found: {csv_file}")
                    return get_csv_file()
            else:
                print("Invalid choice")
                return get_csv_file()
        except ValueError:
            print("Invalid input")
            return get_csv_file()
    else:
        # No CSV files found, ask for custom path
        print("\nNo CSV files found in ../qualtrics/")
        csv_file = input("Enter path to CSV file: ").strip()
        
        if os.path.exists(csv_file):
            return csv_file
        else:
            print(f"Error: File not found: {csv_file}")
            return get_csv_file()


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
            print(f"[OK] {description} completed successfully")
            return True
        else:
            print(f"[ERROR] {description} failed with exit code {result.returncode}")
            return False
    except Exception as e:
        print(f"[ERROR] Error running {description}: {e}")
        return False


def report_type_1_single_venue(csv_file, output_format):
    """Generate single-venue reports - user can choose all venues or specific venue."""
    print("\n" + "="*60)
    print("REPORT TYPE 1: Single-Venue Reports")
    print("="*60)
    
    # Get available venues
    venues = get_venues_from_csv(csv_file)
    if not venues:
        print("Error: No venues found in CSV file")
        return False
    
    print(f"\nAvailable venues ({len(venues)}):")
    for i, venue in enumerate(venues, 1):
        print(f"  {i}) {venue}")
    
    print(f"\n  {len(venues) + 1}) All venues")
    
    choice = input(f"\nSelect venue (1-{len(venues) + 1}): ").strip()
    
    try:
        choice_num = int(choice)
        if choice_num == len(venues) + 1:
            # Generate for all venues
            print("\nGenerating reports for all venues...")
            format_arg = f"--format {output_format}" if output_format != "all" else ""
            cmd = f"python generate_venue_reports.py {csv_file} {format_arg}"
            return run_command(cmd, "Single-venue report generation for all venues")
        elif 1 <= choice_num <= len(venues):
            # Generate for specific venue
            selected_venue = venues[choice_num - 1]
            print(f"\nGenerating report for: {selected_venue}")
            
            # For a single venue, we need to:
            # 1. Generate metrics for just that venue
            # 2. Run AI analysis
            # 3. Generate reports
            
            # First, generate all venue data
            print("Step 1: Processing data...")
            cmd_generate = f"python generate_venue_data.py {csv_file}"
            result = subprocess.run(cmd_generate, shell=True, cwd=os.path.dirname(os.path.abspath(__file__)))
            if result.returncode != 0:
                print("[ERROR] Failed to process data")
                return False
            
            # Run AI analysis
            print("Step 2: Running AI analysis...")
            cmd_analysis = f"python run_analyze_venues.py venue_data.json"
            result = subprocess.run(cmd_analysis, shell=True, cwd=os.path.dirname(os.path.abspath(__file__)))
            if result.returncode != 0:
                print("[ERROR] Failed to run AI analysis")
                return False
            
            # Generate reports for all venues, then filter to just the selected one
            # (We'll generate all then the user can ignore the others, or we could modify the scripts)
            print("Step 3: Generating reports...")
            format_arg = f"--format {output_format}" if output_format != "all" else ""
            cmd_reports = f"python create_html_reports.py venue_data.json --analysis ai_analysis_results.json {format_arg}"
            result = subprocess.run(cmd_reports, shell=True, cwd=os.path.dirname(os.path.abspath(__file__)))
            
            if output_format in ["markdown", "all"]:
                cmd_md = f"python create_markdown_reports.py venue_data.json --analysis ai_analysis_results.json"
                subprocess.run(cmd_md, shell=True, cwd=os.path.dirname(os.path.abspath(__file__)))
            
            if output_format in ["pdf", "all"]:
                cmd_pdf = f"python create_pdf_reports.py venue_data.json --analysis ai_analysis_results.json"
                subprocess.run(cmd_pdf, shell=True, cwd=os.path.dirname(os.path.abspath(__file__)))
            
            print(f"\n[OK] Report generated for {selected_venue}")
            print(f"  (Note: Reports for all venues were generated; look for {selected_venue} in the reports/ directory)")
            return True
        else:
            print("Invalid choice")
            return False
    except ValueError:
        print("Invalid input")
        return False


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
    cmd = f"python create_single_venue_comparison_report.py {csv_file} \"{venue_name}\" {current_start} {current_end} {previous_start} {previous_end} {format_arg}"
    
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
    cmd = f"python create_multi_venue_snapshot_report.py {csv_file} {start_date} {end_date} {format_arg}"
    
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
    cmd = f"python create_multi_venue_comparison_report.py {csv_file} {current_start} {current_end} {previous_start} {previous_end} {format_arg}"
    
    return run_command(cmd, "Multi-venue period comparison")


def show_report_menu():
    """Display the main report type menu."""
    print("\n" + "="*60)
    print("REPORT TYPE SELECTION")
    print("="*60)
    print("\n1) SINGLE-VENUE REPORTS")
    print("   Choose a specific venue or generate for all venues")
    print("   Shows performance for a single time period")
    print("   Includes AI analysis for each venue")
    
    print("\n2) VENUE PERIOD COMPARISON")
    print("   Compare one venue's metrics between two time periods")
    print("   Shows trends and changes for that specific venue")
    
    print("\n3) MULTI-VENUE SINGLE PERIOD")
    print("   Aggregate metrics across all venues for one time period")
    print("   Shows venue ranking by composite score")
    print("   Includes comment themes")
    
    print("\n4) MULTI-VENUE PERIOD COMPARISON")
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
    config_file = None
    csv_file = None
    output_format = "all"
    no_prompt = False

    # Check for --config parameter first
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--config" and i + 1 < len(sys.argv):
            config_file = sys.argv[i + 1]
            break

    # If config file is provided, use it
    if config_file:
        config = load_config(config_file)
        validate_config(config)
        execute_report_from_config(config)
        return

    # Otherwise, use interactive mode
    if len(sys.argv) > 1:
        # Check if first argument is a flag or a file path
        if sys.argv[1].startswith("--"):
            # It's a flag, not a file
            csv_file = None
        else:
            # It's a file path
            csv_file = sys.argv[1]

        # Parse optional arguments
        for i in range(2, len(sys.argv)):
            if sys.argv[i] == "--format" and i + 1 < len(sys.argv):
                output_format = sys.argv[i + 1]
            elif sys.argv[i] == "--no-prompt":
                no_prompt = True

    # Get CSV file if not provided or doesn't exist
    if not csv_file or not os.path.exists(csv_file):
        csv_file = get_csv_file()

    # Extract just the filename for display
    csv_filename = os.path.basename(csv_file)
    print(f"\n[OK] Using CSV file: {csv_filename}")

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
