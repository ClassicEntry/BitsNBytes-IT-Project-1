"""
Charts tab layout builder.

Renders chart type and column selection dropdowns with a chart container.
"""

from dash import dcc, html

from pyexploratory.config import DROPDOWN_STYLE
from pyexploratory.core.data_store import column_options, read_data

CHART_TYPE_OPTIONS = [
    {"label": "Histogram", "value": "histogram"},
    {"label": "Box Plot", "value": "boxplot"},
    {"label": "Scatter Plot", "value": "scatter"},
    {"label": "Line Plot", "value": "line"},
    {"label": "Bar Chart", "value": "bar"},
    {"label": "Pie Chart", "value": "pie"},
]


def render() -> html.Div:
    """Build the Charts tab content."""
    try:
        df = read_data()
    except FileNotFoundError:
        df = None

    col_options = column_options(df) if df is not None else []

    return html.Div(
        [
            html.H3("Chart Types", style={"color": "white"}),
            dcc.Dropdown(
                id="chart-type-dropdown",
                options=CHART_TYPE_OPTIONS,
                value="",
                placeholder="Select a chart type...",
                style=DROPDOWN_STYLE,
            ),
            dcc.Dropdown(
                id="column-dropdown",
                options=col_options,
                value="",
                placeholder="Select a column...",
                style=DROPDOWN_STYLE,
            ),
            dcc.Loading(
                id="loading-chart",
                type="circle",
                color="#56D300",
                children=html.Div(
                    id="chart-container",
                    style={"height": "60vh"},
                ),
            ),
        ]
    )
