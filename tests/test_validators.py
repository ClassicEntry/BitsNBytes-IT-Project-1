"""
Tests for pyexploratory.core.validators.

Covers column existence, type checks, emptiness, cleaning compatibility,
ML input validation, and classification target validation.
"""

import pandas as pd
import pytest

from pyexploratory.core.validators import (
    validate_classification_target,
    validate_cleaning_compatibility,
    validate_column_exists,
    validate_min_rows,
    validate_ml_inputs,
    validate_not_all_nan,
    validate_not_empty,
    validate_numeric_column,
    validate_string_column,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {"name": ["a", "b", "c"], "age": [10, 20, 30], "score": [1.1, 2.2, 3.3]}
    )


class TestColumnExists:
    def test_valid(self, sample_df):
        assert validate_column_exists(sample_df, "name") is None

    def test_missing(self, sample_df):
        result = validate_column_exists(sample_df, "xyz")
        assert "xyz" in result and "not found" in result.lower()


class TestNumericColumn:
    def test_numeric(self, sample_df):
        assert validate_numeric_column(sample_df, "age") is None

    def test_non_numeric(self, sample_df):
        result = validate_numeric_column(sample_df, "name")
        assert result is not None and "numeric" in result.lower()


class TestStringColumn:
    def test_string(self, sample_df):
        assert validate_string_column(sample_df, "name") is None

    def test_non_string(self, sample_df):
        result = validate_string_column(sample_df, "age")
        assert result is not None


class TestNotEmpty:
    def test_non_empty(self, sample_df):
        assert validate_not_empty(sample_df) is None

    def test_empty(self):
        assert validate_not_empty(pd.DataFrame()) is not None


class TestMinRows:
    def test_enough_rows(self, sample_df):
        assert validate_min_rows(sample_df, 3, "test") is None

    def test_insufficient_rows(self, sample_df):
        result = validate_min_rows(sample_df, 10, "test")
        assert result is not None and "10" in result


class TestNotAllNan:
    def test_valid(self, sample_df):
        assert validate_not_all_nan(sample_df, "age") is None

    def test_all_nan(self):
        df = pd.DataFrame({"col": [None, None, None]})
        result = validate_not_all_nan(df, "col")
        assert result is not None and "missing" in result.lower()


class TestCleaningCompatibility:
    def test_string_op_on_numeric_fails(self, sample_df):
        result = validate_cleaning_compatibility(sample_df, "lowercase", "age")
        assert result is not None

    def test_string_op_on_string_ok(self, sample_df):
        assert validate_cleaning_compatibility(sample_df, "lowercase", "name") is None

    def test_numeric_op_on_string_fails(self, sample_df):
        result = validate_cleaning_compatibility(sample_df, "normalize", "name")
        assert result is not None

    def test_numeric_op_on_numeric_ok(self, sample_df):
        assert validate_cleaning_compatibility(sample_df, "normalize", "age") is None


class TestMLInputs:
    def test_valid(self, sample_df):
        assert validate_ml_inputs(sample_df, "age", "score", min_samples=3) is None

    def test_insufficient_rows(self):
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        result = validate_ml_inputs(df, "a", "b", min_samples=10)
        assert result is not None


class TestClassificationTarget:
    def test_valid(self, sample_df):
        assert validate_classification_target(sample_df, "name") is None

    def test_single_class(self):
        df = pd.DataFrame({"target": ["a", "a", "a"]})
        result = validate_classification_target(df, "target")
        assert result is not None
