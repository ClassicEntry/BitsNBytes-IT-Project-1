"""Tests for the extended action log with step metadata."""

import json
import os

import pytest

from pyexploratory.core import action_log


@pytest.fixture(autouse=True)
def temp_action_log(tmp_path, monkeypatch):
    """Redirect action log to temp dir."""
    actions_dir = str(tmp_path / ".pyexploratory_actions")
    actions_file = str(tmp_path / ".pyexploratory_actions" / "actions.json")
    monkeypatch.setattr(action_log, "ACTIONS_DIR", actions_dir)
    monkeypatch.setattr(action_log, "ACTIONS_FILE", actions_file)
    yield actions_file


class TestActionLog:
    def test_log_action_adds_id_and_timestamp(self, temp_action_log):
        action_log.clear_log()
        action_log.log_action({"action_type": "upload", "filename": "test.csv"})
        log = action_log.get_log()
        assert len(log) == 1
        assert "id" in log[0]
        assert "timestamp" in log[0]
        assert log[0]["action_type"] == "upload"

    def test_log_action_increments_id(self, temp_action_log):
        action_log.clear_log()
        action_log.log_action({"action_type": "upload"})
        action_log.log_action({"action_type": "cleaning", "operation": "dropna"})
        log = action_log.get_log()
        assert log[0]["id"] == 0
        assert log[1]["id"] == 1

    def test_disable_step(self, temp_action_log):
        action_log.clear_log()
        action_log.log_action({"action_type": "cleaning", "operation": "dropna"})
        action_log.toggle_step(0)
        log = action_log.get_log()
        assert log[0]["disabled"] is True

    def test_enable_step(self, temp_action_log):
        action_log.clear_log()
        action_log.log_action({"action_type": "cleaning", "operation": "dropna"})
        action_log.toggle_step(0)
        action_log.toggle_step(0)
        log = action_log.get_log()
        assert log[0]["disabled"] is False

    def test_delete_step(self, temp_action_log):
        action_log.clear_log()
        action_log.log_action({"action_type": "upload"})
        action_log.log_action({"action_type": "cleaning"})
        action_log.delete_step(0)
        log = action_log.get_log()
        assert len(log) == 1
        assert log[0]["id"] == 1

    def test_get_step_by_id(self, temp_action_log):
        action_log.clear_log()
        action_log.log_action({"action_type": "upload", "filename": "a.csv"})
        action_log.log_action({"action_type": "cleaning", "operation": "trim"})
        step = action_log.get_step(1)
        assert step is not None
        assert step["action_type"] == "cleaning"

    def test_reset_on_upload_clears_and_adds_upload(self, temp_action_log):
        action_log.log_action({"action_type": "cleaning"})
        action_log.reset_on_upload("new.csv", "csv")
        log = action_log.get_log()
        assert len(log) == 1
        assert log[0]["action_type"] == "upload"
        assert log[0]["id"] == 0
        assert "timestamp" in log[0]
