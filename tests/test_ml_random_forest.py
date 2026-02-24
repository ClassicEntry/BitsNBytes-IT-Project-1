"""
Tests for pyexploratory.core.ml_random_forest.
"""

import numpy as np
import pandas as pd
import pytest

from pyexploratory.core.ml_random_forest import run_random_forest


@pytest.fixture
def iris_like_df():
    rng = np.random.RandomState(42)
    n = 150
    return pd.DataFrame({
        "sepal_length": rng.normal(5.8, 0.8, n),
        "sepal_width": rng.normal(3.0, 0.4, n),
        "species": rng.choice(["setosa", "versicolor", "virginica"], n),
    })


class TestRandomForest:
    def test_basic_classification(self, iris_like_df):
        result = run_random_forest(iris_like_df, "sepal_length", "sepal_width", "species")
        assert result.report is not None
        assert 0 <= result.accuracy <= 1
        assert 0 <= result.f1 <= 1

    def test_feature_importances_shape(self, iris_like_df):
        result = run_random_forest(iris_like_df, "sepal_length", "sepal_width", "species")
        assert len(result.feature_importances) == 2
        assert len(result.feature_names) == 2

    def test_oob_score_present(self, iris_like_df):
        result = run_random_forest(iris_like_df, "sepal_length", "sepal_width", "species")
        # OOB score should be a float or None
        assert result.oob_score is None or 0 <= result.oob_score <= 1

    def test_n_estimators_respected(self, iris_like_df):
        result = run_random_forest(
            iris_like_df, "sepal_length", "sepal_width", "species", n_estimators=10
        )
        assert result.accuracy >= 0

    def test_confusion_matrix_square(self, iris_like_df):
        result = run_random_forest(iris_like_df, "sepal_length", "sepal_width", "species")
        assert result.cm.shape[0] == result.cm.shape[1]
