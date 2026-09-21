"""
Venue data processing and metrics aggregation.

Handles:
- Grouping survey responses by venue
- Calculating aggregate metrics (averages, percentages, etc.)
- Building the final venue_data.json structure
- Period-based aggregation and comparison
- Composite scoring for venue ranking
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime
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
        results['nps_scores'] = []
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
        
        # Real schema: Combined NPS
        if schema_name == 'real':
            nps_val = csv_parser.convert_field_value(
                csv_parser.get_field(row, 'nps', schema_name),
                'nps',
                schema_name
            )
            if nps_val is not None and 1 <= nps_val <= 10:
                results['nps_scores'].append(nps_val)
            
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
            
            if ltr_val is not None and ltr_val >= 4:
                results['high_ltr_comments'].append(comment)
            elif ltr_val is not None and ltr_val <= 2:
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
        results['nps_avg'] = (
            round(sum(results['nps_scores']) / len(results['nps_scores']), 1)
            if results['nps_scores'] else None
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


def get_period_type(start_date: str, end_date: str) -> str:
    """Determine if a date range is a month or quarter.
    
    Args:
        start_date: Start date as string (YYYY-MM-DD format)
        end_date: End date as string (YYYY-MM-DD format)
        
    Returns:
        'month' or 'quarter' based on the date range
        
    Raises:
        ValueError: If dates are invalid
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError as e:
        raise ValueError(f"Invalid date format. Expected YYYY-MM-DD: {e}")
    
    # Calculate days between dates
    days = (end - start).days + 1
    
    # Month: ~28-31 days
    if 25 <= days <= 32:
        return 'month'
    
    # Quarter: ~90-92 days
    if 88 <= days <= 93:
        return 'quarter'
    
    # Default to 'month' for other ranges
    return 'month'


def calculate_composite_score(venue_data: Dict, schema_name: str) -> float:
    """Calculate composite performance score for venue ranking.

    Combined NPS (Qualtrics-computed) is used directly as the ranking score,
    since it is already a composite of underlying satisfaction signals -
    blending it into an additional weighted formula on top of Fun/F&B/
    Resolution would double-count that signal. Only the 'real' schema has an
    NPS field; other schemas have no composite ranking score.
    
    Args:
        venue_data: Venue metrics dict
        schema_name: Schema type ('poc' or 'real')
        
    Returns:
        Composite score (0-10, matching the Combined NPS scale), or None if
        unavailable
    """
    if schema_name != 'real':
        return None
    
    nps = venue_data.get('nps_avg')
    if nps is None:
        return None
    
    return round(nps, 2)


def calculate_period_summary(rows: List[Dict[str, str]], schema_name: str,
                            start_date: str, end_date: str) -> Dict:
    """Calculate aggregated metrics across all venues for a period.
    
    Args:
        rows: CSV rows for the period
        schema_name: Schema type ('poc' or 'real')
        start_date: Period start date (YYYY-MM-DD)
        end_date: Period end date (YYYY-MM-DD)
        
    Returns:
        Dict with aggregated metrics and venue rankings
    """
    if not rows:
        return {
            'period': '',
            'period_type': get_period_type(start_date, end_date),
            'date_range': [start_date, end_date],
            'total_responses': 0,
            'venues_count': 0,
            'metrics_avg': {},
            'venues_ranked': []
        }
    
    # Group by venue and process each
    venues = group_by_venue(rows)
    venue_metrics = []
    
    for venue_name in sorted(venues.keys()):
        venue_rows = venues[venue_name]
        if venue_rows:
            processed = process_venue_data(venue_rows, schema_name)
            if processed:
                # Calculate composite score
                composite = calculate_composite_score(processed, schema_name)
                processed['composite_score'] = composite
                venue_metrics.append(processed)
    
    # Sort by composite score (descending)
    venue_metrics.sort(key=lambda v: (v.get('composite_score') or -1, v.get('ltr_avg', 0)), reverse=True)
    
    # Assign rankings
    for idx, venue in enumerate(venue_metrics, 1):
        venue['rank'] = idx
    
    # Calculate aggregated metrics
    total_responses = sum(v['responses'] for v in venue_metrics)
    
    ltr_values = [v['ltr_avg'] for v in venue_metrics if v['ltr_avg']]
    fun_values = [v['fun_avg'] for v in venue_metrics if v['fun_avg']]
    helpful_values = [v['helpful_avg'] for v in venue_metrics if v['helpful_avg']]
    resolution_values = [v['resolution_avg'] for v in venue_metrics if v['resolution_avg']]
    
    metrics_avg = {
        'ltr_avg': round(sum(ltr_values) / len(ltr_values), 1) if ltr_values else 0,
        'fun_avg': round(sum(fun_values) / len(fun_values), 1) if fun_values else 0,
        'helpful_avg': round(sum(helpful_values) / len(helpful_values), 1) if helpful_values else 0,
        'issues_pct': round(sum(v['issues_pct'] for v in venue_metrics) / len(venue_metrics), 1) if venue_metrics else 0,
        'resolution_avg': round(sum(resolution_values) / len(resolution_values), 1) if resolution_values else None,
    }
    
    # F&B metrics for real schema
    if schema_name == 'real':
        nps_values = [v['nps_avg'] for v in venue_metrics if v.get('nps_avg') is not None]
        metrics_avg['nps_avg'] = round(sum(nps_values) / len(nps_values), 1) if nps_values else None
        
        for fb_metric in ['food_value_avg', 'food_speed_avg', 'food_quality_avg',
                          'beverage_value_avg', 'beverage_speed_avg', 'beverage_quality_avg']:
            values = [v[fb_metric] for v in venue_metrics if v.get(fb_metric)]
            metrics_avg[fb_metric] = round(sum(values) / len(values), 1) if values else None
    
    # Determine period name
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        period_type = get_period_type(start_date, end_date)
        if period_type == 'month':
            period_name = start.strftime('%B %Y')
        else:
            quarter = (start.month - 1) // 3 + 1
            period_name = f"Q{quarter} {start.year}"
    except:
        period_name = f"{start_date} to {end_date}"
    
    return {
        'period': period_name,
        'period_type': get_period_type(start_date, end_date),
        'date_range': [start_date, end_date],
        'total_responses': total_responses,
        'venues_count': len(venue_metrics),
        'metrics_avg': metrics_avg,
        'venues_ranked': [
            {
                'rank': v['rank'],
                'venue': v['venue'],
                'composite_score': v['composite_score'],
                'ltr_avg': v['ltr_avg'],
                'fun_avg': v['fun_avg'],
                'helpful_avg': v['helpful_avg'],
                'issues_pct': v['issues_pct'],
                'resolution_avg': v['resolution_avg'],
                'responses': v['responses'],
                **(
                    {
                        'nps_avg': v.get('nps_avg'),
                        'food_value_avg': v.get('food_value_avg'),
                        'food_speed_avg': v.get('food_speed_avg'),
                        'food_quality_avg': v.get('food_quality_avg'),
                        'beverage_value_avg': v.get('beverage_value_avg'),
                        'beverage_speed_avg': v.get('beverage_speed_avg'),
                        'beverage_quality_avg': v.get('beverage_quality_avg'),
                    } if schema_name == 'real' else {}
                )
            }
            for v in venue_metrics
        ]
    }


