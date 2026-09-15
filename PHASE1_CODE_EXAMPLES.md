# Phase 1: Schema Detection & Field Mapping - Code Examples

This document provides concrete code examples for implementing Phase 1.

---

## Overview

Phase 1 adds three key functions to `python/generate_reports.py`:

1. **`detect_schema(csv_file)`** - Determine which schema is being used
2. **`normalize_row(row, schema)`** - Convert row to normalized format
3. **`process_venue_data(rows, schema)`** - Process rows with schema awareness

---

## Function 1: Schema Detection

```python
def detect_schema(csv_file):
    """
    Auto-detect which schema is being used by checking for key fields.
    
    Returns: 'poc' or 'real'
    """
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        first_row = next(reader, None)
        
        if first_row is None:
            raise ValueError("CSV file is empty")
        
        # Check for schema-specific fields
        if 'Combined NPS' in first_row:
            return 'real'
        elif 'Q1_LTR' in first_row:
            return 'poc'
        else:
            raise ValueError(f"Unknown schema. Expected either 'Q1_LTR' (POC) or 'Combined NPS' (Real)")
```

**Usage:**
```python
schema = detect_schema('../example-data/topgolf_qualtrics_30_responses - DALLAS.csv')
print(schema)  # Output: 'poc'

schema = detect_schema('../qualtrics/Grand_Prarie.csv')
print(schema)  # Output: 'real'
```

---

## Function 2: Field Mapping

```python
# Define field mappings at module level
FIELD_MAPPINGS = {
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
        'fun': 'Fun',
        'helpful': 'Helpfulness',
        'issues': 'Issues During Visit',
        'resolution': 'Issue Resolution Sat',
        'comment': 'Open Comment',
        # F&B fields (optional)
        'food_value': 'F&B Matrix_1 - Value for the price you paid for food',
        'beverage_value': 'F&B Matrix_4 - Value for the price you paid for beverages',
        'food_speed': 'F&B Matrix_2 - Speed of food service',
        'beverage_speed': 'F&B Matrix_5 - Speed of beverage service',
        'food_quality': 'F&B Matrix_3 - Food quality',
        'beverage_quality': 'F&B Matrix_6 - Beverage quality',
        # Customer intent fields (optional)
        'return_likelihood': 'Likelihood to Return - How likely are you to return to this or another Topgolf venue?',
        'price_value': 'Price Value - How would you rate Topgolf\'s price compared to the value of your experience...?',
    }
}

def get_field_value(row, schema, field_key):
    """
    Get a field value from a row, handling both schemas.
    
    Args:
        row: CSV row dict
        schema: 'poc' or 'real'
        field_key: normalized field name (e.g., 'ltr', 'fun', 'comment')
    
    Returns:
        Field value or None if not present
    """
    field_name = FIELD_MAPPINGS[schema].get(field_key)
    if field_name is None:
        return None
    return row.get(field_name, '').strip()
```

**Usage:**
```python
row = {'Q1_LTR': '9', 'Q2_FUN': '5 - Extremely fun', ...}
ltr = get_field_value(row, 'poc', 'ltr')
print(ltr)  # Output: '9'

row = {'Combined NPS': '8', 'Fun': '4', ...}
ltr = get_field_value(row, 'real', 'ltr')
print(ltr)  # Output: '8'
```

---

## Function 3: Row Normalization

