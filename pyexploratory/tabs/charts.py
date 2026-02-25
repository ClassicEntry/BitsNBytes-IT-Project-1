"""
Charts tab layout builder.

Renders multi-control chart selection with 14 chart types.
"""

import dash_bootstrap_components as dbc
from dash import dcc, html

from pyexploratory.config import DROPDOWN_STYLE, LIGHT_GREEN, SECTION_CARD_STYLE, TEXT_MUTED
from pyexploratory.core.data_store import column_options, numeric_column_options, read_data

CHART_TYPE_OPTIONS = [
    {"label": "Histogram", "value": "histogram"},
    {"label": "Box Plot", "value": "boxplot"},
    {"label": "Scatter Plot", "value": "scatter"},
    {"label": "Line Plot", "value": "line"},
    {"label": "Bar Chart", "value": "bar"},
    {"label": "Pie Chart", "value": "pie"},
    {"label": "Area Chart", "value": "area"},
    {"label": "Violin Plot", "value": "violin"},
    {"label": "Heatmap (Correlation)", "value": "heatmap"},
    {"label": "Pair Plot", "value": "pairplot"},
    {"label": "Correlation Matrix", "value": "correlation"},
    {"label": "Bubble Chart", "value": "bubble"},
    {"label": "Treemap", "value": "treemap"},
    {"label": "Sunburst", "value": "sunburst"},
]

# Which controls each chart type needs (for show/hide logic)
CHART_CONTROLS = {
    "histogram":   {"x": True,  "y": False, "color": True,  "size": False},
    "boxplot":     {"x": True,  "y": False, "color": True,  "size": False},
    "scatter":     {"x": True,  "y": True,  "color": True,  "size": False},
    "line":        {"x": True,  "y": True,  "color": False, "size": False},
    "bar":         {"x": True,  "y": False, "color": True,  "size": False},
    "pie":         {"x": True,  "y": False, "color": False, "size": False},
    "area":        {"x": True,  "y": True,  "color": True,  "size": False},
    "violin":      {"x": True,  "y": True,  "color": False, "size": False},
    "heatmap":     {"x": False, "y": False, "color": False, "size": False},
    "pairplot":    {"x": False, "y": False, "color": True,  "size": False},
    "correlation": {"x": False, "y": False, "color": False, "size": False},
    "bubble":      {"x": True,  "y": True,  "color": True,  "size": True},
    "treemap":     {"x": True,  "y": True,  "color": False, "size": False},
    "sunburst":    {"x": True,  "y": True,  "color": False, "size": False},
}


def render() -> html.Div:
    """Build the Charts tab content."""
    try:
        df = read_data()
    except FileNotFoundError:
        df = None

    col_opts = column_options(df) if df is not None else []
    num_opts = numeric_column_options(df) if df is not None else []

    return html.Div(
        [
            # Chart controls card
            dbc.Card(
                [
                    html.H5(
                        "Chart Builder",
                        style={
                            "color": LIGHT_GREEN,
                            "fontWeight": "600",
                            "marginBottom": "16px",
                        },
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label(
                                        "Chart Type:",
                                        style={"color": TEXT_MUTED, "fontSize": "13px"},
                                    ),
                                    dcc.Dropdown(
                                        id="chart-type-dropdown",
                                        options=CHART_TYPE_OPTIONS,
                                        value="",
                                        placeholder="Select a chart type...",
                                        style={**DROPDOWN_STYLE, "color": "black"},
                                    ),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                id="chart-x-col",
                                children=[
                                    html.Label(
                                        "X Axis:",
                                        style={"color": TEXT_MUTED, "fontSize": "13px"},
                                    ),
                                    dcc.Dropdown(
                                        id="chart-x-dropdown",
                                        options=col_opts,
                                        value="",
                                        placeholder="Select column...",
                                        style={**DROPDOWN_STYLE, "color": "black"},
                                    ),
                                ],
                                md=2,
                            ),
                            dbc.Col(
                                id="chart-y-col",
                                children=[
                                    html.Label(
                                        "Y Axis:",
                                        style={"color": TEXT_MUTED, "fontSize": "13px"},
                                    ),
                                    dcc.Dropdown(
                                        id="chart-y-dropdown",
                                        options=col_opts,
                                        value="",
                                        placeholder="Select column...",
                                        style={**DROPDOWN_STYLE, "color": "black"},
                                    ),
                                ],
                                md=2,
                            ),
                            dbc.Col(
                                id="chart-color-col",
                                children=[
                                    html.Label(
                                        "Color By:",
                                        style={"color": TEXT_MUTED, "fontSize": "13px"},
                                    ),
                                    dcc.Dropdown(
                                        id="chart-color-dropdown",
                                        options=col_opts,
                                        value="",
                                        placeholder="(Optional)",
                                        style={**DROPDOWN_STYLE, "color": "black"},
                                    ),
                                ],
                                md=2,
                            ),
                            dbc.Col(
                                id="chart-size-col",
                                style={"display": "none"},
                                children=[
                                    html.Label(
                                        "Size By:",
                                        style={"color": TEXT_MUTED, "fontSize": "13px"},
                                    ),
                                    dcc.Dropdown(
                                        id="chart-size-dropdown",
                                        options=num_opts,
                                        value="",
                                        placeholder="(Optional)",
                                        style={**DROPDOWN_STYLE, "color": "black"},
                                    ),
                                ],
                                md=2,
                            ),
                            dbc.Col(
                                [
                                    html.Label(
                                        "\u00A0",
                                        style={"fontSize": "13px"},
                                    ),
                                    html.Button(
                                        "Generate Chart",
                                        id="generate-chart-btn",
                                        n_clicks=0,
                                        style={
                                            "backgroundColor": LIGHT_GREEN,
                                            "color": "white",
                                            "borderRadius": "10px",
                                            "border": "none",
                                            "padding": "8px 20px",
                                            "fontWeight": "600",
                                            "width": "100%",
                                            "cursor": "pointer",
                                        },
                                    ),
                                ],
                                md=1,
                                style={"display": "flex", "flexDirection": "column"},
                            ),
                        ],
                    ),
                ],
                style=SECTION_CARD_STYLE,
            ),
            # Chart output
            dcc.Loading(
                id="loading-chart",
                type="circle",
                color=LIGHT_GREEN,
                children=html.Div(
                    id="chart-container",
                    style={"minHeight": "400px", "padding": "10px"},
                ),
            ),
        ]
    )
