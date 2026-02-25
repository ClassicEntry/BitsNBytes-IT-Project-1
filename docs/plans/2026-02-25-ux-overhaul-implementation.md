# UX Overhaul Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Redesign PyExploratory from a tab-based UI to an Exploratory.io-inspired 3-zone workspace (sidebar + main workspace + step panel) with glassmorphism, glow effects, and polished interactions.

**Architecture:** The current 4-tab dispatch in `pages/data_analysis.py` is replaced by a unified workspace where the data table is always visible, charts/ML/summary render as overlays, and a right-hand step panel records all operations. All existing `core/` logic is preserved — only the UI and callback layers change.

**Tech Stack:** Dash 2.14+, dash-bootstrap-components, Plotly, custom CSS animations, Google Fonts (Inter + JetBrains Mono).

---

## Task 1: Design System — Config & CSS Foundation

**Files:**
- Modify: `pyexploratory/config.py`
- Create: `pyexploratory/assets/custom.css`
- Test: Visual inspection via Playwright

**Step 1: Update config.py with new design system colors and styles**

Replace the color constants and style dicts in `pyexploratory/config.py`. Keep all ML defaults and paths unchanged.

```python
# Replace the Colors section (lines 17-27) with:

# ---------------------------------------------------------------------------
# Colors — Design System v2
# ---------------------------------------------------------------------------
# Background layers (deep → light)
BG_DEEP = "#111113"
BG_SURFACE = "#1a1a1d"
BG_CARD = "#222226"
BG_HOVER = "#2a2a30"
BG_ACTIVE = "#333338"

# Accent
PRIMARY = "#00c46a"
PRIMARY_DIM = "#00c46a33"

# Text
TEXT_PRIMARY = "#f0f0f0"
TEXT_SECONDARY = "#a0a0a0"
TEXT_MUTED_V2 = "#666666"

# Step type accents
STEP_UPLOAD_COLOR = "#4a9eff"
STEP_CLEAN_COLOR = "#00c46a"
STEP_CHART_COLOR = "#ff9f43"
STEP_ML_COLOR = "#a855f7"

# Borders
BORDER_COLOR = "#3a3a3b"

# Legacy aliases (keep for backward compatibility during migration)
LIGHT_GREEN = "#56D300"
DARK_GREEN = "#00a417"
NEW_GREEN = "#0f4d25"
GREY = "#3f3f3f"
LIGHT_BLUE = "#007BFF"
DARK_BLUE = "#1d06ca"
WHITE = "#f3f3f3"
BLACK = "#000000"
SIDEBAR_BG = BG_DEEP
CARD_BG = BG_CARD
CARD_BORDER = BORDER_COLOR
TEXT_MUTED = TEXT_SECONDARY
```

Add new style dicts below the existing ones (do not remove old ones yet — callbacks still reference them):

```python
# ---------------------------------------------------------------------------
# Design System v2 — Layout styles
# ---------------------------------------------------------------------------
SIDEBAR_STYLE_V2 = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "200px",
    "padding": "20px 16px",
    "background": f"linear-gradient(180deg, {BG_DEEP}, #0d0d10)",
    "zIndex": 10,
    "overflowY": "auto",
    "borderRight": f"1px solid {BORDER_COLOR}",
}

CONTEXT_BAR_STYLE = {
    "background": f"linear-gradient(90deg, {BG_SURFACE}, #1e1e22)",
    "padding": "12px 20px",
    "borderBottom": f"1px solid {BORDER_COLOR}",
    "display": "flex",
    "alignItems": "center",
    "gap": "16px",
    "color": TEXT_SECONDARY,
    "fontSize": "13px",
    "fontFamily": "'Inter', sans-serif",
}

MAIN_WORKSPACE_STYLE = {
    "marginLeft": "200px",
    "marginRight": "280px",
    "minHeight": "100vh",
    "backgroundColor": BG_SURFACE,
    "padding": "0",
}

STEP_PANEL_STYLE = {
    "position": "fixed",
    "top": 0,
    "right": 0,
    "bottom": 0,
    "width": "280px",
    "background": f"linear-gradient(180deg, {BG_DEEP}, #0d0d10)",
    "borderLeft": f"1px solid {BORDER_COLOR}",
    "padding": "20px 12px",
    "overflowY": "auto",
    "zIndex": 10,
}

GLASS_CARD_STYLE = {
    "backgroundColor": "rgba(34, 34, 38, 0.8)",
    "backdropFilter": "blur(12px)",
    "WebkitBackdropFilter": "blur(12px)",
    "border": "1px solid rgba(255, 255, 255, 0.06)",
    "borderRadius": "8px",
    "padding": "16px",
    "marginBottom": "12px",
}

PRIMARY_BUTTON_STYLE = {
    "background": "linear-gradient(135deg, #00c46a, #00a85a)",
    "color": "white",
    "border": "none",
    "borderRadius": "6px",
    "padding": "8px 20px",
    "fontWeight": "600",
    "cursor": "pointer",
    "fontFamily": "'Inter', sans-serif",
    "fontSize": "13px",
    "transition": "all 0.15s ease",
}

GHOST_BUTTON_STYLE = {
    "backgroundColor": "transparent",
    "color": TEXT_SECONDARY,
    "border": f"1px solid {BORDER_COLOR}",
    "borderRadius": "6px",
    "padding": "8px 16px",
    "fontWeight": "500",
    "cursor": "pointer",
    "fontFamily": "'Inter', sans-serif",
    "fontSize": "13px",
    "transition": "all 0.15s ease",
}
```

**Step 2: Create the CSS file with animations and effects**

Create `pyexploratory/assets/custom.css`. Dash auto-serves all files in `assets/`.

