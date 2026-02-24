"""Input validation for cleaning, ML, and upload operations."""

from typing import Optional

import pandas as pd

STRING_OPS = {"lowercase", "uppercase", "trim", "lstrip", "rstrip", "alnum"}
NUMERIC_OPS = {"normalize", "remove_outliers"}


def validate_column_exists(df: pd.DataFrame, column: str) -> Optional[str]:
    if column not in df.columns:
        return f"Column '{column}' not found. Available: {', '.join(df.columns[:10])}"
    return None


def validate_numeric_column(df: pd.DataFrame, column: str) -> Optional[str]:
    if not pd.api.types.is_numeric_dtype(df[column]):
        return f"Column '{column}' is not numeric (type: {df[column].dtype})."
    return None


def validate_string_column(df: pd.DataFrame, column: str) -> Optional[str]:
    if not pd.api.types.is_string_dtype(df[column]):
        return f"Column '{column}' is not text (type: {df[column].dtype})."
    return None


def validate_not_empty(df: pd.DataFrame) -> Optional[str]:
    if df.empty:
        return "The dataset is empty. Please upload data first."
    return None


def validate_min_rows(
    df: pd.DataFrame, min_rows: int, context: str = ""
) -> Optional[str]:
    if len(df) < min_rows:
        return f"Need at least {min_rows} rows for {context}, but only {len(df)} available."
    return None


def validate_not_all_nan(df: pd.DataFrame, column: str) -> Optional[str]:
    if df[column].isna().all():
        return f"Column '{column}' contains only missing values."
    return None


def validate_cleaning_compatibility(
    df: pd.DataFrame, operation: str, column: str
) -> Optional[str]:
    if operation in STRING_OPS and not pd.api.types.is_string_dtype(df[column]):
        return f"Cannot apply '{operation}' to non-text column '{column}'."
    if operation in NUMERIC_OPS and not pd.api.types.is_numeric_dtype(df[column]):
        return f"Cannot apply '{operation}' to non-numeric column '{column}'."
    return None


def validate_ml_inputs(
    df: pd.DataFrame, x_col: str, y_col: str, min_samples: int = 10
) -> Optional[str]:
    for col in [x_col, y_col]:
        err = validate_column_exists(df, col)
        if err:
            return err
        err = validate_numeric_column(df, col)
        if err:
            return err
    if len(df) < min_samples:
        return f"Need at least {min_samples} rows, but only {len(df)} available."
    return None


def validate_classification_target(
    df: pd.DataFrame, target_col: str, min_classes: int = 2
) -> Optional[str]:
    n_classes = df[target_col].nunique()
    if n_classes < min_classes:
        return f"Target '{target_col}' has {n_classes} class(es), need at least {min_classes}."
    return None
