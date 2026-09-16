"""
Unit tests for venue_processor.py new functions.

Tests:
- filter_by_date_range()
- calculate_period_summary()
- compare_periods()
- calculate_composite_score()
- get_period_type()
"""

import unittest
from datetime import datetime, timedelta
from . import csv_parser, venue_processor


class TestGetPeriodType(unittest.TestCase):
    """Tests for get_period_type() function."""
    
    def test_month_period(self):
        """Test identification of month-long period."""
        result = venue_processor.get_period_type('2026-01-01', '2026-01-31')
        self.assertEqual(result, 'month')
    
    def test_quarter_period(self):
        """Test identification of quarter-long period."""
        result = venue_processor.get_period_type('2026-01-01', '2026-03-31')
        self.assertEqual(result, 'quarter')
    
    def test_invalid_date_format(self):
        """Test error handling for invalid date format."""
        with self.assertRaises(ValueError):
            venue_processor.get_period_type('01/01/2026', '01/31/2026')


class TestCalculateCompositeScore(unittest.TestCase):
    """Tests for calculate_composite_score() function."""
    
    def test_complete_metric_data_real_schema(self):
        """Test composite score with all metrics available (real schema)."""
        venue_data = {
            'ltr_avg': 8.0,
            'fun_avg': 4.2,
            'food_value_avg': 4.0,
            'food_speed_avg': 3.8,
            'food_quality_avg': 4.2,
            'beverage_value_avg': 4.1,
            'beverage_speed_avg': 3.9,
            'beverage_quality_avg': 4.0,
            'resolution_avg': 4.5
        }
        
        score = venue_processor.calculate_composite_score(venue_data, 'real')
        self.assertIsNotNone(score)
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 10)
    
    def test_missing_fb_data(self):
        """Test composite score with missing F&B data."""
        venue_data = {
            'ltr_avg': 8.0,
            'fun_avg': 4.2,
            'resolution_avg': 4.5
        }
        
        score = venue_processor.calculate_composite_score(venue_data, 'real')
        self.assertIsNotNone(score)
        self.assertGreater(score, 0)
    
    def test_poc_schema(self):
        """Test composite score with POC schema (no F&B data)."""
        venue_data = {
            'ltr_avg': 8.0,
            'fun_avg': 4.2,
            'resolution_avg': 4.5
        }
        
        score = venue_processor.calculate_composite_score(venue_data, 'poc')
        self.assertIsNotNone(score)
        self.assertGreater(score, 0)
    
    def test_missing_ltr(self):
        """Test that missing LTR returns None."""
        venue_data = {
            'fun_avg': 4.2,
            'resolution_avg': 4.5
        }
        
        score = venue_processor.calculate_composite_score(venue_data, 'poc')
        self.assertIsNone(score)
    
    def test_partial_fb_data(self):
        """Test composite score with partial F&B data."""
        venue_data = {
            'ltr_avg': 8.0,
            'fun_avg': 4.2,
            'food_value_avg': 4.0,
            'food_speed_avg': 3.8,
            'food_quality_avg': 4.2,
            'resolution_avg': 4.5
        }
        
        score = venue_processor.calculate_composite_score(venue_data, 'real')
        self.assertIsNotNone(score)
        self.assertGreater(score, 0)


class TestFilterByDateRange(unittest.TestCase):
    """Tests for filter_by_date_range() function."""
    
    def setUp(self):
        """Set up test data."""
        self.rows = [
            {'Venue': 'Grand Prairie', 'VisitDate': '01/15/2026'},
            {'Venue': 'Chicago', 'VisitDate': '01/20/2026'},
            {'Venue': 'Dallas', 'VisitDate': '02/05/2026'},
            {'Venue': 'Austin', 'VisitDate': '12/25/2025'},
        ]
    
    def test_filter_single_month(self):
        """Test filtering for a single month."""
        result = csv_parser.filter_by_date_range(self.rows, 'poc', '2026-01-01', '2026-01-31')
        self.assertEqual(len(result), 2)
    
    def test_filter_across_months(self):
        """Test filtering across multiple months."""
        result = csv_parser.filter_by_date_range(self.rows, 'poc', '2026-01-01', '2026-02-28')
        self.assertEqual(len(result), 3)
    
    def test_filter_empty_result(self):
        """Test filtering with no matching rows."""
        result = csv_parser.filter_by_date_range(self.rows, 'poc', '2026-03-01', '2026-03-31')
        self.assertEqual(len(result), 0)
    
    def test_invalid_date_format(self):
        """Test error handling for invalid date format."""
        with self.assertRaises(ValueError):
            csv_parser.filter_by_date_range(self.rows, 'poc', '01/01/2026', '01/31/2026')


