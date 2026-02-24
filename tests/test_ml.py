"""
Tests for pyexploratory.core.ml_clustering and ml_classification.
"""

import numpy as np
import pandas as pd
import pytest

from pyexploratory.core.ml_classification import run_svm
from pyexploratory.core.ml_clustering import compute_elbow, run_kmeans


@pytest.fixture
def iris_like_df():
    """Synthetic iris-like data for ML tests."""
    rng = np.random.RandomState(42)
    n = 150
    return pd.DataFrame(
        {
            "sepal_length": rng.normal(5.8, 0.8, n),
            "sepal_width": rng.normal(3.0, 0.4, n),
            "species": rng.choice(["setosa", "versicolor", "virginica"], n),
        }
    )


class TestKMeans:
    def test_produces_correct_cluster_count(self, iris_like_df):
        result = run_kmeans(iris_like_df, "sepal_length", "sepal_width", n_clusters=3)
        unique_labels = set(result.labels)
        assert len(unique_labels) == 3

    def test_produces_correct_centroid_count(self, iris_like_df):
        result = run_kmeans(iris_like_df, "sepal_length", "sepal_width", n_clusters=4)
        assert result.centroids.shape[0] == 4

    def test_silhouette_in_valid_range(self, iris_like_df):
        result = run_kmeans(iris_like_df, "sepal_length", "sepal_width", n_clusters=3)
        assert -1 <= result.silhouette <= 1

    def test_mesh_grid_shape(self, iris_like_df):
        result = run_kmeans(iris_like_df, "sepal_length", "sepal_width", n_clusters=2)
        assert result.xx.shape == result.yy.shape
        assert result.Z.shape == result.xx.shape


class TestElbow:
    def test_returns_correct_k_range(self, iris_like_df):
        elbow = compute_elbow(iris_like_df, "sepal_length", "sepal_width", max_k=5)
        assert elbow["k_values"] == [1, 2, 3, 4, 5]
        assert len(elbow["inertias"]) == 5

    def test_inertia_decreases(self, iris_like_df):
        elbow = compute_elbow(iris_like_df, "sepal_length", "sepal_width", max_k=5)
        # Inertia should generally decrease as k increases
        assert elbow["inertias"][0] > elbow["inertias"][-1]


class TestSVM:
    def test_basic_classification(self, iris_like_df):
        result = run_svm(
            iris_like_df,
            "sepal_length",
            "sepal_width",
            "species",
            kernel="linear",
            test_size=0.25,
        )
        assert result.report is not None
        assert result.cm.shape[0] == result.cm.shape[1]  # square confusion matrix
        assert 0 <= result.accuracy <= 1
        assert 0 <= result.f1 <= 1

    def test_label_encoding_produces_class_names(self, iris_like_df):
        """Regression test for SVM label encoder bug (Phase 0, fix 0.5)."""
        result = run_svm(
            iris_like_df,
            "sepal_length",
            "sepal_width",
            "species",
        )
        # display_labels should contain the original class names, not ints
        labels_set = set(result.display_labels)
        assert "setosa" in labels_set or "versicolor" in labels_set

    def test_rbf_kernel(self, iris_like_df):
        result = run_svm(
            iris_like_df,
            "sepal_length",
            "sepal_width",
            "species",
            kernel="rbf",
        )
        assert result.accuracy >= 0  # just ensure it runs without error

    def test_custom_test_size(self, iris_like_df):
        result = run_svm(
            iris_like_df,
            "sepal_length",
            "sepal_width",
            "species",
            test_size=0.4,
        )
        # With 40% test size on 150 samples, test set should be ~60
        assert len(result.y_pred_test) == pytest.approx(60, abs=5)
