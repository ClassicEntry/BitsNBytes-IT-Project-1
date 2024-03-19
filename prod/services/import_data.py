import dash
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
import io

dash.register_page(__name__, path='/import_data', name='Import Data')

#-----------------------Page Layout-----------------------
layout = html.Div([
    html.Label('Select Data Source'),
    dcc.Dropdown(
        id='data-source',
        options=[
            {'label': 'CSV', 'value': 'csv'},
            {'label': 'Excel', 'value': 'excel'},
            {'label': 'JSON', 'value': 'JSON'},
        ],
        value='csv'
    ),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', 'Click to Select a File']),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Div(id='output-data-upload'),
], className="col-8 mx-auto")

# Modify your upload callback to store the uploaded data
@dash.callback(
    Output('stored-data', 'data'),  # Output to the dcc.Store component
    Input('upload-data', 'contents'),
)
def store_uploaded_data(contents):
    if contents is None:
        return dash.no_update
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    return df.to_dict('records')  # Convert the DataFrame to a list of dicts