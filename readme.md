# Gold vs S&P 500: Interactive Performance Comparison

A Streamlit web application that provides interactive analysis and comparison of Gold futures vs S&P 500 performance over customizable time periods, with historical data dating back to 1833. Users can analyze relative performance across different market conditions and timeframes.

## 🚀 Features

### 📊 Interactive Analysis
- **Multiple Data Sources**: Choose between daily data (2000-present), monthly historical (1833-present), or combined view
- **Flexible Date Range Selection**: 
  - Interactive slider for custom time period analysis
  - Preset ranges: Last 1/5/10/25/50 years, Since 1900, or all data since 1833
- **Performance Metrics**: Calculates percentage changes and relative performance
- **Adjustable Interval Analysis**: Split selected periods into 2-10 intervals for granular comparison
- **Winner Identification**: Clearly highlights which asset outperformed in each period
- **Price Visualization**: Indexed price charts showing normalized performance over time

### 📈 Data Management
- **Historical Gold Data**: Monthly gold prices from 1833 to present (from histprices.json)
- **Modern Market Data**: Daily Gold futures (GC=F) and S&P 500 (^GSPC) from 2000 onwards
- **Automatic Data Fetching**: Downloads recent data from Yahoo Finance using `yfinance`
- **Data Alignment**: Merges and aligns data from multiple sources by date
- **Preprocessing Pipeline**: Automated data cleaning and preparation
- **Persistent Storage**: Cached data in CSV format for improved performance

### 🎨 Visualization & Analysis
- Clean, intuitive Streamlit interface with sidebar controls
- Real-time performance calculations
- Detailed interval breakdowns with color-coded results
- Line charts showing indexed performance (base 100)
- Contextual information about data availability
- Optional exploratory data analysis tools

## 📁 Project Structure

```
├── README.md                   # Project documentation
├── main.py                     # Main Streamlit application
├── config.yaml                 # Configuration settings
├── histprices.json            # Historical monthly gold prices (1833-2025)
├── pyproject.toml             # Project dependencies and metadata
├── uv.lock                    # Lock file for dependencies
├── test.py                    # Test runner
├── .gitignore                 # Git ignore patterns
├── .python-version            # Python version specification
│
├── src/                       # Source code modules
│   ├── eda.py                 # Exploratory data analysis tools
│   ├── fetch_ticker.py        # Data fetching utilities
│   ├── load_historical.py     # Historical data loader (NEW)
│   └── preprocess.py          # Data preprocessing pipeline
│
├── data/                      # Data storage
│   └── gold_sp500_aligned.csv # Processed historical data (daily)
│
├── tests/                     # Unit tests
│   ├── test_eda.py           # EDA function tests
│   └── test_preprocess.py    # Preprocessing tests
│
├── utils/                     # Documentation and utilities
│   ├── copilot-instructions.md
│   ├── load_config.py        # Configuration loader
│   ├── setup.md              # Setup documentation
│   └── yfinance.md           # yfinance usage guide
│
├── logs/                      # Application logs
│   └── main.log
│
└── .github/                   # GitHub specific files
    └── copilot-instructions.md
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip or uv package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gold-vs-equities
   ```

2. **Install dependencies**
   
   Using uv (recommended):
   ```bash
   uv sync
   ```
   
   Or using pip:
   ```bash
   pip install -e .
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```

4. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Start exploring the data!

### Alternative Installation Methods

**Using virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
streamlit run main.py
```

**Development installation:**
```bash
pip install -e .[dev]  # Includes testing dependencies
```

## 📱 Usage Guide

### Basic Usage
1. Launch the Streamlit app using `streamlit run main.py`
2. In the sidebar, select your preferred data source:
   - **Daily Data (2000-Present)**: High-resolution daily prices
   - **Monthly Historical (1833-Present)**: Long-term historical perspective
   - **Combined View**: Best of both worlds with monthly aggregation
3. Choose a preset date range or select "Custom" for full control
4. Adjust the number of intervals (2-10) to split your analysis period
5. View performance metrics, charts, and comparative analysis

### Using Date Range Presets
The sidebar offers convenient preset ranges:
- **Last 1/5/10/25/50 Years**: Recent market performance
- **Since 1900**: 20th century onwards
- **Since 1833 (All Data)**: Complete historical perspective
- **Custom**: Use the slider for exact date selection

### Advanced Features
- **Adjustable Intervals**: Split your analysis into 2-10 equal periods
- **Performance Visualization**: Indexed line charts (base 100) show relative performance
- **Multi-Source Data**: Seamlessly combines historical and modern data
- **Smart Data Handling**: Automatically indicates when S&P 500 data is unavailable
- **Percentage Calculations**: View exact percentage changes for each interval

### Understanding the Data
- **Historical Data (1833-1999)**: Monthly gold prices only (S&P 500 index didn't exist)
- **Modern Data (2000-Present)**: Daily gold and S&P 500 prices
- **Combined View**: Monthly resampling for consistent comparison across all time periods

### Configuration
Modify `config.yaml` to adjust:
- Data sources and tickers
- Analysis parameters
- Application settings

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

## 📊 Data Sources

### Modern Market Data (2000-Present)
- **Gold Futures**: Yahoo Finance ticker `GC=F` (daily prices)
- **S&P 500 Index**: Yahoo Finance ticker `^GSPC` (daily prices)
- **Update Frequency**: Data refreshes automatically when running the application

### Historical Gold Data (1833-Present)
- **Source**: `histprices.json` - Monthly gold price data
- **Coverage**: 1833 to present (192+ years of data)
- **Frequency**: Monthly prices
- **Note**: S&P 500 data only available from 2000 onwards

### Data Processing
- Daily data automatically aligned and merged by date
- Historical monthly data seamlessly integrated
- Combined view resamples daily to monthly for consistency
- Missing values handled appropriately

## 🔧 Dependencies

### Core Dependencies
- `streamlit` - Web application framework
- `pandas` - Data manipulation and analysis
- `yfinance` - Yahoo Finance data fetching
- `pyyaml` - Configuration file handling

### Development Dependencies
- `pytest` - Testing framework
- `matplotlib` - Data visualization
- `seaborn` - Statistical data visualization

See `pyproject.toml` for complete dependency list and version specifications.

## 🚀 Performance Features

- **Caching**: Processed data is cached to avoid redundant API calls
- **Lazy Loading**: Data processing only occurs when needed
- **Efficient Calculations**: Optimized pandas operations for performance
- **Streamlined Interface**: Responsive UI with minimal loading times

## 📈 Analysis Capabilities

### Performance Metrics
- Absolute percentage changes
- Relative performance comparison
- Interval-based analysis
- Historical trend identification

### Time Period Analysis
- Custom date range selection
- Automatic interval splitting (5 equal periods)
- Start-to-end performance calculation
- Period-over-period comparison

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

## 🔄 Changelog

### Latest Updates
- ✅ Streamlined project structure with files at repository root
- ✅ Enhanced README with comprehensive documentation
- ✅ Improved data processing pipeline
- ✅ Added comprehensive test suite
- ✅ Optimized performance and caching

---

*Built using Streamlit and Python*