class TestCalculatePeriodSummary(unittest.TestCase):
    """Tests for calculate_period_summary() function."""
    
    def setUp(self):
        """Set up test data."""
        self.rows = [
            {
                'Venue': 'Grand Prairie',
                'VisitDate': '01/15/2026',
                'Q1_LTR': '8',
                'Q2_FUN': '5 - Extremely fun',
                'Q3_HELPFUL': '5 - Extremely helpful',
                'Q4_ISSUES': 'No',
                'Q5_ISSUE_RESOLUTION': '',
                'Q6_COMMENT': 'Great experience'
            },
            {
                'Venue': 'Chicago',
                'VisitDate': '01/20/2026',
                'Q1_LTR': '7',
                'Q2_FUN': '4 - Very fun',
                'Q3_HELPFUL': '4 - Very helpful',
                'Q4_ISSUES': 'Yes',
                'Q5_ISSUE_RESOLUTION': '5 - Extremely satisfied',
                'Q6_COMMENT': 'Good overall'
            },
        ]
    
    def test_period_summary_calculation(self):
        """Test basic period summary calculation."""
        summary = venue_processor.calculate_period_summary(self.rows, 'poc', '2026-01-01', '2026-01-31')
        
        self.assertEqual(summary['total_responses'], 2)
        self.assertEqual(summary['venues_count'], 2)
        self.assertIn('metrics_avg', summary)
        self.assertIn('venues_ranked', summary)
    
    def test_period_summary_venue_ranking(self):
        """Test that venues are ranked by composite score."""
        summary = venue_processor.calculate_period_summary(self.rows, 'poc', '2026-01-01', '2026-01-31')
        
        venues = summary['venues_ranked']
        self.assertEqual(len(venues), 2)
        self.assertEqual(venues[0]['rank'], 1)
        self.assertEqual(venues[1]['rank'], 2)
    
    def test_empty_period(self):
        """Test handling of empty period."""
        summary = venue_processor.calculate_period_summary([], 'poc', '2026-01-01', '2026-01-31')
        
        self.assertEqual(summary['total_responses'], 0)
        self.assertEqual(summary['venues_count'], 0)
        self.assertEqual(len(summary['venues_ranked']), 0)


class TestComparePeriods(unittest.TestCase):
    """Tests for compare_periods() function."""
    
    def setUp(self):
        """Set up test data."""
        self.current_summary = {
            'period': 'January 2026',
            'total_responses': 500,
            'metrics_avg': {
                'ltr_avg': 8.2,
                'fun_avg': 4.3,
                'helpful_avg': 4.4,
                'issues_pct': 12.0,
                'resolution_avg': 4.5
            },
            'venues_ranked': [
                {'venue': 'Grand Prairie', 'rank': 1, 'composite_score': 7.2},
                {'venue': 'Chicago', 'rank': 2, 'composite_score': 6.8},
                {'venue': 'Dallas', 'rank': 3, 'composite_score': 6.5},
            ]
        }
        
        self.previous_summary = {
            'period': 'December 2025',
            'total_responses': 480,
            'metrics_avg': {
                'ltr_avg': 8.0,
                'fun_avg': 4.2,
                'helpful_avg': 4.3,
                'issues_pct': 15.0,
                'resolution_avg': 4.4
            },
            'venues_ranked': [
                {'venue': 'Chicago', 'rank': 1, 'composite_score': 7.0},
                {'venue': 'Grand Prairie', 'rank': 2, 'composite_score': 6.9},
                {'venue': 'Dallas', 'rank': 3, 'composite_score': 6.5},
            ]
        }
    
    def test_metrics_deltas(self):
        """Test calculation of metric deltas."""
        comparison = venue_processor.compare_periods(self.current_summary, self.previous_summary)
        
        self.assertIn('metrics_deltas', comparison)
        self.assertIn('ltr_avg_delta', comparison['metrics_deltas'])
        self.assertEqual(comparison['metrics_deltas']['ltr_avg_delta'], 0.2)
    
    def test_response_count_change(self):
        """Test response count comparison."""
        comparison = venue_processor.compare_periods(self.current_summary, self.previous_summary)
        
        self.assertIn('response_count_change', comparison)
        self.assertEqual(comparison['response_count_change']['current'], 500)
        self.assertEqual(comparison['response_count_change']['previous'], 480)
        self.assertEqual(comparison['response_count_change']['delta'], 20)
    
    def test_ranking_changes(self):
        """Test identification of ranking changes."""
        comparison = venue_processor.compare_periods(self.current_summary, self.previous_summary)
        
        self.assertIn('ranking_changes', comparison)
        # Grand Prairie moved from 2nd to 1st
        # Chicago moved from 1st to 2nd
        self.assertGreater(len(comparison['ranking_changes']), 0)


if __name__ == '__main__':
    unittest.main()
