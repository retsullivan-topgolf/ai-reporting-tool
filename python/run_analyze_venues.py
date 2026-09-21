#!/usr/bin/env python3
"""
Run AI analysis for all venues in venue_data.json and save to a JSON file.

This script runs the AI analysis pipeline once for all venues, caching the
results so that multiple report formats (HTML, Markdown, PDF) can reuse the
same analysis without re-running the expensive Claude API calls.

Usage:
    python run_analyze_venues.py venue_data.json
    python run_analyze_venues.py venue_data.json --output ai_analysis_results.json
"""
import json
import sys
import os

from analyze_venues import get_ai_analysis


def main():
    # Parse command line arguments
    json_file = 'venue_data.json'
    output_file = 'ai_analysis_results.json'
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--output':
            if i + 1 >= len(sys.argv):
                print("Error: --output requires a value")
                sys.exit(1)
            output_file = sys.argv[i + 1]
            i += 2
        else:
            json_file = arg
            i += 1
    
    # Check if input file exists
    if not os.path.exists(json_file):
        print(f"Error: File not found: {json_file}")
        print(f"\nUsage: python run_analyze_venues.py <path_to_json_file> [--output <output_file>]")
        print(f"\nExamples:")
        print(f"  python run_analyze_venues.py venue_data.json")
        print(f"  python run_analyze_venues.py venue_data.json --output ai_analysis_results.json")
        print(f"\nNote: First run 'python generate_venue_data.py <csv_file>' to create venue_data.json")
        sys.exit(1)
    
    print(f"Reading venue data from: {json_file}")
    
    # Load the venue data
    with open(json_file, 'r') as f:
        venue_data = json.load(f)
    
    # Generate AI analysis for all venues
    analysis_results = {}
    total_venues = len(venue_data)
    
    for idx, venue_key in enumerate(sorted(venue_data.keys()), 1):
        data = venue_data[venue_key]
        venue_name = data['venue']
        
        print(f"\n[{idx}/{total_venues}] Analyzing {venue_name}...")
        
        ai_result, error = get_ai_analysis(data)
        
        if ai_result is not None:
            print(f"  + Analysis complete for {venue_name}")
            analysis_results[venue_key] = {
                'ai_available': True,
                'analysis': ai_result,
            }
        else:
            print(f"  - Analysis failed for {venue_name}: {error}")
            analysis_results[venue_key] = {
                'ai_available': False,
                'unavailable_reason': error,
            }
    
    # Save analysis results to file
    with open(output_file, 'w') as f:
        json.dump(analysis_results, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"AI analysis complete!")
    print(f"{'='*60}")
    print(f"\nResults saved to: {output_file}")
    print(f"Analyzed {total_venues} venue(s)")


if __name__ == '__main__':
    main()
