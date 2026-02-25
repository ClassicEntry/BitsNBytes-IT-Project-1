"""
Decision Tree classification business logic.

Pure computation — no Dash dependencies.
"""

from typing import List, NamedTuple

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from pyexploratory.config import DEFAULT_TEST_SIZE

DT_RANDOM_STATE = 42


class DecisionTreeResult(NamedTuple):
    """All data needed to render Decision Tree results."""

    report: str
    cm: np.ndarray
    display_labels: np.ndarray
    X_train: np.ndarray
    X_test: np.ndarray
    y_pred_train: np.ndarray
    y_pred_test: np.ndarray
    accuracy: float
    f1: float
    feature_importances: np.ndarray
    feature_names: List[str]


def run_decision_tree(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    target_col: str,
    max_depth: int = 5,
    test_size: float = DEFAULT_TEST_SIZE,
) -> DecisionTreeResult:
    """
    Run Decision Tree classification.

    Args:
        df: Source DataFrame.
        x_col: Name of x-axis feature column.
        y_col: Name of y-axis feature column.
        target_col: Name of target column.
        max_depth: Maximum tree depth.
        test_size: Fraction of data for testing.

    Returns:
        DecisionTreeResult with all data for visualization.
    """
    feature_names = [x_col, y_col]
    X = df[feature_names].dropna()
    y = df[target_col].dropna()

    # Align X and y on shared indices
    shared_idx = X.index.intersection(y.index)
    X = X.loc[shared_idx]
    y = y.loc[shared_idx]

    # Encode categorical target
    was_categorical = y.dtype == "object" or y.dtype.name == "category"
    label_encoder = None
    if was_categorical:
        label_encoder = LabelEncoder()
        y = pd.Series(label_encoder.fit_transform(y), index=y.index)

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Stratified train/test split
    sss = StratifiedShuffleSplit(
        n_splits=1, test_size=test_size, random_state=DT_RANDOM_STATE
    )
    for train_index, test_index in sss.split(X_scaled, y):
        X_train, X_test = X_scaled[train_index], X_scaled[test_index]
        y_train, y_test = y.values[train_index], y.values[test_index]

    # Fit Decision Tree
    dt = DecisionTreeClassifier(
        max_depth=max_depth, random_state=DT_RANDOM_STATE
    )
    dt.fit(X_train, y_train)
    y_pred_train = dt.predict(X_train)
    y_pred_test = dt.predict(X_test)

    # Metrics
    display_labels = label_encoder.classes_ if was_categorical else np.unique(y)
    target_names = list(display_labels.astype(str)) if was_categorical else None
    report = classification_report(y_test, y_pred_test, target_names=target_names)
    cm = confusion_matrix(y_test, y_pred_test)
    acc = accuracy_score(y_test, y_pred_test)
    f1_val = f1_score(y_test, y_pred_test, average="weighted")

    return DecisionTreeResult(
        report=report,
        cm=cm,
        display_labels=display_labels,
        X_train=X_train,
        X_test=X_test,
        y_pred_train=y_pred_train,
        y_pred_test=y_pred_test,
        accuracy=acc,
        f1=f1_val,
        feature_importances=dt.feature_importances_,
        feature_names=feature_names,
    )
