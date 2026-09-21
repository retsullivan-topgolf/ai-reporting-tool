"""
Unit tests for csv_parser.py functions.

Tests:
- parse_csv()
- detect_schema()
- get_field()
- convert_field_value()
- validate_row()
- extract_all_fields()
"""

import unittest
import tempfile
import os
from . import csv_parser


class TestParseCSV(unittest.TestCase):
    """Tests for parse_csv() function."""
    
    def setUp(self):
        """Create temporary CSV files for testing."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_parse_valid_poc_csv(self):
        """Test parsing a valid POC format CSV."""
        csv_content = """StartDate,EndDate,Venue,VisitDate,Q1_LTR,Q2_FUN,Q3_HELPFUL,Q4_ISSUES,Q5_ISSUE_RESOLUTION,Q6_COMMENT
2026-01-01,2026-01-31,Topgolf Venue,Date of Visit,LTR,Fun,Helpful,Issues,Resolution,Comment
{"ImportId":"StartDate"},{"ImportId":"EndDate"},{"ImportId":"Venue"},{"ImportId":"VisitDate"},{"ImportId":"Q1_LTR"},{"ImportId":"Q2_FUN"},{"ImportId":"Q3_HELPFUL"},{"ImportId":"Q4_ISSUES"},{"ImportId":"Q5_ISSUE_RESOLUTION"},{"ImportId":"Q6_COMMENT"}
2026-01-15,2026-01-15,Grand Prairie,01/15/2026,8,5 - Extremely fun,5 - Extremely helpful,No,,Great experience
2026-01-20,2026-01-20,Chicago,01/20/2026,7,4 - Very fun,4 - Very helpful,Yes,5 - Extremely satisfied,Good overall"""
        
        csv_file = os.path.join(self.temp_dir, 'test.csv')
        with open(csv_file, 'w') as f:
            f.write(csv_content)
        
        rows, fieldnames = csv_parser.parse_csv(csv_file)
        
        self.assertEqual(len(rows), 2)
        self.assertIn('Venue', fieldnames)
        self.assertEqual(rows[0]['Venue'], 'Grand Prairie')
    
    def test_parse_nonexistent_file(self):
        """Test error handling for nonexistent file."""
        with self.assertRaises(csv_parser.CSVParseError):
            csv_parser.parse_csv('/nonexistent/path/file.csv')
    
    def test_parse_empty_csv(self):
        """Test error handling for empty CSV."""
        csv_file = os.path.join(self.temp_dir, 'empty.csv')
        with open(csv_file, 'w') as f:
            f.write("Venue,VisitDate,Q1_LTR\n")
        
        with self.assertRaises(csv_parser.CSVParseError):
            csv_parser.parse_csv(csv_file)


class TestDetectSchema(unittest.TestCase):
    """Tests for detect_schema() function."""
    
    def test_detect_real_schema(self):
        """Test detection of Real schema."""
        fieldnames = ['Venue', 'Visit Date (+00:00 GMT)', 'Combined NPS', 'F&B Matrix_Food Value', 'Likelihood to Return']
        result = csv_parser.detect_schema(fieldnames)
        self.assertEqual(result, 'real')
    
    def test_detect_unknown_schema(self):
        """Test error handling for unknown schema."""
        fieldnames = ['Column1', 'Column2', 'Column3']
        with self.assertRaises(csv_parser.SchemaDetectionError):
            csv_parser.detect_schema(fieldnames)


class TestGetField(unittest.TestCase):
    """Tests for get_field() function."""
    
    def test_get_field_missing_field(self):
        """Test handling of missing field."""
        row = {'Venue': 'Grand Prairie'}
        result = csv_parser.get_field(row, 'ltr', 'poc')
        self.assertEqual(result, '')
    
    def test_get_field_with_whitespace(self):
        """Test that field values are trimmed."""
        row = {'Venue': '  Grand Prairie  ', 'Q1_LTR': '  8  '}
        
        result = csv_parser.get_field(row, 'venue', 'poc')
        self.assertEqual(result, 'Grand Prairie')


class TestConvertFieldValue(unittest.TestCase):
    """Tests for convert_field_value() function."""
    
    def test_convert_integer_field(self):
        """Test conversion of integer field."""
        result = csv_parser.convert_field_value('8', 'ltr', 'poc')
        self.assertEqual(result, 8)
        self.assertIsInstance(result, int)
    
    def test_convert_categorical_field(self):
        """Test conversion of categorical field."""
        result = csv_parser.convert_field_value('5 - Extremely fun', 'fun', 'poc')
        self.assertEqual(result, 5)
    
    def test_convert_boolean_field(self):
        """Test conversion of boolean field."""
        result = csv_parser.convert_field_value('Yes', 'issues', 'poc')
        self.assertTrue(result)
        
        result = csv_parser.convert_field_value('No', 'issues', 'poc')
        self.assertFalse(result)
    
    def test_convert_empty_value(self):
        """Test handling of empty value."""
        result = csv_parser.convert_field_value('', 'ltr', 'poc')
        self.assertIsNone(result)
    
    def test_convert_invalid_integer(self):
        """Test handling of invalid integer."""
        result = csv_parser.convert_field_value('not_a_number', 'ltr', 'poc')
        self.assertIsNone(result)


class TestValidateRow(unittest.TestCase):
    """Tests for validate_row() function."""
    
    def test_validate_valid_row_poc(self):
        """Test validation of valid POC row."""
        row = {
            'Venue': 'Grand Prairie',
            'VisitDate': '01/15/2026',
            'Q1_LTR': '8',
            'Q2_FUN': '5 - Extremely fun',
            'Q3_HELPFUL': '5 - Extremely helpful',
            'Q4_ISSUES': 'No',
            'Q5_ISSUE_RESOLUTION': '',
            'Q6_COMMENT': 'Great'
        }
        
        is_valid, error = csv_parser.validate_row(row, 'poc')
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_missing_required_field(self):
        """Test validation with missing required field."""
        row = {
            'VisitDate': '01/15/2026',
            'Q1_LTR': '8'
        }
        
        is_valid, error = csv_parser.validate_row(row, 'poc')
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_unknown_schema(self):
        """Test validation with unknown schema."""
        row = {'Venue': 'Grand Prairie'}
        is_valid, error = csv_parser.validate_row(row, 'unknown_schema')
        self.assertFalse(is_valid)


class TestExtractAllFields(unittest.TestCase):
    """Tests for extract_all_fields() function."""
    
    def test_extract_all_fields_poc(self):
        """Test extraction of all fields from POC row."""
        row = {
            'Venue': 'Grand Prairie',
            'VisitDate': '01/15/2026',
            'Q1_LTR': '8',
            'Q2_FUN': '5 - Extremely fun',
            'Q3_HELPFUL': '5 - Extremely helpful',
            'Q4_ISSUES': 'No',
            'Q5_ISSUE_RESOLUTION': '',
            'Q6_COMMENT': 'Great'
        }
        
        result = csv_parser.extract_all_fields(row, 'poc')
        
        self.assertEqual(result['venue'], 'Grand Prairie')
        self.assertEqual(result['ltr'], 8)
        self.assertEqual(result['fun'], 5)
        self.assertEqual(result['helpful'], 5)
        self.assertFalse(result['issues'])
    
    def test_extract_all_fields_with_missing_optional(self):
        """Test extraction with missing optional fields."""
        row = {
            'Venue': 'Grand Prairie',
            'VisitDate': '01/15/2026',
            'Q1_LTR': '8',
            'Q2_FUN': '5 - Extremely fun',
            'Q3_HELPFUL': '5 - Extremely helpful',
            'Q4_ISSUES': 'No',
            'Q6_COMMENT': ''
        }
        
        result = csv_parser.extract_all_fields(row, 'poc')
        
        self.assertEqual(result['venue'], 'Grand Prairie')
        self.assertIsNone(result['comment'])


if __name__ == '__main__':
    unittest.main()
