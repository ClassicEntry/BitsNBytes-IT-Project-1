"""
SVM classification business logic.

Pure computation — no Dash dependencies.
"""

from typing import List, NamedTuple, Optional

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
from sklearn.svm import SVC

from pyexploratory.config import (
    DEFAULT_TEST_SIZE,
    SVM_DEFAULT_KERNEL,
    SVM_RANDOM_STATE,
)


class ClassificationResult(NamedTuple):
    """All data needed to render classification results."""

    report: str
    cm: np.ndarray
    display_labels: np.ndarray
    X_train: np.ndarray
    X_test: np.ndarray
    y_pred_train: np.ndarray
    y_pred_test: np.ndarray
    accuracy: float
    f1: float


def run_svm(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    target_col: str,
    kernel: str = SVM_DEFAULT_KERNEL,
    test_size: float = DEFAULT_TEST_SIZE,
) -> ClassificationResult:
    """
    Run SVM classification.

    Args:
        df: Source DataFrame.
        x_col: Name of x-axis feature column.
        y_col: Name of y-axis feature column.
        target_col: Name of target column.
        kernel: SVM kernel type.
        test_size: Fraction of data for testing.

    Returns:
        ClassificationResult with all data for visualization.
    """
    X = df[[x_col, y_col]].dropna()
    y = df[target_col].dropna()

    # Align X and y on shared indices
    shared_idx = X.index.intersection(y.index)
    X = X.loc[shared_idx]
    y = y.loc[shared_idx]

    # Encode categorical target before any dtype checks
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
        n_splits=1, test_size=test_size, random_state=SVM_RANDOM_STATE
    )
    for train_index, test_index in sss.split(X_scaled, y):
        X_train, X_test = X_scaled[train_index], X_scaled[test_index]
        y_train, y_test = y.values[train_index], y.values[test_index]

    # Fit SVM
    svm = SVC(kernel=kernel, random_state=SVM_RANDOM_STATE)
    svm.fit(X_train, y_train)
    y_pred_train = svm.predict(X_train)
    y_pred_test = svm.predict(X_test)

    # Metrics
    display_labels = label_encoder.classes_ if was_categorical else np.unique(y)
    target_names = list(display_labels.astype(str)) if was_categorical else None
    report = classification_report(y_test, y_pred_test, target_names=target_names)
    cm = confusion_matrix(y_test, y_pred_test)
    acc = accuracy_score(y_test, y_pred_test)
    f1 = f1_score(y_test, y_pred_test, average="weighted")

    return ClassificationResult(
        report=report,
        cm=cm,
        display_labels=display_labels,
        X_train=X_train,
        X_test=X_test,
        y_pred_train=y_pred_train,
        y_pred_test=y_pred_test,
        accuracy=acc,
        f1=f1,
    )