```css
/* ===== Google Fonts ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ===== Base ===== */
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #1a1a1d;
    margin: 0;
    padding: 0;
    -webkit-font-smoothing: antialiased;
}

/* ===== Animations ===== */
@keyframes slideInRight {
    from { transform: translateX(20px); opacity: 0; }
    to   { transform: translateX(0); opacity: 1; }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

@keyframes fadeInScale {
    from { opacity: 0; transform: scale(0.97); }
    to   { opacity: 1; transform: scale(1); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%      { opacity: 0.5; }
}

@keyframes slideDown {
    from { transform: translateY(-12px); opacity: 0; }
    to   { transform: translateY(0); opacity: 1; }
}

/* ===== Step Panel Items ===== */
.step-card {
    animation: slideInRight 0.2s ease-out;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: all 0.15s ease;
    border-left: 3px solid transparent;
}

.step-card:hover {
    background-color: #2a2a30;
    transform: translateY(-1px);
}

.step-card.active {
    box-shadow: 0 0 20px rgba(0, 196, 106, 0.15);
}

.step-card.type-upload  { border-left-color: #4a9eff; }
.step-card.type-clean   { border-left-color: #00c46a; }
.step-card.type-chart   { border-left-color: #ff9f43; }
.step-card.type-ml      { border-left-color: #a855f7; }

.step-card.disabled {
    opacity: 0.4;
}

/* ===== Glass Cards ===== */
.glass-card {
    background-color: rgba(34, 34, 38, 0.8);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
}

/* ===== Buttons ===== */
.btn-primary-glow:hover {
    box-shadow: 0 4px 16px rgba(0, 196, 106, 0.25);
    transform: translateY(-1px);
}

.btn-ghost:hover {
    background-color: #2a2a30;
    border-color: #00c46a;
    color: #f0f0f0;
}

/* ===== Data Table ===== */
.workspace-table .dash-spreadsheet-container .dash-spreadsheet-inner th {
    background-color: #1a1a1d !important;
    color: #a0a0a0 !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 11px;
    font-family: 'Inter', sans-serif;
    border-bottom: 2px solid #3a3a3b !important;
    position: sticky;
    top: 0;
    z-index: 5;
}

.workspace-table .dash-spreadsheet-container .dash-spreadsheet-inner td {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #e0e0e0 !important;
    border-color: #2a2a30 !important;
    padding: 8px 12px !important;
}

.workspace-table .dash-spreadsheet-container .dash-spreadsheet-inner tr:nth-child(even) td {
    background-color: #1a1a1d !important;
}

.workspace-table .dash-spreadsheet-container .dash-spreadsheet-inner tr:nth-child(odd) td {
    background-color: #222226 !important;
}

.workspace-table .dash-spreadsheet-container .dash-spreadsheet-inner tr:hover td {
    background-color: #2a2a30 !important;
}

/* ===== Focus/Input Glow ===== */
input:focus, .Select-control:focus {
    box-shadow: 0 0 0 2px rgba(0, 196, 106, 0.3) !important;
    border-color: #00c46a !important;
    outline: none;
}

/* ===== Toast ===== */
.toast-slide-in {
    animation: slideDown 0.2s ease-out;
}

/* ===== Chart Fade-In ===== */
.chart-fade-in {
    animation: fadeInScale 0.3s ease-out;
}

/* ===== Context Bar ===== */
.context-bar-item {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-right: 1px solid #3a3a3b;
    font-size: 13px;
    color: #a0a0a0;
}

.context-bar-item:last-child {
    border-right: none;
}

/* ===== Slide-in Panel ===== */
.slide-panel {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    width: 420px;
    z-index: 20;
    background: linear-gradient(180deg, #111113, #0d0d10);
    border-left: 1px solid #3a3a3b;
    padding: 24px;
    overflow-y: auto;
    transform: translateX(100%);
    transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-panel.open {
    transform: translateX(0);
}

/* ===== Skeleton Loader ===== */
.skeleton {
    background: linear-gradient(90deg, #222226 25%, #2a2a30 50%, #222226 75%);
    background-size: 200% 100%;
    animation: pulse 1.5s ease-in-out infinite;
    border-radius: 4px;
}

.skeleton-row {
    height: 36px;
    margin-bottom: 4px;
}

/* ===== Scrollbar ===== */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #111113;
}

::-webkit-scrollbar-thumb {
    background: #3a3a3b;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #555;
}

/* ===== Add Step Menu ===== */
.add-step-menu {
    background-color: rgba(34, 34, 38, 0.95);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    padding: 8px;
    animation: fadeIn 0.15s ease-out;
}

.add-step-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-radius: 6px;
    cursor: pointer;
    color: #a0a0a0;
    font-size: 13px;
    transition: all 0.1s ease;
}

.add-step-item:hover {
    background-color: #2a2a30;
    color: #f0f0f0;
}

/* ===== Modal (glassmorphic) ===== */
.modal-content {
    background-color: rgba(34, 34, 38, 0.95) !important;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 12px !important;
    color: #f0f0f0;
}

.modal-header {
    border-bottom: 1px solid #3a3a3b !important;
}

.modal-footer {
    border-top: 1px solid #3a3a3b !important;
}
```

**Step 3: Verify the CSS loads by running the app**

Run: `python pyexploratory/app.py`
Expected: App starts, browser shows updated fonts and scrollbar styling. Existing layout still works.

**Step 4: Commit**

```bash
git add pyexploratory/config.py pyexploratory/assets/custom.css
git commit -m "feat(ui): add v2 design system colors, styles, and CSS animations"
```

---

## Task 2: Extended Action Log — Step Panel Data Layer

**Files:**
- Modify: `pyexploratory/core/action_log.py`
- Create: `tests/test_action_log.py`

**Step 1: Write failing tests for the extended action log**

Create `tests/test_action_log.py`:

```python
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
```

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_action_log.py -v`
Expected: FAIL — `id`, `timestamp`, `toggle_step`, `delete_step`, `get_step` don't exist yet.

**Step 3: Implement extended action log**

Modify `pyexploratory/core/action_log.py`:

```python
"""
Persistent action log for the step panel and script export.

Records every user action (upload, cleaning, chart, ML) as a JSON entry
with id, timestamp, and disabled flag. Powers both the step panel UI
and the script generator.

Storage: ``.pyexploratory_actions/actions.json`` (sibling of the data file).
"""

import json
import os
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
    with open(ACTIONS_FILE) as f:
        return json.load(f)


