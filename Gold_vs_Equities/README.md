# Gold vs Equities: Interactive Analysis

This project provides an interactive Streamlit web app to compare the historical performance of Gold and the S&P 500 index over the past 25 years.

## Features

- **Data Fetching & Preprocessing:**
  - Downloads daily gold futures and S&P 500 index prices from Yahoo Finance.
  - Aligns and merges the data by date, saving it as `data/gold_sp500_aligned.csv`.
- **Interactive App:**
  - Lets users select a custom date range with a slider.
  - Calculates and displays the percentage change in Gold and S&P 500 values over the selected range.
  - Highlights which asset appreciated more (or depreciated less) in the chosen period.
- **Visualisation:**
  - (Optional) Includes a script for plotting both assets' price history using Matplotlib and Seaborn.

## How to Run

1. **Install dependencies:**
   - All requirements are listed in `pyproject.toml`.
   - Recommended: Use a virtual environment.
   - Install with `pip install -e .` or `pip install -r requirements.txt` if you export one.
2. **Start the Streamlit app:**
   ```sh
   streamlit run main.py
   ```
3. **Explore:**
   - Use the slider to select a date range and compare asset performance.

## File Structure

- `main.py` — Streamlit app entry point.
- `src/preprocess.py` — Fetches and aligns raw data.
- `src/eda.py` — (Optional) Script for static data visualisation.
- `data/gold_sp500_aligned.csv` — Aligned dataset (auto-generated).
- `utils/` — Documentation and setup notes.

## Requirements

- Python 3.11+
- See `pyproject.toml` for package dependencies (pandas, streamlit, matplotlib, seaborn, requests, etc.)

## License

MIT License (add details if needed)
