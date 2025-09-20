
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

def split_date_range(start: pd.Timestamp, end: pd.Timestamp, n_parts: int = 5) -> list[pd.Timestamp]:
    """Split a date range into n_parts nearly equal intervals, distributing extra days as needed.
    Args:
        start (pd.Timestamp): Start date.
        end (pd.Timestamp): End date.
        n_parts (int): Number of intervals to split into.
    Returns:
        list[pd.Timestamp]: List of split points (including start and end).
    """
    total_days = (end - start).days
    base = total_days // n_parts
    remainder = total_days % n_parts
    split_points = [start]
    current = start
    for i in range(n_parts):
        days = base + (1 if i < remainder else 0)
        current = current + pd.Timedelta(days=days)
        split_points.append(current)
    return split_points

if len(df_range) < 2:
    st.warning("Please select a wider date range.")
else:
    split_points = split_date_range(start_date, end_date, 5)
    st.write("### Date range split into five intervals:")
    for i in range(5):
        st.write(f"Interval {i+1}: {split_points[i].date()} to {split_points[i+1].date()}")

    # Compare performance from start to the end of each interval
    st.write("\n### Relative performance from start to end of each interval:")
    start_row = df_range.iloc[0]
    for i in range(1, 6):
        interval_end = split_points[i]
        # Find the closest date in df_range to interval_end
        end_idx = df_range["date"].searchsorted(interval_end, side="right") - 1
        if end_idx < 0:
            st.write(f"Interval {i}: No data available.")
            continue
        end_row = df_range.iloc[end_idx]
        gold_pct = 100 * (end_row["gold"] - start_row["gold"]) / start_row["gold"]
        sp500_pct = 100 * (end_row["sp500"] - start_row["sp500"]) / start_row["sp500"]
        st.write(f"**Interval {i} ({start_row['date'].date()} to {end_row['date'].date()}):**")
        st.write(f"- Gold: {gold_pct:.2f}% change")
        st.write(f"- S&P 500: {sp500_pct:.2f}% change")
        if gold_pct > sp500_pct:
            winner = "Gold appreciated more (or depreciated less)"
        elif sp500_pct > gold_pct:
            winner = "S&P 500 appreciated more (or depreciated less)"
        elif gold_pct == sp500_pct:
            winner = "Both performed equally"
        else:
            winner = "Both depreciated equally"
        st.info(winner)
