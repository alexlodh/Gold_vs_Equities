"""gold_vs_equities package shim

This package provides a compatibility layer exposing the main utilities from
the existing project. It intentionally copies core modules into the package
so the project is importable as `gold_vs_equities` for downstream usage.

Versioning and small convenience exports are defined here.
"""
__version__ = "0.1.0"

from .viz import eda  # noqa: F401
from .data import fetch_ticker, preprocess  # noqa: F401
from .config import load_config  # noqa: F401

__all__ = ["__version__", "eda", "fetch_ticker", "preprocess", "load_config"]
