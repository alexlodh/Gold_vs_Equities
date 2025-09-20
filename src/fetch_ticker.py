"""
Fetches historical price data for any ticker from Yahoo Finance and saves it to a CSV file.
"""

import requests
import csv
from datetime import datetime, timezone
from pathlib import Path

BASE_URL = "https://query2.finance.yahoo.com/v8/finance/chart/{}?interval=1d&range=25y"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; DataBot/1.0)"}

from typing import List, Dict, Union

def fetch_ticker_prices(ticker: str) -> List[Dict[str, Union[float, str]]]:
    """
    Fetches historical price data for a given ticker from Yahoo Finance chart API.

    Args:
        ticker (str): The ticker symbol (e.g., 'GC=F', '^GSPC').
    Returns:
        list of dict: List of {"date": str, "close": float} for each available day.
    """
    url = BASE_URL.format(ticker)
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    timestamps = data['chart']['result'][0]['timestamp']
    closes = data['chart']['result'][0]['indicators']['quote'][0]['close']
    result = []
    for ts, close in zip(timestamps, closes):
        if close is not None:
            date = datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d')
            result.append({"date": date, "close": close})
    return result

def save_prices_to_csv(prices: List[Dict[str, Union[float, str]]], filename: Union[str, Path]) -> None:
    """
    Saves a list of price dicts to a CSV file.

    Args:
        prices (list of dict): List of {"date": str, "close": float}.
        filename (str or Path): Path to the output CSV file.
    """
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "close"])
        writer.writeheader()
        for row in prices:
            writer.writerow(row)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python fetch_ticker.py <TICKER> <OUTPUT_CSV>")
        exit(1)
    ticker = sys.argv[1]
    output_csv = sys.argv[2]
    prices = fetch_ticker_prices(ticker)
    save_prices_to_csv(prices, output_csv)
    print(f"Saved {len(prices)} rows to {output_csv}")
