
"""
Preprocesses gold and S&P 500 historical data from Yahoo Finance.

Fetches daily gold futures and S&P 500 index prices for the last 25 years,
aligns them by date, and saves the merged dataset as a CSV file.
"""




import os
import pandas as pd
import yaml
from fetch_ticker import fetch_ticker_prices




def get_csv_path():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config["csv_path"]

def main():
    """
    Fetches, aligns, and saves gold and S&P 500 historical data.

    Downloads daily gold futures and S&P 500 index prices, merges them by date,
    and writes the aligned data to 'gold_sp500_aligned.csv'.
    """
    gold = fetch_ticker_prices("GC=F")
    sp500 = fetch_ticker_prices("^GSPC")
    gold_df = pd.DataFrame([(row["date"], row["close"]) for row in gold], columns=["date", "gold"])
    sp500_df = pd.DataFrame([(row["date"], row["close"]) for row in sp500], columns=["date", "sp500"])
    merged = pd.merge(gold_df, sp500_df, on="date", how="inner")
    merged = merged.dropna()
    merged = merged.sort_values("date")
    # Round gold and sp500 columns to 1 decimal place
    merged["gold"] = merged["gold"].round(1)
    merged["sp500"] = merged["sp500"].round(1)
    # Get output CSV path from config.yaml
    out_path = os.path.join(os.path.dirname(__file__), "..", get_csv_path())
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    merged.to_csv(out_path, index=False)
    print(f"Saved {len(merged)} aligned records to {out_path}")

if __name__ == "__main__":
    main()
