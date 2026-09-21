#!/usr/bin/env python3
"""
Generate single-venue snapshot reports in one command.

This script orchestrates the complete workflow:
1. Processes CSV data → generates venue_data.json
2. Runs AI analysis → generates ai_analysis_results.json
3. Creates reports in selected format(s) (HTML, Markdown, PDF, or all)

Usage:
    python generate_venue_reports.py <csv_file> [--format html|markdown|pdf|all] [--timeout SECONDS]

Examples:
    python generate_venue_reports.py ../example-data/survey.csv
    python generate_venue_reports.py ../example-data/survey.csv --format all
    python generate_venue_reports.py ../example-data/survey.csv --format html,pdf
"""
import subprocess
import sys
import os
import json
from datetime import datetime

SINGLE_FORMATS = ('html', 'markdown', 'pdf')
# 'both' is kept as a legacy alias (html + markdown, from before PDF support
# was added) so existing scripts/docs referencing --format both keep working.
FORMAT_ALIASES = {
    'both': {'html', 'markdown'},
    'all': {'html', 'markdown', 'pdf'},
}


def run_command(script_name, args, env_overrides=None):
    """Run a Python script and return success status"""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, script_name)
        cmd = [sys.executable, script_path] + args
        print(f"\n{'='*60}")
        print(f"Running: {' '.join(cmd)}")
        print(f"{'='*60}\n")
        
        # Prepare environment with any overrides
        env = os.environ.copy()
        if env_overrides:
            env.update(env_overrides)
        
        result = subprocess.run(cmd, check=True, env=env)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError running {script_name}: {e}")
        return False
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return False


def _format_help():
    return "html, markdown, pdf, both (html+markdown), all (html+markdown+pdf), or a comma-separated combo like html,pdf"


def normalize_formats(raw):
    """Turn a --format value into a set of {'html', 'markdown', 'pdf'}, or
    None if it doesn't parse. Accepts a single format, an alias ('both'/
    'all'), or a comma-separated combination of the two ('html,pdf')."""
    tokens = [t.strip().lower() for t in raw.split(',') if t.strip()]
    if not tokens:
        return None

    formats = set()
    for token in tokens:
        if token in SINGLE_FORMATS:
            formats.add(token)
        elif token in FORMAT_ALIASES:
            formats.update(FORMAT_ALIASES[token])
        else:
            return None
    return formats


def parse_format_flag(argv):
    """Look for --format/-f <value> anywhere in argv. Returns
    (formats_set_or_None, remaining_argv). Accepted so the report format(s)
    can be scripted/automated without answering the interactive prompt."""
    remaining = []
    raw_format = None
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ('--format', '-f'):
            if i + 1 >= len(argv):
                print(f"Error: --format requires a value ({_format_help()})")
                sys.exit(1)
            raw_format = argv[i + 1]
            i += 2
            continue
        if arg.startswith('--format='):
            raw_format = arg.split('=', 1)[1]
            i += 1
            continue
        remaining.append(arg)
        i += 1

    if raw_format is None:
        return None, remaining

    formats = normalize_formats(raw_format)
    if formats is None:
        print(f"Error: invalid --format '{raw_format}'. Must be one of: {_format_help()}")
        sys.exit(1)

    return formats, remaining


def parse_timeout_flag(argv):
    """Look for --timeout <seconds> anywhere in argv. Returns
    (timeout_seconds_or_None, remaining_argv). Allows overriding the default
    Claude timeout for AI analysis stages."""
    remaining = []
    timeout = None
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == '--timeout':
            if i + 1 >= len(argv):
                print("Error: --timeout requires a value (in seconds)")
                sys.exit(1)
            try:
                timeout = int(argv[i + 1])
                if timeout <= 0:
                    print("Error: --timeout must be a positive integer")
                    sys.exit(1)
            except ValueError:
                print(f"Error: --timeout value '{argv[i + 1]}' is not a valid integer")
                sys.exit(1)
            i += 2
            continue
        if arg.startswith('--timeout='):
            try:
                timeout = int(arg.split('=', 1)[1])
                if timeout <= 0:
                    print("Error: --timeout must be a positive integer")
                    sys.exit(1)
            except ValueError:
                print(f"Error: --timeout value is not a valid integer")
                sys.exit(1)
            i += 1
            continue
        remaining.append(arg)
        i += 1

    return timeout, remaining


