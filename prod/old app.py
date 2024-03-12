"""
This script defines a Dash application for data exploration and visualization.
Users can upload CSV files, perform data cleaning operations, and generate various types of plots.

The main components of the application include:
- Upload component: Allows users to upload CSV files.
- Data cleaning options: Users can choose to remove duplicates and fill NA values.
- Dropdowns: Users can select a column and a plot type.
- Data visualization: Displays the selected plot based on the uploaded data and user selections.
- Summary statistics: Shows the summary statistics of the uploaded data.
- Export button: Allows users to download the cleaned data as a CSV file.

To run the application, execute this script. The application will run on a local server in debug mode.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from io import StringIO
import base64
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_table
import numpy as np
import os
from dash.exceptions import PreventUpdate

# Create a Dash application
app = dash.Dash(__name__)

# Define the layout of the application

app.layout = html.Div([

    # Title
    html.H1("Data Exploration and Visualization"),

    # Upload component
    dcc.Upload(
        id="upload-data",
        children=html.Div(["Drag and drop or click to select a file to upload."]),
        style={
            "width": "100%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px",
        },
        multiple=False,
    ),

    # Data cleaning options
    html.Div([
        html.H3("Data Cleaning Options"),
        dcc.Checklist(
            id="cleaning-options",
            options=[
                {"label": "Remove Duplicates", "value": "remove-duplicates"},
                {"label": "Fill NA", "value": "fill-na"},
            ],
            value=[],
        ),
    ]),

    # Dropdowns
    html.Div([
        html.H3("Select a Column"),
        dcc.Dropdown(id="column-dropdown"),
        html.H3("Select a Plot Type"),
        dcc.Dropdown(
            id="plot-type-dropdown",
            options=[
                {"label": "Histogram", "value": "histogram"},
                {"label": "Boxplot", "value": "boxplot"},
                {"label": "Scatter Plot", "value": "scatter"},
            ],
            value="histogram",
        ),
    ]),

    # Data visualization
    html.Div(id="plot"),

    # Summary statistics
    html.Div(id="summary-statistics"),

    # Export button
    html.A(
        "Export Data",
        id="export-link",
        download="cleaned_data.csv",
        href="",
        target="_blank",
    ),

])


# Callbacks
@app.callback(
    Output("column-dropdown", "options"),
    Output("column-dropdown", "value"),
    Input("upload-data", "contents"),
    prevent_initial_call=True,
)
def update_column_dropdown(contents):
    # Read the uploaded data
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(StringIO(decoded.decode("utf-8")))

    # Create the column options
    column_options = [{"label": col, "value": col} for col in df.columns]

    return column_options, df.columns[0]


@app.callback(
    Output("plot", "children"),
    Input("upload-data", "contents"),
    Input("column-dropdown", "value"),
    Input("plot-type-dropdown", "value"),
    prevent_initial_call=True,
)

def update_plot(contents, column, plot_type):
    # Read the uploaded data
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(StringIO(decoded.decode("utf-8")))

    # Create the plot
    if plot_type == "histogram":
        fig = px.histogram(df, x=column, title="Histogram")
    elif plot_type == "boxplot":
        fig = px.box(df, y=column, title="Boxplot")
    elif plot_type == "scatter":
        fig = px.scatter(df, x=df.index, y=column, title="Scatter Plot")

    return dcc.Graph(figure=fig)


@app.callback(
    Output("summary-statistics", "children"),
    Input("upload-data", "contents"),
    prevent_initial_call=True,
)

def update_summary_statistics(contents):
    # Read the uploaded data
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(StringIO(decoded.decode("utf-8")))

    # Create the summary statistics
    summary = df.describe().T

    return dash_table.DataTable(
        data=summary.to_dict("records"),
        columns=[{"name": col, "id": col} for col in summary.columns],
    )


@app.callback(
    Output("export-link", "href"),
    Input("cleaning-options", "value"),
    Input("upload-data", "contents"),
    prevent_initial_call=True,
)

def export_data(cleaning_options, contents):
    # Read the uploaded data
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(StringIO(decoded.decode("utf-8")))

    # Apply the cleaning options
    if "remove-duplicates" in cleaning_options:
        df = df.drop_duplicates()
    if "fill-na" in cleaning_options:
        df = df.fillna(0)

    # Export the cleaned data
    csv_string = df.to_csv(index=False, encoding="utf-8")
    csv_string = "data:text/csv;charset=utf-8," + csv_string
    return csv_string


# Run the application
if __name__ == "__main__":
    app.run_server(debug=True)
