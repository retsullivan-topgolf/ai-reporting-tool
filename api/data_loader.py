"""
Data loader abstraction layer for survey data.

This module provides a unified interface for loading survey data, abstracting
away the underlying storage mechanism (currently CSV files, future API calls).

The abstraction allows python scripts to load data by identifier without
needing to know file paths or API endpoints.

Usage:
    from api import data_loader
    
    # Load data by identifier
    rows, fieldnames = data_loader.load_survey_data('Grand_Prairie')
    
    # List available datasets
    datasets = data_loader.list_available_datasets()
"""

import os
from typing import List, Dict, Tuple, Optional
from . import csv_parser


class DataLoaderError(Exception):
    """Raised when data loading fails."""
    pass


def _get_qualtrics_dir() -> str:
    """Get the path to the qualtrics data directory.
    
    Returns:
        Absolute path to api/qualtrics directory
    """
    api_dir = os.path.dirname(os.path.abspath(__file__))
    qualtrics_dir = os.path.join(api_dir, 'qualtrics')
    return qualtrics_dir


def list_available_datasets() -> List[str]:
    """List all available survey datasets.
    
    Returns:
        List of dataset identifiers (filenames without .csv extension)
        
    Raises:
        DataLoaderError: If qualtrics directory cannot be read
    """
    qualtrics_dir = _get_qualtrics_dir()
    
    if not os.path.exists(qualtrics_dir):
        raise DataLoaderError(f"Qualtrics data directory not found: {qualtrics_dir}")
    
    try:
        datasets = []
        for filename in sorted(os.listdir(qualtrics_dir)):
            if filename.lower().endswith('.csv'):
                # Remove .csv extension to get identifier
                identifier = filename[:-4]
                datasets.append(identifier)
        return datasets
    except Exception as e:
        raise DataLoaderError(f"Failed to list datasets: {str(e)}")


def load_survey_data(data_identifier: str) -> Tuple[List[Dict], List[str]]:
    """Load survey data by identifier.
    
    Currently loads from api/qualtrics/{data_identifier}.csv.
    When the real API is available, this function will be updated to call
    the API endpoint instead, without requiring changes to calling code.
    
    Args:
        data_identifier: Dataset identifier (e.g., 'Grand_Prairie', 'texas_venues')
                        This can be a filename without extension or an API ID.
    
    Returns:
        Tuple of (rows, fieldnames) where:
        - rows: List of dictionaries, one per survey response
        - fieldnames: List of column names from the CSV
    
    Raises:
        DataLoaderError: If data cannot be loaded
        
    Examples:
        >>> rows, fieldnames = load_survey_data('Grand_Prairie')
        >>> len(rows)
        42
        >>> 'Venue' in fieldnames
        True
    """
    qualtrics_dir = _get_qualtrics_dir()
    
    # Construct the CSV file path
    # Handle both with and without .csv extension
    if data_identifier.lower().endswith('.csv'):
        filename = data_identifier
    else:
        filename = f"{data_identifier}.csv"
    
    file_path = os.path.join(qualtrics_dir, filename)
    
    # Validate file exists
    if not os.path.exists(file_path):
        available = list_available_datasets()
        raise DataLoaderError(
            f"Dataset not found: {data_identifier}\n"
            f"Available datasets: {', '.join(available)}"
        )
    
    try:
        # Use csv_parser to load and parse the CSV
        rows, fieldnames = csv_parser.parse_csv(file_path)
        return rows, fieldnames
    except csv_parser.CSVParseError as e:
        raise DataLoaderError(f"Failed to load dataset '{data_identifier}': {str(e)}")
    except Exception as e:
        raise DataLoaderError(f"Unexpected error loading dataset '{data_identifier}': {str(e)}")


def load_survey_data_with_identifier(data_identifier: str) -> Tuple[List[Dict], List[str], str]:
    """Load survey data and return the actual identifier used.
    
    Useful when you want to know which dataset was actually loaded.
    
    Args:
        data_identifier: Dataset identifier
    
    Returns:
        Tuple of (rows, fieldnames, actual_identifier)
        
    Raises:
        DataLoaderError: If data cannot be loaded
    """
    rows, fieldnames = load_survey_data(data_identifier)
    
    # Normalize identifier (remove .csv if present)
    if data_identifier.lower().endswith('.csv'):
        actual_identifier = data_identifier[:-4]
    else:
        actual_identifier = data_identifier
    
    return rows, fieldnames, actual_identifier
