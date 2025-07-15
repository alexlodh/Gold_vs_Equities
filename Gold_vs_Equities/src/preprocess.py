
"""
Preprocesses gold and S&P 500 historical data from Yahoo Finance.

Fetches daily gold futures and S&P 500 index prices for the last 25 years,
aligns them by date, and saves the merged dataset as a CSV file.
"""



import os
import pandas as pd
from fetch_gold import fetch_gold_data
from fetch_sp500 import fetch_sp500_prices




def main():
    """
    Fetches, aligns, and saves gold and S&P 500 historical data.

    Downloads daily gold futures and S&P 500 index prices, merges them by date,
    and writes the aligned data to 'gold_sp500_aligned.csv'.
    """
    gold = fetch_gold_data()
    sp500 = fetch_sp500_prices()
    gold_df = pd.DataFrame([(row["date"], row["close"]) for row in gold], columns=["date", "gold"])
    sp500_df = pd.DataFrame([(row["date"], row["close"]) for row in sp500], columns=["date", "sp500"])
    merged = pd.merge(gold_df, sp500_df, on="date", how="inner")
    merged = merged.dropna()
    merged = merged.sort_values("date")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "gold_sp500_aligned.csv")
    merged.to_csv(out_path, index=False)
    print(f"Saved {len(merged)} aligned records to {out_path}")

if __name__ == "__main__":
    main()
