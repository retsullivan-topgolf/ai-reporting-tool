"""
Schema definitions for Topgolf survey data.

Supports two survey formats:
1. POC (Proof of Concept) - Original format with Q1_LTR, Q2_FUN, etc.
2. Real - Production format with "Combined NPS", "F&B Matrix_*", etc.

Each schema defines:
- Required fields
- Field type and validation rules
- Mapping from CSV column names to logical field names
"""

# POC Schema (Original format)
POC_SCHEMA = {
    "name": "poc",
    "description": "Proof of Concept survey format",
    "fields": {
        "venue": {
            "csv_column": "Venue",
            "type": "string",
            "required": True,
            "description": "Venue name"
        },
        "visit_date": {
            "csv_column": "VisitDate",
            "type": "date",
            "required": True,
            "description": "Date of visit"
        },
        "ltr": {
            "csv_column": "Q1_LTR",
            "type": "integer",
            "range": [1, 10],
            "required": True,
            "description": "Likelihood to Return (1-10 scale)"
        },
        "fun": {
            "csv_column": "Q2_FUN",
            "type": "categorical",
            "values": ["5 - Extremely fun", "4 - Very fun", "3 - Moderately fun", "2 - Slightly fun", "1 - Not at all fun"],
            "numeric_map": {"5 - Extremely fun": 5, "4 - Very fun": 4, "3 - Moderately fun": 3, "2 - Slightly fun": 2, "1 - Not at all fun": 1},
            "required": True,
            "description": "Fun experience rating"
        },
        "helpful": {
            "csv_column": "Q3_HELPFUL",
            "type": "categorical",
            "values": ["5 - Extremely helpful", "4 - Very helpful", "3 - Moderately helpful", "2 - Slightly helpful", "1 - Not at all helpful"],
            "numeric_map": {"5 - Extremely helpful": 5, "4 - Very helpful": 4, "3 - Moderately helpful": 3, "2 - Slightly helpful": 2, "1 - Not at all helpful": 1},
            "required": True,
            "description": "Staff helpfulness rating"
        },
        "issues": {
            "csv_column": "Q4_ISSUES",
            "type": "boolean",
            "values": ["yes", "no"],
            "required": True,
            "description": "Whether issues occurred during visit"
        },
        "resolution": {
            "csv_column": "Q5_ISSUE_RESOLUTION",
            "type": "categorical",
            "values": ["5 - Extremely satisfied", "4 - Very satisfied", "3 - Moderately satisfied", "2 - Slightly satisfied", "1 - Extremely dissatisfied"],
            "numeric_map": {"5 - Extremely satisfied": 5, "4 - Very satisfied": 4, "3 - Moderately satisfied": 3, "2 - Slightly satisfied": 2, "1 - Extremely dissatisfied": 1},
            "required": False,
            "description": "Issue resolution satisfaction (only if issues=yes)"
        },
        "comment": {
            "csv_column": "Q6_COMMENT",
            "type": "string",
            "required": False,
            "description": "Open-ended comment"
        }
    },
    "detection_rule": "Has Q1_LTR, Q2_FUN, Q3_HELPFUL, Q4_ISSUES, Q5_ISSUE_RESOLUTION, Q6_COMMENT columns"
}

# Real Schema (Production format)
REAL_SCHEMA = {
    "name": "real",
    "description": "Production survey format with F&B metrics",
    "fields": {
        "venue": {
            "csv_column": "Venue",
            "type": "string",
            "required": True,
            "description": "Venue name"
        },
        "visit_date": {
            "csv_column": "Visit Date (+00:00 GMT)",
            "type": "date",
            "required": True,
            "description": "Date of visit"
        },
        "ltr": {
            "csv_column": "Combined NPS",
            "type": "integer",
            "range": [1, 10],
            "required": True,
            "description": "Likelihood to Return (1-10 scale, called Combined NPS)"
        },
        "fun": {
            "csv_column": "Fun - How much fun did you have during your visit at Topgolf [Field-Venue_Name]?",
            "type": "integer",
            "range": [1, 5],
            "required": True,
            "description": "Fun experience rating (1-5 scale)"
        },
        "helpful": {
            "csv_column": "Helpfulness - How satisfied were you with the overall helpfulness of our staff?",
            "type": "integer",
            "range": [1, 5],
            "required": True,
            "description": "Staff helpfulness rating (1-5 scale)"
        },
        "issues": {
            "csv_column": "Issues During Visit",
            "type": "boolean",
            "values": ["yes", "no"],
            "required": True,
            "description": "Whether issues occurred during visit"
        },
        "resolution": {
            "csv_column": "Issue Resolution Sat",
            "type": "integer",
            "range": [1, 5],
            "required": False,
            "description": "Issue resolution satisfaction (1-5 scale, only if issues=yes)"
        },
        "comment": {
            "csv_column": "Open Comment",
            "type": "string",
            "required": False,
            "description": "Open-ended comment"
        },
        "return_likelihood": {
            "csv_column": "Likelihood to Return - How likely are you to return to this or another Topgolf venue?",
            "type": "integer",
            "range": [1, 5],
            "required": False,
            "description": "Return likelihood (1-5 scale)"
        },
        "price_value": {
            "csv_column": "Price Value - How would you rate Topgolf's price compared to the value of your experience...",
            "type": "integer",
            "range": [1, 5],
            "required": False,
            "description": "Price to value perception (1-5 scale)"
        },
        "food_value": {
            "csv_column": "F&B Matrix_1 - Value for the price you paid for food",
            "type": "integer",
            "range": [1, 5],
            "required": False,
            "description": "Food value perception (1-5 scale)"
        },
        "food_speed": {
            "csv_column": "F&B Matrix_2 - Speed of food service",
            "type": "integer",
            "range": [1, 5],
            "required": False,
            "description": "Food service speed (1-5 scale)"
        },
        "food_quality": {
            "csv_column": "F&B Matrix_3 - Food quality",
            "type": "integer",
            "range": [1, 5],
            "required": False,
            "description": "Food quality rating (1-5 scale)"
        },
        "beverage_value": {
            "csv_column": "F&B Matrix_4 - Value for the price you paid for beverages",
            "type": "integer",
            "range": [1, 5],
            "required": False,
            "description": "Beverage value perception (1-5 scale)"
        },
        "beverage_speed": {
            "csv_column": "F&B Matrix_5 - Speed of beverage service",
            "type": "integer",
            "range": [1, 5],
            "required": False,
            "description": "Beverage service speed (1-5 scale)"
        },
        "beverage_quality": {
            "csv_column": "F&B Matrix_6 - Beverage quality",
            "type": "integer",
            "range": [1, 5],
            "required": False,
            "description": "Beverage quality rating (1-5 scale)"
        }
    },
    "detection_rule": "Has 'F&B Matrix' fields AND 'Combined NPS' AND 'Likelihood to Return' fields"
}

# Schema registry for easy lookup
SCHEMAS = {
    "poc": POC_SCHEMA,
    "real": REAL_SCHEMA
}


def get_schema(schema_name):
    """Get a schema by name.
    
    Args:
        schema_name: 'poc' or 'real'
        
    Returns:
        Schema dict or None if not found
    """
    return SCHEMAS.get(schema_name.lower())


def list_schemas():
    """List all available schemas.
    
    Returns:
        List of schema names
    """
    return list(SCHEMAS.keys())