```python
def parse_date(date_str, schema):
    """
    Parse date string based on schema format.
    
    POC format: YYYY-MM-DD (e.g., "2026-08-01")
    Real format: M/D/YYYY (e.g., "6/21/2026")
    
    Returns: normalized date string (YYYY-MM-DD)
    """
    if not date_str:
        return None
    
    try:
        if schema == 'poc':
            # Already in correct format
            return date_str
        elif schema == 'real':
            # Convert M/D/YYYY to YYYY-MM-DD
            from datetime import datetime
            dt = datetime.strptime(date_str, '%m/%d/%Y')
            return dt.strftime('%Y-%m-%d')
    except:
        return None

def convert_fun_to_numeric(fun_value, schema):
    """
    Convert fun value to numeric 1-5 scale.
    
    POC: Text labels ("5 - Extremely fun" → 5)
    Real: Already numeric (4 → 4)
    
    Returns: int 1-5 or None
    """
    if not fun_value:
        return None
    
    if schema == 'poc':
        # Text to numeric conversion
        fun_map = {
            '5 - Extremely fun': 5,
            '4 - Very fun': 4,
            '3 - Moderately fun': 3,
            '2 - Slightly fun': 2,
            '1 - Not at all fun': 1
        }
        return fun_map.get(fun_value.strip())
    elif schema == 'real':
        # Already numeric
        try:
            return int(fun_value)
        except:
            return None

def convert_helpful_to_numeric(helpful_value, schema):
    """
    Convert helpful value to numeric 1-5 scale.
    
    POC: Text labels ("5 - Extremely helpful" → 5)
    Real: Already numeric (5 → 5)
    
    Returns: int 1-5 or None
    """
    if not helpful_value:
        return None
    
    if schema == 'poc':
        # Text to numeric conversion
        helpful_map = {
            '5 - Extremely helpful': 5,
            '4 - Very helpful': 4,
            '3 - Moderately helpful': 3,
            '2 - Slightly helpful': 2,
            '1 - Not at all helpful': 1
        }
        return helpful_map.get(helpful_value.strip())
    elif schema == 'real':
        # Already numeric
        try:
            return int(helpful_value)
        except:
            return None

def normalize_row(row, schema):
    """
    Convert a CSV row to normalized format, handling both schemas.
    
    Returns a dict with normalized field names and converted values.
    """
    normalized = {
        'venue': get_field_value(row, schema, 'venue'),
        'visit_date': parse_date(get_field_value(row, schema, 'visit_date'), schema),
        'ltr': get_field_value(row, schema, 'ltr'),
        'fun': convert_fun_to_numeric(get_field_value(row, schema, 'fun'), schema),
        'helpful': convert_helpful_to_numeric(get_field_value(row, schema, 'helpful'), schema),
        'issues': get_field_value(row, schema, 'issues'),
        'resolution': get_field_value(row, schema, 'resolution'),
        'comment': get_field_value(row, schema, 'comment'),
    }
    
    # Add optional F&B fields (real schema only)
    if schema == 'real':
        normalized['food_value'] = get_field_value(row, schema, 'food_value')
        normalized['beverage_value'] = get_field_value(row, schema, 'beverage_value')
        normalized['food_speed'] = get_field_value(row, schema, 'food_speed')
        normalized['beverage_speed'] = get_field_value(row, schema, 'beverage_speed')
        normalized['food_quality'] = get_field_value(row, schema, 'food_quality')
        normalized['beverage_quality'] = get_field_value(row, schema, 'beverage_quality')
        normalized['return_likelihood'] = get_field_value(row, schema, 'return_likelihood')
        normalized['price_value'] = get_field_value(row, schema, 'price_value')
    
    return normalized
```

**Usage:**
```python
# POC row
poc_row = {
    'Venue': 'Dallas',
    'VisitDate': '2026-08-01',
    'Q1_LTR': '9',
    'Q2_FUN': '5 - Extremely fun',
    'Q3_HELPFUL': '5 - Extremely helpful',
    'Q4_ISSUES': 'No',
    'Q5_ISSUE_RESOLUTION': '',
    'Q6_COMMENT': 'Great experience!'
}
normalized = normalize_row(poc_row, 'poc')
print(normalized)
# Output: {
#     'venue': 'Dallas',
#     'visit_date': '2026-08-01',
#     'ltr': '9',
#     'fun': 5,
#     'helpful': 5,
#     'issues': 'No',
#     'resolution': '',
#     'comment': 'Great experience!'
# }

# Real row
real_row = {
    'Venue': 'Grand Prairie',
    'Visit Date (+00:00 GMT)': '6/21/2026',
    'Combined NPS': '8',
    'Fun': '4',
    'Helpfulness': '5',
    'Issues During Visit': 'No',
    'Issue Resolution Sat': '',
    'Open Comment': 'Very clean!',
    'F&B Matrix_1 - Value for the price you paid for food': '4',
    'F&B Matrix_4 - Value for the price you paid for beverages': '3',
    # ... other F&B fields
}
normalized = normalize_row(real_row, 'real')
print(normalized)
# Output: {
#     'venue': 'Grand Prairie',
#     'visit_date': '2026-06-21',
#     'ltr': '8',
#     'fun': 4,
#     'helpful': 5,
#     'issues': 'No',
#     'resolution': '',
#     'comment': 'Very clean!',
#     'food_value': '4',
#     'beverage_value': '3',
#     # ... other F&B fields
# }
```

