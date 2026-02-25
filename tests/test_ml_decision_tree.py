"""
Tests for pyexploratory.core.ml_decision_tree.
"""

import numpy as np
import pandas as pd
import pytest

from pyexploratory.core.ml_decision_tree import run_decision_tree


@pytest.fixture
def iris_like_df():
    rng = np.random.RandomState(42)
    n = 150
    return pd.DataFrame({
        "sepal_length": rng.normal(5.8, 0.8, n),
        "sepal_width": rng.normal(3.0, 0.4, n),
        "species": rng.choice(["setosa", "versicolor", "virginica"], n),
    })


class TestDecisionTree:
    def test_basic_classification(self, iris_like_df):
        result = run_decision_tree(iris_like_df, "sepal_length", "sepal_width", "species")
        assert result.report is not None
        assert 0 <= result.accuracy <= 1
        assert 0 <= result.f1 <= 1

    def test_feature_importances_shape(self, iris_like_df):
        result = run_decision_tree(iris_like_df, "sepal_length", "sepal_width", "species")
        assert len(result.feature_importances) == 2
        assert len(result.feature_names) == 2

    def test_max_depth_respected(self, iris_like_df):
        result = run_decision_tree(iris_like_df, "sepal_length", "sepal_width", "species", max_depth=2)
        assert result.accuracy >= 0

    def test_confusion_matrix_square(self, iris_like_df):
        result = run_decision_tree(iris_like_df, "sepal_length", "sepal_width", "species")
        assert result.cm.shape[0] == result.cm.shape[1]

    def test_display_labels_present(self, iris_like_df):
        result = run_decision_tree(iris_like_df, "sepal_length", "sepal_width", "species")
        assert len(result.display_labels) >= 2
