# User Guide: Gold vs S&P 500 Historical Analysis

## Getting Started

This application allows you to analyze and compare gold and S&P 500 performance across nearly 200 years of history (1833-present).

## Data Sources

### Historical Gold Prices (1833-2025)
- **Source**: `histprices.json`
- **Frequency**: Monthly
- **Records**: 2,311 data points
- **Coverage**: Complete history from 1833 to July 2025

### Modern Market Data (2000-Present)
- **Sources**: Yahoo Finance (GC=F for gold, ^GSPC for S&P 500)
- **Frequency**: Daily
- **Coverage**: Both gold and S&P 500 index

## Feature Guide

### 1. Selecting Data Source

In the sidebar, choose from three data source options:

#### Daily Data (2000-Present)
- **Best for**: Recent market analysis with high granularity
- **Resolution**: Daily prices
- **Assets**: Both gold and S&P 500
- **Use cases**: 
  - Short-term performance comparison
  - Detailed recent market movements
  - Day-to-day volatility analysis

#### Monthly Historical (1833-Present)
- **Best for**: Long-term historical perspective
- **Resolution**: Monthly prices
- **Assets**: Gold only (S&P 500 didn't exist before 1957)
- **Use cases**:
  - Understanding gold's long-term value
  - Historical crisis periods (Great Depression, World Wars, etc.)
  - Multi-generational wealth preservation analysis

#### Combined View
- **Best for**: Complete picture with historical context
- **Resolution**: Monthly (daily data resampled)
- **Assets**: Gold throughout, S&P 500 from 2000 onwards
- **Use cases**:
  - Comprehensive historical analysis
  - Comparing modern performance to historical baseline
  - Understanding gold's role across different eras

### 2. Date Range Selection

#### Preset Ranges
Quick access to common time periods:
- **Last 1 Year**: Recent performance
- **Last 5 Years**: Medium-term trends
- **Last 10 Years**: Decade-long perspective
- **Last 25 Years**: Quarter-century view
- **Last 50 Years**: Half-century analysis
- **Since 1900**: 20th century onwards
- **Since 1833 (All Data)**: Complete historical record

#### Custom Selection
- Choose "Custom" from the dropdown
- Use the slider to select exact start and end dates
- Range automatically adjusts based on available data

### 3. Interval Analysis

**Number of Intervals Slider**: 2-10 intervals
- **Fewer intervals (2-3)**: Broad comparison across major periods
- **More intervals (7-10)**: Granular analysis of shorter periods
- Default: 5 intervals for balanced analysis

### 4. Understanding the Results

#### Interval Breakdown
Each interval shows:
- **Date range**: Start and end dates for the interval
- **Gold performance**: Percentage change
- **S&P 500 performance**: Percentage change (when available)
- **Winner indication**: Which asset outperformed

#### Performance Metrics
- **Positive %**: Asset appreciated in value
- **Negative %**: Asset depreciated in value
- **Comparison**: Direct head-to-head performance

#### Visualization
- **Indexed chart**: All values normalized to 100 at start date
- **Line colors**: 
  - Blue: Gold
  - Orange: S&P 500 (when available)
- **Y-axis**: Index value (start = 100)
- **X-axis**: Time period

## Example Use Cases

### Case 1: Great Depression Analysis (1929-1939)
1. Select "Monthly Historical (1833-Present)"
2. Choose "Custom" date range
3. Set range: 1929-01-01 to 1939-12-31
4. Set intervals to 5
5. Observe gold's stability during this crisis period

### Case 2: Modern Bull Market (2009-2019)
1. Select "Daily Data (2000-Present)"
2. Choose "Custom" date range
3. Set range: 2009-03-01 to 2019-12-31
4. Set intervals to 5
5. Compare gold vs stocks during the recovery

### Case 3: COVID-19 Impact (2020-2021)
1. Select "Daily Data (2000-Present)"
2. Choose "Custom" date range
3. Set range: 2020-01-01 to 2021-12-31
4. Set intervals to 4 (quarterly analysis)
5. Analyze safe-haven behavior

### Case 4: Long-Term Wealth Preservation (1900-2025)
1. Select "Combined View"
2. Choose "Since 1900"
3. Set intervals to 10 (decade-by-decade)
4. Understand gold's role across different economic eras

## Tips for Effective Analysis

1. **Start Broad**: Begin with larger time periods to understand overall trends
2. **Zoom In**: Use custom ranges to examine specific events or periods
3. **Adjust Intervals**: More intervals for detailed analysis, fewer for big picture
4. **Compare Views**: Switch between data sources to see different perspectives
5. **Context Matters**: Remember S&P 500 data only available from 2000 onwards

## Data Interpretation Notes

### Historical Considerations
- Gold prices before 1971 were heavily influenced by government fixed rates
- S&P 500 index methodology has changed over time
- Inflation significantly affects real returns (not adjusted in raw data)
- Historical prices don't include dividends or storage costs

### Modern Market Context
- Daily data shows higher volatility
- Monthly data smooths short-term fluctuations
- Recent gold prices reflect current market conditions
- S&P 500 represents diversified equity exposure

## Troubleshooting

### "No S&P 500 data available"
This is expected for periods before 2000. The application will show gold-only analysis.

### "Please select a wider date range"
The selected range is too narrow for meaningful interval analysis. Expand your date range or reduce the number of intervals.

### Data seems incorrect
- Ensure `histprices.json` exists in project root
- Run preprocessing: `python -m src.preprocess` to refresh modern data
- Check internet connection for Yahoo Finance data

## Further Resources

- **Project README**: Detailed installation and setup instructions
- **CHANGELOG**: Recent updates and version history
- **Tests**: `tests/test_load_historical.py` for data validation

---

For questions or issues, please refer to the project repository or open an issue on GitHub.
