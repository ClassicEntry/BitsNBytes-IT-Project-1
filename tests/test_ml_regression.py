"""
Tests for pyexploratory.core.ml_regression.
"""

import numpy as np
import pandas as pd
import pytest

from pyexploratory.core.ml_regression import run_linear_regression


@pytest.fixture
def numeric_df():
    rng = np.random.RandomState(42)
    n = 100
    x = rng.normal(10, 3, n)
    return pd.DataFrame({
        "feature": x,
        "target": 2 * x + rng.normal(0, 1, n),
    })


class TestLinearRegression:
    def test_basic_regression(self, numeric_df):
        result = run_linear_regression(numeric_df, "feature", "target")
        assert result.r2 > 0.5  # Strong linear relationship
        assert result.mse >= 0

    def test_residuals_match(self, numeric_df):
        result = run_linear_regression(numeric_df, "feature", "target")
        expected = result.y_test - result.y_pred_test
        np.testing.assert_array_almost_equal(result.residuals, expected)

    def test_coefficients_shape(self, numeric_df):
        result = run_linear_regression(numeric_df, "feature", "target")
        assert len(result.coefficients) == 1  # Single feature
        assert isinstance(result.intercept, float)

    def test_r2_in_valid_range(self, numeric_df):
        result = run_linear_regression(numeric_df, "feature", "target")
        assert -1 <= result.r2 <= 1  # Can be negative for very bad fits

    def test_train_test_sizes(self, numeric_df):
        result = run_linear_regression(numeric_df, "feature", "target", test_size=0.3)
        total = len(result.y_train) + len(result.y_test)
        assert total <= len(numeric_df)
        assert len(result.y_test) > 0
        assert len(result.y_train) > 0
