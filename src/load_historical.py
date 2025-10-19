"""
Load and process historical monthly gold price data from histprices.json.

This module provides utilities for loading historical gold prices dating back to 1833,
processing them into a pandas DataFrame, and merging with other data sources.
"""

import json
import os
from datetime import datetime
from typing import Dict

import pandas as pd


def load_historical_gold_prices(json_path: str = None) -> pd.DataFrame:
    """
    Load historical monthly gold prices from histprices.json.

    Args:
        json_path (str, optional): Path to the JSON file. If None, uses default location.

    Returns:
        pd.DataFrame: DataFrame with columns ['date', 'gold'] where date is datetime
                     and gold is the price.
    
    Raises:
        FileNotFoundError: If the JSON file doesn't exist.
        ValueError: If the JSON format is invalid.
    """
    if json_path is None:
        # Default to project root
        json_path = os.path.join(
            os.path.dirname(__file__), "..", "histprices.json"
        )
    
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Historical data file not found: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Parse the data
    records = []
    for item in data:
        date_str = item.get('Date')
        price = item.get('Price')
        
        if date_str and price is not None:
            # Parse YYYY-MM format to datetime (use first day of month)
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m')
                records.append({
                    'date': date_obj,
                    'gold': float(price)
                })
            except ValueError:
                # Skip invalid dates
                continue
    
    df = pd.DataFrame(records)
    df = df.sort_values('date').reset_index(drop=True)
    
    return df


def get_combined_gold_data(
    daily_csv_path: str = None,
    historical_json_path: str = None,
    resample_freq: str = 'ME'
) -> pd.DataFrame:
    """
    Combine historical monthly data with daily data.

    Args:
        daily_csv_path (str, optional): Path to daily gold/SP500 CSV.
        historical_json_path (str, optional): Path to historical JSON.
        resample_freq (str): Resampling frequency ('ME' for month-end, 'D' for daily).

    Returns:
        pd.DataFrame: Combined DataFrame with gold prices.
    """
    # Load historical data
    historical_df = load_historical_gold_prices(historical_json_path)
    
    # If we have a daily CSV, load and combine
    if daily_csv_path and os.path.exists(daily_csv_path):
        daily_df = pd.read_csv(daily_csv_path, parse_dates=['date'])
        
        # Resample daily to monthly if needed
        if resample_freq == 'ME':
            # Take end-of-month values
            daily_df_monthly = daily_df.set_index('date').resample('ME').last().reset_index()
            daily_df_monthly = daily_df_monthly[['date', 'gold']].dropna()
        else:
            daily_df_monthly = daily_df[['date', 'gold']].copy()
        
        # Combine: use historical for older dates, daily for newer
        # Find the overlap point
        if len(daily_df_monthly) > 0:
            daily_start = daily_df_monthly['date'].min()
            
            # Keep historical data before daily data starts
            historical_before = historical_df[historical_df['date'] < daily_start]
            
            # Concatenate
            combined = pd.concat([historical_before, daily_df_monthly], ignore_index=True)
            combined = combined.sort_values('date').reset_index(drop=True)
            
            return combined
    
    # If no daily data, return historical only
    return historical_df


def get_date_range_bounds() -> Dict[str, datetime]:
    """
    Get the earliest and latest dates available across all data sources.

    Returns:
        Dict[str, datetime]: Dictionary with 'min_date' and 'max_date' keys.
    """
    try:
        historical_df = load_historical_gold_prices()
        csv_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "gold_sp500_aligned.csv"
        )
        
        min_date = historical_df['date'].min()
        max_date = historical_df['date'].max()
        
        # Check if we have more recent data in CSV
        if os.path.exists(csv_path):
            daily_df = pd.read_csv(csv_path, parse_dates=['date'])
            if len(daily_df) > 0:
                max_date = max(max_date, daily_df['date'].max())
        
        return {
            'min_date': min_date,
            'max_date': max_date
        }
    except (FileNotFoundError, ValueError, KeyError):
        # Fallback to reasonable defaults if data is unavailable
        return {
            'min_date': datetime(1833, 1, 1),
            'max_date': datetime.now()
        }
