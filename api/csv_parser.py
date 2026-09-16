"""
CSV parsing and validation for Topgolf survey data.

Handles:
- Reading CSV files with proper encoding and header handling
- Detecting schema type (POC vs Real)
- Extracting and converting field values
- Validating data against schema
- Filtering records by date range
"""

import csv
import os
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from . import schemas


class CSVParseError(Exception):
    """Raised when CSV parsing fails."""
    pass


class SchemaDetectionError(Exception):
    """Raised when schema cannot be detected."""
    pass


def parse_csv(file_path: str) -> Tuple[List[Dict], List[str]]:
    """Read a CSV file and return rows and fieldnames.
    
    Handles Qualtrics CSV format with header rows.
    Skips the first 2 header rows (lines 1 and 2), uses line 0 as header.
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        Tuple of (list of row dicts, list of fieldnames)
        
    Raises:
        CSVParseError: If file cannot be read or parsed
    """
    if not os.path.exists(file_path):
        raise CSVParseError(f"File not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Skip the first 2 header rows (lines 1 and 2), use line 0 as header
            reader = csv.DictReader(lines)
            data = list(reader)
        
        if not data:
            raise CSVParseError(f"CSV file is empty: {file_path}")
        
        fieldnames = reader.fieldnames if hasattr(reader, 'fieldnames') else []
        
        # Filter out the header rows that got included as data
        data = [
            row for row in data 
            if row.get('Venue', '').strip() not in ['Topgolf Venue', '{"ImportId":"Venue"}', '']
        ]
        
        if not data:
            raise CSVParseError(f"No valid data rows found in CSV: {file_path}")
        
        return data, fieldnames
    
    except CSVParseError:
        raise
    except Exception as e:
        raise CSVParseError(f"Failed to parse CSV {file_path}: {str(e)}")


def detect_schema(fieldnames: List[str]) -> str:
    """Detect which schema (POC or Real) the CSV uses.
    
    Args:
        fieldnames: List of column names from CSV
        
    Returns:
        Schema name: 'poc' or 'real'
        
    Raises:
        SchemaDetectionError: If schema cannot be determined
    """
    fieldnames_str = ' '.join(fieldnames).lower()
    
    # Check for Real schema indicators
    has_fb_metrics = any('F&B Matrix' in field for field in fieldnames)
    has_combined_nps = any('Combined NPS' in field for field in fieldnames)
    has_return_likelihood = any('Likelihood to Return' in field for field in fieldnames)
    
    if has_fb_metrics and has_combined_nps and has_return_likelihood:
        return 'real'
    
    # Check for POC schema indicators
    has_q1_ltr = any('Q1_LTR' in field for field in fieldnames)
    has_q2_fun = any('Q2_FUN' in field for field in fieldnames)
    has_q3_helpful = any('Q3_HELPFUL' in field for field in fieldnames)
    
    if has_q1_ltr and has_q2_fun and has_q3_helpful:
        return 'poc'
    
    raise SchemaDetectionError(
        f"Could not detect schema. Expected either:\n"
        f"  - POC: Q1_LTR, Q2_FUN, Q3_HELPFUL, Q4_ISSUES, Q5_ISSUE_RESOLUTION, Q6_COMMENT\n"
        f"  - Real: Combined NPS, F&B Matrix_*, Likelihood to Return\n"
        f"Found columns: {', '.join(fieldnames[:10])}..."
    )


def get_field(row: Dict[str, str], field_name: str, schema_name: str) -> str:
    """Safely extract a field value from a row using schema mapping.
    
    Args:
        row: CSV row as dict
        field_name: Logical field name (e.g., 'ltr', 'fun')
        schema_name: Schema to use ('poc' or 'real')
        
    Returns:
        Field value (trimmed), or empty string if not found
    """
    schema = schemas.get_schema(schema_name)
    if not schema:
        return ''
    
    field_def = schema['fields'].get(field_name)
    if not field_def:
        return ''
    
    csv_column = field_def.get('csv_column')
    if not csv_column:
        return ''
    
    return row.get(csv_column, '').strip()


def convert_field_value(value: str, field_name: str, schema_name: str) -> any:
    """Convert a field value to its proper type.
    
    Args:
        value: Raw string value from CSV
        field_name: Logical field name
        schema_name: Schema to use
        
    Returns:
        Converted value (int, float, bool, or str), or None if conversion fails
    """
    if not value:
        return None
    
    schema = schemas.get_schema(schema_name)
    if not schema:
        return value
    
    field_def = schema['fields'].get(field_name)
    if not field_def:
        return value
    
    field_type = field_def.get('type')
    
    # Handle categorical fields with numeric mapping
    if field_type == 'categorical' and 'numeric_map' in field_def:
        return field_def['numeric_map'].get(value)
    
    # Handle integer fields
    if field_type == 'integer':
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    
    # Handle boolean fields
    if field_type == 'boolean':
        return value.lower() == 'yes'
    
    # Handle numeric fields (for ranges)
    if field_type in ['integer', 'float']:
        try:
            return int(value) if field_type == 'integer' else float(value)
        except (ValueError, TypeError):
            return None
    
    # Default: return as string
    return value


def validate_row(row: Dict[str, str], schema_name: str) -> Tuple[bool, Optional[str]]:
    """Validate a row against a schema.
    
    Args:
        row: CSV row as dict
        schema_name: Schema to validate against
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    schema = schemas.get_schema(schema_name)
    if not schema:
        return False, f"Unknown schema: {schema_name}"
    
    # Check required fields
    for field_name, field_def in schema['fields'].items():
        if field_def.get('required', False):
            value = get_field(row, field_name, schema_name)
            if not value:
                return False, f"Missing required field: {field_name}"
    
    return True, None


def extract_all_fields(row: Dict[str, str], schema_name: str) -> Dict[str, any]:
    """Extract and convert all fields from a row.
    
    Args:
        row: CSV row as dict
        schema_name: Schema to use
        
    Returns:
        Dict with all field values (converted to proper types)
    """
    schema = schemas.get_schema(schema_name)
    if not schema:
        return {}
    
    result = {}
    for field_name in schema['fields'].keys():
        value = get_field(row, field_name, schema_name)
        converted = convert_field_value(value, field_name, schema_name)
        result[field_name] = converted
    
    return result


def filter_by_date_range(rows: List[Dict[str, str]], schema_name: str, 
                         start_date: str, end_date: str) -> List[Dict[str, str]]:
    """Filter CSV rows to those within a date range (inclusive).
    
    Args:
        rows: List of CSV rows
        schema_name: Schema type ('poc' or 'real')
        start_date: Start date as string (YYYY-MM-DD format)
        end_date: End date as string (YYYY-MM-DD format)
        
    Returns:
        List of rows with visit_date within the range (inclusive)
        
    Raises:
        ValueError: If date format is invalid
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError as e:
        raise ValueError(f"Invalid date format. Expected YYYY-MM-DD: {e}")
    
    filtered = []
    for row in rows:
        date_str = get_field(row, 'visit_date', schema_name)
        if not date_str:
            continue
        
        try:
            # Try common date formats
            for fmt in ['%m/%d/%Y', '%Y-%m-%d', '%m/%d/%y']:
                try:
                    row_date = datetime.strptime(date_str, fmt).date()
                    if start <= row_date <= end:
                        filtered.append(row)
                    break
                except ValueError:
                    continue
        except Exception:
            # Skip rows with unparseable dates
            continue
    
    return filtered
