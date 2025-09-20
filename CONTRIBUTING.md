# Contributing to Gold vs S&P 500 Analysis

Thank you for considering contributing to this project! This document provides guidelines for contributing to the Gold vs S&P 500 Analysis application.

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Basic knowledge of Python, Pandas, and Streamlit

### Setting Up Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/gold-vs-equities.git
   cd gold-vs-equities
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   # Or for development dependencies:
   pip install -e .[dev]
   ```

4. **Run tests to ensure everything works**
   ```bash
   python -m pytest
   ```

## 📋 How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use the issue template** when creating new issues
3. **Provide detailed information** including:
   - Steps to reproduce the problem
   - Expected vs actual behavior
   - Environment details (Python version, OS, etc.)
   - Error messages and logs

### Suggesting Features

1. **Check existing feature requests** in issues
2. **Create a detailed proposal** including:
   - Use case and motivation
   - Proposed implementation approach
   - Potential impact on existing functionality

### Pull Requests

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Follow the existing code style
   - Add tests for new functionality

3. **Test your changes**
   ```bash
   python -m pytest
   streamlit run main.py  # Manual testing
   ```

4. **Commit with clear messages**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and small
- Use type hints where helpful

### Example Code Structure
```python
def calculate_performance_metrics(
    data: pd.DataFrame, 
    start_date: pd.Timestamp, 
    end_date: pd.Timestamp
) -> Dict[str, float]:
    """
    Calculate performance metrics for given date range.
    
    Args:
        data: DataFrame with price data
        start_date: Start of analysis period
        end_date: End of analysis period
        
    Returns:
        Dictionary containing performance metrics
    """
    # Implementation here
    pass
```

### Commit Message Format

Use clear, descriptive commit messages:

- `Add:` for new features
- `Fix:` for bug fixes
- `Update:` for changes to existing features
- `Remove:` for removed functionality
- `Refactor:` for code improvements without feature changes

Examples:
```
Add: Interactive chart visualization for price comparison
Fix: Date range validation error when selecting invalid ranges
Update: Improve performance calculation accuracy
```

## 🧪 Testing Guidelines

### Writing Tests

1. **Add tests for new features** in the `tests/` directory
2. **Use descriptive test names** that explain what is being tested
3. **Follow the existing test patterns**

### Test Structure
```python
def test_performance_calculation_basic():
    """Test basic performance calculation with valid data."""
    # Arrange
    data = create_test_dataframe()
    
    # Act
    result = calculate_performance(data, start_date, end_date)
    
    # Assert
    assert result['gold_pct'] > 0
    assert result['sp500_pct'] > 0
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_preprocess.py

# Run with coverage
python -m pytest --cov=src tests/

# Run with verbose output
python -m pytest -v
```

## 📁 Project Structure

Understanding the project layout helps with contributions:

```
├── src/                    # Core application logic
├── tests/                  # Unit tests
├── data/                   # Data storage
├── utils/                  # Utility functions and docs
├── logs/                   # Application logs
├── main.py                 # Streamlit entry point
├── config.yaml            # Configuration settings
└── pyproject.toml         # Project metadata and dependencies
```

## 🐛 Debugging Tips

### Common Issues

1. **Data fetching errors**: Check internet connection and Yahoo Finance API status
2. **Date range issues**: Ensure dates are within available data range
3. **Performance problems**: Check data size and consider caching improvements

### Debugging Tools

- Use `streamlit run main.py --logger.level=debug` for detailed logging
- Add `st.write()` statements for debugging in Streamlit
- Use `pandas.DataFrame.info()` to inspect data structure

## 📊 Data Handling Guidelines

### Data Sources
- Use reliable, consistent data sources (Yahoo Finance via yfinance)
- Handle missing data gracefully
- Validate data before processing

### Performance Considerations
- Cache expensive operations
- Use efficient pandas operations
- Minimize API calls through smart caching

## 🔄 Release Process

For maintainers:

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with release notes
3. **Create release tag**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

## ❓ Questions and Support

- **General questions**: Open a GitHub issue with the "question" label
- **Feature discussions**: Use GitHub Discussions
- **Bug reports**: Create detailed issue reports

## 📜 Code of Conduct

Please be respectful and constructive in all interactions. We aim to create a welcoming environment for all contributors.

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Gold vs S&P 500 Analysis! 🎉