"""
Data Analysis page — unified workspace layout.

Replaces the tab-based system with a 3-zone workspace:
- Context bar (top)
- Main workspace (center): data table + overlay panels
- Step panel (right): managed at app level

All cleaning, chart, and ML IDs are pre-rendered (hidden) so that
Dash callbacks can reference them at startup without errors.
"""

import os

import dash
import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html

from pyexploratory.config import (
    BG_CARD,
    BG_SURFACE,
    BORDER_COLOR,
    DEFAULT_TEST_SIZE,
    DT_DEFAULT_MAX_DEPTH,
    DROPDOWN_STYLE,
    GLASS_CARD_STYLE,
    KMEANS_DEFAULT_CLUSTERS,
    MAX_UPLOAD_SIZE_MB,
    PRIMARY,
    PRIMARY_BUTTON_STYLE,
    RF_DEFAULT_ESTIMATORS,
    GHOST_BUTTON_STYLE,
    SECTION_CARD_STYLE,
    TEXT_MUTED_V2,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)
from pyexploratory.components.context_bar import render as render_context_bar
from pyexploratory.tabs.table import CLEANING_OPTIONS
from pyexploratory.tabs.charts import CHART_TYPE_OPTIONS

os.environ["OMP_NUM_THREADS"] = "1"

dash.register_page(
    __name__,
    path="/data_analysis",
    name="Data Analysis",
    order=3,
)

# ---------------------------------------------------------------------------
# Inline cleaning form (hidden by default, shown via callback)
# ---------------------------------------------------------------------------
_cleaning_form = html.Div(
    id="cleaning-panel",
    style={"display": "none", "padding": "0 20px", "marginBottom": "12px"},
    children=html.Div(
        [
            html.H6(
                "Clean / Transform",
                style={"color": "#00c46a", "fontWeight": "600", "marginBottom": "12px"},
            ),
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
                        style={
                            "borderRadius": "6px", "width": "100%", "padding": "8px",
                            "backgroundColor": "#222226", "color": "#f0f0f0",
                            "border": "1px solid #3a3a3b",
                        },
                    ),
                ], md=3),
                dbc.Col([
                    html.Label("Fill Value:", style={"color": TEXT_SECONDARY, "fontSize": "12px"}),
                    dcc.Input(
                        id="fill-value", type="text", placeholder="Value...",
                        style={
                            "borderRadius": "6px", "width": "100%", "padding": "8px",
                            "backgroundColor": "#222226", "color": "#f0f0f0",
                            "border": "1px solid #3a3a3b",
                        },
                    ),
                ], md=2),
                dbc.Col([
                    html.Label("New Name:", style={"color": TEXT_SECONDARY, "fontSize": "12px"}),
                    dcc.Input(
                        id="new-column-name", type="text", placeholder="New name...",
                        style={
                            "borderRadius": "6px", "width": "100%", "padding": "8px",
                            "backgroundColor": "#222226", "color": "#f0f0f0",
                            "border": "1px solid #3a3a3b",
                        },
                    ),
                ], md=2),
                dbc.Col([
                    html.Label("\u00a0", style={"fontSize": "12px"}),
                    html.Div([
                        html.Button(
                            "Apply", id="clean-data-btn", n_clicks=0,
                            style={**PRIMARY_BUTTON_STYLE, "padding": "8px 16px"},
                            className="btn-primary-glow",
                        ),
                        html.Button(
                            "Preview", id="preview-btn", n_clicks=0,
                            style={**GHOST_BUTTON_STYLE, "marginLeft": "6px"},
                        ),
                    ], style={"display": "flex"}),
                ], md=2),
            ]),
        ],
        className="glass-card",
    ),
)

# ---------------------------------------------------------------------------
# Chart builder (hidden by default, shown via callback)
# ---------------------------------------------------------------------------
_DROPDOWN_BLACK = {**DROPDOWN_STYLE, "color": "black"}
_TEXT_MUTED_STYLE = {"color": TEXT_SECONDARY, "fontSize": "13px"}