def _write_log(log: List[Dict]) -> None:
    _ensure_dir()
    with open(ACTIONS_FILE, "w") as f:
        json.dump(log, f, indent=2)


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
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_action_log.py -v`
Expected: All 7 tests PASS.

**Step 5: Run existing tests to verify no regressions**

Run: `pytest -v`
Expected: All existing tests PASS. The new `id`/`timestamp` fields are additive — existing callers ignore them.

**Step 6: Commit**

```bash
git add pyexploratory/core/action_log.py tests/test_action_log.py
git commit -m "feat(core): extend action log with step id, timestamp, toggle, delete"
```

---

## Task 3: Step Panel Component

**Files:**
- Create: `pyexploratory/components/step_panel.py`
- Create: `pyexploratory/components/context_bar.py`
- Test: Visual verification via Playwright after integration

**Step 1: Create the step panel layout builder**

Create `pyexploratory/components/step_panel.py`:

```python
"""
Step panel layout builder.

Renders the right-hand step panel showing all operations as clickable cards.
"""

import time

from dash import dcc, html

from pyexploratory.config import (
    BG_DEEP,
    BORDER_COLOR,
    PRIMARY,
    PRIMARY_BUTTON_STYLE,
    STEP_PANEL_STYLE,
    STEP_CHART_COLOR,
    STEP_CLEAN_COLOR,
    STEP_ML_COLOR,
    STEP_UPLOAD_COLOR,
    TEXT_MUTED_V2,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from pyexploratory.core.action_log import get_log

_STEP_ICONS = {
    "upload": "\u2b06",  # ⬆
    "cleaning": "\U0001f9f9",  # 🧹
    "chart": "\U0001f4ca",  # 📊
    "ml": "\U0001f916",  # 🤖
}

_STEP_COLORS = {
    "upload": STEP_UPLOAD_COLOR,
    "cleaning": STEP_CLEAN_COLOR,
    "chart": STEP_CHART_COLOR,
    "ml": STEP_ML_COLOR,
}


def _relative_time(ts: float) -> str:
    """Convert a Unix timestamp to a human-readable relative time."""
    diff = time.time() - ts
    if diff < 60:
        return "just now"
    if diff < 3600:
        return f"{int(diff // 60)}m ago"
    if diff < 86400:
        return f"{int(diff // 3600)}h ago"
    return f"{int(diff // 86400)}d ago"


def _step_title(entry: dict) -> str:
    """Build a human-readable title for a step."""
    at = entry.get("action_type", "unknown")
    if at == "upload":
        return f"Upload {entry.get('filename', 'file')}"
    if at == "cleaning":
        op = entry.get("operation", "?")
        col = entry.get("column", "?")
        return f"{op} on \"{col}\""
    if at == "chart":
        return f"{entry.get('chart_type', 'chart')} chart"
    if at == "ml":
        return f"{entry.get('task', 'ML')} task"
    return "Unknown step"


def _step_card(entry: dict) -> html.Div:
    """Render a single step card."""
    at = entry.get("action_type", "unknown")
    step_id = entry.get("id", 0)
    icon = _STEP_ICONS.get(at, "?")
    color = _STEP_COLORS.get(at, TEXT_SECONDARY)
    title = _step_title(entry)
    ts = entry.get("timestamp", time.time())
    disabled = entry.get("disabled", False)

    css_classes = f"step-card type-{at}"
    if disabled:
        css_classes += " disabled"

    return html.Div(
        [
            html.Div(
                [
                    html.Span(icon, style={"fontSize": "16px", "marginRight": "8px"}),
                    html.Span(title, style={"color": TEXT_PRIMARY, "fontSize": "13px", "fontWeight": "500"}),
                ],
                style={"display": "flex", "alignItems": "center"},
            ),
            html.Div(
                _relative_time(ts),
                style={"color": TEXT_MUTED_V2, "fontSize": "11px", "marginTop": "4px", "paddingLeft": "24px"},
            ),
            html.Div(
                [
                    html.Button(
                        "\u2298" if not disabled else "\u25cb",  # ⊘ or ○
                        id={"type": "step-toggle", "index": step_id},
                        n_clicks=0,
                        style={
                            "background": "none", "border": "none", "color": TEXT_SECONDARY,
                            "cursor": "pointer", "fontSize": "14px", "padding": "2px 6px",
                        },
                        title="Disable step" if not disabled else "Enable step",
                    ),
                    html.Button(
                        "\u2715",  # ✕
                        id={"type": "step-delete", "index": step_id},
                        n_clicks=0,
                        style={
                            "background": "none", "border": "none", "color": TEXT_SECONDARY,
                            "cursor": "pointer", "fontSize": "14px", "padding": "2px 6px",
                        },
                        title="Delete step",
                    ),
                ],
                style={"display": "flex", "justifyContent": "flex-end", "marginTop": "4px", "gap": "4px"},
            ),
        ],
        className=css_classes,
        id={"type": "step-card", "index": step_id},
        style={"backgroundColor": BG_DEEP, "borderLeftColor": color},
    )


def render() -> html.Div:
    """Build the step panel."""
    log = get_log()

    step_cards = [_step_card(entry) for entry in log] if log else [
        html.Div(
            "Start by uploading a dataset",
            style={"color": TEXT_MUTED_V2, "fontSize": "13px", "textAlign": "center", "padding": "40px 0"},
        )
    ]

    return html.Div(
        [
            html.Div(
                "Steps",
                style={
                    "color": TEXT_PRIMARY, "fontSize": "15px", "fontWeight": "600",
                    "marginBottom": "16px", "fontFamily": "'Inter', sans-serif",
                },
            ),
            html.Div(id="step-list", children=step_cards),
            html.Hr(style={"borderColor": BORDER_COLOR, "margin": "12px 0"}),
            # Add Step button + dropdown
            html.Div(
                [
                    html.Button(
                        "+ Add Step",
                        id="add-step-btn",
                        n_clicks=0,
                        style={**PRIMARY_BUTTON_STYLE, "width": "100%"},
                        className="btn-primary-glow",
                    ),
                    html.Div(
                        id="add-step-menu",
                        style={"display": "none"},
                        children=html.Div(
                            [
                                html.Div(
                                    [html.Span("\U0001f9f9", style={"fontSize": "16px"}), "Clean / Transform"],
                                    id="menu-clean",
                                    className="add-step-item",
                                    n_clicks=0,
                                ),
                                html.Div(
                                    [html.Span("\U0001f4ca", style={"fontSize": "16px"}), "Visualize"],
                                    id="menu-chart",
                                    className="add-step-item",
                                    n_clicks=0,
                                ),
                                html.Div(
                                    [html.Span("\U0001f916", style={"fontSize": "16px"}), "Machine Learning"],
                                    id="menu-ml",
                                    className="add-step-item",
                                    n_clicks=0,
                                ),
                                html.Div(
                                    [html.Span("\U0001f4cb", style={"fontSize": "16px"}), "Summary Stats"],
                                    id="menu-summary",
                                    className="add-step-item",
                                    n_clicks=0,
                                ),
                            ],
                            className="add-step-menu",
                        ),
                    ),
                ]
            ),
        ],
        id="step-panel",
        style=STEP_PANEL_STYLE,
    )
```

**Step 2: Create the context bar component**

Create `pyexploratory/components/context_bar.py`:

```python
"""
Context bar layout builder.

Always-visible bar at the top of the main workspace showing dataset metadata.
"""

import os

from dash import html

from pyexploratory.config import CONTEXT_BAR_STYLE, DATA_FILE, TEXT_PRIMARY, TEXT_SECONDARY
from pyexploratory.core.data_store import read_data


def render() -> html.Div:
    """Build the context bar showing current dataset info."""
    try:
        df = read_data()
        filename = os.path.basename(DATA_FILE)
        rows = len(df)
        cols = len(df.columns)
        memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

        return html.Div(
            [
                html.Span(
                    ["\U0001f4c4 ", html.Span(filename, style={"color": TEXT_PRIMARY, "fontWeight": "500"})],
                    className="context-bar-item",
                ),
                html.Span(
                    f"{rows:,} rows \u00d7 {cols} cols",
                    className="context-bar-item",
                ),
                html.Span(
                    f"{memory_mb:.1f} MB",
                    className="context-bar-item",
                ),
            ],
            id="context-bar",
            style=CONTEXT_BAR_STYLE,
        )
    except FileNotFoundError:
        return html.Div(
            "No dataset loaded",
            id="context-bar",
            style={**CONTEXT_BAR_STYLE, "color": "#666666"},
        )
```

**Step 3: Commit**

```bash
git add pyexploratory/components/step_panel.py pyexploratory/components/context_bar.py
git commit -m "feat(ui): add step panel and context bar components"
```

---

## Task 4: Workspace Layout — Rewrite data_analysis.py

**Files:**
- Modify: `pyexploratory/pages/data_analysis.py` (complete rewrite)
- Modify: `pyexploratory/app.py` (update to 3-zone layout)
- Test: Visual verification via Playwright

**Step 1: Rewrite pages/data_analysis.py**

Replace the entire file. The new layout has: context bar + main workspace (data table as base, with overlay areas for charts/ML/summary) + all hidden stores/modals from the old table tab.

```python
"""
Data Analysis page — unified workspace layout.

Replaces the tab-based system with a 3-zone workspace:
- Context bar (top)
- Main workspace (center): data table + overlay panels
- Step panel (right): managed at app level
"""

import os

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from pyexploratory.config import (
    BG_CARD,
    BG_SURFACE,
    BORDER_COLOR,
    GLASS_CARD_STYLE,
    LIGHT_GREEN,
    MAX_UPLOAD_SIZE_MB,
    PRIMARY,
    PRIMARY_BUTTON_STYLE,
    TEXT_MUTED_V2,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from pyexploratory.components.context_bar import render as render_context_bar

os.environ["OMP_NUM_THREADS"] = "1"

dash.register_page(
    __name__,
    path="/data_analysis",
    name="Data Analysis",
    order=3,
)

layout = html.Div(
    [
        # Context bar
        html.Div(id="context-bar-container", children=render_context_bar()),

        # Upload area (shown when no data loaded, or as a collapsible)
        html.Div(
            id="upload-area",
            children=[
                dcc.Upload(
                    id="upload-data",
                    children=html.Div(
                        [
                            html.Div(
                                "Upload Your Data",
                                style={
                                    "fontSize": "16px", "fontWeight": "600",
                                    "color": PRIMARY, "marginBottom": "8px",
                                },
                            ),
                            html.Div(
                                [
                                    "Drag and Drop or ",
                                    html.A(
                                        "Browse Files",
                                        style={"color": TEXT_PRIMARY, "textDecoration": "underline"},
                                    ),
                                ],
                                style={"color": TEXT_SECONDARY},
                            ),
                            html.Small(
                                f"Supports CSV, Excel, JSON — max {MAX_UPLOAD_SIZE_MB}MB",
                                style={"color": TEXT_MUTED_V2, "marginTop": "4px"},
                            ),
                        ],
                    ),
                    style={
                        "width": "100%", "height": "100px",
                        "lineHeight": "30px", "borderWidth": "2px",
                        "borderStyle": "dashed", "borderColor": PRIMARY,
                        "borderRadius": "8px", "textAlign": "center",
                        "backgroundColor": BG_CARD, "cursor": "pointer",
                        "padding": "16px",
                    },
                    max_size=MAX_UPLOAD_SIZE_MB * 1024 * 1024,
                    multiple=True,
                ),
            ],
            className="glass-card",
            style={"margin": "16px 20px"},
        ),

        dcc.Loading(
            id="loading-upload",
            type="circle",
            color=PRIMARY,
            children=html.Div(id="output-data-upload"),
        ),

        # Hidden stores and modals (from old table tab — needed by callbacks)
        dcc.Store(id="pending-operation", data=None),
        dcc.Store(id="history-trigger", data=0),
        dcc.Store(id="active-panel", data=None),  # tracks which slide-in panel is open

        # Confirmation modal
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Confirm Operation")),
                dbc.ModalBody(id="confirm-modal-body"),
                dbc.ModalFooter([
                    dbc.Button("Cancel", id="confirm-cancel", className="ms-auto", color="secondary"),
                    dbc.Button("Confirm", id="confirm-execute", color="danger"),
                ]),
            ],
            id="confirm-modal", is_open=False,
        ),

        # Preview modal
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Operation Preview")),
                dbc.ModalBody(id="preview-modal-body"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="preview-close", color="secondary"),
                ),
            ],
            id="preview-modal", is_open=False,
        ),

        # Toast
        dbc.Toast(
            id="cleaning-toast",
            header="Result",
            is_open=False,
            dismissable=True,
            duration=4000,
            icon="success",
            className="toast-slide-in",
            style={"position": "fixed", "top": 20, "right": 300, "width": 350, "zIndex": 9999},
        ),

        # Summary stats overlay (toggled by menu-summary)
        html.Div(id="summary-overlay", style={"display": "none", "padding": "0 20px"}),

        # Main data table workspace
        html.Div(
            id="table-workspace",
            className="workspace-table",
            style={"padding": "0 20px 20px 20px"},
        ),

        # Save + Undo/Redo row
        html.Div(
            id="table-controls",
            style={
                "padding": "8px 20px", "display": "flex",
                "alignItems": "center", "gap": "8px", "flexWrap": "wrap",
            },
        ),

        # Inline cleaning form (rendered when "Clean" is selected from + menu)
        html.Div(id="cleaning-panel", style={"display": "none", "padding": "0 20px"}),

        # Chart/ML results render here
        html.Div(id="chart-container", style={"padding": "0 20px"}, className="chart-fade-in"),
        html.Div(id="ml-results", style={"padding": "0 20px"}),

        # Cleaning result text (for alerts)
        html.Div(id="cleaning-result", style={"padding": "0 20px"}),

        # History log (hidden, kept for callback compatibility)
        html.Div(id="history-log", style={"display": "none"}),
        html.Div(id="output-container-button", style={"display": "none"}),

        # Refresh location
        dcc.Location(id="refresh", refresh=True),
    ],
    style={"backgroundColor": BG_SURFACE, "minHeight": "100vh", "paddingBottom": "40px"},
)
```

**Step 2: Update app.py for the 3-zone layout**

The sidebar stays at the app level. The step panel also renders at the app level (so it's visible on the data analysis page). The main content area is adjusted for the 3-zone margins.

Rewrite `pyexploratory/app.py`:

```python
"""
PyExploratory — Dash application entry point.

Creates the Dash app with 3-zone layout:
- Sidebar (left, 200px)
- Main workspace (center, fluid)
- Step panel (right, 280px — only on data_analysis page)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from pyexploratory.components.step_panel import render as render_step_panel
from pyexploratory.components.styles import DOWNLOAD_BUTTON_STYLE
from pyexploratory.config import (
    BG_DEEP,
    BG_SURFACE,
    BORDER_COLOR,
    DATA_FILE,
    PRIMARY,
    PRIMARY_BUTTON_STYLE,
    SIDEBAR_STYLE_V2,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)

px.defaults.template = "plotly_dark"

app = Dash(
    __name__,
    pages_folder="pages",
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

# Sidebar
sidebar = html.Div(
    [
        html.Div(
            "PyExploratory",
            style={
                "fontSize": "18px", "fontWeight": "700", "color": TEXT_PRIMARY,
                "fontFamily": "'Inter', sans-serif", "padding": "0 0 40px 0",
            },
        ),
        dcc.Location(id="url", refresh=False),
        dbc.Nav(id="sidebar-nav", vertical=True, pills=True),
        html.Hr(style={"borderColor": BORDER_COLOR, "margin": "20px 0"}),
        dcc.Download(id="download-data"),
        html.Button(
            "Download Data", id="btn-download", n_clicks=0,
            style={**PRIMARY_BUTTON_STYLE, "width": "100%", "marginBottom": "8px"},
            className="btn-primary-glow",
        ),
        dcc.Download(id="download-script"),
        html.Button(
            "Export Script", id="btn-export-script", n_clicks=0,
            style={**PRIMARY_BUTTON_STYLE, "width": "100%", "marginBottom": "8px"},
            className="btn-primary-glow",
        ),
        dcc.Upload(
            id="upload-script",
            children=html.Button(
                "Import Script",
                style={**PRIMARY_BUTTON_STYLE, "width": "100%"},
                className="btn-primary-glow",
            ),
            accept=".py",
            max_size=5 * 1024 * 1024,
        ),
        html.Div(id="import-script-feedback", style={"marginTop": "8px"}),
    ],
    style=SIDEBAR_STYLE_V2,
)

# Layout
app.layout = html.Div(
    [
        sidebar,
        # Step panel (renders on data_analysis page)
        html.Div(id="step-panel-container"),
        # Main content
        html.Div(
            dash.page_container,
            id="main-content",
            style={
                "marginLeft": "200px",
                "minHeight": "100vh",
                "backgroundColor": BG_SURFACE,
            },
        ),
    ],
    style={"backgroundColor": BG_SURFACE, "margin": 0, "padding": 0},
)


# Sidebar nav
@app.callback(Output("sidebar-nav", "children"), [Input("url", "pathname")])
def update_sidebar(pathname):
    return [
        dbc.NavLink(
            [html.Div(page["name"], style={"color": TEXT_PRIMARY, "fontSize": "13px"})],
            href=page["path"],
            active="exact",
            style={
                "backgroundColor": PRIMARY if page["path"] == pathname else "transparent",
                "borderRadius": "6px",
                "margin": "2px 0",
                "padding": "8px 12px",
            },
        )
        for page in dash.page_registry.values()
    ]


# Step panel — only render on data_analysis page
@app.callback(
    Output("step-panel-container", "children"),
    Output("main-content", "style"),
    Input("url", "pathname"),
)
def toggle_step_panel(pathname):
    if pathname == "/data_analysis":
        return render_step_panel(), {
            "marginLeft": "200px",
            "marginRight": "280px",
            "minHeight": "100vh",
            "backgroundColor": BG_SURFACE,
        }
    return html.Div(), {
        "marginLeft": "200px",
        "minHeight": "100vh",
        "backgroundColor": BG_SURFACE,
    }


# Download data
@dash.callback(
    Output("download-data", "data"),
    Input("btn-download", "n_clicks"),
    prevent_initial_call=True,
)
def download_data(n_clicks):
    if n_clicks:
        df = pd.read_csv(DATA_FILE)
        return dcc.send_data_frame(df.to_excel, "mydata.xlsx")


# Import callbacks
import pyexploratory.callbacks  # noqa: E402, F401

if __name__ == "__main__":
    app.run(debug=True)
```

**Step 3: Run the app and verify with Playwright**

Run: `python pyexploratory/app.py`

Use Playwright to navigate to `http://127.0.0.1:8050/data_analysis` and verify:
- Sidebar renders on the left (200px, dark gradient)
- Step panel renders on the right (280px, dark gradient)
- Main content is between them
- Context bar shows "No dataset loaded" or dataset info
- Upload area is visible with green dashed border
- CSS animations and fonts loaded (Inter font visible)

**Step 4: Commit**

```bash
git add pyexploratory/app.py pyexploratory/pages/data_analysis.py
git commit -m "feat(ui): implement 3-zone workspace layout"
```

---

## Task 5: Step Panel Callbacks

**Files:**
- Create: `pyexploratory/callbacks/step_panel.py`
- Modify: `pyexploratory/callbacks/__init__.py`

**Step 1: Create step panel callbacks**

Create `pyexploratory/callbacks/step_panel.py`:

```python
"""
Callbacks for the step panel — toggle add-step menu, handle step
toggle/delete, refresh step list after operations.
"""

import dash
from dash import html, no_update
from dash.dependencies import Input, Output, State, ALL

from pyexploratory.components.step_panel import render as render_step_panel
from pyexploratory.core import action_log


@dash.callback(
    Output("add-step-menu", "style"),
    Input("add-step-btn", "n_clicks"),
    State("add-step-menu", "style"),
    prevent_initial_call=True,
)
def toggle_add_menu(n_clicks, current_style):
    """Toggle the + Add Step dropdown menu."""
    if not n_clicks:
        return no_update
    if current_style and current_style.get("display") == "block":
        return {"display": "none"}
    return {"display": "block", "marginTop": "8px"}


@dash.callback(
    Output("step-list", "children"),
    Input("add-step-btn", "n_clicks"),
    Input({"type": "step-toggle", "index": ALL}, "n_clicks"),
    Input({"type": "step-delete", "index": ALL}, "n_clicks"),
    Input("output-data-upload", "children"),
    Input("cleaning-result", "children"),
    Input("chart-container", "children"),
    Input("ml-results", "children"),
)
def refresh_step_list(*_):
    """Re-render the step list whenever the action log changes."""
    panel = render_step_panel()
    # Extract just the step-list children from the panel
    for child in panel.children:
        if hasattr(child, 'id') and child.id == "step-list":
            return child.children
    return []


@dash.callback(
    Output("step-list", "children", allow_duplicate=True),
    Input({"type": "step-toggle", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def handle_step_toggle(n_clicks_list):
    """Toggle the disabled state of a step."""
    triggered = dash.ctx.triggered_id
    if triggered and isinstance(triggered, dict) and triggered.get("type") == "step-toggle":
        step_id = triggered["index"]
        if any(n for n in n_clicks_list if n):
            action_log.toggle_step(step_id)
    return no_update


@dash.callback(
    Output("step-list", "children", allow_duplicate=True),
    Input({"type": "step-delete", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def handle_step_delete(n_clicks_list):
    """Delete a step from the action log."""
    triggered = dash.ctx.triggered_id
    if triggered and isinstance(triggered, dict) and triggered.get("type") == "step-delete":
        step_id = triggered["index"]
        if any(n for n in n_clicks_list if n):
            action_log.delete_step(step_id)
    return no_update
```

**Step 2: Register the new callback module**

Add to `pyexploratory/callbacks/__init__.py`:

```python
from pyexploratory.callbacks import step_panel  # noqa: F401
```

**Step 3: Commit**

```bash
git add pyexploratory/callbacks/step_panel.py pyexploratory/callbacks/__init__.py
git commit -m "feat(ui): add step panel callbacks for toggle, delete, refresh"
```

---

## Task 6: Wire Up Table + Cleaning to New Layout

**Files:**
- Modify: `pyexploratory/callbacks/table.py` (update component IDs if needed)
- Modify: `pyexploratory/pages/data_analysis.py` (add table rendering callback)

**Step 1: Add callback to render the data table in the workspace**

Add a new callback in `pyexploratory/callbacks/table.py` (at the top, after imports) that populates the `table-workspace` div and `table-controls` div:

```python
@dash.callback(
    Output("table-workspace", "children"),
    Output("table-controls", "children"),
    Input("output-data-upload", "children"),
    Input("cleaning-toast", "is_open"),
    Input("history-trigger", "data"),
)
def render_workspace_table(*_):
    """Render the editable data table in the main workspace."""
    from pyexploratory.components.tables import DATA_TABLE_CELL_STYLE, TABLE_HEADER_STYLE, DATA_TABLE_STYLE
    from pyexploratory.config import BG_CARD, GHOST_BUTTON_STYLE, PRIMARY_BUTTON_STYLE, TEXT_SECONDARY

    try:
        df = read_data()
    except FileNotFoundError:
        return html.Div(), html.Div()

    table = dash_table.DataTable(
        id="table",
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        page_action="native",
        page_size=50,
        style_table={**DATA_TABLE_STYLE, "maxHeight": "60vh", "overflowY": "auto"},
        style_cell={
            "textAlign": "center",
            "backgroundColor": BG_CARD,
            "color": "#e0e0e0",
            "border": f"1px solid #2a2a30",
            "fontFamily": "'JetBrains Mono', monospace",
            "fontSize": "12px",
        },
        style_header={
            "backgroundColor": "#1a1a1d",
            "fontWeight": "600",
            "color": "#a0a0a0",
            "textTransform": "uppercase",
            "letterSpacing": "0.5px",
            "fontSize": "11px",
            "fontFamily": "'Inter', sans-serif",
            "borderBottom": "2px solid #3a3a3b",
        },
        editable=True,
    )

    controls = [
        html.Button("Save Changes", id="save-button", style={**PRIMARY_BUTTON_STYLE, "padding": "6px 16px"}, className="btn-primary-glow"),
        html.Button("Undo", id="undo-btn", n_clicks=0, style={**GHOST_BUTTON_STYLE, "borderColor": "#e67e22", "color": "#e67e22"}),
        html.Button("Redo", id="redo-btn", n_clicks=0, style={**GHOST_BUTTON_STYLE, "borderColor": "#3498db", "color": "#3498db"}),
    ]

    return table, controls
```

Add the missing `dash_table` import at the top of the file:

```python
from dash import dash_table, html, no_update
```

**Step 2: Add cleaning panel callback**

Add a callback that shows the inline cleaning form when "Clean" is selected from the + menu:

```python
@dash.callback(
    Output("cleaning-panel", "children"),
    Output("cleaning-panel", "style"),
    Input("menu-clean", "n_clicks"),
    prevent_initial_call=True,
)
def show_cleaning_panel(n_clicks):
    """Show the inline cleaning form."""
    if not n_clicks:
        return no_update, no_update

    from pyexploratory.tabs.table import CLEANING_OPTIONS
    from pyexploratory.config import GLASS_CARD_STYLE, TEXT_SECONDARY, PRIMARY_BUTTON_STYLE, GHOST_BUTTON_STYLE

    form = html.Div(
        [
            html.H6("Clean / Transform", style={"color": "#00c46a", "fontWeight": "600", "marginBottom": "12px"}),
            dbc.Row([
                dbc.Col([
                    html.Label("Operation:", style={"color": TEXT_SECONDARY, "fontSize": "12px"}),
                    dcc.Dropdown(
                        id="cleaning-operation",
                        options=CLEANING_OPTIONS,
                        placeholder="Select operation...",
                        style={"borderRadius": "6px", "fontSize": "13px"},
                    ),
                ], md=3),
                dbc.Col([
                    html.Label("Column:", style={"color": TEXT_SECONDARY, "fontSize": "12px"}),
                    dcc.Input(
                        id="column-to-clean", type="text", placeholder="Column...",
                        style={"borderRadius": "6px", "width": "100%", "padding": "8px", "backgroundColor": "#222226", "color": "#f0f0f0", "border": "1px solid #3a3a3b"},
                    ),
                ], md=3),
                dbc.Col([
                    html.Label("Fill Value:", style={"color": TEXT_SECONDARY, "fontSize": "12px"}),
                    dcc.Input(
                        id="fill-value", type="text", placeholder="Value...",
                        style={"borderRadius": "6px", "width": "100%", "padding": "8px", "backgroundColor": "#222226", "color": "#f0f0f0", "border": "1px solid #3a3a3b"},
                    ),
                ], md=2),
                dbc.Col([
                    html.Label("New Name:", style={"color": TEXT_SECONDARY, "fontSize": "12px"}),
                    dcc.Input(
                        id="new-column-name", type="text", placeholder="New name...",
                        style={"borderRadius": "6px", "width": "100%", "padding": "8px", "backgroundColor": "#222226", "color": "#f0f0f0", "border": "1px solid #3a3a3b"},
                    ),
                ], md=2),
                dbc.Col([
                    html.Label("\u00a0", style={"fontSize": "12px"}),
                    html.Div([
                        html.Button("Apply", id="clean-data-btn", n_clicks=0, style={**PRIMARY_BUTTON_STYLE, "padding": "8px 16px"}, className="btn-primary-glow"),
                        html.Button("Preview", id="preview-btn", n_clicks=0, style={**GHOST_BUTTON_STYLE, "marginLeft": "6px"}),
                    ], style={"display": "flex"}),
                ], md=2),
            ]),
        ],
        className="glass-card",
    )

    return form, {"display": "block", "padding": "0 20px", "marginBottom": "12px"}
```

**Step 3: Run the app and test with Playwright**

Navigate to `http://127.0.0.1:8050/data_analysis`, upload a CSV, and verify:
- Data table renders in the main workspace with the new styling
- Save/Undo/Redo buttons appear
- Clicking "+ Add Step" shows the menu
- Clicking "Clean / Transform" shows the inline cleaning form
- Applying a cleaning operation works and a new step appears in the panel

**Step 4: Run existing tests**

Run: `pytest -v`
Expected: All tests PASS.

**Step 5: Commit**

```bash
git add pyexploratory/callbacks/table.py pyexploratory/pages/data_analysis.py
git commit -m "feat(ui): wire table and cleaning to new workspace layout"
```

---

## Task 7: Wire Up Charts to New Layout

**Files:**
- Modify: `pyexploratory/callbacks/charts.py` (minor — add show/hide for chart builder)
- Modify: `pyexploratory/callbacks/table.py` (add chart panel callback)

**Step 1: Add chart builder panel callback**

In `pyexploratory/callbacks/table.py`, add a callback that shows the chart builder when "Visualize" is clicked from + menu. The chart builder should reuse `tabs/charts.py` options:

```python
@dash.callback(
    Output("chart-container", "children", allow_duplicate=True),
    Output("chart-container", "style"),
    Input("menu-chart", "n_clicks"),
    prevent_initial_call=True,
)
def show_chart_panel(n_clicks):
    """Show the chart builder in the main workspace."""
    if not n_clicks:
        return no_update, no_update

    from pyexploratory.tabs.charts import CHART_TYPE_OPTIONS, render as render_chart_tab
    # Re-use existing chart tab render
    chart_content = render_chart_tab()

    return chart_content, {"display": "block", "padding": "0 20px"}
```

**Step 2: Add ML panel callback**

Similarly for ML:

```python
@dash.callback(
    Output("ml-results", "children", allow_duplicate=True),
    Output("ml-results", "style"),
    Input("menu-ml", "n_clicks"),
    prevent_initial_call=True,
)
def show_ml_panel(n_clicks):
    """Show the ML task selector in the main workspace."""
    if not n_clicks:
        return no_update, no_update

    from pyexploratory.tabs.machine_learning import render as render_ml_tab
    ml_content = render_ml_tab()

    return ml_content, {"display": "block", "padding": "0 20px"}
```

**Step 3: Add summary overlay callback**

```python
@dash.callback(
    Output("summary-overlay", "children"),
    Output("summary-overlay", "style"),
    Input("menu-summary", "n_clicks"),
    State("summary-overlay", "style"),
    prevent_initial_call=True,
)
def toggle_summary(n_clicks, current_style):
    """Toggle the summary stats overlay above the table."""
    if not n_clicks:
        return no_update, no_update

    # If already visible, hide it
    if current_style and current_style.get("display") == "block":
        return html.Div(), {"display": "none", "padding": "0 20px"}

    from pyexploratory.tabs.summary import render as render_summary
    return render_summary(), {"display": "block", "padding": "0 20px", "marginBottom": "12px"}
```

**Step 4: Verify all panels work via Playwright**

Upload data, then test each panel from the + menu.

**Step 5: Run all tests**

Run: `pytest -v`
Expected: All tests PASS.

**Step 6: Commit**

```bash
git add pyexploratory/callbacks/table.py
git commit -m "feat(ui): wire chart, ML, and summary panels to workspace"
```

---

## Task 8: Update Sidebar Styles

**Files:**
- Modify: `pyexploratory/components/styles.py`

**Step 1: Update shared button styles**

```python
"""
Shared component styles for buttons, inputs, and dropdowns.
"""

from pyexploratory.config import (
    GHOST_BUTTON_STYLE,
    PRIMARY_BUTTON_STYLE,
    # Legacy imports for backward compatibility
    DARK_GREEN,
    DROPDOWN_STYLE,
    GREEN_BUTTON_STYLE,
    INPUT_STYLE,
    WHITE,
)

__all__ = [
    "GREEN_BUTTON_STYLE",
    "DROPDOWN_STYLE",
    "INPUT_STYLE",
    "SAVE_BUTTON_STYLE",
    "DOWNLOAD_BUTTON_STYLE",
    "CLEAN_BUTTON_STYLE",
    "PRIMARY_BUTTON_STYLE",
    "GHOST_BUTTON_STYLE",
]

SAVE_BUTTON_STYLE = {**PRIMARY_BUTTON_STYLE, "width": "auto"}
DOWNLOAD_BUTTON_STYLE = {**PRIMARY_BUTTON_STYLE, "width": "100%", "marginBottom": "8px"}
CLEAN_BUTTON_STYLE = {**PRIMARY_BUTTON_STYLE, "width": "auto"}
```

**Step 2: Commit**

```bash
git add pyexploratory/components/styles.py
git commit -m "refactor(ui): update shared button styles to v2 design system"
```

---

## Task 9: Update Introduction Page

**Files:**
- Modify: `pyexploratory/pages/introduction.py`

**Step 1: Read current introduction page**

Read the file first, then update styles to match the new design system.

**Step 2: Update with new styles**

Use `BG_SURFACE`, `TEXT_PRIMARY`, `PRIMARY` instead of the old color constants.

**Step 3: Commit**

```bash
git add pyexploratory/pages/introduction.py
git commit -m "style(ui): update introduction page to v2 design system"
```

---

## Task 10: Visual QA with Playwright

**Files:** None (visual verification only)

**Step 1: Start the app**

Run: `python pyexploratory/app.py`

**Step 2: Playwright verification checklist**

Use the Playwright MCP tools to verify each of these:

1. Navigate to `http://127.0.0.1:8050/`
   - Verify: Introduction page renders with new fonts and dark background
   - Verify: Sidebar has gradient background, green buttons with glow

2. Navigate to `http://127.0.0.1:8050/data_analysis`
   - Verify: 3-zone layout visible (sidebar, main, step panel)
   - Verify: Context bar shows "No dataset loaded"
   - Verify: Upload area has green dashed border

3. Upload `data/test_data.csv`
   - Verify: Data table renders with striped rows, monospace font
   - Verify: Context bar updates with filename, row/col count
   - Verify: Step panel shows "Upload test_data.csv" step card

4. Click "+ Add Step" → "Clean / Transform"
   - Verify: Cleaning form appears with glassmorphic card
   - Verify: Apply a cleaning operation (e.g., "Trim Whitespace" on a column)
   - Verify: New step appears in the panel

5. Click "+ Add Step" → "Visualize"
   - Verify: Chart builder appears
   - Verify: Generate a histogram
   - Verify: Chart renders with fade-in animation

6. Click "+ Add Step" → "Machine Learning"
   - Verify: ML task selector appears
   - Verify: Run a clustering task
   - Verify: Results render in workspace

7. Click "+ Add Step" → "Summary Stats"
   - Verify: KPI tiles and column cards appear above the table

8. Take screenshots at each step for documentation.

**Step 3: Fix any visual issues found**

Address any layout, spacing, or color issues discovered.

**Step 4: Commit fixes**

```bash
git add -A
git commit -m "fix(ui): visual QA fixes from Playwright testing"
```

---

## Task 11: Run Full Test Suite & Final Cleanup

**Files:** Various (cleanup only)

**Step 1: Run full test suite**

Run: `pytest -v`
Expected: All tests PASS. If any fail, fix them.

**Step 2: Run linting**

Run: `black pyexploratory tests && isort pyexploratory tests && flake8 pyexploratory tests`
Expected: Clean output.

**Step 3: Remove legacy style constants if no longer used**

Check `config.py` for any old constants (like `TAB_STYLE`, `SELECTED_TAB_STYLE`) that are no longer referenced. Remove them.

**Step 4: Final commit**

```bash
git add -A
git commit -m "chore: cleanup legacy styles and lint fixes"
```

---

## Summary of All Commits

| Task | Commit Message |
|------|---------------|
| 1 | `feat(ui): add v2 design system colors, styles, and CSS animations` |
| 2 | `feat(core): extend action log with step id, timestamp, toggle, delete` |
| 3 | `feat(ui): add step panel and context bar components` |
| 4 | `feat(ui): implement 3-zone workspace layout` |
| 5 | `feat(ui): add step panel callbacks for toggle, delete, refresh` |
| 6 | `feat(ui): wire table and cleaning to new workspace layout` |
| 7 | `feat(ui): wire chart, ML, and summary panels to workspace` |
| 8 | `refactor(ui): update shared button styles to v2 design system` |
| 9 | `style(ui): update introduction page to v2 design system` |
| 10 | `fix(ui): visual QA fixes from Playwright testing` |
| 11 | `chore: cleanup legacy styles and lint fixes` |