---

## Function 4: Updated process_venue_data

```python
def process_venue_data(rows, schema):
    """
    Process venue data with schema awareness.
    
    Normalizes all rows, then calculates metrics.
    """
    if not rows:
        return None
    
    # Normalize all rows
    normalized_rows = [normalize_row(row, schema) for row in rows]
    
    # Filter out invalid rows (missing critical fields)
    normalized_rows = [
        row for row in normalized_rows 
        if row['venue'] and row['visit_date'] and row['ltr']
    ]
    
    if not normalized_rows:
        return None
    
    results = {
        'venue': normalized_rows[0]['venue'],
        'responses': len(normalized_rows),
        'date_range': (
            min(r['visit_date'] for r in normalized_rows if r['visit_date']),
            max(r['visit_date'] for r in normalized_rows if r['visit_date'])
        ),
        'ltr_scores': [],
        'fun_scores': [],
        'helpful_scores': [],
        'issues_count': 0,
        'resolution_scores': [],
        'comments': [],
        'high_ltr_comments': [],
        'low_ltr_comments': [],
        # F&B scores (optional)
        'food_value_scores': [],
        'beverage_value_scores': [],
        'food_speed_scores': [],
        'beverage_speed_scores': [],
        'food_quality_scores': [],
        'beverage_quality_scores': [],
        'return_likelihood_scores': [],
        'price_value_scores': [],
    }
    
    for row in normalized_rows:
        # LTR (1-10 or 0-10 scale)
        try:
            ltr = int(row['ltr'])
            results['ltr_scores'].append(ltr)
        except:
            pass
        
        # Fun (already numeric 1-5)
        if row['fun']:
            try:
                results['fun_scores'].append(int(row['fun']))
            except:
                pass
        
        # Helpful (already numeric 1-5)
        if row['helpful']:
            try:
                results['helpful_scores'].append(int(row['helpful']))
            except:
                pass
        
        # Issues
        if row['issues'].lower() == 'yes':
            results['issues_count'] += 1
            # Resolution (only if issues=yes)
            if row['resolution']:
                try:
                    results['resolution_scores'].append(int(row['resolution']))
                except:
                    pass
        
        # Comments
        if row['comment']:
            results['comments'].append(row['comment'])
            # Categorize by LTR
            try:
                ltr = int(row['ltr'])
                if ltr >= 8:
                    results['high_ltr_comments'].append(row['comment'])
                elif ltr <= 5:
                    results['low_ltr_comments'].append(row['comment'])
            except:
                pass
        
        # F&B scores (optional, only if present)
        if row.get('food_value'):
            try:
                results['food_value_scores'].append(int(row['food_value']))
            except:
                pass
        
        if row.get('beverage_value'):
            try:
                results['beverage_value_scores'].append(int(row['beverage_value']))
            except:
                pass
        
        if row.get('food_speed'):
            try:
                results['food_speed_scores'].append(int(row['food_speed']))
            except:
                pass
        
        if row.get('beverage_speed'):
            try:
                results['beverage_speed_scores'].append(int(row['beverage_speed']))
            except:
                pass
        
        if row.get('food_quality'):
            try:
                results['food_quality_scores'].append(int(row['food_quality']))
            except:
                pass
        
        if row.get('beverage_quality'):
            try:
                results['beverage_quality_scores'].append(int(row['beverage_quality']))
            except:
                pass
        
        if row.get('return_likelihood'):
            try:
                results['return_likelihood_scores'].append(int(row['return_likelihood']))
            except:
                pass
        
        if row.get('price_value'):
            try:
                results['price_value_scores'].append(int(row['price_value']))
            except:
                pass
    
    return results
```

---

## Integration into Main Script

Update the main script to use schema detection:

