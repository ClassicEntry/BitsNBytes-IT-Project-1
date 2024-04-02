"""
This script controls the data analysis within the Dash application.

It creates a Dash app with a sidebar, right sidebar, and content area.
The sidebar contains navigation links to different pages of the app.
The right sidebar includes additional information and a link to generate a script.
The content area displays the selected page content.

The app layout is structured using Bootstrap grid system.

To run the app, execute this script.

Author: BitNBytes
"""

# Import necessary libraries
import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import plotly.express as px

# Register the page with Dash
dash.register_page(__name__, path="/data_analysis", name="Data Analysis", order=2)

# Define the layout of the page
layout = html.Div(
    [
        html.H1("Data Analysis"),
        dcc.Tabs(
            id="tabs",
            value="tab-summary",
            children=[
                dcc.Tab(label="Summary", value="tab-summary"),
                dcc.Tab(label="Table", value="tab-table"),
                dcc.Tab(label="Charts", value="tab-charts"),
            ],
        ),
        html.Div(id="tabs-content"),
    ]
)


@dash.callback(Output("tabs-content", "children"), Input("tabs", "value"))
def render_tab_content(tab):
    """
    Renders the content for the selected tab.

    Parameters:
    - tab (str): The value of the selected tab.

    Returns:
    - html.Div: The rendered content for the selected tab.
    """
    if tab == "tab-summary":
        try:
            # Read the data from the local_data.csv file
            df = pd.read_csv("local_data.csv")

            # Calculate summary statistics for the data
            summary_stats = df.describe().reset_index()

            # Create a DataTable component to display the summary statistics
            summary_table = dash_table.DataTable(
                data=summary_stats.to_dict("records"),
                columns=[{"name": i, "id": i} for i in summary_stats.columns],
                style_cell={"textAlign": "left"},
                style_header={"backgroundColor": "white", "fontWeight": "bold"},
                fill_width=False,
            )

            graphs = []

            # Generate histograms for each numeric column in the data
            for col in df.select_dtypes(include=[np.number]).columns:
                graphs.append(
                    dcc.Graph(
                        figure=px.histogram(
                            df,
                            x=col,
                            title=f"Distribution of {col}",
                            template="plotly_dark",
                        )
                    )
                )

            # Return the summary table and the generated histograms
            return html.Div([summary_table] + graphs)

        except FileNotFoundError:
            # Return an error message if the data file is not found
            return html.Div(
                "Data file not found. Please upload data in the 'Import Data' section."
            )

    elif tab == "tab-table":
        try:
            # Read the data from the local_data.csv file
            df = pd.read_csv("local_data.csv")

            # Create a DataTable component to display the data as a table
            return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

        except FileNotFoundError:
            # Return an error message if the data file is not found
            return html.Div(
                "Data file not found. Please upload data in the 'Import Data' section."
            )

    elif tab == "tab-charts":
        # Read the data from the local_data.csv file
        df = pd.read_csv("local_data.csv")

        # Create options for the column dropdown based on the columns in the data
        column_options = [{"label": col, "value": col} for col in df.columns]

        # Return a Div component with dropdowns for chart type and column selection
        return html.Div(
            [
                html.H3("Chart Types"),
                dcc.Dropdown(
                    id="chart-type-dropdown",
                    options=[
                        {"label": "Histogram", "value": "histogram"},
                        {"label": "Box Plot", "value": "boxplot"},
                        {"label": "Scatter Plot", "value": "scatter"},
                        {"label": "Line Plot", "value": "line"},
                    ],
                    value="",
                ),
                dcc.Dropdown(id="column-dropdown", options=column_options, value=""),
                html.Div(id="chart-container"),
            ]
        )


@dash.callback(
    Output("chart-container", "children"),
    [Input("chart-type-dropdown", "value"), Input("column-dropdown", "value")],
    prevent_initial_call=True,
)
def update_chart(chart_type, column_name):
    """
    Update the chart based on the selected chart type and column name.

    Parameters:
    - chart_type (str): The selected chart type.
    - column_name (str): The selected column name.

    Returns:
    - chart_container (dash.html.Div or dcc.Graph): The updated chart container.
    """
    # Read the data from the local_data.csv file
    df = pd.read_csv("local_data.csv")
    if chart_type == "histogram":
        # Generate a histogram for the selected column
        return dcc.Graph(figure=px.histogram(df, x=column_name))
    elif chart_type == "boxplot":
        # Generate a box plot for the selected column
        return dcc.Graph(figure=px.box(df, y=column_name))
    elif chart_type == "scatter":
        # Create options for the scatter plot axes dropdowns based on the columns in the data
        column_options = [{"label": col, "value": col} for col in df.columns]
        return html.Div(
            [
                html.H3("Scatter plot axes"),
                dcc.Dropdown(id="x-axis-dropdown", options=column_options, value=""),
                dcc.Dropdown(id="y-axis-dropdown", options=column_options, value=""),
                html.Div(id="scatter-chart-container"),
            ]
        )
    elif chart_type == "line":
        # Generate a line plot for the selected column
        return dcc.Graph(figure=px.line(df, x=df.index, y=column_name))
    else:
        # Return an error message if no chart type is selected
        return html.Div("Select a chart type.")


@dash.callback(
    Output("scatter-chart-container", "children"),
    [Input("x-axis-dropdown", "value"), Input("y-axis-dropdown", "value")],
    prevent_initial_call=True,
)
def update_scatter_chart(x_axis, y_axis):
    """
    Update the scatter chart based on the selected x-axis and y-axis values.

    Parameters:
    - x_axis (str): The selected x-axis value.
    - y_axis (str): The selected y-axis value.

    Returns:
    - dash_html_components.Div: The scatter chart container with the updated scatter chart.
    """
    df = pd.read_csv("local_data.csv")
    fig = px.scatter(df, x=x_axis, y=y_axis)
    return dcc.Graph(figure=fig)
