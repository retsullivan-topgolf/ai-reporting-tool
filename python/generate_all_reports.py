#!/usr/bin/env python3
"""
Generate all venue reports in one command.
This script runs generate_reports.py, then whichever of create_html_reports.py
/ create_markdown_reports.py / create_pdf_reports.py the user asks for.
"""
import subprocess
import sys
import os

SINGLE_FORMATS = ('html', 'markdown', 'pdf')
# 'both' is kept as a legacy alias (html + markdown, from before PDF support
# was added) so existing scripts/docs referencing --format both keep working.
FORMAT_ALIASES = {
    'both': {'html', 'markdown'},
    'all': {'html', 'markdown', 'pdf'},
}


def run_command(script_name, args):
    """Run a Python script and return success status"""
    try:
        # Get the directory where this script is located
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
        answer = input("Enter choice [1-4] (default: 4): ").strip().lower()
        if answer == '':
            return FORMAT_ALIASES['all']
        if answer in choices:
            return choices[answer]
        print("Please enter 1, 2, 3, or 4.")

    print("No valid selection after 3 attempts - defaulting to All.")
    return FORMAT_ALIASES['all']


def main():
    formats, remaining_args = parse_format_flag(sys.argv[1:])

    # Get CSV file from command line argument or use default
    if len(remaining_args) > 0:
        csv_file = remaining_args[0]
    else:
        csv_file = '../example-data/topgolf_qualtrics_week_responses.csv'

    # Check if CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found: {csv_file}")
        print(f"\nUsage: python generate_all_reports.py <path_to_csv_file> [--format {_format_help()}]")
        print(f"\nExamples:")
        print(f"  python generate_all_reports.py ../example-data/topgolf_qualtrics_week_responses.csv")
        print(f"  python generate_all_reports.py ../example-data/topgolf_qualtrics_30_responses_DALLAS.csv --format pdf")
        sys.exit(1)

    print(f"Generating all reports from: {csv_file}\n")

    # Step 1: Generate reports (creates venue_data.json)
    print("STEP 1: Processing CSV data and generating metrics...")
    if not run_command('generate_reports.py', [csv_file]):
        print("\nFailed to generate reports from CSV. Aborting.")
        sys.exit(1)

    # Step 2: Ask (or use --format) which report format(s) to build
    if formats is None:
        formats = prompt_for_format()
    print(f"\nSelected format(s): {', '.join(sorted(formats))}")

    generated_files = []

    if 'html' in formats:
        print("\nSTEP 2: Creating HTML reports from metrics...")
        if not run_command('create_html_reports.py', ['venue_data.json']):
            print("\nFailed to create HTML reports. Aborting.")
            sys.exit(1)
        generated_files.append("  - Reports: ../reports/Topgolf_Venue_Report_*_1PAGE.html")

    if 'markdown' in formats:
        print("\nSTEP 2: Creating Markdown reports from metrics...")
        if not run_command('create_markdown_reports.py', ['venue_data.json']):
            print("\nFailed to create Markdown reports. Aborting.")
            sys.exit(1)
        generated_files.append("  - Reports: ../reports/Topgolf_Venue_Report_*_1PAGE.md")

    if 'pdf' in formats:
        print("\nSTEP 2: Creating PDF reports from metrics...")
        if not run_command('create_pdf_reports.py', ['venue_data.json']):
            print("\nFailed to create PDF reports. Aborting.")
            sys.exit(1)
        generated_files.append("  - Reports: ../reports/Topgolf_Venue_Report_*_1PAGE.pdf")

    print(f"\n{'='*60}")
    print("[SUCCESS] All reports generated successfully!")
    print(f"{'='*60}")
    print(f"\nGenerated files:")
    print(f"  - Metrics: venue_data.json")
    for line in generated_files:
        print(line)


if __name__ == '__main__':
    main()
