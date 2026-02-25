"""
Callbacks for the Charts tab — render charts based on user selections.

Supports 14 chart types with a multi-control layout.
"""

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output, State

from pyexploratory.config import PRIMARY
from pyexploratory.core import action_log
from pyexploratory.core.data_store import column_options, numeric_column_options, read_data
from pyexploratory.tabs.charts import CHART_CONTROLS

_DARK_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)


# ---------------------------------------------------------------------------
# Populate chart dropdowns when data changes
# ---------------------------------------------------------------------------


@dash.callback(
    [
        Output("chart-x-dropdown", "options"),
        Output("chart-y-dropdown", "options"),
        Output("chart-color-dropdown", "options"),
        Output("chart-size-dropdown", "options"),
    ],
    Input("output-data-upload", "children"),
    Input("cleaning-toast", "is_open"),
)
def populate_chart_dropdowns(*_):
    """Populate chart column dropdowns when data is loaded or modified."""
    try:
        df = read_data()
    except FileNotFoundError:
        return [], [], [], []

    col_opts = column_options(df)
    num_opts = numeric_column_options(df)
    return col_opts, col_opts, col_opts, num_opts


# ---------------------------------------------------------------------------
# Toggle chart controls visibility based on chart type
# ---------------------------------------------------------------------------


@dash.callback(
    [
        Output("chart-x-col", "style"),
        Output("chart-y-col", "style"),
        Output("chart-color-col", "style"),
        Output("chart-size-col", "style"),
    ],
    Input("chart-type-dropdown", "value"),
)
def toggle_chart_controls(chart_type):
    """Show/hide control columns based on what the selected chart needs."""
    show = {"display": "block"}
    hide = {"display": "none"}

    if not chart_type or chart_type not in CHART_CONTROLS:
        return show, show, show, hide

    needs = CHART_CONTROLS[chart_type]
    return (
        show if needs["x"] else hide,
        show if needs["y"] else hide,
        show if needs["color"] else hide,
        show if needs["size"] else hide,
    )


# ---------------------------------------------------------------------------
# Generate chart on button click
# ---------------------------------------------------------------------------


@dash.callback(
    Output("chart-container", "children"),
    Input("generate-chart-btn", "n_clicks"),
    [
        State("chart-type-dropdown", "value"),
        State("chart-x-dropdown", "value"),
        State("chart-y-dropdown", "value"),
        State("chart-color-dropdown", "value"),
        State("chart-size-dropdown", "value"),
    ],
    prevent_initial_call=True,
)
def generate_chart(n_clicks, chart_type, x_col, y_col, color_col, size_col):
    """Route to the appropriate chart builder."""
    if not n_clicks or not chart_type:
        return html.Div("Select a chart type and click Generate.", style={"color": "white"})

    try:
        df = read_data()
    except FileNotFoundError:
        return dbc.Alert("Upload data first.", color="warning")

    # Clear empty strings to None for cleaner logic
    x_col = x_col or None
    y_col = y_col or None
    color_col = color_col if color_col and color_col in df.columns else None
    size_col = size_col if size_col and size_col in df.columns else None

    try:
        builders = {
            "histogram": _build_histogram,
            "boxplot": _build_boxplot,
            "scatter": _build_scatter,
            "line": _build_line,
            "bar": _build_bar,
            "pie": _build_pie,
            "area": _build_area,
            "violin": _build_violin,
            "heatmap": _build_heatmap,
            "pairplot": _build_pairplot,
            "correlation": _build_correlation_matrix,
            "bubble": _build_bubble,
            "treemap": _build_treemap,
            "sunburst": _build_sunburst,
        }
        builder = builders.get(chart_type)
        if not builder:
            return html.Div("Unknown chart type.", style={"color": "white"})
        result = builder(df, x_col, y_col, color_col, size_col)
        action_log.log_action({
            "action_type": "chart",
            "chart_type": chart_type,
            "x_col": x_col,
            "y_col": y_col,
            "color_col": color_col,
            "size_col": size_col,
        })
        return result
    except Exception as e:
        return dbc.Alert(f"Chart error: {e}", color="danger")


# ---------------------------------------------------------------------------
# Private chart builder functions
# ---------------------------------------------------------------------------


def _build_histogram(df, x, y, color, size):
    if not x:
        return _missing("X axis")
    fig = px.histogram(df, x=x, color=color, title=f"Histogram of {x}")
    fig.update_layout(**_DARK_LAYOUT)
    return dcc.Graph(figure=fig)


def _build_boxplot(df, x, y, color, size):
    if not x:
        return _missing("X axis")
    fig = px.box(df, y=x, color=color, title=f"Box Plot of {x}")
    fig.update_layout(**_DARK_LAYOUT)
    return dcc.Graph(figure=fig)


def _build_scatter(df, x, y, color, size):
    if not x or not y:
        return _missing("X and Y axes")
    fig = px.scatter(df, x=x, y=y, color=color, title=f"{x} vs {y}")
    fig.update_traces(marker=dict(line=dict(width=0.5, color="DarkSlateGrey")))
    fig.update_layout(**_DARK_LAYOUT)
    return dcc.Graph(figure=fig)


def _build_line(df, x, y, color, size):
    if not x or not y:
        return _missing("X and Y axes")
    fig = px.line(df, x=x, y=y, title=f"Line: {x} vs {y}")
    fig.update_layout(**_DARK_LAYOUT)
    return dcc.Graph(figure=fig)


