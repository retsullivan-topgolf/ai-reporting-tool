"""
Data loader abstraction layer for survey data.

This module provides a unified interface for loading survey data, abstracting
away the underlying storage mechanism (currently CSV files, future API calls).

The abstraction allows python scripts to load data by identifier without
needing to know file paths or API endpoints.

Usage:
    from api import data_loader
    
    # Load all data (texas_venues by default)
    rows, fieldnames = data_loader.load_survey_data()
    
    # Load data for a specific venue (filters from texas_venues)
    rows, fieldnames = data_loader.load_survey_data(venue='Grand Prairie')
    
    # Load a specific dataset (for backward compatibility)
    rows, fieldnames = data_loader.load_survey_data(dataset='Grand_Prairie')
    
    # List available datasets
    datasets = data_loader.list_available_datasets()
    
    # List available venues
    venues = data_loader.list_available_venues()
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


def load_survey_data(dataset: Optional[str] = None, venue: Optional[str] = None) -> Tuple[List[Dict], List[str]]:
    """Load survey data by dataset or venue.
    
    Default behavior: Loads all data from texas_venues.csv (the complete dataset).
    
    When the real API is available, this function will be updated to call
    the API endpoint instead, without requiring changes to calling code.
    
    Args:
        dataset: (Optional) Dataset identifier (e.g., 'Grand_Prairie', 'texas_venues')
                 If provided, loads from api/qualtrics/{dataset}.csv
                 If not provided, defaults to 'texas_venues'
        venue: (Optional) Venue name to filter by (e.g., 'Grand Prairie')
               Only used when dataset is not specified.
               Filters rows from texas_venues where Venue column matches.
    
    Returns:
        Tuple of (rows, fieldnames) where:
        - rows: List of dictionaries, one per survey response
        - fieldnames: List of column names from the CSV
    
    Raises:
        DataLoaderError: If data cannot be loaded
        
    Examples:
        >>> # Load all data (texas_venues)
        >>> rows, fieldnames = load_survey_data()
        >>> len(rows) > 60000
        True
        
        >>> # Load data for a specific venue
        >>> rows, fieldnames = load_survey_data(venue='Grand Prairie')
        >>> all(row.get('Venue') == 'Grand Prairie' for row in rows)
        True
        
        >>> # Load a specific dataset (backward compatible)
        >>> rows, fieldnames = load_survey_data(dataset='Grand_Prairie')
        >>> len(rows)
        475
    """
    qualtrics_dir = _get_qualtrics_dir()
    
    # Determine which dataset to load
    if dataset is None:
        # Default to texas_venues (the complete dataset)
        dataset = 'texas_venues'
    
    # Construct the CSV file path
    # Handle both with and without .csv extension
    if dataset.lower().endswith('.csv'):
        filename = dataset
        dataset_name = dataset[:-4]
    else:
        filename = f"{dataset}.csv"
        dataset_name = dataset
    
    file_path = os.path.join(qualtrics_dir, filename)
    
    # Validate file exists
    if not os.path.exists(file_path):
        available = list_available_datasets()
        raise DataLoaderError(
            f"Dataset not found: {dataset}\n"
            f"Available datasets: {', '.join(available)}"
        )
    
    try:
        # Use csv_parser to load and parse the CSV
        rows, fieldnames = csv_parser.parse_csv(file_path)
        
        # If venue filter is specified, filter the rows
        if venue is not None:
            rows = [row for row in rows if row.get('Venue', '').strip() == venue.strip()]
            if not rows:
                available_venues = list_available_venues(dataset_name)
                raise DataLoaderError(
                    f"No data found for venue '{venue}' in dataset '{dataset_name}'\n"
                    f"Available venues: {', '.join(available_venues)}"
                )
        
        return rows, fieldnames
    except csv_parser.CSVParseError as e:
        raise DataLoaderError(f"Failed to load dataset '{dataset}': {str(e)}")
    except DataLoaderError:
        raise
    except Exception as e:
        raise DataLoaderError(f"Unexpected error loading dataset '{dataset}': {str(e)}")


def list_available_venues(dataset: str = 'texas_venues') -> List[str]:
    """List all available venues in a dataset.
    
    Args:
        dataset: Dataset identifier (default: 'texas_venues')
    
    Returns:
        Sorted list of unique venue names
        
    Raises:
        DataLoaderError: If dataset cannot be loaded
    """
    try:
        rows, fieldnames = load_survey_data(dataset=dataset)
        
        # Extract unique venues from the Venue column
        venues = set()
        for row in rows:
            venue = row.get('Venue', '').strip()
            if venue:
                venues.add(venue)
        
        return sorted(venues)
    except Exception as e:
        raise DataLoaderError(f"Failed to list venues from dataset '{dataset}': {str(e)}")


def load_survey_data_with_identifier(data_identifier: str = None, venue: str = None) -> Tuple[List[Dict], List[str], str]:
    """Load survey data and return the actual identifier/venue used.
    
    Useful when you want to know which dataset/venue was actually loaded.
    
    Args:
        data_identifier: Dataset identifier (optional, defaults to 'texas_venues')
        venue: Venue name to filter by (optional)
    
    Returns:
        Tuple of (rows, fieldnames, actual_identifier)
        
    Raises:
        DataLoaderError: If data cannot be loaded
    """
    rows, fieldnames = load_survey_data(dataset=data_identifier, venue=venue)
    
    # Determine the actual identifier used
    if data_identifier is None:
        actual_identifier = 'texas_venues'
    elif data_identifier.lower().endswith('.csv'):
        actual_identifier = data_identifier[:-4]
    else:
        actual_identifier = data_identifier
    
    # If venue was specified, append it to the identifier
    if venue is not None:
        actual_identifier = f"{actual_identifier}:{venue}"
    
    return rows, fieldnames, actual_identifier
