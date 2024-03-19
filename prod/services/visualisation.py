import dash
import io
from dash import Dash, dcc, html, Output, Input, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import base64
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np  
from io import StringIO

dash.register_page(__name__, path='/visualisation', name='Visualisation')

layout = html.Div([
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
            value="",
        ),
    ]),

    # Data visualization
    html.Div(id="plot"),
], className="col-8 mx-auto")

@dash.callback(
    Output('some-output', 'children'),
    Input('stored-data', 'data'),
)
def use_stored_data(data):
    if data is None:
        return dash.no_update
    df = pd.DataFrame(data)


@dash.callback(
    Output("column-dropdown", "options"),
    Output("column-dropdown", "value"),
    Input('stored-data', 'data'),
)
def update_column_dropdown(data):
    if data is None:
        return dash.no_update
    df = pd.DataFrame(data)  # Convert the list of dicts back to a DataFrame
    column_options = [{"label": col, "value": col} for col in df.columns]
    return column_options, df.columns[0]

@dash.callback(
    Output("plot", "children"),
    Input('stored-data', 'data'),
    Input("column-dropdown", "value"),
    Input("plot-type-dropdown", "value"),
    prevent_initial_call=True,
)
def update_plot(data, column, plot_type):
    if data is None:
        return dash.no_update
    df = pd.DataFrame(data)  # Convert the list of dicts back to a DataFrame

    # Create the plot
    if plot_type == "histogram":
        fig = px.histogram(df, x=column, title="Histogram")
    elif plot_type == "boxplot":
        fig = px.box(df, y=column, title="Boxplot")

    return dcc.Graph(figure=fig)