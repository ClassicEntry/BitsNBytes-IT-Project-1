"""
Persistent action log for script export.

Records every user action (upload, cleaning, chart, ML) as a JSON entry
so that ``script_generator`` can replay the session as standalone Python code.

Storage: ``.pyexploratory_actions/actions.json`` (sibling of the data file).
"""

import json
import os
from typing import Dict, List

from pyexploratory.config import DATA_FILE

ACTIONS_DIR = os.path.join(os.path.dirname(DATA_FILE), ".pyexploratory_actions")
ACTIONS_FILE = os.path.join(ACTIONS_DIR, "actions.json")


def _ensure_dir() -> None:
    os.makedirs(ACTIONS_DIR, exist_ok=True)


def _read_log() -> List[Dict]:
    _ensure_dir()
    if not os.path.exists(ACTIONS_FILE):
        return []
    with open(ACTIONS_FILE) as f:
        return json.load(f)


def _write_log(log: List[Dict]) -> None:
    _ensure_dir()
    with open(ACTIONS_FILE, "w") as f:
        json.dump(log, f, indent=2)


def log_action(entry: dict) -> None:
    """Append an action entry to the log and persist to disk."""
    log = _read_log()
    log.append(entry)
    _write_log(log)


def get_log() -> List[Dict]:
    """Return the current action log."""
    return _read_log()


def clear_log() -> None:
    """Wipe the action log."""
    _write_log([])


def reset_on_upload(filename: str, file_format: str) -> None:
    """Clear the log and record an upload as the first entry."""
    _write_log([{"action_type": "upload", "filename": filename, "file_format": file_format}])


def undo_last_cleaning() -> None:
    """Remove the last cleaning entry from the log (called on undo)."""
    log = _read_log()
    # Walk backwards to find the last cleaning entry
    for i in range(len(log) - 1, -1, -1):
        if log[i].get("action_type") == "cleaning":
            log.pop(i)
            break
    _write_log(log)
