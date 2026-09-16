"""
Venue data processing and metrics aggregation.

Handles:
- Grouping survey responses by venue
- Calculating aggregate metrics (averages, percentages, etc.)
- Building the final venue_data.json structure
"""

from typing import List, Dict, Optional
from . import csv_parser


class VenueProcessingError(Exception):
    """Raised when venue processing fails."""
    pass


def group_by_venue(rows: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    """Group CSV rows by venue.
    
    Args:
        rows: List of CSV rows
        
    Returns:
        Dict mapping venue name to list of rows for that venue
    """
    venues = {}
    
    for row in rows:
        venue = row.get('Venue', '').strip()
        if venue:
            if venue not in venues:
                venues[venue] = []
            venues[venue].append(row)
    
    return venues


def process_venue_data(rows: List[Dict[str, str]], schema_name: str) -> Optional[Dict]:
    """Process venue data and calculate all metrics.
    
    Handles both POC and Real schemas.
    
    Args:
        rows: List of CSV rows for a single venue
        schema_name: Schema type ('poc' or 'real')
        
    Returns:
        Dict with aggregated metrics, or None if no rows
    """
    if not rows:
        return None
    
    # Initialize results dict
    results = {
        'venue': csv_parser.get_field(rows[0], 'venue', schema_name),
        'responses': len(rows),
        'date_range': [
            min(csv_parser.get_field(r, 'visit_date', schema_name) for r in rows),
            max(csv_parser.get_field(r, 'visit_date', schema_name) for r in rows)
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
    if schema_name == 'real':
        results['return_likelihood_scores'] = []
        results['price_value_scores'] = []
        results['food_value_scores'] = []
        results['food_speed_scores'] = []
        results['food_quality_scores'] = []
        results['beverage_value_scores'] = []
        results['beverage_speed_scores'] = []
        results['beverage_quality_scores'] = []
    
    # Process each row
    for row in rows:
        # LTR (1-10 scale)
        ltr_val = csv_parser.convert_field_value(
            csv_parser.get_field(row, 'ltr', schema_name),
            'ltr',
            schema_name
        )
        if ltr_val is not None:
            results['ltr_scores'].append(ltr_val)
        
        # Fun (convert to numeric)
        fun_val = csv_parser.convert_field_value(
            csv_parser.get_field(row, 'fun', schema_name),
            'fun',
            schema_name
        )
        if fun_val is not None and 1 <= fun_val <= 5:
            results['fun_scores'].append(fun_val)
        
        # Helpful (convert to numeric)
        helpful_val = csv_parser.convert_field_value(
            csv_parser.get_field(row, 'helpful', schema_name),
            'helpful',
            schema_name
        )
        if helpful_val is not None and 1 <= helpful_val <= 5:
            results['helpful_scores'].append(helpful_val)
        
        # Issues
        issues_val = csv_parser.convert_field_value(
            csv_parser.get_field(row, 'issues', schema_name),
            'issues',
            schema_name
        )
        if issues_val:
            results['issues_count'] += 1
        
        # Resolution (only if issues = yes)
        if issues_val:
            resolution_val = csv_parser.convert_field_value(
                csv_parser.get_field(row, 'resolution', schema_name),
                'resolution',
                schema_name
            )
            if resolution_val is not None and 1 <= resolution_val <= 5:
                results['resolution_scores'].append(resolution_val)
        
        # Real schema: Return Likelihood
        if schema_name == 'real':
            return_likelihood_val = csv_parser.convert_field_value(
                csv_parser.get_field(row, 'return_likelihood', schema_name),
                'return_likelihood',
                schema_name
            )
            if return_likelihood_val is not None and 1 <= return_likelihood_val <= 5:
                results['return_likelihood_scores'].append(return_likelihood_val)
            
            # Price Value
            price_value_val = csv_parser.convert_field_value(
                csv_parser.get_field(row, 'price_value', schema_name),
                'price_value',
                schema_name
            )
            if price_value_val is not None and 1 <= price_value_val <= 5:
                results['price_value_scores'].append(price_value_val)
            
            # Food Value
            food_value_val = csv_parser.convert_field_value(
                csv_parser.get_field(row, 'food_value', schema_name),
                'food_value',
                schema_name
            )
            if food_value_val is not None and 1 <= food_value_val <= 5:
                results['food_value_scores'].append(food_value_val)
            
            # Food Speed
            food_speed_val = csv_parser.convert_field_value(
                csv_parser.get_field(row, 'food_speed', schema_name),
                'food_speed',
                schema_name
            )
            if food_speed_val is not None and 1 <= food_speed_val <= 5:
                results['food_speed_scores'].append(food_speed_val)
            
            # Food Quality
            food_quality_val = csv_parser.convert_field_value(
                csv_parser.get_field(row, 'food_quality', schema_name),
                'food_quality',
                schema_name
            )
            if food_quality_val is not None and 1 <= food_quality_val <= 5:
                results['food_quality_scores'].append(food_quality_val)
            
            # Beverage Value
            beverage_value_val = csv_parser.convert_field_value(
                csv_parser.get_field(row, 'beverage_value', schema_name),
                'beverage_value',
                schema_name
            )
            if beverage_value_val is not None and 1 <= beverage_value_val <= 5:
                results['beverage_value_scores'].append(beverage_value_val)
            
            # Beverage Speed
            beverage_speed_val = csv_parser.convert_field_value(
                csv_parser.get_field(row, 'beverage_speed', schema_name),
                'beverage_speed',
                schema_name
            )
            if beverage_speed_val is not None and 1 <= beverage_speed_val <= 5:
                results['beverage_speed_scores'].append(beverage_speed_val)
            
            # Beverage Quality
            beverage_quality_val = csv_parser.convert_field_value(
                csv_parser.get_field(row, 'beverage_quality', schema_name),
                'beverage_quality',
                schema_name
            )
            if beverage_quality_val is not None and 1 <= beverage_quality_val <= 5:
                results['beverage_quality_scores'].append(beverage_quality_val)
        
        # Comments
        comment = csv_parser.get_field(row, 'comment', schema_name)
        if comment:
            results['comments'].append({
                'ltr': ltr_val if ltr_val is not None else 0,
                'fun': fun_val if fun_val is not None else 0,
                'text': comment
            })
            
            if ltr_val is not None and ltr_val >= 8:
                results['high_ltr_comments'].append(comment)
            elif ltr_val is not None and ltr_val <= 6:
                results['low_ltr_comments'].append(comment)
    
    # Calculate averages
    results['ltr_avg'] = (
        round(sum(results['ltr_scores']) / len(results['ltr_scores']), 1)
        if results['ltr_scores'] else 0
    )
    results['fun_avg'] = (
        round(sum(results['fun_scores']) / len(results['fun_scores']), 1)
        if results['fun_scores'] else 0
    )
    results['helpful_avg'] = (
        round(sum(results['helpful_scores']) / len(results['helpful_scores']), 1)
        if results['helpful_scores'] else 0
    )
    results['issues_pct'] = (
        round((results['issues_count'] / len(rows)) * 100, 1) if rows else 0
    )
    results['resolution_avg'] = (
        round(sum(results['resolution_scores']) / len(results['resolution_scores']), 1)
        if results['resolution_scores'] else None
    )
    
    # Calculate F&B averages for real schema
    if schema_name == 'real':
        results['return_likelihood_avg'] = (
            round(sum(results['return_likelihood_scores']) / len(results['return_likelihood_scores']), 1)
            if results['return_likelihood_scores'] else None
        )
        results['price_value_avg'] = (
            round(sum(results['price_value_scores']) / len(results['price_value_scores']), 1)
            if results['price_value_scores'] else None
        )
        results['food_value_avg'] = (
            round(sum(results['food_value_scores']) / len(results['food_value_scores']), 1)
            if results['food_value_scores'] else None
        )
        results['food_speed_avg'] = (
            round(sum(results['food_speed_scores']) / len(results['food_speed_scores']), 1)
            if results['food_speed_scores'] else None
        )
        results['food_quality_avg'] = (
            round(sum(results['food_quality_scores']) / len(results['food_quality_scores']), 1)
            if results['food_quality_scores'] else None
        )
        results['beverage_value_avg'] = (
            round(sum(results['beverage_value_scores']) / len(results['beverage_value_scores']), 1)
            if results['beverage_value_scores'] else None
        )
        results['beverage_speed_avg'] = (
            round(sum(results['beverage_speed_scores']) / len(results['beverage_speed_scores']), 1)
            if results['beverage_speed_scores'] else None
        )
        results['beverage_quality_avg'] = (
            round(sum(results['beverage_quality_scores']) / len(results['beverage_quality_scores']), 1)
            if results['beverage_quality_scores'] else None
        )
    
    # Clean up temporary score lists
    for key in list(results.keys()):
        if key.endswith('_scores'):
            del results[key]
    
    return results


def build_venue_data_dict(rows: List[Dict[str, str]], schema_name: str) -> Dict[str, Dict]:
    """Build the complete venue_data dictionary from all rows.
    
    Args:
        rows: All CSV rows
        schema_name: Schema type ('poc' or 'real')
        
    Returns:
        Dict mapping venue keys to venue data dicts
    """
    venues = group_by_venue(rows)
    venue_data_dict = {}
    
    for venue_name in sorted(venues.keys()):
        venue_rows = venues[venue_name]
        if venue_rows:
            processed_data = process_venue_data(venue_rows, schema_name)
            if processed_data:
                # Create a safe key for JSON (lowercase, replace spaces with underscores)
                safe_key = venue_name.lower().replace(' ', '_')
                venue_data_dict[safe_key] = processed_data
    
    return venue_data_dict
