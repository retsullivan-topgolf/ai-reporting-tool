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
    print(f"  python generate_reports.py ../example-data/topgolf_qualtrics_week_responses.csv")
    print(f"  python generate_reports.py ../example-data/topgolf_qualtrics_30_responses_DALLAS.csv")
    sys.exit(1)

print(f"Reading data from: {csv_file}")

# Read the CSV file
with open(csv_file, 'r') as f:
    lines = f.readlines()
    # Skip the first 2 header rows (lines 1 and 2), use line 0 as header
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

# Process data for each venue
def process_venue_data(rows):
    if not rows:
        return None
    
    results = {
        'venue': rows[0]['Venue'],
        'responses': len(rows),
        'date_range': (min(r['VisitDate'] for r in rows), max(r['VisitDate'] for r in rows)),
        'ltr_scores': [],
        'fun_scores': [],
        'helpful_scores': [],
        'issues_count': 0,
        'resolution_scores': [],
        'comments': [],
        'high_ltr_comments': [],
        'low_ltr_comments': []
    }
    
    for row in rows:
        # LTR (1-10 scale)
        try:
            ltr = int(row['Q1_LTR'])
            results['ltr_scores'].append(ltr)
        except:
            pass
        
        # Fun (convert text to numeric)
        fun_map = {
            '5 - Extremely fun': 5,
            '4 - Very fun': 4,
            '3 - Moderately fun': 3,
            '2 - Slightly fun': 2,
            '1 - Not at all fun': 1
        }
        fun_text = row['Q2_FUN'].strip()
        if fun_text in fun_map:
            results['fun_scores'].append(fun_map[fun_text])
        
        # Helpful (convert text to numeric)
        helpful_map = {
            '5 - Extremely helpful': 5,
            '4 - Very helpful': 4,
            '3 - Moderately helpful': 3,
            '2 - Slightly helpful': 2,
            '1 - Not at all helpful': 1
        }
        helpful_text = row['Q3_HELPFUL'].strip()
        if helpful_text in helpful_map:
            results['helpful_scores'].append(helpful_map[helpful_text])
        
        # Issues
        if row['Q4_ISSUES'].strip().lower() == 'yes':
            results['issues_count'] += 1
        
        # Resolution (only if issues = yes)
        if row['Q4_ISSUES'].strip().lower() == 'yes':
            resolution_map = {
                '5 - Extremely satisfied': 5,
                '4 - Very satisfied': 4,
                '3 - Moderately satisfied': 3,
                '2 - Slightly satisfied': 2,
                '1 - Extremely dissatisfied': 1
            }
            resolution_text = row['Q5_ISSUE_RESOLUTION'].strip()
            if resolution_text in resolution_map:
                results['resolution_scores'].append(resolution_map[resolution_text])
        
        # Comments
        comment = row['Q6_COMMENT'].strip()
        if comment:
            ltr_val = int(row['Q1_LTR'])
            fun_val = fun_map.get(fun_text, 0)
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
    results['resolution_avg'] = round(sum(results['resolution_scores']) / len(results['resolution_scores']), 1) if results['resolution_scores'] else 0
    
    return results

# Process all venues
venue_data_dict = {}
for venue_name in sorted(venues.keys()):
    venue_rows = venues[venue_name]
    if venue_rows:
        processed_data = process_venue_data(venue_rows)
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

# Save to JSON for use in HTML generation
with open('venue_data.json', 'w') as f:
    json.dump(venue_data_dict, f, indent=2)

print(f"\nData saved to venue_data.json")
print(f"Processed {len(venue_data_dict)} venue(s)")