_chart_builder = html.Div(
    id="chart-panel-wrapper",
    style={"display": "none", "padding": "0 20px"},
    children=dbc.Card(
        [
            html.H5(
                "Chart Builder",
                style={"color": PRIMARY, "fontWeight": "600", "marginBottom": "16px"},
            ),
            dbc.Row([
                dbc.Col([
                    html.Label("Chart Type:", style=_TEXT_MUTED_STYLE),
                    dcc.Dropdown(
                        id="chart-type-dropdown",
                        options=CHART_TYPE_OPTIONS,
                        value="",
                        placeholder="Select a chart type...",
                        style=_DROPDOWN_BLACK,
                    ),
                ], md=3),
                dbc.Col(
                    id="chart-x-col",
                    children=[
                        html.Label("X Axis:", style=_TEXT_MUTED_STYLE),
                        dcc.Dropdown(
                            id="chart-x-dropdown", options=[], value="",
                            placeholder="Select column...", style=_DROPDOWN_BLACK,
                        ),
                    ], md=2,
                ),
                dbc.Col(
                    id="chart-y-col",
                    children=[
                        html.Label("Y Axis:", style=_TEXT_MUTED_STYLE),
                        dcc.Dropdown(
                            id="chart-y-dropdown", options=[], value="",
                            placeholder="Select column...", style=_DROPDOWN_BLACK,
                        ),
                    ], md=2,
                ),
                dbc.Col(
                    id="chart-color-col",
                    children=[
                        html.Label("Color By:", style=_TEXT_MUTED_STYLE),
                        dcc.Dropdown(
                            id="chart-color-dropdown", options=[], value="",
                            placeholder="(Optional)", style=_DROPDOWN_BLACK,
                        ),
                    ], md=2,
                ),
                dbc.Col(
                    id="chart-size-col",
                    style={"display": "none"},
                    children=[
                        html.Label("Size By:", style=_TEXT_MUTED_STYLE),
                        dcc.Dropdown(
                            id="chart-size-dropdown", options=[], value="",
                            placeholder="(Optional)", style=_DROPDOWN_BLACK,
                        ),
                    ], md=2,
                ),
                dbc.Col([
                    html.Label("\u00A0", style={"fontSize": "13px"}),
                    html.Button(
                        "Generate Chart", id="generate-chart-btn", n_clicks=0,
                        style={**PRIMARY_BUTTON_STYLE, "width": "100%", "whiteSpace": "nowrap"},
                        className="btn-primary-glow",
                    ),
                ], md=2, style={"display": "flex", "flexDirection": "column"}),
            ]),
        ],
        style=SECTION_CARD_STYLE,
    ),
)