def _build_bar(df, x, y, color, size):
    if not x:
        return _missing("X axis")
    if pd.api.types.is_numeric_dtype(df[x]):
        data = pd.cut(df[x], bins=10).value_counts().reset_index()
        data.columns = [x, "count"]
        data = data.sort_values(by=x)
        data[x] = data[x].astype(str)
    else:
        data = df[x].value_counts().reset_index()
        data.columns = [x, "count"]
    fig = px.bar(data, x=x, y="count", color=color if color and color in data.columns else None,
                 title=f"Distribution of {x}")
    fig.update_layout(**_DARK_LAYOUT)
    return dcc.Graph(figure=fig)


def _build_pie(df, x, y, color, size):
    if not x:
        return _missing("X axis (category column)")
    if pd.api.types.is_numeric_dtype(df[x]):
        return dbc.Alert("Pie chart needs a categorical column.", color="warning")
    fig = px.pie(df, names=x, title=f"Pie Chart of {x}")
    fig.update_layout(**_DARK_LAYOUT)
    return dcc.Graph(figure=fig)


def _build_area(df, x, y, color, size):
    if not x or not y:
        return _missing("X and Y axes")
    fig = px.area(df, x=x, y=y, color=color, title=f"Area: {x} vs {y}")
    fig.update_layout(**_DARK_LAYOUT)
    return dcc.Graph(figure=fig)


def _build_violin(df, x, y, color, size):
    if not x or not y:
        return _missing("X and Y axes")
    fig = px.violin(df, x=x, y=y, box=True, title=f"Violin: {y} by {x}")
    fig.update_layout(**_DARK_LAYOUT)
    return dcc.Graph(figure=fig)


def _build_heatmap(df, x, y, color, size):
    """Correlation heatmap of all numeric columns."""
    num_df = df.select_dtypes("number")
    if num_df.empty or len(num_df.columns) < 2:
        return dbc.Alert("Need at least 2 numeric columns for a heatmap.", color="warning")
    corr = num_df.corr()
    fig = go.Figure(
        go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.columns.tolist(),
            colorscale="RdBu_r",
            zmin=-1,
            zmax=1,
            text=np.round(corr.values, 2),
            texttemplate="%{text}",
        )
    )
    fig.update_layout(title="Correlation Heatmap", **_DARK_LAYOUT)
    return dcc.Graph(figure=fig)


def _build_pairplot(df, x, y, color, size):
    """Scatter matrix of first 6 numeric columns."""
    num_cols = df.select_dtypes("number").columns.tolist()[:6]
    if len(num_cols) < 2:
        return dbc.Alert("Need at least 2 numeric columns for a pair plot.", color="warning")
    fig = px.scatter_matrix(
        df,
        dimensions=num_cols,
        color=color,
        title="Pair Plot",
    )
    fig.update_traces(diagonal_visible=True, marker=dict(size=3))
    fig.update_layout(height=700, **_DARK_LAYOUT)
    return dcc.Graph(figure=fig)


def _build_correlation_matrix(df, x, y, color, size):
    """Correlation matrix with Viridis colorscale and 3-decimal text."""
    num_df = df.select_dtypes("number")
    if num_df.empty or len(num_df.columns) < 2:
        return dbc.Alert("Need at least 2 numeric columns.", color="warning")
    corr = num_df.corr()
    fig = go.Figure(
        go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.columns.tolist(),
            colorscale="Viridis",
            text=np.round(corr.values, 3),
            texttemplate="%{text}",
        )
    )
    fig.update_layout(title="Correlation Matrix", **_DARK_LAYOUT)
    return dcc.Graph(figure=fig)


def _build_bubble(df, x, y, color, size):
    if not x or not y:
        return _missing("X and Y axes")
    fig = px.scatter(
        df, x=x, y=y, color=color, size=size,
        title=f"Bubble: {x} vs {y}",
    )
    fig.update_layout(**_DARK_LAYOUT)
    return dcc.Graph(figure=fig)


def _build_treemap(df, x, y, color, size):
    """Treemap using x as path and y as values (or count)."""
    if not x:
        return _missing("X axis (category column)")
    if y and pd.api.types.is_numeric_dtype(df[y]):
        agg = df.groupby(x)[y].sum().reset_index()
        fig = px.treemap(agg, path=[x], values=y, title=f"Treemap: {x} by {y}")
    else:
        counts = df[x].value_counts().reset_index()
        counts.columns = [x, "count"]
        fig = px.treemap(counts, path=[x], values="count", title=f"Treemap: {x}")
    fig.update_layout(**_DARK_LAYOUT)
    return dcc.Graph(figure=fig)


def _build_sunburst(df, x, y, color, size):
    """Sunburst using x as path and y as values (or count)."""
    if not x:
        return _missing("X axis (category column)")
    if y and pd.api.types.is_numeric_dtype(df[y]):
        agg = df.groupby(x)[y].sum().reset_index()
        fig = px.sunburst(agg, path=[x], values=y, title=f"Sunburst: {x} by {y}")
    else:
        counts = df[x].value_counts().reset_index()
        counts.columns = [x, "count"]
        fig = px.sunburst(counts, path=[x], values="count", title=f"Sunburst: {x}")
    fig.update_layout(**_DARK_LAYOUT)
    return dcc.Graph(figure=fig)


def _missing(field: str) -> html.Div:
    """Return a prompt to select the required field."""
    return html.Div(f"Please select {field}.", style={"color": "#aaaaaa", "padding": "20px"})
