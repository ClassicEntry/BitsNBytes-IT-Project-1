"""
Shared test fixtures for PyExploratory tests.
"""

import os
import tempfile

import pandas as pd
import pytest

from pyexploratory import config


@pytest.fixture
def sample_df():
    """A small DataFrame for testing cleaning operations."""
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "Alice", None],
            "age": [25, 30, None, 25, 40],
            "salary": [50000.0, 60000.0, 70000.0, 50000.0, 80000.0],
            "city": ["NYC", "LA", "NYC", "NYC", "LA"],
        }
    )


@pytest.fixture
def iris_df():
    """Load iris.csv from the data directory."""
    iris_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "iris.csv"
    )
    return pd.read_csv(iris_path)


@pytest.fixture
def tmp_data_file(sample_df, monkeypatch):
    """Write sample_df to a temp CSV and patch DATA_FILE to point there."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        sample_df.to_csv(f, index=False)
        tmp_path = f.name

    monkeypatch.setattr(config, "DATA_FILE", tmp_path)
    yield tmp_path
    os.unlink(tmp_path)