# ---------------------------------------------------------------------------
# ML panel (hidden by default, shown via callback)
# ---------------------------------------------------------------------------
_ml_panel = html.Div(
    id="ml-panel-wrapper",
    style={"display": "none", "padding": "0 20px"},
    children=[
        dbc.Card(
            [
                html.H5(
                    "Machine Learning Task Selector",
                    style={"color": PRIMARY, "fontWeight": "600", "marginBottom": "16px"},
                ),
                dbc.Row([
                    dbc.Col([
                        html.Label("Task:", style=_TEXT_MUTED_STYLE),
                        dcc.Dropdown(
                            id="task-dropdown",
                            options=[
                                {"label": "Clustering", "value": "clustering"},
                                {"label": "Classification (SVM)", "value": "classification"},
                                {"label": "Decision Tree", "value": "decision_tree"},
                                {"label": "Random Forest", "value": "random_forest"},
                                {"label": "Linear Regression", "value": "regression"},
                            ],
                            value="",
                            placeholder="Select a task...",
                            style=_DROPDOWN_BLACK,
                        ),
                    ], md=4),
                    dbc.Col([
                        html.Label("X Variable:", style=_TEXT_MUTED_STYLE),
                        dcc.Dropdown(
                            id="x-variable", value="",
                            placeholder="Select x-axis...", style=_DROPDOWN_BLACK,
                        ),
                    ], md=4),
                    dbc.Col([
                        html.Label("Y Variable:", style=_TEXT_MUTED_STYLE),
                        dcc.Dropdown(
                            id="y-variable", value="",
                            placeholder="Select y-axis...", style=_DROPDOWN_BLACK,
                        ),
                    ], md=4),
                ]),
            ],
            style=SECTION_CARD_STYLE,
        ),
        # Clustering controls
        html.Div(
            id="clustering-controls", style={"display": "none"},
            children=[dbc.Card([
                html.H6("Clustering Parameters", style={"color": PRIMARY, "fontWeight": "600"}),
                html.Label("Number of Clusters:", style={"color": TEXT_SECONDARY, "margin": "10px 0 5px 0"}),
                dcc.Slider(
                    id="n-clusters", min=2, max=10, step=1,
                    value=KMEANS_DEFAULT_CLUSTERS,
                    marks={i: str(i) for i in range(2, 11)},
                    tooltip={"placement": "bottom"},
                ),
            ], style=SECTION_CARD_STYLE)],
        ),
        # Classification (SVM) controls
        html.Div(
            id="classification-controls", style={"display": "none"},
            children=[dbc.Card([
                html.H6("SVM Classification Parameters", style={"color": PRIMARY, "fontWeight": "600"}),
                dbc.Row([
                    dbc.Col([
                        html.Label("Target Variable:", style=_TEXT_MUTED_STYLE),
                        dcc.Dropdown(
                            id="target-variable", value="",
                            placeholder="Select target variable...", style=_DROPDOWN_BLACK,
                        ),
                    ], md=4),
                    dbc.Col([
                        html.Label("SVM Kernel:", style=_TEXT_MUTED_STYLE),
                        dcc.Dropdown(
                            id="svm-kernel",
                            options=[
                                {"label": "Linear", "value": "linear"},
                                {"label": "RBF", "value": "rbf"},
                                {"label": "Polynomial", "value": "poly"},
                                {"label": "Sigmoid", "value": "sigmoid"},
                            ],
                            value="linear", style=_DROPDOWN_BLACK,
                        ),
                    ], md=4),
                    dbc.Col([
                        html.Label("Test Size:", style=_TEXT_MUTED_STYLE),
                        dcc.Slider(
                            id="test-size", min=0.1, max=0.5, step=0.05,
                            value=DEFAULT_TEST_SIZE,
                            marks={i / 10: f"{i / 10:.1f}" for i in range(1, 6)},
                            tooltip={"placement": "bottom"},
                        ),
                    ], md=4),
                ]),
            ], style=SECTION_CARD_STYLE)],
        ),
        # Decision Tree controls
        html.Div(
            id="decision-tree-controls", style={"display": "none"},
            children=[dbc.Card([
                html.H6("Decision Tree Parameters", style={"color": PRIMARY, "fontWeight": "600"}),
                dbc.Row([
                    dbc.Col([
                        html.Label("Target Variable:", style=_TEXT_MUTED_STYLE),
                        dcc.Dropdown(
                            id="dt-target-variable", value="",
                            placeholder="Select target variable...", style=_DROPDOWN_BLACK,
                        ),
                    ], md=4),
                    dbc.Col([
                        html.Label("Max Depth:", style=_TEXT_MUTED_STYLE),
                        dcc.Slider(
                            id="dt-max-depth", min=1, max=20, step=1,
                            value=DT_DEFAULT_MAX_DEPTH,
                            marks={i: str(i) for i in [1, 5, 10, 15, 20]},
                            tooltip={"placement": "bottom"},
                        ),
                    ], md=4),
                    dbc.Col([
                        html.Label("Test Size:", style=_TEXT_MUTED_STYLE),
                        dcc.Slider(
                            id="dt-test-size", min=0.1, max=0.5, step=0.05,
                            value=DEFAULT_TEST_SIZE,
                            marks={i / 10: f"{i / 10:.1f}" for i in range(1, 6)},
                            tooltip={"placement": "bottom"},
                        ),
                    ], md=4),
                ]),
            ], style=SECTION_CARD_STYLE)],
        ),
        # Random Forest controls
        html.Div(
            id="random-forest-controls", style={"display": "none"},
            children=[dbc.Card([
                html.H6("Random Forest Parameters", style={"color": PRIMARY, "fontWeight": "600"}),
                dbc.Row([
                    dbc.Col([
                        html.Label("Target Variable:", style=_TEXT_MUTED_STYLE),
                        dcc.Dropdown(
                            id="rf-target-variable", value="",
                            placeholder="Select target variable...", style=_DROPDOWN_BLACK,
                        ),
                    ], md=3),
                    dbc.Col([
                        html.Label("Estimators:", style=_TEXT_MUTED_STYLE),
                        dcc.Slider(
                            id="rf-n-estimators", min=10, max=500, step=10,
                            value=RF_DEFAULT_ESTIMATORS,
                            marks={i: str(i) for i in [10, 100, 200, 300, 500]},
                            tooltip={"placement": "bottom"},
                        ),
                    ], md=3),
                    dbc.Col([
                        html.Label("Max Depth:", style=_TEXT_MUTED_STYLE),
                        dcc.Slider(
                            id="rf-max-depth", min=1, max=20, step=1,
                            value=DT_DEFAULT_MAX_DEPTH,
                            marks={i: str(i) for i in [1, 5, 10, 15, 20]},
                            tooltip={"placement": "bottom"},
                        ),
                    ], md=3),
                    dbc.Col([
                        html.Label("Test Size:", style=_TEXT_MUTED_STYLE),
                        dcc.Slider(
                            id="rf-test-size", min=0.1, max=0.5, step=0.05,
                            value=DEFAULT_TEST_SIZE,
                            marks={i / 10: f"{i / 10:.1f}" for i in range(1, 6)},
                            tooltip={"placement": "bottom"},
                        ),
                    ], md=3),
                ]),
            ], style=SECTION_CARD_STYLE)],
        ),
        # Regression controls
        html.Div(
            id="regression-controls", style={"display": "none"},
            children=[dbc.Card([
                html.H6("Linear Regression Parameters", style={"color": PRIMARY, "fontWeight": "600"}),
                dbc.Row([
                    dbc.Col([
                        html.Label("Target (Y) Variable:", style=_TEXT_MUTED_STYLE),
                        dcc.Dropdown(
                            id="regression-target", value="",
                            placeholder="Select numeric target...", style=_DROPDOWN_BLACK,
                        ),
                    ], md=4),
                    dbc.Col([
                        html.Label("Test Size:", style=_TEXT_MUTED_STYLE),
                        dcc.Slider(
                            id="reg-test-size", min=0.1, max=0.5, step=0.05,
                            value=DEFAULT_TEST_SIZE,
                            marks={i / 10: f"{i / 10:.1f}" for i in range(1, 6)},
                            tooltip={"placement": "bottom"},
                        ),
                    ], md=4),
                ]),
            ], style=SECTION_CARD_STYLE)],
        ),
    ],
)

# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------
layout = html.Div(
    [
        # Context bar
        html.Div(id="context-bar-container", children=render_context_bar()),

        # Upload area
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

        # Hidden stores and modals
        dcc.Store(id="pending-operation", data=None),
        dcc.Store(id="history-trigger", data=0),
        dcc.Store(id="active-panel", data=None),

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

        # Summary stats overlay
        html.Div(id="summary-overlay", style={"display": "none", "padding": "0 20px"}),

        # Main data table workspace (placeholder table until data loads)
        html.Div(
            id="table-workspace",
            children=dash_table.DataTable(id="table", data=[], columns=[]),
            className="workspace-table",
            style={"padding": "0 20px 20px 20px"},
        ),

        # Save + Undo/Redo row (pre-rendered so IDs exist at startup)
        html.Div(
            id="table-controls",
            children=[
                html.Button(
                    "Save Changes", id="save-button",
                    style={**PRIMARY_BUTTON_STYLE, "padding": "6px 16px"},
                    className="btn-primary-glow",
                ),
                html.Button(
                    "Undo", id="undo-btn", n_clicks=0,
                    style={**GHOST_BUTTON_STYLE, "borderColor": "#e67e22", "color": "#e67e22"},
                ),
                html.Button(
                    "Redo", id="redo-btn", n_clicks=0,
                    style={**GHOST_BUTTON_STYLE, "borderColor": "#3498db", "color": "#3498db"},
                ),
            ],
            style={
                "padding": "8px 20px", "display": "flex",
                "alignItems": "center", "gap": "8px", "flexWrap": "wrap",
            },
        ),

        # Inline cleaning form (pre-rendered, hidden)
        _cleaning_form,

        # Chart builder (pre-rendered, hidden)
        _chart_builder,

        # Chart output area
        dcc.Loading(
            type="circle",
            color=PRIMARY,
            children=html.Div(id="chart-container", style={"padding": "0 20px"}, className="chart-fade-in"),
        ),

        # ML panel (pre-rendered, hidden)
        _ml_panel,

        # ML results area
        dcc.Loading(
            type="circle",
            color=PRIMARY,
            children=html.Div(id="ml-results", style={"padding": "0 20px"}),
        ),

        # Cleaning result alerts
        html.Div(id="cleaning-result", style={"padding": "0 20px"}),

        # Hidden elements for callback compatibility
        html.Div(id="history-log", style={"display": "none"}),
        html.Div(id="output-container-button", style={"display": "none"}),

        # Refresh location
        dcc.Location(id="refresh", refresh=True),
    ],
    style={"backgroundColor": BG_SURFACE, "minHeight": "100vh", "paddingBottom": "40px"},
)
