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
    "upload": "\u2b06",
    "cleaning": "\U0001f9f9",
    "chart": "\U0001f4ca",
    "ml": "\U0001f916",
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
                    html.Span(
                        title,
                        style={
                            "color": TEXT_PRIMARY,
                            "fontSize": "13px",
                            "fontWeight": "500",
                        },
                    ),
                ],
                style={"display": "flex", "alignItems": "center"},
            ),
            html.Div(
                _relative_time(ts),
                style={
                    "color": TEXT_MUTED_V2,
                    "fontSize": "11px",
                    "marginTop": "4px",
                    "paddingLeft": "24px",
                },
            ),
            html.Div(
                [
                    html.Button(
                        "\u2298" if not disabled else "\u25cb",
                        id={"type": "step-toggle", "index": step_id},
                        n_clicks=0,
                        style={
                            "background": "none",
                            "border": "none",
                            "color": TEXT_SECONDARY,
                            "cursor": "pointer",
                            "fontSize": "14px",
                            "padding": "2px 6px",
                        },
                        title="Disable step" if not disabled else "Enable step",
                    ),
                    html.Button(
                        "\u2715",
                        id={"type": "step-delete", "index": step_id},
                        n_clicks=0,
                        style={
                            "background": "none",
                            "border": "none",
                            "color": TEXT_SECONDARY,
                            "cursor": "pointer",
                            "fontSize": "14px",
                            "padding": "2px 6px",
                        },
                        title="Delete step",
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "flex-end",
                    "marginTop": "4px",
                    "gap": "4px",
                },
            ),
        ],
        className=css_classes,
        id={"type": "step-card", "index": step_id},
        style={"backgroundColor": BG_DEEP, "borderLeftColor": color},
    )


def render() -> html.Div:
    """Build the step panel."""
    log = get_log()

    step_cards = (
        [_step_card(entry) for entry in log]
        if log
        else [
            html.Div(
                "Start by uploading a dataset",
                style={
                    "color": TEXT_MUTED_V2,
                    "fontSize": "13px",
                    "textAlign": "center",
                    "padding": "40px 0",
                },
            )
        ]
    )

    return html.Div(
        [
            html.Div(
                "Steps",
                style={
                    "color": TEXT_PRIMARY,
                    "fontSize": "15px",
                    "fontWeight": "600",
                    "marginBottom": "16px",
                    "fontFamily": "'Inter', sans-serif",
                },
            ),
            html.Div(id="step-list", children=step_cards),
            html.Hr(style={"borderColor": BORDER_COLOR, "margin": "12px 0"}),
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
                                    [
                                        html.Span(
                                            "\U0001f9f9",
                                            style={"fontSize": "16px"},
                                        ),
                                        " Clean / Transform",
                                    ],
                                    id="menu-clean",
                                    className="add-step-item",
                                    n_clicks=0,
                                ),
                                html.Div(
                                    [
                                        html.Span(
                                            "\U0001f4ca",
                                            style={"fontSize": "16px"},
                                        ),
                                        " Visualize",
                                    ],
                                    id="menu-chart",
                                    className="add-step-item",
                                    n_clicks=0,
                                ),
                                html.Div(
                                    [
                                        html.Span(
                                            "\U0001f916",
                                            style={"fontSize": "16px"},
                                        ),
                                        " Machine Learning",
                                    ],
                                    id="menu-ml",
                                    className="add-step-item",
                                    n_clicks=0,
                                ),
                                html.Div(
                                    [
                                        html.Span(
                                            "\U0001f4cb",
                                            style={"fontSize": "16px"},
                                        ),
                                        " Summary Stats",
                                    ],
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
