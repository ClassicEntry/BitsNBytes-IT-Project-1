import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import plotly.express as px


dash.register_page(__name__, path="/data_analysis", name="Data Analysis", order=2)

# -----------------------Page Layout-----------------------

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
        html.Div(id="tabs-content")
    ]
)

@dash.callback(
    Output("tabs-content", "children"),
    Input("tabs", "value")
)
def render_tab_content(tab):
# Assuming this code is inside the render_content function that responds to tab changes

    if tab == "tab-summary":
        try:
            df = pd.read_csv("local_data.csv")
            
            # Generate summary statistics
            summary_stats = df.describe().reset_index()
            
            # Create a table with the summary statistics
            summary_table = dash_table.DataTable(
                data=summary_stats.to_dict('records'),
                columns=[{"name": i, "id": i} for i in summary_stats.columns],
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
                fill_width=False
            )

            # Create a list to hold the graph components
            graphs = []
            
            # Create a histogram for each numeric column
            for col in df.select_dtypes(include=[np.number]).columns:
                graphs.append(
                    dcc.Graph(
                        figure=px.histogram(
                            df, 
                            x=col, 
                            title=f'Distribution of {col}',
                            template='plotly_dark'
                        )
                    )
                )
            
            # Return the summary table and the list of graph components
            return html.Div([summary_table] + graphs)

        except FileNotFoundError:
            return html.Div("Data file not found. Please upload data in the 'Import Data' section.")

    elif tab == "tab-table":
        try:
            df = pd.read_csv("local_data.csv")
            return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

        except FileNotFoundError:
            return html.Div("Data file not found. Please upload data in the 'Import Data' section.")

    elif tab == "tab-charts":
        df = pd.read_csv("local_data.csv")  # Load your dataframe here
        column_options = [{'label': col, 'value': col} for col in df.columns]
        
        return html.Div([
            html.H3("Chart Types"),
            dcc.Dropdown(
                id='chart-type-dropdown',
                options=[
                    {'label': 'Histogram', 'value': 'histogram'},
                    {'label': 'Box Plot', 'value': 'boxplot'},
                    {'label': 'Scatter Plot', 'value': 'scatter'},
                    {'label': 'Line Plot', 'value': 'line'},
                    # more chart types can be added here
                ],
                value=''
            ),
            dcc.Dropdown(
                id='column-dropdown',
                options=column_options,
                value=''  # Default to first column
            ),
            html.Div(id='chart-container')
        ])

# Modify the callback to include the column dropdown value
@dash.callback(
    Output('chart-container', 'children'),
    [Input('chart-type-dropdown', 'value'), Input('column-dropdown', 'value')],
    prevent_initial_call=True
)
def update_chart(chart_type, column_name):
    df = pd.read_csv("local_data.csv")  
    if chart_type == "histogram":
        return dcc.Graph(figure=px.histogram(df, x=column_name))
    elif chart_type == "boxplot":
        return dcc.Graph(figure=px.box(df, y=column_name))
    elif chart_type == "scatter":
        column_options = [{'label': col, 'value': col} for col in df.columns]
        return html.Div([
            html.H3("Scatter plot axes"),
            dcc.Dropdown(
                id='x-axis-dropdown',
                options=column_options,
                value=''  
            ),
            dcc.Dropdown(
                id='y-axis-dropdown',
                options=column_options,
                value=''  
            ),
            html.Div(id='scatter-chart-container')
        ])
    elif chart_type == "line":
        return dcc.Graph(figure=px.line(df, x=df.index, y=column_name))
    else:
        return html.Div("Select a chart type.")

# Callback for updating the scatter chart based on selected x-axis and y-axis
@dash.callback(
    Output('scatter-chart-container', 'children'),
    [Input('x-axis-dropdown', 'value'), Input('y-axis-dropdown', 'value')],
    prevent_initial_call=True
)
def update_scatter_chart(x_axis, y_axis):
    df = pd.read_csv("local_data.csv")  # Load your dataframe here
    fig = px.scatter(df, x=x_axis, y=y_axis)
    return dcc.Graph(figure=fig)


"""import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import os
import atexit


dash.register_page(__name__, path="/data_analysis", name="Data Analysis", order=2)

# -----------------------Page Layout-----------------------

layout = html.Div(
    [
        html.H1("Exploratory data"),
        dcc.Tabs(
            id="Summary",
            value="generate_summary",
            children=[
                dcc.Tab(label="Summary", value="generate_summary"),
                dcc.Tab(label="Table", value="generate_tables"),
                dcc.Tab(label="Charts", value="display_charts"),
            ],
        ),
        html.Div(id="tabs-content-example-graph"),
        dcc.Interval(
            id="interval-component", interval=1 * 1000, n_intervals=0  # in milliseconds
        ),
    ]
)


@dash.callback(
    Output("tabs-content-example-graph", "children"),
    [Input("Summary", "value")]
)
def render_content(tab):
    if tab == "generate_summary":
        try:
            df = pd.read_csv("local_data.csv")
            summary = df.describe().transpose()

            figure = go.Figure(data=[
                go.Table(
                    header=dict(values=list(summary.columns), align='left'),
                    cells=dict(values=[summary[col] for col in summary.columns], align='left')
                )
            ])

            return dcc.Graph(figure=figure)

        except FileNotFoundError:
            return html.Div("Data file not found. Please upload data in the 'Import Data' section.")

"""
'''
@dash.callback(
    Output("tabs-content-example-graph", "children"),
    [Input("Summary", "value"), Input("interval-component", "n_intervals")],
)
def render_content(tab, n):
    file_path = "local_data.csv"
    atexit.register(os.remove, file_path)
    if tab == "generate_summary":
        # Check if the file exists
        if os.path.exists("local_data.csv"):
            # If the file exists, read it
            df = pd.read_csv("local_data.csv")
        else:
            # If the file does not exist, print an error message
            print("The file local_data.csv does not exist.")
            return html.Div()
        # Calculate the summary statistics
        summary = df.describe().transpose()

        # Create a table with the summary statistics
        summary_table = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=list(summary.columns),
                        fill_color="paleturquoise",
                        align="left",
                    ),
                    cells=dict(
                        values=[summary[k].tolist() for k in summary.columns],
                        fill_color="lavender",
                        align="left",
                    ),
                )
            ]
        )

        # Create a bar chart for each column
        bar_charts = []
        for column in df.columns:
            bar_charts.append(
                dcc.Graph(
                    figure={"data": [{"x": df.index, "y": df[column], "type": "bar"}]}
                )
            )

        return html.Div(
            [html.H3("Summary of data"), dcc.Graph(figure=summary_table)] + bar_charts
        )
    elif tab == "tab-2-example-graph":
        return html.Div(
            [
                html.H3("Tab content 2"),
                dcc.Graph(
                    id="graph-2-tabs-dcc",
                    figure={"data": [{"x": [1, 2, 3], "y": [5, 10, 6], "type": "bar"}]},
                ),
            ]
        )
'''