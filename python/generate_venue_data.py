#!/usr/bin/env python3
"""
Generate venue metrics from survey data.

This script:
1. Loads survey data by identifier (e.g., 'Grand_Prairie', 'texas_venues')
2. Detects the schema type (POC or Real)
3. Parses and validates the data using the API
4. Aggregates metrics by venue
5. Saves the result to venue_data.json

Usage:
    python generate_venue_data.py Grand_Prairie
    python generate_venue_data.py texas_venues
    
To see available datasets:
    python generate_venue_data.py --list
"""

import json
import sys
import os

# Add parent directory to path to import api module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from the API module
from api import csv_parser, venue_processor, data_loader


def main():
    # Handle --list flag to show available datasets
    if len(sys.argv) > 1 and sys.argv[1] == '--list':
        try:
            datasets = data_loader.list_available_datasets()
            print("Available datasets:")
            for dataset in datasets:
                print(f"  - {dataset}")
        except data_loader.DataLoaderError as e:
            print(f"Error: {e}")
            sys.exit(1)
        return
    
    # Get dataset identifier from command line argument
    if len(sys.argv) > 1:
        data_identifier = sys.argv[1]
    else:
        # Show available datasets and ask user to choose
        try:
            datasets = data_loader.list_available_datasets()
            if not datasets:
                print("Error: No datasets available")
                sys.exit(1)
            
            print("Available datasets:")
            for i, dataset in enumerate(datasets, 1):
                print(f"  {i}) {dataset}")
            
            choice = input(f"\nSelect dataset (1-{len(datasets)}): ").strip()
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(datasets):
                    data_identifier = datasets[choice_num - 1]
                else:
                    print("Invalid choice")
                    sys.exit(1)
            except ValueError:
                print("Invalid input")
                sys.exit(1)
        except data_loader.DataLoaderError as e:
            print(f"Error: {e}")
            sys.exit(1)

    print(f"Loading dataset: {data_identifier}")

    try:
        # Step 1: Load survey data using data_loader
        rows, fieldnames = data_loader.load_survey_data(data_identifier)
        print(f"Loaded {len(rows)} rows from dataset")

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

    except data_loader.DataLoaderError as e:
        print(f"Data Loading Error: {e}")
        sys.exit(1)
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
