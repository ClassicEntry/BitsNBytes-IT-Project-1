"""
KMeans clustering business logic.

Pure computation — no Dash dependencies. Returns data structures that
callbacks convert into Plotly figures.
"""

from typing import NamedTuple

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from pyexploratory.config import (
    KMEANS_DEFAULT_CLUSTERS,
    KMEANS_RANDOM_STATE,
    MESH_STEP_SIZE,
)


class ClusteringResult(NamedTuple):
    """All data needed to render a clustering visualization."""

    X_scaled: np.ndarray
    labels: np.ndarray
    centroids: np.ndarray
    xx: np.ndarray
    yy: np.ndarray
    Z: np.ndarray
    silhouette: float


def run_kmeans(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    n_clusters: int = KMEANS_DEFAULT_CLUSTERS,
) -> ClusteringResult:
    """
    Run KMeans clustering on two numeric columns.

    Args:
        df: Source DataFrame.
        x_col: Name of x-axis column.
        y_col: Name of y-axis column.
        n_clusters: Number of clusters.

    Returns:
        ClusteringResult with all data for visualization.
    """
    X = df[[x_col, y_col]].dropna().values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=KMEANS_RANDOM_STATE)
    kmeans.fit(X_scaled)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    # Mesh grid for decision boundaries
    h = MESH_STEP_SIZE
    x_min, x_max = X_scaled[:, 0].min() - 1, X_scaled[:, 0].max() + 1
    y_min, y_max = X_scaled[:, 1].min() - 1, X_scaled[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    sil = silhouette_score(X_scaled, labels)

    return ClusteringResult(
        X_scaled=X_scaled,
        labels=labels,
        centroids=centroids,
        xx=xx,
        yy=yy,
        Z=Z,
        silhouette=sil,
    )


def compute_elbow(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    max_k: int = 10,
) -> dict:
    """
    Compute inertia for k=1..max_k for the elbow method.

    Returns:
        Dict with keys "k_values" and "inertias".
    """
    X = df[[x_col, y_col]].dropna().values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    k_values = list(range(1, max_k + 1))
    inertias = []
    for k in k_values:
        km = KMeans(n_clusters=k, random_state=KMEANS_RANDOM_STATE)
        km.fit(X_scaled)
        inertias.append(km.inertia_)

    return {"k_values": k_values, "inertias": inertias}
