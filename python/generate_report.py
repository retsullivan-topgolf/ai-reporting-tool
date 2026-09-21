#!/usr/bin/env python3
"""
Unified report generation entry point.

This script provides a single command to generate any report type:
- Single-venue snapshot (current period)
- Single-venue comparison (two periods)
- Multi-venue snapshot (current period, all venues)
- Multi-venue comparison (two periods, all venues)

Usage:
    python generate_report.py [--report-type TYPE] [--venue VENUE] [--format FORMAT] [--start-date DATE] [--end-date DATE] [--prev-start DATE] [--prev-end DATE] [--force-analysis]

Examples:
    # Interactive mode - prompts for all inputs
    python generate_report.py

    # Single-venue snapshot for Grand Prairie
    python generate_report.py --report-type snapshot --venue "Grand Prairie" --format all

    # Single-venue snapshot with fresh AI analysis (bypass cache)
    python generate_report.py --report-type snapshot --venue "Grand Prairie" --format all --force-analysis

    # Single-venue comparison
    python generate_report.py --report-type comparison --venue "Grand Prairie" --start-date 2026-01-01 --end-date 2026-01-31 --prev-start 2025-12-01 --prev-end 2025-12-31 --format html

    # Multi-venue snapshot
    python generate_report.py --report-type multi-snapshot --start-date 2026-01-01 --end-date 2026-01-31 --format all

    # Multi-venue comparison
    python generate_report.py --report-type multi-comparison --start-date 2026-01-01 --end-date 2026-01-31 --prev-start 2025-12-01 --prev-end 2025-12-31 --format pdf
"""

import subprocess
import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import data_loader


REPORT_TYPES = {
    'snapshot': {
        'name': 'Single-Venue Snapshot',
        'description': 'Current period report for a single venue',
        'requires': ['venue'],
        'script': 'create_single_venue_report.py',
    },
    'comparison': {
        'name': 'Single-Venue Comparison',
        'description': 'Compare a single venue between two periods',
        'requires': ['venue', 'start_date', 'end_date', 'prev_start', 'prev_end'],
        'script': 'create_single_venue_comparison_report.py',
    },
    'multi-snapshot': {
        'name': 'Multi-Venue Snapshot',
        'description': 'Current period report for all venues',
        'requires': ['start_date', 'end_date'],
        'script': 'create_multi_venue_report.py',
    },
    'multi-comparison': {
        'name': 'Multi-Venue Comparison',
        'description': 'Compare all venues between two periods',
        'requires': ['start_date', 'end_date', 'prev_start', 'prev_end'],
        'script': 'create_multi_venue_comparison_report.py',
    },
}

FORMATS = ['html', 'markdown', 'pdf', 'all']


def parse_args():
    """Parse command line arguments."""
    args = {
        'report_type': None,
        'venue': None,
        'format': None,
        'start_date': None,
        'end_date': None,
        'prev_start': None,
        'prev_end': None,
        'force_analysis': False,
    }
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--report-type':
            if i + 1 >= len(sys.argv):
                print("Error: --report-type requires a value")
                sys.exit(1)
            args['report_type'] = sys.argv[i + 1]
            i += 2
        elif arg == '--venue':
            if i + 1 >= len(sys.argv):
                print("Error: --venue requires a value")
                sys.exit(1)
            args['venue'] = sys.argv[i + 1]
            i += 2
        elif arg == '--format':
            if i + 1 >= len(sys.argv):
                print("Error: --format requires a value")
                sys.exit(1)
            args['format'] = sys.argv[i + 1]
            i += 2
        elif arg == '--start-date':
            if i + 1 >= len(sys.argv):
                print("Error: --start-date requires a value")
                sys.exit(1)
            args['start_date'] = sys.argv[i + 1]
            i += 2
        elif arg == '--end-date':
            if i + 1 >= len(sys.argv):
                print("Error: --end-date requires a value")
                sys.exit(1)
            args['end_date'] = sys.argv[i + 1]
            i += 2
        elif arg == '--prev-start':
            if i + 1 >= len(sys.argv):
                print("Error: --prev-start requires a value")
                sys.exit(1)
            args['prev_start'] = sys.argv[i + 1]
            i += 2
        elif arg == '--prev-end':
            if i + 1 >= len(sys.argv):
                print("Error: --prev-end requires a value")
                sys.exit(1)
            args['prev_end'] = sys.argv[i + 1]
            i += 2
        elif arg == '--force-analysis':
            args['force_analysis'] = True
            i += 1
        else:
            print(f"Error: Unknown argument '{arg}'")
            sys.exit(1)
    
    return args


