"""
AI Reporting Tool API Module

This package provides CSV parsing, validation, and venue data aggregation
for the Topgolf survey reporting system.

Main components:
- schemas: JSON Schema definitions for POC and Real survey formats
- csv_parser: CSV reading, schema detection, and field extraction
- venue_processor: Venue data aggregation and metrics calculation
- data_loader: Abstraction layer for loading survey data (currently CSV, future API)
- app: Optional Flask REST API wrapper (future use)
"""

from . import csv_parser
from . import venue_processor
from . import schemas
from . import data_loader

__version__ = "1.0.0"
__all__ = ["csv_parser", "venue_processor", "schemas", "data_loader"]
