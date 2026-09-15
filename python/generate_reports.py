#!/usr/bin/env python3
import csv
from datetime import datetime
import json
import sys
import os

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

# Read the CSV file
with open(csv_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    # Skip the first 2 header rows (lines 1 and 2), use line 0 as header
    reader = csv.DictReader(lines)
    data = list(reader)

# Detect schema type based on available columns
def detect_schema(fieldnames):
    """Detect if this is POC (old) or Real (new) schema"""
    has_fb_metrics = any('F&B Matrix' in field for field in fieldnames)
    has_return_likelihood = any('Likelihood to Return' in field for field in fieldnames)
    has_price_value = any('Price Value' in field for field in fieldnames)
    
    if has_fb_metrics and has_return_likelihood and has_price_value:
        return 'real'
    else:
        return 'poc'

schema_type = detect_schema(reader.fieldnames if hasattr(reader, 'fieldnames') else [])
print(f"Detected schema: {schema_type}")

# Re-read the CSV file since we consumed the reader
with open(csv_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    reader = csv.DictReader(lines)
    data = list(reader)
    
# Filter out the header rows that got included as data
data = [row for row in data if row['Venue'] not in ['Topgolf Venue', '{"ImportId":"Venue"}', '']]

# Dynamically find all unique venues in the data
unique_venues = set()
for row in data:
    venue = row.get('Venue', '').strip()
    if venue:
        unique_venues.add(venue)

# Create a dictionary for each venue
venues = {venue: [] for venue in sorted(unique_venues)}

# Group data by venue
for row in data:
    venue = row.get('Venue', '').strip()
    if venue in venues:
        venues[venue].append(row)

# Field mapping for different schemas
FIELD_MAPPING = {
    'poc': {
        'venue': 'Venue',
        'visit_date': 'VisitDate',
        'ltr': 'Q1_LTR',
        'fun': 'Q2_FUN',
        'helpful': 'Q3_HELPFUL',
        'issues': 'Q4_ISSUES',
        'resolution': 'Q5_ISSUE_RESOLUTION',
        'comment': 'Q6_COMMENT',
    },
    'real': {
        'venue': 'Venue',
        'visit_date': 'Visit Date (+00:00 GMT)',
        'ltr': 'Combined NPS',
        'fun': 'Fun - How much fun did you have during your visit at Topgolf [Field-Venue_Name]?',
        'helpful': 'Helpfulness - How satisfied were you with the overall helpfulness of our staff?',
        'issues': 'Issues During Visit',
        'resolution': 'Issue Resolution Sat',
        'comment': 'Open Comment',
        'return_likelihood': 'Likelihood to Return - How likely are you to return to this or another Topgolf venue?',
        'price_value': 'Price Value - How would you rate Topgolf\'s price compared to the value of your experience...?',
        'food_value': 'F&B Matrix_1 - Value for the price you paid for food',
        'food_speed': 'F&B Matrix_2 - Speed of food service',
        'food_quality': 'F&B Matrix_3 - Food quality',
        'beverage_value': 'F&B Matrix_4 - Value for the price you paid for beverages',
        'beverage_speed': 'F&B Matrix_5 - Speed of beverage service',
        'beverage_quality': 'F&B Matrix_6 - Beverage quality',
    }
}

def get_field(row, field_name, schema):
    """Safely get a field value from a row using schema mapping"""
    mapping = FIELD_MAPPING.get(schema, {})
    col_name = mapping.get(field_name)
    if col_name:
        return row.get(col_name, '').strip()
    return ''

def process_venue_data(rows, schema):
    """Process venue data for both POC and Real schemas"""
    if not rows:
        return None
    
    results = {
        'venue': get_field(rows[0], 'venue', schema),
        'responses': len(rows),
        'date_range': [
            min(get_field(r, 'visit_date', schema) for r in rows),
            max(get_field(r, 'visit_date', schema) for r in rows)
        ],
        'ltr_scores': [],
        'fun_scores': [],
        'helpful_scores': [],
        'issues_count': 0,
        'resolution_scores': [],
        'comments': [],
        'high_ltr_comments': [],
        'low_ltr_comments': []
    }
    
    # Initialize F&B metric lists for real schema
    if schema == 'real':
        results['return_likelihood_scores'] = []
        results['price_value_scores'] = []
        results['food_value_scores'] = []
        results['food_speed_scores'] = []
        results['food_quality_scores'] = []
        results['beverage_value_scores'] = []
        results['beverage_speed_scores'] = []
        results['beverage_quality_scores'] = []
    
    for row in rows:
        # LTR (1-10 scale)
        try:
            ltr = int(get_field(row, 'ltr', schema))
            results['ltr_scores'].append(ltr)
        except:
            pass
        
        # Fun (convert text to numeric if needed)
        fun_text = get_field(row, 'fun', schema)
        if schema == 'poc':
            fun_map = {
                '5 - Extremely fun': 5,
                '4 - Very fun': 4,
                '3 - Moderately fun': 3,
                '2 - Slightly fun': 2,
                '1 - Not at all fun': 1
            }
            if fun_text in fun_map:
                results['fun_scores'].append(fun_map[fun_text])
        else:  # real schema - already numeric
            try:
                fun_val = int(fun_text)
                if 1 <= fun_val <= 5:
                    results['fun_scores'].append(fun_val)
            except:
                pass
        
        # Helpful (convert text to numeric if needed)
        helpful_text = get_field(row, 'helpful', schema)
        if schema == 'poc':
            helpful_map = {
                '5 - Extremely helpful': 5,
                '4 - Very helpful': 4,
                '3 - Moderately helpful': 3,
                '2 - Slightly helpful': 2,
                '1 - Not at all helpful': 1
            }
            if helpful_text in helpful_map:
                results['helpful_scores'].append(helpful_map[helpful_text])
        else:  # real schema - already numeric
            try:
                helpful_val = int(helpful_text)
                if 1 <= helpful_val <= 5:
                    results['helpful_scores'].append(helpful_val)
            except:
                pass
        
        # Issues
        issues_text = get_field(row, 'issues', schema).lower()
        if issues_text == 'yes':
            results['issues_count'] += 1
        
        # Resolution (only if issues = yes)
        if issues_text == 'yes':
            resolution_text = get_field(row, 'resolution', schema)
            if schema == 'poc':
                resolution_map = {
                    '5 - Extremely satisfied': 5,
                    '4 - Very satisfied': 4,
                    '3 - Moderately satisfied': 3,
                    '2 - Slightly satisfied': 2,
                    '1 - Extremely dissatisfied': 1
                }
                if resolution_text in resolution_map:
                    results['resolution_scores'].append(resolution_map[resolution_text])
            else:  # real schema - already numeric
                try:
                    resolution_val = int(resolution_text)
                    if 1 <= resolution_val <= 5:
                        results['resolution_scores'].append(resolution_val)
                except:
                    pass
        
        # Real schema: Return Likelihood (1-5 scale)
        if schema == 'real':
            try:
                return_likelihood = int(get_field(row, 'return_likelihood', schema))
                if 1 <= return_likelihood <= 5:
                    results['return_likelihood_scores'].append(return_likelihood)
            except:
                pass
            
            # Price Value (1-5 scale)
            try:
                price_value = int(get_field(row, 'price_value', schema))
                if 1 <= price_value <= 5:
                    results['price_value_scores'].append(price_value)
            except:
                pass
            
            # Food Value (1-5 scale)
            try:
                food_value = int(get_field(row, 'food_value', schema))
                if 1 <= food_value <= 5:
                    results['food_value_scores'].append(food_value)
            except:
                pass
            
            # Food Speed (1-5 scale)
            try:
                food_speed = int(get_field(row, 'food_speed', schema))
                if 1 <= food_speed <= 5:
                    results['food_speed_scores'].append(food_speed)
            except:
                pass
            
            # Food Quality (1-5 scale)
            try:
                food_quality = int(get_field(row, 'food_quality', schema))
                if 1 <= food_quality <= 5:
                    results['food_quality_scores'].append(food_quality)
            except:
                pass
            
            # Beverage Value (1-5 scale)
            try:
                beverage_value = int(get_field(row, 'beverage_value', schema))
                if 1 <= beverage_value <= 5:
                    results['beverage_value_scores'].append(beverage_value)
            except:
                pass
            
            # Beverage Speed (1-5 scale)
            try:
                beverage_speed = int(get_field(row, 'beverage_speed', schema))
                if 1 <= beverage_speed <= 5:
                    results['beverage_speed_scores'].append(beverage_speed)
            except:
                pass
            
            # Beverage Quality (1-5 scale)
            try:
                beverage_quality = int(get_field(row, 'beverage_quality', schema))
                if 1 <= beverage_quality <= 5:
                    results['beverage_quality_scores'].append(beverage_quality)
            except:
                pass
        
        # Comments
        comment = get_field(row, 'comment', schema)
        if comment:
            try:
                ltr_val = int(get_field(row, 'ltr', schema))
            except:
                ltr_val = 0
            
            fun_val = 0
            fun_text = get_field(row, 'fun', schema)
            if schema == 'poc':
                fun_map = {
                    '5 - Extremely fun': 5,
                    '4 - Very fun': 4,
                    '3 - Moderately fun': 3,
                    '2 - Slightly fun': 2,
                    '1 - Not at all fun': 1
                }
                fun_val = fun_map.get(fun_text, 0)
            else:
                try:
                    fun_val = int(fun_text)
                except:
                    fun_val = 0
            
            results['comments'].append({
                'ltr': ltr_val,
                'fun': fun_val,
                'text': comment
            })
            
            if ltr_val >= 8:
                results['high_ltr_comments'].append(comment)
            elif ltr_val <= 6:
                results['low_ltr_comments'].append(comment)
    
    # Calculate averages
    results['ltr_avg'] = round(sum(results['ltr_scores']) / len(results['ltr_scores']), 1) if results['ltr_scores'] else 0
    results['fun_avg'] = round(sum(results['fun_scores']) / len(results['fun_scores']), 1) if results['fun_scores'] else 0
    results['helpful_avg'] = round(sum(results['helpful_scores']) / len(results['helpful_scores']), 1) if results['helpful_scores'] else 0
    results['issues_pct'] = round((results['issues_count'] / len(rows)) * 100, 1) if rows else 0
    results['resolution_avg'] = round(sum(results['resolution_scores']) / len(results['resolution_scores']), 1) if results['resolution_scores'] else None
    
    # Calculate F&B averages for real schema
    if schema == 'real':
        results['return_likelihood_avg'] = round(sum(results['return_likelihood_scores']) / len(results['return_likelihood_scores']), 1) if results['return_likelihood_scores'] else None
        results['price_value_avg'] = round(sum(results['price_value_scores']) / len(results['price_value_scores']), 1) if results['price_value_scores'] else None
        results['food_value_avg'] = round(sum(results['food_value_scores']) / len(results['food_value_scores']), 1) if results['food_value_scores'] else None
        results['food_speed_avg'] = round(sum(results['food_speed_scores']) / len(results['food_speed_scores']), 1) if results['food_speed_scores'] else None
        results['food_quality_avg'] = round(sum(results['food_quality_scores']) / len(results['food_quality_scores']), 1) if results['food_quality_scores'] else None
        results['beverage_value_avg'] = round(sum(results['beverage_value_scores']) / len(results['beverage_value_scores']), 1) if results['beverage_value_scores'] else None
        results['beverage_speed_avg'] = round(sum(results['beverage_speed_scores']) / len(results['beverage_speed_scores']), 1) if results['beverage_speed_scores'] else None
        results['beverage_quality_avg'] = round(sum(results['beverage_quality_scores']) / len(results['beverage_quality_scores']), 1) if results['beverage_quality_scores'] else None
    
    # Clean up temporary score lists
    for key in list(results.keys()):
        if key.endswith('_scores'):
            del results[key]

    return results

# Process all venues
venue_data_dict = {}
for venue_name in sorted(venues.keys()):
    venue_rows = venues[venue_name]
    if venue_rows:
        processed_data = process_venue_data(venue_rows, schema_type)
        if processed_data:
            # Create a safe key for JSON (lowercase, replace spaces with underscores)
            safe_key = venue_name.lower().replace(' ', '_')
            venue_data_dict[safe_key] = processed_data
            
            print(f"\n=== {venue_name.upper()} ===")
            print(f"Responses: {processed_data['responses']}")
            print(f"LTR: {processed_data['ltr_avg']}")
            print(f"Fun: {processed_data['fun_avg']}")
            print(f"Helpful: {processed_data['helpful_avg']}")
            print(f"Issues: {processed_data['issues_pct']}%")
            print(f"Resolution: {processed_data['resolution_avg']}")
            print(f"Date Range: {processed_data['date_range']}")
            
            # Print F&B metrics if available
            if schema_type == 'real':
                print(f"Return Likelihood: {processed_data.get('return_likelihood_avg')}")
                print(f"Price Value: {processed_data.get('price_value_avg')}")
                print(f"Food Value: {processed_data.get('food_value_avg')}")
                print(f"Food Speed: {processed_data.get('food_speed_avg')}")
                print(f"Food Quality: {processed_data.get('food_quality_avg')}")
                print(f"Beverage Value: {processed_data.get('beverage_value_avg')}")
                print(f"Beverage Speed: {processed_data.get('beverage_speed_avg')}")
                print(f"Beverage Quality: {processed_data.get('beverage_quality_avg')}")

# Save to JSON for use in HTML generation
with open('venue_data.json', 'w') as f:
    json.dump(venue_data_dict, f, indent=2)

print(f"\nData saved to venue_data.json")
print(f"Processed {len(venue_data_dict)} venue(s)")