def prompt_for_format():
    """Interactive prompt for which report format(s) to generate. Falls back
    to 'all' (without prompting) when stdin isn't a real terminal - e.g. this
    script is run from another script or a CI job - so automated runs never
    hang waiting for input that will never come."""
    if not sys.stdin.isatty():
        print("Non-interactive session detected - defaulting to generating HTML, Markdown, and PDF.")
        print(f"(Pass --format to choose explicitly: {_format_help()}.)")
        return FORMAT_ALIASES['all']

    print("\nWould you like to generate:")
    print("  1) HTML")
    print("  2) Markdown")
    print("  3) PDF")
    print("  4) All")

    choices = {
        '1': {'html'}, 'html': {'html'},
        '2': {'markdown'}, 'markdown': {'markdown'},
        '3': {'pdf'}, 'pdf': {'pdf'},
        '4': FORMAT_ALIASES['all'], 'all': FORMAT_ALIASES['all'],
    }

    for _ in range(3):
        try:
            answer = input("Enter choice [1-4] (default: 4): ").strip().lower()
        except EOFError:
            print("Non-interactive session detected - defaulting to All.")
            return FORMAT_ALIASES['all']
        if answer == '':
            return FORMAT_ALIASES['all']
        if answer in choices:
            return choices[answer]
        print("Please enter 1, 2, 3, or 4.")

    print("No valid selection after 3 attempts - defaulting to All.")
    return FORMAT_ALIASES['all']


def main():
    formats, remaining_args = parse_format_flag(sys.argv[1:])
    timeout, remaining_args = parse_timeout_flag(remaining_args)

    # Get CSV file from command line argument or use default
    if len(remaining_args) > 0:
        csv_file = remaining_args[0]
    else:
        csv_file = '../example-data/topgolf_qualtrics_week_responses.csv'

    # Check if CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found: {csv_file}")
        print(f"\nUsage: python generate_venue_reports.py <path_to_csv_file> [--format {_format_help()}] [--timeout SECONDS]")
        print(f"\nExamples:")
        print(f"  python generate_venue_reports.py ../example-data/topgolf_qualtrics_week_responses.csv")
        print(f"  python generate_venue_reports.py ../example-data/topgolf_qualtrics_30_responses_DALLAS.csv --format pdf")
        print(f"  python generate_venue_reports.py ../example-data/topgolf_qualtrics_week_responses.csv --timeout 600")
        sys.exit(1)

    print(f"Generating venue reports from: {csv_file}\n")
    if timeout:
        print(f"Claude timeout set to: {timeout} seconds\n")

    # Prepare environment overrides for subcommands
    env_overrides = {}
    if timeout:
        env_overrides['CLAUDE_TIMEOUT_SECONDS'] = str(timeout)

    # Step 1: Generate venue data (creates venue_data.json)
    print("STEP 1: Processing data and generating metrics...")
    if not run_command('generate_venue_data.py', [csv_file], env_overrides):
        print("\nFailed to generate venue data. Aborting.")
        sys.exit(1)

    # Step 2: Generate AI analysis once for all venues
    print("\nSTEP 2: Generating AI analysis for all venues...")
    analysis_file = 'ai_analysis_results.json'
    if not run_command('run_analyze_venues.py', ['venue_data.json', '--output', analysis_file], env_overrides):
        print("\nFailed to generate AI analysis. Aborting.")
        sys.exit(1)

    # Step 3: Ask (or use --format) which report format(s) to build
    if formats is None:
        formats = prompt_for_format()
    print(f"\nSelected format(s): {', '.join(sorted(formats))}")

    generated_files = []
    
    # Generate timestamp once for all report formats
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Step 4: Generate reports in selected format(s)
    print("\nSTEP 4: Creating reports in selected format(s)...")
    format_arg = ','.join(sorted(formats))
    if not run_command('create_single_venue_report.py', ['venue_data.json', '--format', format_arg, '--timestamp', timestamp, '--analysis', analysis_file], env_overrides):
        print("\nFailed to create reports. Aborting.")
        sys.exit(1)
    
    if 'html' in formats:
        generated_files.append("  - HTML: ../reports/Topgolf_Venue_Report_*.html")
    if 'markdown' in formats:
        generated_files.append("  - Markdown: ../reports/Topgolf_Venue_Report_*.md")
    if 'pdf' in formats:
        generated_files.append("  - PDF: ../reports/Topgolf_Venue_Report_*.pdf")

    print(f"\n{'='*60}")
    print("[SUCCESS] All venue reports generated successfully!")
    print(f"{'='*60}")
    print(f"\nGenerated files:")
    print(f"  - Metrics: venue_data.json")
    for line in generated_files:
        print(line)


if __name__ == '__main__':
    main()
