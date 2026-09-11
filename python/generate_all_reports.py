#!/usr/bin/env python3
"""
Generate all venue reports in one command.
This script runs both generate_reports.py and create_html_reports.py sequentially.
"""
import subprocess
import sys
import os

def run_command(script_name, args):
    """Run a Python script and return success status"""
    try:
        cmd = [sys.executable, script_name] + args
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
    # Get CSV file from command line argument or use default
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = '../example-data/topgolf_qualtrics_week_responses.csv'
    
    # Check if CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found: {csv_file}")
        print(f"\nUsage: python generate_all_reports.py <path_to_csv_file>")
        print(f"\nExamples:")
        print(f"  python generate_all_reports.py ../example-data/topgolf_qualtrics_week_responses.csv")
        print(f"  python generate_all_reports.py ../example-data/topgolf_qualtrics_30_responses_DALLAS.csv")
        sys.exit(1)
    
    print(f"Generating all reports from: {csv_file}\n")
    
    # Step 1: Generate reports (creates venue_data.json)
    print("STEP 1: Processing CSV data and generating metrics...")
    if not run_command('generate_reports.py', [csv_file]):
        print("\nFailed to generate reports from CSV. Aborting.")
        sys.exit(1)
    
    # Step 2: Create HTML reports
    print("\nSTEP 2: Creating HTML reports from metrics...")
    if not run_command('create_html_reports.py', ['venue_data.json']):
        print("\nFailed to create HTML reports. Aborting.")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print("[SUCCESS] All reports generated successfully!")
    print(f"{'='*60}")
    print(f"\nGenerated files:")
    print(f"  - Metrics: venue_data.json")
    print(f"  - Reports: ../Topgolf_Venue_Report_*.html")

if __name__ == '__main__':
    main()
