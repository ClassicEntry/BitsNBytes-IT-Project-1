import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import os



dash.register_page(__name__, path="/clean_data", name="Clean Data", order= 2)

# -----------------------Page Layout-----------------------

layout = html.Div([
    html.H1('Exploratory data'),
    dcc.Tabs(id="Summary-example", value='generate_summary', children=[
        dcc.Tab(label='Summary', value='generate_summary'),
        dcc.Tab(label='Table', value='generate_tables'),
        dcc.Tab(label='Charts', value='display_charts'),
    ]),
    html.Div(id='tabs-content-example-graph'),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )

])

@dash.callback(Output('tabs-content-example-graph', 'children'),
              [Input('Summary-example', 'value'),
               Input('interval-component', 'n_intervals')])


def render_content(tab, n):
    if tab == 'generate_summary':
        # Check if the file exists
        if os.path.exists('local_data.csv'):
            # If the file exists, read it
            df = pd.read_csv('local_data.csv')
        else:
            # If the file does not exist, print an error message
            print('The file local_data.csv does not exist.')
            return html.Div()
        # Calculate the summary statistics
        summary = df.describe().transpose()

        # Create a table with the summary statistics
        summary_table = go.Figure(data=[go.Table(
            header=dict(values=list(summary.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[summary[k].tolist() for k in summary.columns],
                       fill_color='lavender',
                       align='left'))
        ])

        # Create a bar chart for each column
        bar_charts = []
        for column in df.columns:
            bar_charts.append(dcc.Graph(
                figure={
                    'data': [{
                        'x': df.index,
                        'y': df[column],
                        'type': 'bar'
                    }]
                }
            ))

        return html.Div([
            html.H3('Summary of data'),
            dcc.Graph(figure=summary_table)
        ] + bar_charts)
    elif tab == 'tab-2-example-graph':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs-dcc',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])