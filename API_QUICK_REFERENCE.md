# API Quick Reference

## Module Overview

```
api/
├── schemas.py         - Schema definitions (POC & Real)
├── csv_parser.py      - CSV parsing & validation
├── venue_processor.py - Venue aggregation & metrics
└── app.py            - Optional Flask REST API
```

## Common Tasks

### Parse a CSV and Generate Venue Data

```python
from api import csv_parser, venue_processor
import json

# Read CSV
rows, fieldnames = csv_parser.parse_csv('../qualtrics/Grand_Prarie.csv')

# Detect schema
schema = csv_parser.detect_schema(fieldnames)  # 'poc' or 'real'

# Process venues
venue_data = venue_processor.build_venue_data_dict(rows, schema)

# Save to JSON
with open('venue_data.json', 'w') as f:
    json.dump(venue_data, f, indent=2)
```

### Validate a Single Row

```python
from api import csv_parser

row = {"Venue": "Grand Prairie", "Likelihood to Return - How likely are you to return to this or another Topgolf venue?": "4", ...}
is_valid, error = csv_parser.validate_row(row, 'real')

if not is_valid:
    print(f"Validation error: {error}")
```

### Extract and Convert a Field

```python
from api import csv_parser

row = {"Likelihood to Return - How likely are you to return to this or another Topgolf venue?": "4"}
value = csv_parser.get_field(row, 'ltr', 'real')  # "4"
converted = csv_parser.convert_field_value(value, 'ltr', 'real')  # 4 (int)
```

### List Available Schemas

```python
from api import schemas

for schema_name in schemas.list_schemas():
    schema = schemas.get_schema(schema_name)
    print(f"{schema_name}: {schema['description']}")
    print(f"  Fields: {list(schema['fields'].keys())}")
```

### Get Schema Details

```python
from api import schemas

schema = schemas.get_schema('real')

# Access field info
ltr_field = schema['fields']['ltr']
print(f"CSV column: {ltr_field['csv_column']}")
print(f"Type: {ltr_field['type']}")
print(f"Range: {ltr_field['range']}")
```

## API Functions

### csv_parser

| Function | Returns | Raises |
|----------|---------|--------|
| `parse_csv(path)` | (rows, fieldnames) | CSVParseError |
| `detect_schema(fieldnames)` | 'poc' \| 'real' | SchemaDetectionError |
| `get_field(row, field, schema)` | str | - |
| `convert_field_value(value, field, schema)` | int\|float\|bool\|str\|None | - |
| `validate_row(row, schema)` | (bool, error_msg) | - |
| `extract_all_fields(row, schema)` | dict | - |

### venue_processor

| Function | Returns |
|----------|---------|
| `group_by_venue(rows)` | dict[venue_name → rows] |
| `process_venue_data(rows, schema)` | dict with metrics |
| `build_venue_data_dict(rows, schema)` | dict[venue_key → venue_data] |

### schemas

| Function | Returns |
|----------|---------|
| `get_schema(name)` | schema dict \| None |
| `list_schemas()` | list of schema names |

## Error Handling

```python
from api import csv_parser

try:
    rows, fieldnames = csv_parser.parse_csv(csv_file)
except csv_parser.CSVParseError as e:
    print(f"CSV error: {e}")

try:
    schema = csv_parser.detect_schema(fieldnames)
except csv_parser.SchemaDetectionError as e:
    print(f"Schema error: {e}")
```

## REST API Endpoints

### Start Server
```bash
cd api
python app.py --port 5000
```

### GET /api/health
```bash
curl http://localhost:5000/api/health
```

### GET /api/schemas
```bash
curl http://localhost:5000/api/schemas
```

### POST /api/parse-csv (File Upload)
```bash
curl -F "file=@Grand_Prarie.csv" \
  http://localhost:5000/api/parse-csv
```

### POST /api/parse-csv (File Path)
```bash
curl -X POST http://localhost:5000/api/parse-csv \
  -H "Content-Type: application/json" \
  -d '{"csv_path": "/path/to/file.csv"}'
```

### POST /api/validate-row
```bash
curl -X POST http://localhost:5000/api/validate-row \
  -H "Content-Type: application/json" \
  -d '{
    "schema": "real",
    "row": {"Venue": "Grand Prairie", "Combined NPS": "8"}
  }'
```

## Schema Comparison

### POC Schema
- **LTR**: Q1_LTR (1-10 integer)
- **Fun**: Q2_FUN (5-point categorical text)
- **Helpful**: Q3_HELPFUL (5-point categorical text)
- **Issues**: Q4_ISSUES (yes/no)
- **Resolution**: Q5_ISSUE_RESOLUTION (5-point categorical text)
- **Comment**: Q6_COMMENT (text)

### Real Schema
- **LTR**: Likelihood to Return field (1-5 integer)
- **NPS**: Combined NPS (1-10 integer, Qualtrics-computed)
- **Fun**: Fun field (1-5 integer)
- **Helpful**: Helpfulness field (1-5 integer)
- **Issues**: Issues During Visit (yes/no)
- **Resolution**: Issue Resolution Sat (1-5 integer)
- **Comment**: Open Comment (text)
- **Plus F&B metrics**: Food/Beverage Value, Speed, Quality (1-5 integers)
- **Plus**: Price Value (1-5 integer)

## Output Structure

```json
{
  "grand_prairie": {
    "venue": "Grand Prairie",
    "responses": 475,
    "date_range": ["1/16/2026 0:00", "9/8/2026 0:00"],
    "ltr_avg": 4.3,
    "nps_avg": 8.3,
    "fun_avg": 4.4,
    "helpful_avg": 4.2,
    "issues_count": 125,
    "issues_pct": 26.3,
    "resolution_avg": 2.6,
    "price_value_avg": 3.2,
    "food_value_avg": 3.8,
    "food_speed_avg": 4.1,
    "food_quality_avg": 4.1,
    "beverage_value_avg": 3.8,
    "beverage_speed_avg": 4.0,
    "beverage_quality_avg": 4.2,
    "comments": [
      {"ltr": 8, "fun": 4, "text": "..."},
      ...
    ],
    "high_ltr_comments": ["..."],
    "low_ltr_comments": ["..."]
  }
}
```

## Integration with Report Generation

The `python/generate_reports.py` script automatically uses the API:

```bash
cd python
python generate_reports.py ../qualtrics/Grand_Prarie.csv
# Outputs: venue_data.json
```

Then use with report generation:

```bash
python generate_all_reports.py ../qualtrics/Grand_Prarie.csv --format all
```

## Tips

1. **Schema detection is automatic** - Just call `detect_schema(fieldnames)` and it returns 'poc' or 'real'

2. **Field extraction is safe** - `get_field()` returns empty string if field not found, never raises

3. **Type conversion is lenient** - `convert_field_value()` returns None if conversion fails, doesn't raise

4. **Validation is optional** - Use `validate_row()` to check before processing, or just process directly

5. **Comments are categorized** - Automatically split into `high_ltr_comments` (≥8) and `low_ltr_comments` (≤6)

6. **Metrics are pre-calculated** - All averages and percentages computed in `process_venue_data()`

## See Also

- `AGENTS.md` - Full API documentation
- `API_REFACTORING_SUMMARY.md` - Detailed refactoring notes
- `api/schemas.py` - Schema definitions
- `api/csv_parser.py` - Parsing functions
- `api/venue_processor.py` - Processing functions
