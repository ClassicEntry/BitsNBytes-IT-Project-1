"""
Data cleaning operations using a strategy-pattern dispatch.

Each operation is a standalone function with a consistent signature:
    (df, column, fill_value, new_name) -> df

The OPERATIONS dict maps operation keys to their implementations.
"""

from typing import Optional

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import MinMaxScaler

# ---------------------------------------------------------------------------
# Individual cleaning operations
# ---------------------------------------------------------------------------


def lstrip_op(
    df: pd.DataFrame, col: str, fill_value: Optional[str] = None, **_
) -> pd.DataFrame:
    df[col] = df[col].str.lstrip(fill_value)
    return df


def rstrip_op(
    df: pd.DataFrame, col: str, fill_value: Optional[str] = None, **_
) -> pd.DataFrame:
    df[col] = df[col].str.rstrip(fill_value)
    return df


def alnum_op(df: pd.DataFrame, col: str, **_) -> pd.DataFrame:
    df[col] = df[col].str.replace("[^a-zA-Z0-9]", "", regex=True)
    return df


def dropna_op(df: pd.DataFrame, col: str, **_) -> pd.DataFrame:
    df = df.dropna(subset=[col])
    return df


def fillna_op(
    df: pd.DataFrame, col: str, fill_value: Optional[str] = None, **_
) -> pd.DataFrame:
    if fill_value is None:
        if pd.api.types.is_numeric_dtype(df[col]):
            fill_value = df[col].mean()
        else:
            fill_value = df[col].mode()[0]
    df[col] = df[col].fillna(fill_value)
    return df


def to_numeric_op(df: pd.DataFrame, col: str, **_) -> pd.DataFrame:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def to_string_op(df: pd.DataFrame, col: str, **_) -> pd.DataFrame:
    df[col] = df[col].astype(str)
    return df


def to_datetime_op(df: pd.DataFrame, col: str, **_) -> pd.DataFrame:
    df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def lowercase_op(df: pd.DataFrame, col: str, **_) -> pd.DataFrame:
    df[col] = df[col].str.lower()
    return df


def uppercase_op(df: pd.DataFrame, col: str, **_) -> pd.DataFrame:
    df[col] = df[col].str.upper()
    return df


def trim_op(df: pd.DataFrame, col: str, **_) -> pd.DataFrame:
    df[col] = df[col].str.strip()
    return df


def drop_column_op(df: pd.DataFrame, col: str, **_) -> pd.DataFrame:
    df = df.drop(columns=[col])
    return df


def rename_column_op(
    df: pd.DataFrame, col: str, new_name: Optional[str] = None, **_
) -> pd.DataFrame:
    if new_name:
        df = df.rename(columns={col: new_name})
    return df


def normalize_op(df: pd.DataFrame, col: str, **_) -> pd.DataFrame:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col] = df[col].fillna(0)
    scaler = MinMaxScaler()
    df[col] = scaler.fit_transform(df[[col]])
    return df


def remove_outliers_op(df: pd.DataFrame, col: str, **_) -> pd.DataFrame:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    z_scores = np.abs(stats.zscore(df[col].dropna()))
    full_mask = df[col].notna()
    full_mask.loc[df[col].notna()] = z_scores >= 3
    df.loc[full_mask, col] = None
    return df


def drop_duplicates_op(df: pd.DataFrame, col: str, **_) -> pd.DataFrame:
    df = df.drop_duplicates(subset=[col])
    return df


def sort_asc_op(df: pd.DataFrame, col: str, **_) -> pd.DataFrame:
    df = df.sort_values(by=col, ascending=True)
    return df


def sort_desc_op(df: pd.DataFrame, col: str, **_) -> pd.DataFrame:
    df = df.sort_values(by=col, ascending=False)
    return df


# ---------------------------------------------------------------------------
# Dispatch dictionary
# ---------------------------------------------------------------------------

OPERATIONS = {
    "lstrip": lstrip_op,
    "rstrip": rstrip_op,
    "alnum": alnum_op,
    "dropna": dropna_op,
    "fillna": fillna_op,
    "to_numeric": to_numeric_op,
    "to_string": to_string_op,
    "to_datetime": to_datetime_op,
    "lowercase": lowercase_op,
    "uppercase": uppercase_op,
    "trim": trim_op,
    "drop_column": drop_column_op,
    "rename_column": rename_column_op,
    "normalize": normalize_op,
    "remove_outliers": remove_outliers_op,
    "drop_duplicates": drop_duplicates_op,
    "sort_asc": sort_asc_op,
    "sort_desc": sort_desc_op,
}


def apply_operation(
    df: pd.DataFrame,
    operation: str,
    column: str,
    fill_value: Optional[str] = None,
    new_name: Optional[str] = None,
) -> pd.DataFrame:
    """
    Apply a named cleaning operation to a DataFrame column.

    Args:
        df: The input DataFrame.
        operation: Key from OPERATIONS dict.
        column: Target column name.
        fill_value: Optional value for fill/strip operations.
        new_name: Optional new name for rename operation.

    Returns:
        The modified DataFrame.

    Raises:
        KeyError: If the operation is not recognized.
    """
    if df.empty:
        raise ValueError("Cannot apply operations to an empty DataFrame.")
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found. Available: {list(df.columns)}")
    fn = OPERATIONS[operation]
    return fn(df, column, fill_value=fill_value, new_name=new_name)
