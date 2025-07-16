"""
Unit tests for preprocess.py functions.

Tests the get_csv_path function and the main data processing pipeline.
"""

import os
import tempfile
import yaml
import pandas as pd
import pytest
from unittest import mock
from src import preprocess

def test_get_csv_path(tmp_path: pytest.TempPathFactory) -> None:
    """Test get_csv_path returns the correct path from config.yaml."""
    config_path = tmp_path / "config.yaml"
    config = {"csv_path": "data/test_output.csv"}
    with open(config_path, "w") as f:
        yaml.safe_dump(config, f)
    with mock.patch("os.path.dirname", return_value=str(tmp_path)):
        with mock.patch("builtins.open", mock.mock_open(read_data=yaml.safe_dump(config))):
            result = preprocess.get_csv_path()
            assert result == "data/test_output.csv"

def test_main_merges_and_saves(monkeypatch: pytest.MonkeyPatch, tmp_path: pytest.TempPathFactory) -> None:
    """Test main fetches, merges, rounds, and saves the aligned CSV correctly."""
    gold_data = [
        {"date": "2020-01-01", "close": 1550.123},
        {"date": "2020-01-02", "close": 1560.456},
    ]
    sp500_data = [
        {"date": "2020-01-01", "close": 3200.789},
        {"date": "2020-01-02", "close": 3210.123},
    ]
    # Patch fetch_ticker_prices to return our test data
    monkeypatch.setattr(preprocess, "fetch_ticker_prices", lambda ticker: gold_data if ticker == "GC=F" else sp500_data)
    # Patch get_csv_path to write to a temp file
    out_csv = tmp_path / "gold_sp500_aligned.csv"
    monkeypatch.setattr(preprocess, "get_csv_path", lambda: str(out_csv.relative_to(tmp_path)))
    # Patch os.path.dirname to tmp_path
    monkeypatch.setattr(os.path, "dirname", lambda _: str(tmp_path))
    # Run main
    preprocess.main()
    # Check output
    df = pd.read_csv(out_csv)
    assert list(df.columns) == ["date", "gold", "sp500"]
    assert df.shape == (2, 3)
    assert df["gold"].tolist() == [1550.1, 1560.5]
    assert df["sp500"].tolist() == [3200.8, 3210.1]
