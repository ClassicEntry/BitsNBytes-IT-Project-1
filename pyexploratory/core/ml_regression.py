"""
Linear Regression business logic.

Pure computation — no Dash dependencies.
"""

from typing import NamedTuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from pyexploratory.config import DEFAULT_TEST_SIZE


class RegressionResult(NamedTuple):
    """All data needed to render Linear Regression results."""

    X_train: np.ndarray
    X_test: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray
    y_pred_train: np.ndarray
    y_pred_test: np.ndarray
    r2: float
    mse: float
    residuals: np.ndarray
    coefficients: np.ndarray
    intercept: float


def run_linear_regression(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    test_size: float = DEFAULT_TEST_SIZE,
) -> RegressionResult:
    """
    Run Linear Regression.

    Args:
        df: Source DataFrame.
        x_col: Name of the feature column (numeric).
        y_col: Name of the target column (numeric).
        test_size: Fraction of data for testing.

    Returns:
        RegressionResult with all data for visualization.
    """
    data = df[[x_col, y_col]].dropna()
    X = data[[x_col]].values
    y = data[y_col].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    r2 = r2_score(y_test, y_pred_test)
    mse = mean_squared_error(y_test, y_pred_test)
    residuals = y_test - y_pred_test

    return RegressionResult(
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        y_pred_train=y_pred_train,
        y_pred_test=y_pred_test,
        r2=r2,
        mse=mse,
        residuals=residuals,
        coefficients=model.coef_,
        intercept=float(model.intercept_),
    )