```python
# At the top of generate_reports.py, after imports:

# Get CSV file from command line argument or use default
if len(sys.argv) > 1:
    csv_file = sys.argv[1]
else:
    csv_file = '../example-data/topgolf_qualtrics_week_responses.csv'

# Check if file exists
if not os.path.exists(csv_file):
    print(f"Error: File not found: {csv_file}")
    sys.exit(1)

print(f"Reading data from: {csv_file}")

# Detect schema
schema = detect_schema(csv_file)
print(f"Detected schema: {schema}")

# Read the CSV file
with open(csv_file, 'r') as f:
    lines = f.readlines()
    reader = csv.DictReader(lines)
    data = list(reader)

# Filter out header rows
data = [row for row in data if row.get('Venue') not in ['Topgolf Venue', '{"ImportId":"Venue"}', '']]

# Dynamically find all unique venues
unique_venues = set()
for row in data:
    venue = normalize_row(row, schema).get('venue', '').strip()
    if venue:
        unique_venues.add(venue)

# Create a dictionary for each venue
venues = {venue: [] for venue in sorted(unique_venues)}

# Group data by venue
for row in data:
    venue = normalize_row(row, schema).get('venue', '').strip()
    if venue in venues:
        venues[venue].append(row)

# Process data for each venue (using schema-aware function)
venue_data_list = []
for venue_name, venue_rows in venues.items():
    venue_data = process_venue_data(venue_rows, schema)
    if venue_data:
        venue_data_list.append(venue_data)

# Continue with rest of script...
```

---

## Testing Phase 1

Create a simple test file to verify the functions work:

```python
# test_phase1.py
import csv
from generate_reports import detect_schema, normalize_row, process_venue_data

# Test 1: Schema detection
print("Test 1: Schema Detection")
poc_schema = detect_schema('../example-data/topgolf_qualtrics_30_responses - DALLAS.csv')
print(f"  POC schema: {poc_schema}")
assert poc_schema == 'poc', "POC schema detection failed"

real_schema = detect_schema('../qualtrics/Grand_Prarie.csv')
print(f"  Real schema: {real_schema}")
assert real_schema == 'real', "Real schema detection failed"
print("  ✓ Schema detection passed\n")

# Test 2: Row normalization
print("Test 2: Row Normalization")
with open('../example-data/topgolf_qualtrics_30_responses - DALLAS.csv', 'r') as f:
    reader = csv.DictReader(f)
    poc_row = next(reader)
    normalized = normalize_row(poc_row, 'poc')
    print(f"  POC row normalized: {normalized['venue']}, {normalized['ltr']}, {normalized['fun']}")
    assert normalized['fun'] in [1, 2, 3, 4, 5], "Fun conversion failed"

with open('../qualtrics/Grand_Prarie.csv', 'r') as f:
    reader = csv.DictReader(f)
    real_row = next(reader)
    normalized = normalize_row(real_row, 'real')
    print(f"  Real row normalized: {normalized['venue']}, {normalized['ltr']}, {normalized['fun']}")
    assert isinstance(normalized['fun'], int), "Fun should be numeric"

print("  ✓ Row normalization passed\n")

# Test 3: Metrics calculation
print("Test 3: Metrics Calculation")
with open('../example-data/topgolf_qualtrics_30_responses - DALLAS.csv', 'r') as f:
    reader = csv.DictReader(f)
    poc_rows = list(reader)
    venue_data = process_venue_data(poc_rows, 'poc')
    print(f"  POC venue: {venue_data['venue']}, responses: {venue_data['responses']}")
    print(f"  LTR avg: {sum(venue_data['ltr_scores']) / len(venue_data['ltr_scores']):.2f}")
    print(f"  Fun avg: {sum(venue_data['fun_scores']) / len(venue_data['fun_scores']):.2f}")

with open('../qualtrics/Grand_Prarie.csv', 'r') as f:
    reader = csv.DictReader(f)
    real_rows = list(reader)
    venue_data = process_venue_data(real_rows, 'real')
    print(f"  Real venue: {venue_data['venue']}, responses: {venue_data['responses']}")
    print(f"  LTR avg: {sum(venue_data['ltr_scores']) / len(venue_data['ltr_scores']):.2f}")
    if venue_data['food_value_scores']:
        print(f"  Food Value avg: {sum(venue_data['food_value_scores']) / len(venue_data['food_value_scores']):.2f}")

print("  ✓ Metrics calculation passed\n")

print("All tests passed! ✓")
```

---

## Summary

Phase 1 adds:
1. **`detect_schema()`** - Auto-detect POC vs Real schema
2. **`normalize_row()`** - Convert any row to normalized format
3. **`process_venue_data()`** - Calculate metrics with schema awareness
4. **Field mappings** - Define field names for both schemas
5. **Data conversion** - Handle text-to-numeric conversions, date formats

This foundation enables Phases 2-6 to work seamlessly with both schemas.

