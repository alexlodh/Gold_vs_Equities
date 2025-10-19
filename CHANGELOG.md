# Changelog

All notable changes to the Gold vs S&P 500 Analysis project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Historical Data Integration**: Monthly gold price data from 1833 to present (192+ years)
- **New Data Source Module** (`src/load_historical.py`): Utilities for loading and combining historical data
- **Multiple Data View Options**: Users can now choose between daily, monthly historical, or combined views
- **Preset Date Ranges**: Quick selection for 1/5/10/25/50 years, since 1900, or all data since 1833
- **Adjustable Intervals**: Users can now split analysis into 2-10 intervals (previously fixed at 5)
- **Price Visualization**: Indexed line charts showing normalized performance over time
- **Enhanced Sidebar Controls**: Organized data settings and date range options
- **Contextual Information**: Smart notifications about data availability for different time periods
- **Test Suite** for historical data loading (`tests/test_load_historical.py`)
- `histprices.json` containing monthly gold prices from 1833-2025

### Changed
- **Enhanced Main Application**: Completely redesigned `main.py` with multi-source data support
- **Date Range Selection**: Now supports both preset ranges and custom slider selection
- **Documentation**: Updated README with new features, usage guide, and data source information
- **Data Handling**: Improved monthly resampling using 'ME' (month-end) instead of deprecated 'M'

### Fixed
- Deprecation warnings for pandas resampling frequency
- Proper handling of missing S&P 500 data in historical periods
- Enhanced error handling in data loading functions

## [0.2.0] - 2024-10-17

### Added
- Comprehensive project restructuring with files at repository root
- Enhanced README.md with detailed documentation
- Improved .gitignore with comprehensive patterns
- requirements.txt for pip compatibility
- MIT License file
- Changelog

### Changed
- Moved all project files from `Gold_vs_Equities/` subdirectory to repository root
- Updated project structure for better GitHub visibility
- Enhanced documentation and setup instructions

### Fixed
- File path references now work correctly after restructuring
- Improved data processing pipeline reliability

## [0.1.0] - 2024-XX-XX

### Added
- Initial Streamlit application for Gold vs S&P 500 comparison
- Interactive date range selection
- Performance calculation and comparison features
- Data fetching from Yahoo Finance
- Automated data preprocessing pipeline
- Unit tests for core functionality
- Configuration management system
- Logging infrastructure

### Features
- Interactive web interface built with Streamlit
- Historical data analysis and comparison
- Customizable time period selection
- Interval-based performance breakdown
- Automatic data caching and refresh
- Comprehensive error handling
- Performance metrics calculation

---

## Legend

- **Added** for new features
- **Changed** for changes in existing functionality  
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities