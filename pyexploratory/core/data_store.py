"""
Abstraction over the local CSV data store.

All modules should use these functions instead of directly calling
pd.read_csv("local_data.csv") or df.to_csv("local_data.csv").
"""

from typing import Dict, List

import pandas as pd

from pyexploratory.config import DATA_FILE


def read_data() -> pd.DataFrame:
    """Read the current dataset from disk."""
    return pd.read_csv(DATA_FILE)


def write_data(df: pd.DataFrame) -> None:
    """Persist a DataFrame back to disk."""
    df.to_csv(DATA_FILE, index=False)


def column_options(df: pd.DataFrame) -> List[Dict[str, str]]:
    """Build Dash dropdown options from DataFrame columns."""
    return [{"label": col, "value": col} for col in df.columns]


def numeric_column_options(df: pd.DataFrame) -> List[Dict[str, str]]:
    """Build Dash dropdown options for numeric columns only."""
    return [
        {"label": col, "value": col}
        for col in df.columns
        if df[col].dtype != "object" and df[col].dtype.name != "category"
    ]


def categorical_column_options(df: pd.DataFrame) -> List[Dict[str, str]]:
    """Build Dash dropdown options for categorical columns only."""
    return [
        {"label": col, "value": col}
        for col in df.columns
        if df[col].dtype == "object" or df[col].dtype.name == "category"
    ]
