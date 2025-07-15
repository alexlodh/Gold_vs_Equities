"""
Fetches historical S&P 500 price data from Yahoo Finance.
"""

import requests
from datetime import datetime

SP500_URL = "https://query2.finance.yahoo.com/v8/finance/chart/^GSPC?interval=1d&range=25y"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; DataBot/1.0)"}

def fetch_sp500_prices():
    """
    Fetches historical S&P 500 price data from Yahoo Finance chart API.

    Returns:
        list of dict: List of {"date": str, "close": float} for each available day.
    """
    response = requests.get(SP500_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    timestamps = data['chart']['result'][0]['timestamp']
    closes = data['chart']['result'][0]['indicators']['quote'][0]['close']
    result = []
    for ts, close in zip(timestamps, closes):
        if close is not None:
            date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
            result.append({"date": date, "close": close})
    return result
