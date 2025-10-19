"""
Enhanced preprocessing for gold and S&P 500 data including historical data from 1971.

This module fetches historical S&P 500 data from yfinance, combines it with historical
gold prices, and creates a comprehensive dataset from 1971 to present.
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime
import yaml

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fetch_ticker import fetch_ticker_prices


def get_csv_path() -> str:
    """
    Get the CSV output path from config.yaml.
    
    Returns:
        str: Path to the CSV file.
    """
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    with open(config_path, "r", encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config["csv_path"]


def load_historical_gold_from_json(json_path: str, start_year: int = 1971) -> pd.DataFrame:
    """
    Load historical gold prices from JSON file, filtered from start_year onwards.
    
    Args:
        json_path (str): Path to histprices.json
        start_year (int): Start year for filtering (default 1971)
    
    Returns:
        pd.DataFrame: DataFrame with monthly gold prices from start_year onwards
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = []
    for item in data:
        date_str = item.get('Date')
        price = item.get('Price')
        
        if date_str and price is not None:
            try:
                # Parse YYYY-MM format
                date_obj = datetime.strptime(date_str, '%Y-%m')
                
                # Only include dates from start_year onwards
                if date_obj.year >= start_year:
                    records.append({
                        'date': date_obj.strftime('%Y-%m-%d'),
                        'gold': float(price)
                    })
            except ValueError:
                continue
    
    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    
    return df


def fetch_sp500_historical(start_year: int = 1971) -> pd.DataFrame:
    """
    Fetch S&P 500 historical data from Yahoo Finance from start_year to present.
    
    Args:
        start_year (int): Start year for fetching data (default 1971)
    
    Returns:
        pd.DataFrame: DataFrame with S&P 500 prices
    """
    print(f"Fetching S&P 500 data from {start_year} onwards...")
    
    start_date = f"{start_year}-01-01"
    sp500_data = fetch_ticker_prices("^GSPC", start=start_date)
    
    df = pd.DataFrame(sp500_data)
    df.columns = ['date', 'sp500']
    df['date'] = pd.to_datetime(df['date'])
    
    print(f"Fetched {len(df)} S&P 500 records from {df['date'].min()} to {df['date'].max()}")
    
    return df


def create_combined_dataset(
    hist_json_path: str = "histprices.json",
    start_year: int = 1971,
    resample_to_monthly: bool = True
) -> pd.DataFrame:
    """
    Create a combined dataset with gold and S&P 500 from start_year onwards.
    
    Args:
        hist_json_path (str): Path to historical gold prices JSON
        start_year (int): Start year for the dataset (default 1971)
        resample_to_monthly (bool): If True, resample daily data to monthly
    
    Returns:
        pd.DataFrame: Combined dataset with gold and sp500 columns
    """
    print(f"Creating combined dataset from {start_year} onwards...")
    
    # Load historical gold data (monthly)
    gold_hist = load_historical_gold_from_json(hist_json_path, start_year=start_year)
    
    # Fetch S&P 500 data (daily)
    sp500_daily = fetch_sp500_historical(start_year=start_year)
    
    if resample_to_monthly:
        # Resample S&P 500 to monthly (end of month)
        sp500_monthly = sp500_daily.set_index('date').resample('ME').last().reset_index()
        sp500_monthly = sp500_monthly.dropna()
        
        # Convert gold dates to end of month for alignment
        gold_hist['date'] = pd.to_datetime(gold_hist['date']) + pd.offsets.MonthEnd(0)
        
        # Merge on date
        combined = pd.merge(gold_hist, sp500_monthly, on='date', how='outer')
        combined = combined.sort_values('date')
        
        # Forward fill S&P 500 for any missing months (should be minimal)
        combined['sp500'] = combined['sp500'].ffill()
        
        # For months where we have S&P but not gold (shouldn't happen), forward fill gold
        combined['gold'] = combined['gold'].ffill()
        
    else:
        # For daily data, we need to interpolate gold prices
        # Get date range from S&P 500
        all_dates = pd.DataFrame({'date': sp500_daily['date']})
        
        # Merge gold (monthly values will repeat across days in that month)
        combined = pd.merge(all_dates, sp500_daily, on='date', how='left')
        
        # For gold, merge and forward fill
        gold_hist_daily = gold_hist.copy()
        combined = pd.merge(combined, gold_hist_daily, on='date', how='left')
        combined['gold'] = combined['gold'].ffill()
    
    # Drop any remaining NaN rows
    combined = combined.dropna()
    
    # Round values
    combined['gold'] = combined['gold'].round(2)
    combined['sp500'] = combined['sp500'].round(2)
    
    print(f"Combined dataset: {len(combined)} records from {combined['date'].min()} to {combined['date'].max()}")
    
    return combined


def main():
    """
    Main preprocessing function: creates comprehensive gold vs S&P 500 dataset from 1971.
    
    This fetches:
    - Historical gold prices from histprices.json (1971+)
    - S&P 500 data from Yahoo Finance (1971+)
    
    And creates a merged, aligned dataset.
    """
    # Check if histprices.json exists
    hist_json = os.path.join(os.path.dirname(__file__), "..", "histprices.json")
    
    if not os.path.exists(hist_json):
        print("Warning: histprices.json not found. Using only yfinance data.")
        # Fetch both from yfinance
        gold = fetch_ticker_prices("GC=F", start="1971-01-01")
        sp500 = fetch_ticker_prices("^GSPC", start="1971-01-01")
        
        gold_df = pd.DataFrame(gold).rename(columns={'close': 'gold'})
        sp500_df = pd.DataFrame(sp500).rename(columns={'close': 'sp500'})
        
        gold_df['date'] = pd.to_datetime(gold_df['date'])
        sp500_df['date'] = pd.to_datetime(sp500_df['date'])
        
        combined = pd.merge(gold_df, sp500_df, on='date', how='inner')
    else:
        # Use historical data + yfinance
        combined = create_combined_dataset(
            hist_json_path=hist_json,
            start_year=1971,
            resample_to_monthly=True
        )
    
    # Save to output path
    out_path = os.path.join(os.path.dirname(__file__), "..", get_csv_path())
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    combined.to_csv(out_path, index=False)
    
    earliest = combined['date'].min()
    latest = combined['date'].max()
    print(f"✓ Saved {len(combined)} records from {earliest.date()} to {latest.date()} to {out_path}")


if __name__ == "__main__":
    main()
