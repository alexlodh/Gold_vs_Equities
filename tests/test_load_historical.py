"""
Tests for the historical data loading module.
"""

import os
import pytest
import pandas as pd
from datetime import datetime
from src.load_historical import (
    load_historical_gold_prices,
    get_combined_gold_data,
    get_date_range_bounds
)


def test_load_historical_gold_prices():
    """Test that historical gold prices load correctly."""
    # This assumes histprices.json exists in the project root
    json_path = os.path.join(
        os.path.dirname(__file__), "..", "histprices.json"
    )
    
    if not os.path.exists(json_path):
        pytest.skip("histprices.json not found")
    
    df = load_historical_gold_prices(json_path)
    
    # Check that we got a DataFrame
    assert isinstance(df, pd.DataFrame)
    
    # Check columns
    assert 'date' in df.columns
    assert 'gold' in df.columns
    
    # Check data types
    assert pd.api.types.is_datetime64_any_dtype(df['date'])
    assert pd.api.types.is_numeric_dtype(df['gold'])
    
    # Check we have data
    assert len(df) > 0
    
    # Check date range makes sense (should start in 1833)
    min_year = df['date'].min().year
    assert min_year == 1833
    
    # Check prices are positive
    assert (df['gold'] > 0).all()
    
    # Check data is sorted
    assert df['date'].is_monotonic_increasing


def test_load_historical_missing_file():
    """Test that FileNotFoundError is raised for missing file."""
    with pytest.raises(FileNotFoundError):
        load_historical_gold_prices("/nonexistent/path/to/file.json")


def test_get_date_range_bounds():
    """Test getting date range bounds."""
    bounds = get_date_range_bounds()
    
    assert 'min_date' in bounds
    assert 'max_date' in bounds
    
    assert isinstance(bounds['min_date'], datetime)
    assert isinstance(bounds['max_date'], datetime)
    
    assert bounds['min_date'] < bounds['max_date']


def test_get_combined_gold_data():
    """Test combining historical and daily data."""
    json_path = os.path.join(
        os.path.dirname(__file__), "..", "histprices.json"
    )
    csv_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "gold_sp500_aligned.csv"
    )
    
    if not os.path.exists(json_path):
        pytest.skip("histprices.json not found")
    
    # Test with historical data only
    df_hist_only = get_combined_gold_data(
        daily_csv_path=None,
        historical_json_path=json_path
    )
    
    assert isinstance(df_hist_only, pd.DataFrame)
    assert 'date' in df_hist_only.columns
    assert 'gold' in df_hist_only.columns
    
    # Test with combined data if CSV exists
    if os.path.exists(csv_path):
        df_combined = get_combined_gold_data(
            daily_csv_path=csv_path,
            historical_json_path=json_path,
            resample_freq='ME'
        )
        
        assert isinstance(df_combined, pd.DataFrame)
        assert len(df_combined) >= len(df_hist_only)
        
        # Should have more recent data
        assert df_combined['date'].max() >= df_hist_only['date'].max()