def compare_periods(current_summary: Dict, previous_summary: Dict) -> Dict:
    """Calculate deltas and percent changes between two period summaries.
    
    Args:
        current_summary: Current period summary dict
        previous_summary: Previous period summary dict
        
    Returns:
        Dict with comparison data including deltas and ranking changes
    """
    comparison = {
        'metrics_deltas': {},
        'response_count_change': {},
        'ranking_changes': []
    }
    
    # Compare metrics
    for metric in ['ltr_avg', 'nps_avg', 'fun_avg', 'helpful_avg', 'issues_pct', 'resolution_avg']:
        current_val = current_summary.get('metrics_avg', {}).get(metric)
        previous_val = previous_summary.get('metrics_avg', {}).get(metric)
        
        if current_val is not None and previous_val is not None:
            delta = round(current_val - previous_val, 2)
            if previous_val != 0:
                pct_change = round((delta / previous_val) * 100, 1)
            else:
                pct_change = 0
            
            comparison['metrics_deltas'][f'{metric}_delta'] = delta
            comparison['metrics_deltas'][f'{metric}_percent_change'] = pct_change
    
    # F&B metrics
    for fb_metric in ['food_value_avg', 'food_speed_avg', 'food_quality_avg',
                      'beverage_value_avg', 'beverage_speed_avg', 'beverage_quality_avg']:
        current_val = current_summary.get('metrics_avg', {}).get(fb_metric)
        previous_val = previous_summary.get('metrics_avg', {}).get(fb_metric)
        
        if current_val is not None and previous_val is not None:
            delta = round(current_val - previous_val, 2)
            if previous_val != 0:
                pct_change = round((delta / previous_val) * 100, 1)
            else:
                pct_change = 0
            
            comparison['metrics_deltas'][f'{fb_metric}_delta'] = delta
            comparison['metrics_deltas'][f'{fb_metric}_percent_change'] = pct_change
    
    # Response count comparison
    current_responses = current_summary.get('total_responses', 0)
    previous_responses = previous_summary.get('total_responses', 0)
    
    if previous_responses > 0:
        response_delta = current_responses - previous_responses
        response_pct = round((response_delta / previous_responses) * 100, 1)
    else:
        response_delta = 0
        response_pct = 0
    
    comparison['response_count_change'] = {
        'current': current_responses,
        'previous': previous_responses,
        'delta': response_delta,
        'percent_change': response_pct
    }
    
    # Ranking changes
    current_venues = {v['venue']: v for v in current_summary.get('venues_ranked', [])}
    previous_venues = {v['venue']: v for v in previous_summary.get('venues_ranked', [])}
    
    for venue_name, current_data in current_venues.items():
        previous_data = previous_venues.get(venue_name)
        if previous_data:
            previous_rank = previous_data['rank']
            current_rank = current_data['rank']
            
            if previous_rank != current_rank:
                rank_change = previous_rank - current_rank
                if rank_change > 0:
                    change_str = f"↑ {rank_change} positions"
                else:
                    change_str = f"↓ {abs(rank_change)} positions"
                
                composite_delta = round(current_data['composite_score'] - previous_data['composite_score'], 2) if current_data['composite_score'] and previous_data['composite_score'] else 0
                
                comparison['ranking_changes'].append({
                    'venue': venue_name,
                    'previous_rank': previous_rank,
                    'current_rank': current_rank,
                    'change': change_str,
                    'composite_score_delta': composite_delta
                })
    
    # Sort ranking changes by magnitude
    comparison['ranking_changes'].sort(key=lambda x: abs(x['previous_rank'] - x['current_rank']), reverse=True)
    
    return comparison
