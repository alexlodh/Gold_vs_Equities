# Gold vs S&P 500: Historical Analysis (1971-Present)

A sophisticated Streamlit web application for analyzing and comparing Gold vs S&P 500 performance from 1971 onwards—the year the US left the gold standard. Features advanced statistical analysis, correlation studies, and recession period highlighting for comprehensive investment insights.

## 🚀 Features

### 📊 Comprehensive Analysis Tools
- **Historical Dataset**: 658 monthly records from January 1971 to October 2025
- **Calendar-Style Date Selection**: Easy-to-use date pickers for precise period selection
- **Preset Ranges**: Quick access to 1Y, 5Y, 10Y, 20Y, Since 2000, Since 1980, or complete dataset
- **Overall Performance Metrics**: Clear percentage changes with start/end values
- **Indexed Price Charts**: Normalized performance visualization (base 100)
- **Recession Highlighting**: Gray shading on all charts for NBER-defined recession periods

### 📈 Statistical Analysis (PMCC)
- **Pearson Correlation Coefficient**: Measure linear relationship between assets
- **Statistical Significance**: P-values and confidence metrics
- **Scatter Plot with Best-Fit Line**: Matplotlib visualization with linear regression
- **Coefficient of Determination (R²)**: Variance explanation analysis
- **Rolling Correlation**: Time-varying correlation with adjustable windows (3-36 months)
- **Correlation Strength Interpretation**: Automated categorization (Strong/Moderate/Weak)

### 🎨 Advanced Visualizations
````markdown
# Gold vs S&P 500: Historical Analysis (1971-Present)

A sophisticated Streamlit web application for analyzing and comparing Gold vs S&P 500 performance from 1971 onwards—the year the US left the gold standard. Features advanced statistical analysis, correlation studies, and recession period highlighting for comprehensive investment insights.

## 🚀 Features

### 📊 Comprehensive Analysis Tools
- **Historical Dataset**: 658 monthly records from January 1971 to October 2025
- **Calendar-Style Date Selection**: Easy-to-use date pickers for precise period selection
- **Preset Ranges**: Quick access to 1Y, 5Y, 10Y, 20Y, Since 2000, Since 1980, or complete dataset
- **Overall Performance Metrics**: Clear percentage changes with start/end values
- **Indexed Price Charts**: Normalized performance visualization (base 100)
- **Recession Highlighting**: Gray shading on all charts for NBER-defined recession periods

### 📈 Statistical Analysis (PMCC)
- **Pearson Correlation Coefficient**: Measure linear relationship between assets
- **Statistical Significance**: P-values and confidence metrics
- **Scatter Plot with Best-Fit Line**: Matplotlib visualization with linear regression
- **Coefficient of Determination (R²)**: Variance explanation analysis
- **Rolling Correlation**: Time-varying correlation with adjustable windows (3-36 months)
- **Correlation Strength Interpretation**: Automated categorization (Strong/Moderate/Weak)

### 🎨 Advanced Visualizations
- **Professional Charts**: Matplotlib-based with recession period shading
- **Line of Best Fit**: Linear regression on scatter plots
- **Multiple Chart Types**: Price history, scatter plots, rolling correlations
- **Recession Context**: Visual markers for 7 major US recessions (1973-2020)
- **Interactive Elements**: Tooltips, legends, and detailed annotations
- **Responsive Design**: Clean Streamlit interface optimized for analysis

### 📊 Data Sources & Quality
- **Historical Gold Prices**: Monthly data from histprices.json (1971-2025)
- **S&P 500 Index**: Yahoo Finance API integration (^GSPC)
- **Recent Updates**: Includes October 16, 2025 data
- **No Gaps**: Complete coverage for entire 54+ year period
- **Automatic Preprocessing**: Alignment and monthly resampling

## 📁 Project Structure

```
├── README.md                      # Project documentation
├── main.py                        # Main Streamlit application
├── config.yaml                    # Configuration settings
├── histprices.json                # Historical monthly gold prices (1971-2025)
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Project metadata
│
├── src/                           # Source code modules
│   ├── eda.py                     # Exploratory data analysis tools
│   ├── fetch_ticker.py            # Yahoo Finance data fetching
│   ├── preprocess.py              # Data preprocessing
│   └── preprocess_1971.py         # Enhanced preprocessing for 1971+ data
│
├── data/                          # Data storage
│   └── gold_sp500_aligned.csv     # 658 monthly records (1971-2025)
│
├── tests/                         # Unit tests
│   ├── test_eda.py               # Analysis function tests
│   └── test_preprocess.py        # Data processing tests
│
├── utils/                         # Utilities and documentation
│   ├── load_config.py            # Configuration loader
│   └── copilot-instructions.md   # Development guidelines
│
└── web/                          # Next.js + shadcn dashboard (React)
    ├── app/                     # App router pages/layouts
    ├── components/              # Shadcn UI components
    └── package.json             # Node dependencies
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11.9 or higher
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/alexlodh/Gold_vs_Equities.git
   cd Gold_vs_Equities
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python -m streamlit run main.py
   ```

4. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Start analyzing!

### 🆕 Shadcn (Next.js) Dashboard

The repository now includes a fully responsive React implementation using Next.js 14 and shadcn/ui components. It reads the same CSV dataset and mirrors the Streamlit experience with modern web tooling.

1. **Install Node dependencies**
   ```bash
   cd web
   npm install
   ```
2. **Start the development server**
   ```bash
   npm run dev
   ```
3. **Open your browser**
   - Navigate to `http://localhost:3000`
   - Interact with the shadcn dashboard (preset ranges, custom date picker, indexed charts, correlation + rolling analysis, recession shading)

The Next.js app reads data from `../data/gold_sp500_aligned.csv`. Ensure the dataset exists (generate it with `python src/preprocess_1971.py` if needed) before launching the React dashboard.

### Data Regeneration (Optional)

To regenerate the dataset with fresh data from Yahoo Finance:

```bash
python src/preprocess_1971.py
```

This will:
- Load historical gold prices from histprices.json (1971+)
- Fetch S&P 500 data from Yahoo Finance
- Create monthly aligned dataset
- Save to `data/gold_sp500_aligned.csv`

## 📱 Usage Guide

### Basic Usage
1. Launch the app: `python -m streamlit run main.py`
2. **Select Date Range** in sidebar:
   - Choose a preset (1Y, 5Y, 10Y, 20Y, Since 2000, Since 1980, Since 1971)
   - Or select "Custom" for calendar date pickers
3. View **Overall Performance** summary with percentage changes
4. Explore **Price History** chart with recession shading
5. Analyze **Correlation (PMCC)** section for statistical insights

### Date Range Selection
**Preset Options:**
- **Last 1/5/10/20 Years**: Recent market analysis
- **Since 2000**: 21st century performance
- **Since 1980**: Modern economic era
- **Since 1971 (All Data)**: Complete post-gold-standard analysis

**Custom Selection:**
- Click "Custom" in dropdown
- Use calendar widgets to pick exact start/end dates
- Validation ensures start date is before end date

### Understanding the Analysis

**Overall Performance**
- Shows total % change for selected period
- Displays start and end values with dates
- Identifies which asset outperformed and by how much

**Price History Visualization**
- Indexed to 100 at start date
- Gray shading = US recession periods
- Both assets normalized for direct comparison

**Correlation Analysis (PMCC)**
- **r value**: Correlation coefficient (-1 to +1)
- **p-value**: Statistical significance (< 0.05 = significant)
- **Scatter plot**: Visual relationship with regression line
- **R²**: Proportion of variance explained
- **Rolling correlation**: Time-varying relationship (with data limitation warning)

### Recession Periods Highlighted
- 1973-75: Oil Crisis
- 1980: Early 80s Recession (Part 1)
- 1981-82: Early 80s Recession (Part 2)
- 1990-91: Gulf War Recession
- 2001: Dot-com Recession
- 2007-09: Great Recession
- 2020: COVID-19 Recession

### Why 1971?
August 15, 1971: President Nixon ended the gold standard, making this the most relevant starting point for comparing gold and equities as investment assets in the modern fiat currency era.

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python -m pytest

# Run specific test files
python -m pytest tests/test_preprocess.py
python -m pytest tests/test_eda.py

