"""
Fetch historical price data for any ticker from Yahoo Finance and optionally save it to CSV.
"""

import csv
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Union

import requests

BASE_URL = "https://query2.finance.yahoo.com/v8/finance/chart/{}"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; DataBot/1.0)"}
DEFAULT_START_DATE = datetime(1971, 1, 1, tzinfo=timezone.utc)


def _to_utc_datetime(value: Optional[Union[str, date, datetime]]) -> datetime:
    """Convert a supported date-like value into an aware UTC datetime."""
    if value is None:
        return DEFAULT_START_DATE
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, date):
        dt = datetime(value.year, value.month, value.day)
    elif isinstance(value, str):
        dt = datetime.fromisoformat(value)
    else:
        raise TypeError(f"Unsupported date type: {type(value)!r}")
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def fetch_ticker_prices(
    ticker: str,
    start: Optional[Union[str, date, datetime]] = None,
    end: Optional[Union[str, date, datetime]] = None,
) -> List[Dict[str, Union[float, str]]]:
    """
    Fetch historical price data for a given ticker from the Yahoo Finance chart API.

    Args:
        ticker: Ticker symbol (e.g., 'GC=F', '^GSPC').
        start: Inclusive start date (defaults to 1971-01-01).
        end: Exclusive end date (defaults to "now").

    Returns:
        List of {"date": str, "close": float} for each available day.
    """
    start_dt = _to_utc_datetime(start)
    end_dt = _to_utc_datetime(end) if end is not None else datetime.now(timezone.utc)
    params = {
        "interval": "1d",
        "period1": int(start_dt.timestamp()),
        "period2": int(end_dt.timestamp()),
    }
    response = requests.get(BASE_URL.format(ticker), headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()
    result_data = data["chart"]["result"][0]
    timestamps = result_data["timestamp"]
    closes = result_data["indicators"]["quote"][0]["close"]
    result: List[Dict[str, Union[float, str]]] = []
    for ts, close in zip(timestamps, closes):
        if close is not None:
            date_str = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
            result.append({"date": date_str, "close": close})
    return result


def save_prices_to_csv(prices: List[Dict[str, Union[float, str]]], filename: Union[str, Path]) -> None:
    """
    Save a list of price dicts to a CSV file.

    Args:
        prices: List of {"date": str, "close": float}.
        filename: Path to the output CSV file.
    """
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "close"])
        writer.writeheader()
        for row in prices:
            writer.writerow(row)


if __name__ == "__main__":
    import sys

    if len(sys.argv) not in (3, 4, 5):
        print("Usage: python fetch_ticker.py <TICKER> <OUTPUT_CSV> [<START>] [<END>]")
        exit(1)
    ticker = sys.argv[1]
    output_csv = sys.argv[2]
    start_arg = sys.argv[3] if len(sys.argv) >= 4 else None
    end_arg = sys.argv[4] if len(sys.argv) == 5 else None
    prices = fetch_ticker_prices(ticker, start=start_arg, end=end_arg)
    save_prices_to_csv(prices, output_csv)
    print(f"Saved {len(prices)} rows to {output_csv}")
