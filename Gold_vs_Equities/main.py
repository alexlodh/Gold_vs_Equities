
import os
import streamlit as st
import pandas as pd
from datetime import datetime
import importlib.util

# Path to the aligned data CSV
DATA_PATH = os.path.join("data", "gold_sp500_aligned.csv")

# Check if CSV exists, if not, run preprocess.main()
if not os.path.exists(DATA_PATH):
    spec = importlib.util.spec_from_file_location("preprocess", os.path.join("src", "preprocess.py"))
    preprocess = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(preprocess)
    preprocess.main()

# Load the data
df = pd.read_csv(DATA_PATH, parse_dates=["date"])

st.title("Gold vs S&P 500: Range Comparison")


# Date slider (convert to datetime.date for Streamlit)
min_date = df["date"].min().date()
max_date = df["date"].max().date()
date_range = st.slider(
    "Select date range:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

# Convert back to pd.Timestamp for filtering
start_date, end_date = [pd.Timestamp(d) for d in date_range]
mask = (df["date"] >= start_date) & (df["date"] <= end_date)
df_range = df.loc[mask]

if len(df_range) < 2:
    st.warning("Please select a wider date range.")
else:
    start_row = df_range.iloc[0]
    end_row = df_range.iloc[-1]
    gold_pct = 100 * (end_row["gold"] - start_row["gold"]) / start_row["gold"]
    sp500_pct = 100 * (end_row["sp500"] - start_row["sp500"]) / start_row["sp500"]

    st.write(f"**Gold**: {gold_pct:.2f}% change")
    st.write(f"**S&P 500**: {sp500_pct:.2f}% change")

    if gold_pct > sp500_pct:
        winner = "Gold appreciated more (or depreciated less)"
    elif sp500_pct > gold_pct:
        winner = "S&P 500 appreciated more (or depreciated less)"
    elif gold_pct == sp500_pct:
        winner = "Both performed equally"
    else:
        winner = "Both depreciated equally"

    st.success(winner)