# Run with coverage
python -m pytest --cov=src tests/
```

## 📊 Data Sources & Statistics

### Dataset Overview
- **658 monthly records** from January 1971 to October 2025
- **54+ years** of consistent, aligned data
- **No gaps**: Complete coverage for entire period
- **Monthly frequency**: End-of-month values

### Gold Price Data
- **Source**: `histprices.json` (historical monthly gold prices)
- **Range**: $37.88 (Jan 1971) to $4,369.20 (Oct 2025)
- **Mean**: $729.86
- **Coverage**: Complete from 1971 onwards

### S&P 500 Index Data
- **Source**: Yahoo Finance API (^GSPC)
- **Range**: 63.54 (Jan 1971) to 6,688.46 (Sep 2025)
- **Mean**: $1,230.50
- **Updated**: October 16, 2025

### Data Processing Pipeline
1. Load historical gold from JSON (1971+)
2. Fetch S&P 500 from Yahoo Finance API
3. Resample daily data to monthly (month-end)
4. Align dates and merge datasets
5. Validate and save to CSV

### Recession Period Data
Source: National Bureau of Economic Research (NBER)
- 7 recession periods from 1973-2020
- Accurately dated start and end months
- Visualized as gray shading on all time-series charts

## 🔧 Dependencies

### Core Dependencies
- `streamlit>=1.46.1` - Web application framework
- `pandas>=2.3.1` - Data manipulation and analysis
- `numpy` - Numerical computations
- `matplotlib>=3.10.3` - Professional data visualization
- `scipy>=1.11.0` - Statistical analysis (Pearson correlation)
- `requests>=2.32.4` - HTTP library for API calls
- `pyyaml>=6.0.2` - Configuration file handling

### Development Dependencies
- `pytest>=8.4.1` - Testing framework
- `seaborn>=0.13.2` - Statistical data visualization

See `requirements.txt` for complete dependency list with exact versions.

## � Key Insights & Use Cases

### Investment Analysis
- **Safe Haven Testing**: See if gold truly performs better during recessions
- **Diversification**: Analyze correlation to understand portfolio diversification benefits
- **Long-term Trends**: 54+ years of data reveals secular trends
- **Crisis Performance**: Examine behavior during 7 major economic crises

### Statistical Applications
- **Correlation Studies**: Measure relationship strength between assets
- **Regression Analysis**: Linear relationships and predictive modeling
- **Variance Explanation**: Understanding how much one asset explains the other
- **Time-Varying Relationships**: Rolling correlation reveals changing dynamics

### Historical Context
- **Post-Gold Standard Era**: Analysis from the modern fiat currency period
- **Multiple Market Cycles**: Bull markets, bear markets, and transitions
- **Economic Regime Changes**: From stagflation to Great Moderation to QE era
- **Crisis Comparisons**: Compare 1970s oil shocks to 2008 financial crisis to COVID-19

### Practical Applications
- **Portfolio Construction**: Data-driven asset allocation decisions
- **Risk Management**: Understanding correlation during market stress
- **Academic Research**: Comprehensive dataset for financial studies
- **Economic Education**: Visual learning about asset behavior over decades

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♀️ Support & Contact

- **Issues**: Please use the GitHub Issues tab for bug reports and feature requests
- **Documentation**: Additional docs available in the `utils/` directory
- **Configuration**: See `config.yaml` and `utils/setup.md` for detailed setup information

## 🔄 Recent Updates

### v2.0 - Major Overhaul (October 2025)
- ✅ **Focused 1971-Present Analysis**: Trimmed to post-gold-standard era
- ✅ **Complete S&P 500 Integration**: Full dataset from Yahoo Finance
- ✅ **Calendar Date Pickers**: Replaced slider with intuitive date selection
- ✅ **Correlation Analysis (PMCC)**: Full statistical suite with scatter plots
- ✅ **Recession Highlighting**: Visual markers for 7 NBER recession periods
- ✅ **Matplotlib Visualizations**: Professional charts with line of best fit
- ✅ **Removed Intervals**: Simplified to overall performance metrics
- ✅ **Enhanced Documentation**: Comprehensive README with usage examples
- ✅ **658 Monthly Records**: Complete, gap-free dataset

### Data Quality
- Latest data: October 16, 2025
- No missing values in 54+ year period
- Consistent monthly frequency throughout
- Validated against source data

## 📊 Technical Details

### Why Monthly Data?
- **Historical Consistency**: histprices.json provides reliable monthly gold data from 1971
- **Reduced Noise**: Monthly data smooths out daily volatility for clearer trends
- **Complete Coverage**: No gaps across entire 54-year period
- **Trade-off**: Less granularity than daily data, but more robust for long-term analysis

### Statistical Considerations
- **Pearson Correlation**: Measures linear relationships (r from -1 to +1)
- **P-value < 0.05**: Indicates statistically significant correlation
- **Rolling Correlation Warning**: Monthly data limits reliability (see app disclaimer)
- **R² Interpretation**: Coefficient of determination shows variance explained

### Chart Features
- **Recession Shading**: Semi-transparent gray for NBER recession periods
- **Indexed Charts**: Base 100 at start date for normalized comparison
- **Linear Regression**: Best-fit line on scatter plots
- **Responsive Design**: Charts adapt to date range selection

---

**Repository**: [github.com/alexlodh/Gold_vs_Equities](https://github.com/alexlodh/Gold_vs_Equities)

*Built with Streamlit, Pandas, Matplotlib, and SciPy*

## 🐳 Docker: Run the shadcn (Next.js) frontend

You can build and run the shadcn/Next.js dashboard in a container. The repository includes a production Dockerfile at `web/Dockerfile` and a `docker-compose.yml` that exposes the frontend at http://localhost:3001.

1) Build and run (production image)

```bash
# from repository root
docker compose build web
docker compose up -d web
```

2) Verify

Open your browser at:

- Frontend: http://localhost:3001

3) Stop and remove

```bash
docker compose down
```

Dev notes
- The production image runs `next start` on port `3000` inside the container and `docker-compose.yml` maps it to `3001` on the host. If you prefer fast local iteration, run the dev server locally with `npm run dev` inside `web/` (bind mounts or a dev-specific compose file reduce rebuilds).

If you want me to also add a development `docker-compose.override.yml` with volumes for hot-reload, tell me and I'll add it.

````
