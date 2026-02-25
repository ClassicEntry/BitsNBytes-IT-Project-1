"""Undo/Redo history manager for data cleaning operations."""

import json
import os
import shutil
from typing import Dict, List, Optional

import pandas as pd

from pyexploratory.config import DATA_FILE

HISTORY_DIR = os.path.join(os.path.dirname(DATA_FILE), ".pyexploratory_history")
MAX_HISTORY = 10
HISTORY_LOG_FILE = os.path.join(HISTORY_DIR, "log.json")

_redo_stack: List[str] = []


def init_history():
    """Ensure the history directory and log file exist."""
    os.makedirs(HISTORY_DIR, exist_ok=True)
    if not os.path.exists(HISTORY_LOG_FILE):
        _write_log([])


def save_snapshot(operation: str, column: str, description: str) -> None:
    """Save a snapshot of the current data file before a cleaning operation."""
    init_history()
    log = get_history_log()
    idx = len(log)
    snapshot_path = os.path.join(HISTORY_DIR, f"snapshot_{idx}.csv")
    try:
        shutil.copy2(DATA_FILE, snapshot_path)
    except OSError:
        return  # silently skip if snapshot cannot be saved
    log.append({
        "index": idx,
        "operation": operation,
        "column": column,
        "description": description,
        "snapshot": snapshot_path,
    })
    # Trim to max history
    if len(log) > MAX_HISTORY:
        old = log.pop(0)
        try:
            if os.path.exists(old["snapshot"]):
                os.remove(old["snapshot"])
        except OSError:
            pass
    _write_log(log)
    _redo_stack.clear()


def undo() -> Optional[pd.DataFrame]:
    """Undo the last cleaning operation by restoring the snapshot."""
    log = get_history_log()
    if not log:
        return None
    entry = log.pop()
    try:
        # Save current state for redo
        redo_path = os.path.join(HISTORY_DIR, f"redo_{len(_redo_stack)}.csv")
        shutil.copy2(DATA_FILE, redo_path)
        _redo_stack.append(redo_path)
        # Restore snapshot
        shutil.copy2(entry["snapshot"], DATA_FILE)
        if os.path.exists(entry["snapshot"]):
            os.remove(entry["snapshot"])
    except OSError:
        return None
    _write_log(log)
    from pyexploratory.core.data_store import invalidate_cache
    invalidate_cache()
    return pd.read_csv(DATA_FILE)


def redo() -> Optional[pd.DataFrame]:
    """Redo a previously undone operation."""
    if not _redo_stack:
        return None
    redo_path = _redo_stack.pop()
    try:
        shutil.copy2(redo_path, DATA_FILE)
        if os.path.exists(redo_path):
            os.remove(redo_path)
    except OSError:
        return None
    from pyexploratory.core.data_store import invalidate_cache
    invalidate_cache()
    return pd.read_csv(DATA_FILE)


def get_history_log() -> List[Dict]:
    """Read the history log from disk."""
    init_history()
    try:
        with open(HISTORY_LOG_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []


def clear_history() -> None:
    """Remove all history snapshots and reset the log."""
    try:
        if os.path.exists(HISTORY_DIR):
            shutil.rmtree(HISTORY_DIR)
    except OSError:
        pass
    init_history()


def preview_operation(
    df: pd.DataFrame,
    operation: str,
    column: str,
    fill_value=None,
    new_name=None,
) -> Dict:
    """Preview the effect of a cleaning operation without modifying the data."""
    from pyexploratory.core.cleaning_ops import apply_operation
    df_copy = df.copy()
    df_after = apply_operation(df_copy, operation, column, fill_value, new_name)
    return {
        "rows_before": len(df),
        "rows_after": len(df_after),
        "rows_affected": abs(len(df) - len(df_after)),
    }


def _write_log(log: List[Dict]) -> None:
    """Write the history log to disk."""
    with open(HISTORY_LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)
