"""
Tests for pyexploratory.core.cleaning_ops.

Covers all 17 operations + regression tests for the dropna/drop_duplicates
data-alignment bugs fixed in Phase 0.
"""

import numpy as np
import pandas as pd
import pytest

from pyexploratory.core.cleaning_ops import OPERATIONS, apply_operation


class TestApplyOperationDispatch:
    """Verify the dispatch dict covers all operations."""

    def test_all_operations_registered(self):
        expected = {
            "lstrip",
            "rstrip",
            "alnum",
            "dropna",
            "fillna",
            "to_numeric",
            "to_string",
            "to_datetime",
            "lowercase",
            "uppercase",
            "trim",
            "drop_column",
            "rename_column",
            "normalize",
            "remove_outliers",
            "drop_duplicates",
            "sort_asc",
            "sort_desc",
        }
        assert set(OPERATIONS.keys()) == expected

    def test_unknown_operation_raises(self, sample_df):
        with pytest.raises(KeyError):
            apply_operation(sample_df, "nonexistent", "name")


class TestStringOperations:
    def test_lstrip(self):
        df = pd.DataFrame({"col": ["  hello", "  world"]})
        result = apply_operation(df, "lstrip", "col")
        assert list(result["col"]) == ["hello", "world"]

    def test_rstrip(self):
        df = pd.DataFrame({"col": ["hello  ", "world  "]})
        result = apply_operation(df, "rstrip", "col")
        assert list(result["col"]) == ["hello", "world"]

    def test_lstrip_with_char(self):
        df = pd.DataFrame({"col": ["xxhello", "xxworld"]})
        result = apply_operation(df, "lstrip", "col", fill_value="x")
        assert list(result["col"]) == ["hello", "world"]

    def test_alnum(self):
        df = pd.DataFrame({"col": ["he!llo#", "wo@rld"]})
        result = apply_operation(df, "alnum", "col")
        assert list(result["col"]) == ["hello", "world"]

    def test_lowercase(self):
        df = pd.DataFrame({"col": ["HELLO", "World"]})
        result = apply_operation(df, "lowercase", "col")
        assert list(result["col"]) == ["hello", "world"]

    def test_uppercase(self):
        df = pd.DataFrame({"col": ["hello", "World"]})
        result = apply_operation(df, "uppercase", "col")
        assert list(result["col"]) == ["HELLO", "WORLD"]

    def test_trim(self):
        df = pd.DataFrame({"col": ["  hello  ", "  world  "]})
        result = apply_operation(df, "trim", "col")
        assert list(result["col"]) == ["hello", "world"]


class TestDropnaRegression:
    """Regression tests for the dropna data-alignment bug (Phase 0, fix 0.1)."""

    def test_dropna_preserves_alignment(self, sample_df):
        """After dropping NAs, remaining rows must have correct values across all columns."""
        original_len = len(sample_df)
        result = apply_operation(sample_df.copy(), "dropna", "age")

        # Should have dropped 1 row (index 2 where age is NaN)
        assert len(result) == original_len - 1

        # All remaining ages must be non-null
        assert result["age"].notna().all()

        # Names must still correspond to the correct ages
        for _, row in result.iterrows():
            if row["name"] == "Alice":
                assert row["age"] == 25
            elif row["name"] == "Bob":
                assert row["age"] == 30

    def test_dropna_no_nulls_noop(self):
        """Dropping NAs on a column with no NAs should leave data unchanged."""
        df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
        result = apply_operation(df.copy(), "dropna", "a")
        assert len(result) == 3


class TestDropDuplicatesRegression:
    """Regression tests for the drop_duplicates alignment bug (Phase 0, fix 0.2)."""

    def test_drop_duplicates_preserves_alignment(self, sample_df):
        """After dedup, remaining rows must be internally consistent."""
        result = apply_operation(sample_df.copy(), "drop_duplicates", "name")

        # "Alice" appears twice; after dedup on name, only first kept
        alice_rows = result[result["name"] == "Alice"]
        assert len(alice_rows) == 1
        assert alice_rows.iloc[0]["age"] == 25

        # Bob's row must be intact
        bob_rows = result[result["name"] == "Bob"]
        assert len(bob_rows) == 1
        assert bob_rows.iloc[0]["age"] == 30

    def test_drop_duplicates_no_dupes_noop(self):
        df = pd.DataFrame({"a": [1, 2, 3]})
        result = apply_operation(df.copy(), "drop_duplicates", "a")
        assert len(result) == 3


class TestFillna:
    def test_fillna_with_value(self, sample_df):
        result = apply_operation(sample_df.copy(), "fillna", "age", fill_value="0")
        assert result["age"].notna().all()

    def test_fillna_default_numeric_uses_mean(self):
        df = pd.DataFrame({"val": [10.0, 20.0, None, 40.0]})
        result = apply_operation(df.copy(), "fillna", "val")
        # Mean of 10, 20, 40 = 23.333...
        assert result["val"].iloc[2] == pytest.approx(23.333, abs=0.01)

    def test_fillna_default_object_uses_mode(self):
        df = pd.DataFrame({"cat": ["a", "a", "b", None]})
        result = apply_operation(df.copy(), "fillna", "cat")
        assert result["cat"].iloc[3] == "a"


class TestTypeConversions:
    def test_to_numeric(self):
        df = pd.DataFrame({"col": ["1", "2", "abc"]})
        result = apply_operation(df, "to_numeric", "col")
        assert result["col"].iloc[0] == 1.0
        assert pd.isna(result["col"].iloc[2])

    def test_to_string(self):
        df = pd.DataFrame({"col": [1, 2, 3]})
        result = apply_operation(df, "to_string", "col")
        assert pd.api.types.is_string_dtype(result["col"])

    def test_to_datetime(self):
        df = pd.DataFrame({"col": ["2024-01-01", "2024-06-15"]})
        result = apply_operation(df, "to_datetime", "col")
        assert pd.api.types.is_datetime64_any_dtype(result["col"])


class TestStructuralOperations:
    def test_drop_column(self, sample_df):
        result = apply_operation(sample_df.copy(), "drop_column", "city")
        assert "city" not in result.columns

    def test_rename_column(self, sample_df):
        result = apply_operation(
            sample_df.copy(), "rename_column", "name", new_name="full_name"
        )
        assert "full_name" in result.columns
        assert "name" not in result.columns

    def test_sort_asc(self, sample_df):
        result = apply_operation(sample_df.copy(), "sort_asc", "salary")
        assert list(result["salary"]) == sorted(sample_df["salary"])

    def test_sort_desc(self, sample_df):
        result = apply_operation(sample_df.copy(), "sort_desc", "salary")
        assert list(result["salary"]) == sorted(sample_df["salary"], reverse=True)


class TestNormalize:
    def test_normalize_range(self):
        df = pd.DataFrame({"val": [10, 20, 30, 40, 50]})
        result = apply_operation(df, "normalize", "val")
        assert result["val"].min() == pytest.approx(0.0)
        assert result["val"].max() == pytest.approx(1.0)


class TestRemoveOutliers:
    def test_remove_outliers_flags_extreme_values(self):
        """Values far from the mean should be set to None."""
        normal = list(range(100))
        outlier_df = pd.DataFrame({"val": normal + [99999]})
        result = apply_operation(outlier_df, "remove_outliers", "val")
        assert pd.isna(result["val"].iloc[-1])
