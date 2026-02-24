"""
Callbacks for the Charts tab — render charts based on user selections.
"""

import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

from pyexploratory.core.data_store import column_options, read_data


@dash.callback(
    Output("chart-container", "children"),
    [Input("chart-type-dropdown", "value"), Input("column-dropdown", "value")],
    prevent_initial_call=True,
)
def update_chart(chart_type, column_name):
    """Render the selected chart type for the chosen column."""
    try:
        df = read_data()
    except FileNotFoundError:
        return html.Div("Upload data first.")

    if not column_name or column_name not in df.columns:
        return html.Div("Select a valid column.")

    if chart_type == "histogram":
        return dcc.Graph(figure=px.histogram(df, x=column_name, template="seaborn"))

    elif chart_type == "boxplot":
        return dcc.Graph(figure=px.box(df, y=column_name, template="seaborn"))

    elif chart_type == "scatter":
        col_opts = column_options(df)
        return html.Div(
            [
                html.H3("Scatter plot axes"),
                dcc.Dropdown(id="x-axis-dropdown", options=col_opts, value=""),
                dcc.Dropdown(
                    id="y-axis-dropdown",
                    options=col_opts,
                    value="",
                    style={"margin-top": "10px"},
                ),
                html.Div(id="scatter-chart-container"),
            ]
        )

    elif chart_type == "line":
        if pd.api.types.is_numeric_dtype(df[column_name]):
            fig = px.line(
                df,
                x=df.index,
                y=column_name,
                title=f"Line Plot of {column_name}",
                template="seaborn",
            )
        else:
            data = df[column_name].value_counts().reset_index()
            data.columns = [column_name, "count"]
            fig = px.line(
                data,
                x=column_name,
                y="count",
                title=f"Line Plot of {column_name}",
                template="seaborn",
            )
        return dcc.Graph(figure=fig)

    elif chart_type == "bar":
        if pd.api.types.is_numeric_dtype(df[column_name]):
            data = pd.cut(df[column_name], bins=10).value_counts().reset_index()
            data.columns = [column_name, "count"]
            data = data.sort_values(by=column_name)
            data[column_name] = data[column_name].astype(str)
        else:
            data = df[column_name].value_counts().reset_index()
            data.columns = [column_name, "count"]
        return dcc.Graph(
            figure=px.bar(
                data,
                x=column_name,
                y="count",
                title=f"Distribution of {column_name}",
                template="seaborn",
            )
        )

    elif chart_type == "pie":
        if pd.api.types.is_numeric_dtype(df[column_name]):
            return html.Div("Pie chart cannot be created for numeric data.")
        return dcc.Graph(
            figure=px.pie(
                df,
                names=column_name,
                title=f"Pie chart of {column_name}",
                template="seaborn",
            )
        )

    return html.Div("Select a chart type.")


@dash.callback(
    Output("scatter-chart-container", "children"),
    [Input("x-axis-dropdown", "value"), Input("y-axis-dropdown", "value")],
    prevent_initial_call=True,
)
def update_scatter_chart(x_axis, y_axis):
    """Render the scatter plot for the selected axes."""
    if not x_axis or not y_axis:
        return html.Div(
            "Select valid x-axis and y-axis values.", style={"color": "white"}
        )
    df = read_data()
    fig = px.scatter(df, x=x_axis, y=y_axis, template="seaborn")
    return dcc.Graph(figure=fig)
