"""
Fetches historical gold price data from Yahoo Finance.
"""

import requests
from datetime import datetime

API_URL = "https://query2.finance.yahoo.com/v8/finance/chart/GC=F?interval=1d&range=25y"

def fetch_gold_data():
    """
    Fetches historical gold price data from Yahoo Finance chart API.

    Returns:
        list of dict: List of {"date": str, "close": float} for each available day.
    """
    headers = {"User-Agent": "Mozilla/5.0 (compatible; GoldDataBot/1.0)"}
    max_retries = 5
    backoff = 2
    for attempt in range(max_retries):
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 429:
            wait_time = backoff ** attempt
            print(f"Rate limited (429). Retrying in {wait_time} seconds...")
            import time
            time.sleep(wait_time)
            continue
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
    raise Exception("Failed to fetch data after multiple retries due to rate limiting.")

