"""
Persistent action log for the step panel and script export.

Records every user action (upload, cleaning, chart, ML) as a JSON entry
with id, timestamp, and disabled flag. Powers both the step panel UI
and the script generator.

Storage: ``.pyexploratory_actions/actions.json`` (sibling of the data file).
"""

import json
import os
import tempfile
import time
from typing import Dict, List, Optional

from pyexploratory.config import DATA_FILE

ACTIONS_DIR = os.path.join(os.path.dirname(DATA_FILE), ".pyexploratory_actions")
ACTIONS_FILE = os.path.join(ACTIONS_DIR, "actions.json")


def _ensure_dir() -> None:
    os.makedirs(ACTIONS_DIR, exist_ok=True)


def _read_log() -> List[Dict]:
    _ensure_dir()
    if not os.path.exists(ACTIONS_FILE):
        return []
    try:
        with open(ACTIONS_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []


def _write_log(log: List[Dict]) -> None:
    _ensure_dir()
    fd, tmp_path = tempfile.mkstemp(dir=ACTIONS_DIR, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(log, f, indent=2)
        os.replace(tmp_path, ACTIONS_FILE)
    except BaseException:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def _next_id(log: List[Dict]) -> int:
    """Return the next sequential ID."""
    if not log:
        return 0
    return max(entry.get("id", 0) for entry in log) + 1


def log_action(entry: dict) -> None:
    """Append an action entry with auto-assigned id and timestamp."""
    log = _read_log()
    entry["id"] = _next_id(log)
    entry["timestamp"] = time.time()
    entry.setdefault("disabled", False)
    log.append(entry)
    _write_log(log)


def get_log() -> List[Dict]:
    """Return the current action log."""
    return _read_log()


def get_step(step_id: int) -> Optional[Dict]:
    """Return a single step by its id, or None."""
    for entry in _read_log():
        if entry.get("id") == step_id:
            return entry
    return None


def toggle_step(step_id: int) -> None:
    """Toggle the disabled flag on a step."""
    log = _read_log()
    for entry in log:
        if entry.get("id") == step_id:
            entry["disabled"] = not entry.get("disabled", False)
            break
    _write_log(log)


def delete_step(step_id: int) -> None:
    """Remove a step by its id."""
    log = _read_log()
    log = [e for e in log if e.get("id") != step_id]
    _write_log(log)


def clear_log() -> None:
    """Wipe the action log."""
    _write_log([])


def reset_on_upload(filename: str, file_format: str) -> None:
    """Clear the log and record an upload as the first entry."""
    entry = {
        "action_type": "upload",
        "filename": filename,
        "file_format": file_format,
        "id": 0,
        "timestamp": time.time(),
        "disabled": False,
    }
    _write_log([entry])


def undo_last_cleaning() -> None:
    """Remove the last cleaning entry from the log (called on undo)."""
    log = _read_log()
    for i in range(len(log) - 1, -1, -1):
        if log[i].get("action_type") == "cleaning":
            log.pop(i)
            break
    _write_log(log)
