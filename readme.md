# Gold vs S&P 500: Interactive Performance Comparison

A Streamlit web application that provides interactive analysis and comparison of Gold futures vs S&P 500 performance over customizable time periods. Users can analyze relative performance across different market conditions and timeframes.

## 🚀 Features

### 📊 Interactive Analysis
- **Date Range Selection**: Interactive slider for custom time period analysis
- **Performance Metrics**: Calculates percentage changes and relative performance
- **Interval Analysis**: Splits selected periods into 5 equal intervals for granular comparison
- **Winner Identification**: Clearly highlights which asset outperformed in each period

### 📈 Data Management
- **Automatic Data Fetching**: Downloads historical data from Yahoo Finance using `yfinance`
- **Data Alignment**: Merges and aligns Gold futures (GC=F) and S&P 500 (^GSPC) data by date
- **Preprocessing Pipeline**: Automated data cleaning and preparation
- **Persistent Storage**: Cached data in CSV format for improved performance

### 🎨 Visualization & Analysis
- Clean, intuitive Streamlit interface
- Real-time performance calculations
- Detailed interval breakdowns
- Optional exploratory data analysis tools

## 📁 Project Structure

```
├── README.md                   # Project documentation
├── main.py                     # Main Streamlit application
├── config.yaml                 # Configuration settings
├── pyproject.toml             # Project dependencies and metadata
├── uv.lock                    # Lock file for dependencies
├── test.py                    # Test runner
├── .gitignore                 # Git ignore patterns
├── .python-version            # Python version specification
│
├── src/                       # Source code modules
│   ├── eda.py                 # Exploratory data analysis tools
│   ├── fetch_ticker.py        # Data fetching utilities
│   └── preprocess.py          # Data preprocessing pipeline
│
├── data/                      # Data storage
│   └── gold_sp500_aligned.csv # Processed historical data
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
2. Use the date range slider to select your analysis period
3. View the automatic interval breakdown (5 equal periods)
4. Compare Gold vs S&P 500 performance metrics
5. Identify the winning asset for each interval

### Advanced Features
- **Custom Date Ranges**: Select any period from the available historical data
- **Interval Analysis**: Automatic splitting of selected periods for detailed comparison
- **Performance Metrics**: View percentage changes and relative performance
- **Data Refresh**: Data automatically updates and processes if source files are missing

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

- **Gold Futures**: Yahoo Finance ticker `GC=F`
- **S&P 500 Index**: Yahoo Finance ticker `^GSPC`
- **Data Range**: Approximately 25 years of historical data
- **Update Frequency**: Data refreshes automatically when running the application

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
