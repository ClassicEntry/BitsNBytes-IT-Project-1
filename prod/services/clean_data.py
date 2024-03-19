import dash
from dash import html, dcc

dash.register_page(__name__, path='/clean_data', name='Clean Data')

#-----------------------Page Layout-----------------------
layout = html.Div([
    html.Br(),
    html.P('Clean Data', className="text-dark text-center fw-bold fs-1"),
    html.Div([
        html.Div([
            html.Label('Select Column'),
            dcc.Dropdown(
                id='select-column',
                options=[
                    {'label': 'Column 1', 'value': 'col1'},
                    {'label': 'Column 2', 'value': 'col2'},
                    {'label': 'Column 3', 'value': 'col3'},],
                value='col1'
            ),
        ], className="col-6"),
        html.Div([
            html.Label('Select Data Type'),
            dcc.Dropdown(
                id='select-data-type',
                options=[
                    {'label': 'String', 'value': 'string'},
                    {'label': 'Integer', 'value': 'integer'},
                    {'label': 'Float', 'value': 'float'},],
                value='string'
            ),
        ], className="col-6"),
    ], className="row"),
    html.Div(id='output-clean-data'),
], className="col-8 mx-auto")