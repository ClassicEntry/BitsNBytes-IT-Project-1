"""
Tests for pyexploratory.core.history — undo/redo history manager.

Uses tmp_path and monkeypatch to isolate history to temp directories.
"""

import os

import pandas as pd
import pytest

from pyexploratory.core import history


@pytest.fixture(autouse=True)
def tmp_history(tmp_path, monkeypatch):
    """Redirect history to temp directory."""
    data_file = str(tmp_path / "local_data.csv")
    hist_dir = str(tmp_path / ".pyexploratory_history")
    monkeypatch.setattr("pyexploratory.core.history.DATA_FILE", data_file)
    monkeypatch.setattr("pyexploratory.core.history.HISTORY_DIR", hist_dir)
    monkeypatch.setattr("pyexploratory.core.history.HISTORY_LOG_FILE", os.path.join(hist_dir, "log.json"))
    # Reset redo stack between tests
    history._redo_stack.clear()
    # Write initial data
    pd.DataFrame({"a": [1, 2, 3]}).to_csv(data_file, index=False)
    history.init_history()
    return data_file, hist_dir


class TestSaveAndUndo:
    def test_save_creates_snapshot(self, tmp_history):
        history.save_snapshot("fillna", "a", "Fill NA on a")
        log = history.get_history_log()
        assert len(log) == 1
        assert log[0]["operation"] == "fillna"

    def test_undo_restores_previous(self, tmp_history):
        data_file, _ = tmp_history
        # Save snapshot of original (3 rows)
        history.save_snapshot("dropna", "a", "Drop NA on a")
        # Simulate cleaning: overwrite with 2 rows
        pd.DataFrame({"a": [1, 2]}).to_csv(data_file, index=False)
        # Undo should restore 3 rows
        df = history.undo()
        assert df is not None
        assert len(df) == 3

    def test_redo_after_undo(self, tmp_history):
        data_file, _ = tmp_history
        history.save_snapshot("dropna", "a", "Drop NA")
        pd.DataFrame({"a": [1, 2]}).to_csv(data_file, index=False)
        history.undo()  # back to 3 rows
        df = history.redo()  # forward to 2 rows
        assert df is not None
        assert len(df) == 2

    def test_undo_empty_returns_none(self, tmp_history):
        assert history.undo() is None

    def test_redo_empty_returns_none(self, tmp_history):
        assert history.redo() is None

    def test_max_history_trims(self, tmp_history):
        for i in range(15):
            history.save_snapshot("fillna", "a", f"Op {i}")
        log = history.get_history_log()
        assert len(log) <= 10

    def test_new_save_clears_redo(self, tmp_history):
        data_file, _ = tmp_history
        history.save_snapshot("dropna", "a", "Op 1")
        pd.DataFrame({"a": [1, 2]}).to_csv(data_file, index=False)
        history.undo()
        # Now save a new operation — redo should be cleared
        history.save_snapshot("fillna", "a", "Op 2")
        assert history.redo() is None


class TestClearHistory:
    def test_clear_removes_all(self, tmp_history):
        history.save_snapshot("fillna", "a", "Op 1")
        history.save_snapshot("fillna", "a", "Op 2")
        history.clear_history()
        assert len(history.get_history_log()) == 0


class TestPreview:
    def test_preview_returns_metadata(self, tmp_history):
        data_file, _ = tmp_history
        df = pd.read_csv(data_file)
        result = history.preview_operation(df, "dropna", "a")
        assert "rows_before" in result
        assert "rows_after" in result
        assert result["rows_before"] == 3

    def test_preview_does_not_modify_original(self, tmp_history):
        data_file, _ = tmp_history
        df = pd.read_csv(data_file)
        original_len = len(df)
        history.preview_operation(df, "dropna", "a")
        # Original df should be unchanged
        assert len(df) == original_len