def prompt_for_report_type():
    """Interactive prompt for report type."""
    print("\n" + "="*60)
    print("REPORT TYPE")
    print("="*60)
    
    for i, (key, info) in enumerate(REPORT_TYPES.items(), 1):
        print(f"  {i}) {info['name']}")
        print(f"     {info['description']}")
    
    choices = {
        '1': 'snapshot', 'snapshot': 'snapshot',
        '2': 'comparison', 'comparison': 'comparison',
        '3': 'multi-snapshot', 'multi-snapshot': 'multi-snapshot',
        '4': 'multi-comparison', 'multi-comparison': 'multi-comparison',
    }
    
    for _ in range(3):
        try:
            answer = input("\nEnter choice [1-4]: ").strip().lower()
        except EOFError:
            print("Non-interactive session detected - defaulting to snapshot.")
            return 'snapshot'
        
        if answer in choices:
            return choices[answer]
        print("Please enter 1, 2, 3, or 4.")
    
    print("No valid selection after 3 attempts - defaulting to snapshot.")
    return 'snapshot'


def get_available_venues():
    """Get list of available venues from texas_venues."""
    try:
        rows = data_loader.load_data('texas_venues')
        venues = set()
        for row in rows:
            venue = row.get('Venue') or row.get('venue')
            if venue:
                venues.add(venue)
        return sorted(list(venues))
    except Exception as e:
        print(f"Warning: Could not load venues: {e}")
        return []


def prompt_for_venue():
    """Interactive prompt for venue selection."""
    print("\n" + "="*60)
    print("VENUE SELECTION")
    print("="*60)
    
    venues = get_available_venues()
    
    if not venues:
        print("Error: Could not load available venues.")
        print("Please enter venue name manually:")
        return input("Venue name: ").strip()
    
    print("\nAvailable venues:")
    for i, venue in enumerate(venues, 1):
        print(f"  {i}) {venue}")
    
    print(f"  {len(venues) + 1}) Enter custom venue name")
    
    for _ in range(3):
        try:
            answer = input(f"\nEnter choice [1-{len(venues) + 1}]: ").strip()
        except EOFError:
            print("Non-interactive session detected - using first venue.")
            return venues[0] if venues else "Grand Prairie"
        
        try:
            choice = int(answer)
            if 1 <= choice <= len(venues):
                return venues[choice - 1]
            elif choice == len(venues) + 1:
                return input("Enter venue name: ").strip()
        except ValueError:
            pass
        
        print(f"Please enter a number between 1 and {len(venues) + 1}.")
    
    print("No valid selection after 3 attempts - using first venue.")
    return venues[0] if venues else "Grand Prairie"


def prompt_for_date(prompt_text):
    """Interactive prompt for date input (YYYY-MM-DD format)."""
    for _ in range(3):
        try:
            date_str = input(f"{prompt_text} (YYYY-MM-DD): ").strip()
            # Validate format
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
        except EOFError:
            print("Non-interactive session detected - using today's date.")
            return datetime.now().strftime('%Y-%m-%d')
    
    print("No valid date after 3 attempts - using today's date.")
    return datetime.now().strftime('%Y-%m-%d')


def prompt_for_format():
    """Interactive prompt for output format."""
    print("\n" + "="*60)
    print("OUTPUT FORMAT")
    print("="*60)
    print("  1) HTML")
    print("  2) Markdown")
    print("  3) PDF")
    print("  4) All (HTML, Markdown, PDF)")
    
    choices = {
        '1': 'html', 'html': 'html',
        '2': 'markdown', 'markdown': 'markdown',
        '3': 'pdf', 'pdf': 'pdf',
        '4': 'all', 'all': 'all',
    }
    
    for _ in range(3):
        try:
            answer = input("\nEnter choice [1-4] (default: 4): ").strip().lower()
        except EOFError:
            print("Non-interactive session detected - defaulting to all formats.")
            return 'all'
        
        if answer == '':
            return 'all'
        if answer in choices:
            return choices[answer]
        print("Please enter 1, 2, 3, or 4.")
    
    print("No valid selection after 3 attempts - defaulting to all formats.")
    return 'all'


def validate_format(fmt):
    """Validate and normalize format string."""
    if fmt is None:
        return None
    
    fmt = fmt.lower().strip()
    if fmt in FORMATS:
        return fmt
    
    # Try comma-separated
    parts = [p.strip() for p in fmt.split(',')]
    for part in parts:
        if part not in ['html', 'markdown', 'pdf']:
            print(f"Error: Invalid format '{part}'. Must be one of: {', '.join(FORMATS)}")
            sys.exit(1)
    
    return fmt


