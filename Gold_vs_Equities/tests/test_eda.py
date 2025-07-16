import pytest
import pandas as pd
import os
from src import eda

def test_plot_gold_sp500_runs(tmp_path):
    # Create a small dummy CSV file
    data = {
        'date': pd.date_range(start='2020-01-01', periods=3, freq='D'),
        'gold': [1500, 1510, 1520],
        'sp500': [3200, 3210, 3220]
    }
    df = pd.DataFrame(data)
    csv_path = tmp_path / "dummy.csv"
    df.to_csv(csv_path, index=False)

    # Should not raise any exceptions
    eda.plot_gold_sp500(str(csv_path))

def test_plot_gold_sp500_file_not_found():
    with pytest.raises(FileNotFoundError):
        eda.plot_gold_sp500("nonexistent_file.csv")
