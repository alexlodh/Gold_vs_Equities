"""Project configuration loader for gold_vs_equities.

This module locates the top-level `config.yaml` by default and applies
environment variable overrides where appropriate.
"""
from pathlib import Path
import os
from typing import Dict, Any

try:
    # Reuse existing utility if present
    from utils.load_config import load_config as _load_yaml_config
except Exception:
    _load_yaml_config = None


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.yaml"


def load_config(path: str | Path | None = None) -> Dict[str, Any]:
    """Load project configuration.

    Args:
        path: Optional path to a YAML config file. If omitted, the project
            root `config.yaml` is used.

    Returns:
        dict: Configuration dictionary with environment overrides applied.
    """
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    if _load_yaml_config:
        cfg = _load_yaml_config(str(config_path))
    else:
        # Lightweight fallback if utils.load_config isn't importable
        import yaml

        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)

    # Apply common environment override pattern
    cfg_env_map = {"api_key": "GOLD_VS_EQ_API_KEY", "csv_path": "GOLD_VS_EQ_CSV_PATH"}
    for key, env_var in cfg_env_map.items():
        val = os.getenv(env_var)
        if val:
            cfg[key] = val

    return cfg