def run_command(script_name, args):
    """Run a Python script and return success status."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, script_name)
        cmd = [sys.executable, script_path] + args
        
        print(f"\n{'='*60}")
        print(f"Running: {' '.join(cmd)}")
        print(f"{'='*60}\n")
        
        result = subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError running {script_name}: {e}")
        return False
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return False


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("UNIFIED REPORT GENERATOR")
    print("="*60)
    
    # Parse command line arguments
    args = parse_args()
    
    # Get report type (prompt if not provided)
    report_type = args['report_type']
    if not report_type:
        report_type = prompt_for_report_type()
    
    if report_type not in REPORT_TYPES:
        print(f"Error: Unknown report type '{report_type}'")
        print(f"Valid types: {', '.join(REPORT_TYPES.keys())}")
        sys.exit(1)
    
    report_info = REPORT_TYPES[report_type]
    print(f"\nSelected: {report_info['name']}")
    
    # Collect required parameters
    params = {}
    
    # Venue (if required)
    if 'venue' in report_info['requires']:
        venue = args['venue']
        if not venue:
            venue = prompt_for_venue()
        params['venue'] = venue
        print(f"Venue: {venue}")
    
    # Dates (if required)
    if 'start_date' in report_info['requires']:
        start_date = args['start_date']
        if not start_date:
            start_date = prompt_for_date("Enter start date")
        params['start_date'] = start_date
        print(f"Start date: {start_date}")
    
    if 'end_date' in report_info['requires']:
        end_date = args['end_date']
        if not end_date:
            end_date = prompt_for_date("Enter end date")
        params['end_date'] = end_date
        print(f"End date: {end_date}")
    
    if 'prev_start' in report_info['requires']:
        prev_start = args['prev_start']
        if not prev_start:
            prev_start = prompt_for_date("Enter previous period start date")
        params['prev_start'] = prev_start
        print(f"Previous start date: {prev_start}")
    
    if 'prev_end' in report_info['requires']:
        prev_end = args['prev_end']
        if not prev_end:
            prev_end = prompt_for_date("Enter previous period end date")
        params['prev_end'] = prev_end
        print(f"Previous end date: {prev_end}")
    
    # Output format (always required)
    output_format = args['format']
    if not output_format:
        output_format = prompt_for_format()
    
    output_format = validate_format(output_format)
    print(f"Output format: {output_format}")
    
    # Build command arguments based on report type
    script_name = report_info['script']
    cmd_args = []
    
    if report_type == 'snapshot':
        # Single-venue snapshot: generate_venue_data.py -> run_analyze_venues.py -> create_single_venue_report.py
        print("\n" + "="*60)
        print("STEP 1: Processing data and generating metrics...")
        print("="*60)
        
        if not run_command('generate_venue_data.py', [params['venue']]):
            print("\nFailed to generate venue data. Aborting.")
            sys.exit(1)
        
        print("\n" + "="*60)
        print("STEP 2: Generating AI analysis...")
        if args['force_analysis']:
            print("(--force-analysis: bypassing cache)")
        print("="*60)
        
        analyze_args = ['venue_data.json', '--output', 'ai_analysis_results.json']
        if args['force_analysis']:
            analyze_args.append('--force')
        
        if not run_command('run_analyze_venues.py', analyze_args):
            print("\nFailed to generate AI analysis. Aborting.")
            sys.exit(1)
        
        print("\n" + "="*60)
        print("STEP 3: Creating report...")
        print("="*60)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cmd_args = ['venue_data.json', '--format', output_format, '--timestamp', timestamp, '--analysis', 'ai_analysis_results.json']
    
    elif report_type == 'comparison':
        # Single-venue comparison
        cmd_args = [
            'texas_venues',
            params['venue'],
            params['start_date'],
            params['end_date'],
            params['prev_start'],
            params['prev_end'],
            '--format', output_format
        ]
    
    elif report_type == 'multi-snapshot':
        # Multi-venue snapshot
        cmd_args = [
            'texas_venues',
            params['start_date'],
            params['end_date'],
            '--format', output_format
        ]
    
    elif report_type == 'multi-comparison':
        # Multi-venue comparison
        cmd_args = [
            'texas_venues',
            params['start_date'],
            params['end_date'],
            params['prev_start'],
            params['prev_end'],
            '--format', output_format
        ]
    
    # Run the appropriate script
    if report_type != 'snapshot':  # snapshot already ran its scripts above
        if not run_command(script_name, cmd_args):
            print(f"\nFailed to create report. Aborting.")
            sys.exit(1)
    else:
        if not run_command(script_name, cmd_args):
            print(f"\nFailed to create report. Aborting.")
            sys.exit(1)
    
    print(f"\n{'='*60}")
    print("[SUCCESS] Report generated successfully!")
    print(f"{'='*60}")
    print(f"\nCheck the 'reports/' directory for your generated report.")


if __name__ == '__main__':
    main()
