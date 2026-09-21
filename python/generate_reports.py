#!/usr/bin/env python3
"""
Generate venue metrics from CSV survey data.

This script:
1. Reads a CSV file from the qualtrics folder
2. Detects the schema type (POC or Real)
3. Parses and validates the data using the API
4. Aggregates metrics by venue
5. Saves the result to venue_data.json

Usage:
    python generate_reports.py ../qualtrics/Grand_Prarie.csv
    python generate_reports.py ../qualtrics/texas_venues.csv
"""

import json
import sys
import os

# Add parent directory to path to import api module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from the API module
from api import csv_parser, venue_processor


def main():
    # Get CSV file from command line argument or use default
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = '../example-data/topgolf_qualtrics_week_responses.csv'

    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"Error: File not found: {csv_file}")
        print(f"\nUsage: python generate_reports.py <path_to_csv_file>")
        print(f"\nExamples:")
        print(f"  python generate_reports.py ../qualtrics/Grand_Prarie.csv")
        print(f"  python generate_reports.py ../qualtrics/texas_venues.csv")
        sys.exit(1)

    print(f"Reading data from: {csv_file}")

    try:
        # Step 1: Parse CSV
        rows, fieldnames = csv_parser.parse_csv(csv_file)
        print(f"Loaded {len(rows)} rows from CSV")

        # Step 2: Detect schema
        schema_type = csv_parser.detect_schema(fieldnames)
        print(f"Detected schema: {schema_type}")

        # Step 3: Build venue data dictionary
        venue_data_dict = venue_processor.build_venue_data_dict(rows, schema_type)

        # Step 4: Print summary for each venue
        for venue_name in sorted(venue_data_dict.keys()):
            processed_data = venue_data_dict[venue_name]
            
            print(f"\n=== {processed_data['venue'].upper()} ===")
            print(f"Responses: {processed_data['responses']}")
            print(f"NPS: {processed_data.get('nps_avg')}")
            print(f"LTR: {processed_data['ltr_avg']}")
            print(f"Fun: {processed_data['fun_avg']}")
            print(f"Helpful: {processed_data['helpful_avg']}")
            print(f"Issues: {processed_data['issues_pct']}%")
            print(f"Resolution: {processed_data['resolution_avg']}")
            print(f"Date Range: {processed_data['date_range']}")
            
            # Print F&B metrics if available
            if schema_type == 'real':
             
                print(f"Price Value: {processed_data.get('price_value_avg')}")
                print(f"Food Value: {processed_data.get('food_value_avg')}")
                print(f"Food Speed: {processed_data.get('food_speed_avg')}")
                print(f"Food Quality: {processed_data.get('food_quality_avg')}")
                print(f"Beverage Value: {processed_data.get('beverage_value_avg')}")
                print(f"Beverage Speed: {processed_data.get('beverage_speed_avg')}")
                print(f"Beverage Quality: {processed_data.get('beverage_quality_avg')}")

        # Step 5: Save to JSON
        with open('venue_data.json', 'w') as f:
            json.dump(venue_data_dict, f, indent=2)

        print(f"\nData saved to venue_data.json")
        print(f"Processed {len(venue_data_dict)} venue(s)")

    except csv_parser.CSVParseError as e:
        print(f"CSV Parse Error: {e}")
        sys.exit(1)
    except csv_parser.SchemaDetectionError as e:
        print(f"Schema Detection Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
