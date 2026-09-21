#!/usr/bin/env python3
"""
Generate venue metrics from survey data.

This script:
1. Loads survey data (defaults to texas_venues, can filter by venue)
2. Detects the schema type (POC or Real)
3. Parses and validates the data using the API
4. Aggregates metrics by venue
5. Saves the result to venue_data.json

Usage:
    python generate_venue_data.py                    # Load all venues from texas_venues
    python generate_venue_data.py "Grand Prairie"    # Load only Grand Prairie from texas_venues
    python generate_venue_data.py --dataset Grand_Prairie  # Load from Grand_Prairie.csv (backward compat)
    python generate_venue_data.py --list             # List available datasets
    python generate_venue_data.py --venues           # List available venues
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
    
    # Handle --venues flag to show available venues
    if len(sys.argv) > 1 and sys.argv[1] == '--venues':
        try:
            venues = data_loader.list_available_venues()
            print("Available venues in texas_venues:")
            for venue in venues:
                print(f"  - {venue}")
        except data_loader.DataLoaderError as e:
            print(f"Error: {e}")
            sys.exit(1)
        return
    
    # Parse command line arguments
    dataset = None
    venue = None
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--dataset':
            if i + 1 < len(sys.argv):
                dataset = sys.argv[i + 1]
                i += 2
            else:
                print("Error: --dataset requires a value")
                sys.exit(1)
        else:
            # Treat as venue name
            venue = arg
            i += 1
    
    # If no venue specified, ask user
    if venue is None and dataset is None:
        try:
            venues = data_loader.list_available_venues()
            if not venues:
                print("Error: No venues available")
                sys.exit(1)
            
            print("Available venues in texas_venues:")
            for i, v in enumerate(venues, 1):
                print(f"  {i}) {v}")
            
            choice = input(f"\nSelect venue (1-{len(venues)}) or press Enter for all: ").strip()
            if choice:
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(venues):
                        venue = venues[choice_num - 1]
                    else:
                        print("Invalid choice")
                        sys.exit(1)
                except ValueError:
                    print("Invalid input")
                    sys.exit(1)
        except data_loader.DataLoaderError as e:
            print(f"Error: {e}")
            sys.exit(1)

    # Display what we're loading
    if dataset:
        print(f"Loading dataset: {dataset}")
    elif venue:
        print(f"Loading venue: {venue} from texas_venues")
    else:
        print(f"Loading all venues from texas_venues")

    try:
        # Step 1: Load survey data using data_loader
        rows, fieldnames = data_loader.load_survey_data(dataset=dataset, venue=venue)
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
