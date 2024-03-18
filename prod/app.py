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


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
    # html.Div([
    #     html.H3("Data Cleaning Options"),
    #     dcc.Checklist(
    #         id="cleaning-options",
    #         options=[
    #             {"label": "Remove Duplicates", "value": "remove-duplicates"},
    #             {"label": "Fill NA", "value": "fill-na"},
    #         ],
    #         value=[],
    #     ),
    # ]),

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

    # Summary statistics
    # html.Div(id="summary-statistics"),

    # Export button
    # html.A(
    #     "Export Data",
    #     id="export-link",
    #     download="cleaned_data.csv",
    #     href="",
    #     target="_blank",
    # ),

])

@app.callback(
    Output("table-container", "children"),
    Output("column-dropdown", "options"),
    Output("column-dropdown", "value"),
    Input("upload-data", "contents"),
    Input("upload-data", "filename"),
)
def update_column_dropdown(contents):
    # Read the uploaded data
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(StringIO(decoded.decode("utf-8")))

    # Create the column options
    column_options = [{"label": col, "value": col} for col in df.columns]

    return column_options, df.columns[0]

def update_table(contents, filename):
    """
    Update the table based on the uploaded data.
    """
    if contents is None:
        return "", [], ""
    df = pd.read_csv(io.StringIO(contents))
    table = html.Div([
        html.H3(filename),
        html.Table([
            html.Thead([html.Tr([html.Th(col) for col in df.columns])]),
            html.Tbody([
                html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
                for i in range(min(len(df), 5))
            ]),
        ]),
    ])
    options = [{"label": col, "value": col} for col in df.columns]
    return table, options, df.columns[0]


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

    # Initialize fig as an empty figure
    fig = go.Figure()

    # Create the plot
    if plot_type == "histogram":
        fig = px.histogram(df, x=column, title="Histogram")
    elif plot_type == "boxplot":
        fig = px.box(df, y=column, title="Boxplot")
    elif plot_type == "scatter":
        fig = px.scatter(df, x=df.index, y=column, title="Scatter Plot")

    return dcc.Graph(figure=fig)


# @app.callback(
#     Output("histogram-container", "children"),
#     Input("column-dropdown", "value"),
#     Input("upload-data", "contents"),
# )
# def update_histogram(column, contents):
#     """
#     Update the histogram based on the selected column.
#     """
#     if contents is None:
#         return ""
#     df = pd.read_csv(io.StringIO(contents))
#     if column is None or column not in df.columns:
#         return dcc.Graph(figure={})
#     fig = px.histogram(df, x=column)
#     return dcc.Graph(figure=fig)


# @app.callback(
#     Output("scatter-container", "children"),
#     Input("column-dropdown", "value"),
#     Input("upload-data", "contents"),
# )
# def update_scatter(column, contents):
#     """
#     Update the scatter plot based on the selected column.
#     """
#     if contents is None:
#         return ""
#     df = pd.read_csv(io.StringIO(contents))
#     fig = px.scatter(df, x=column, y=df.columns[-1])
#     return dcc.Graph(figure=fig)


# @app.callback(
#     Output("boxplot-container", "children"),
#     Input("column-dropdown", "value"),
#     Input("upload-data", "contents"),
#     Input("additional-graphs", "value"),
# )
# def update_boxplot(column, contents, additional_graphs):
#     """
#     Update the box plot based on the selected column.
#     """
#     if contents is None or "box-plot" not in additional_graphs:
#         return ""
#     df = pd.read_csv(io.StringIO(contents))
#     if column is None or column not in df.columns:
#         return dcc.Graph(figure={})
#     fig = px.box(df, x=column)
#     return dcc.Graph(figure=fig)


# @app.callback(
#     Output("lineplot-container", "children"),
#     Input("column-dropdown", "value"),
#     Input("upload-data", "contents"),
#     Input("additional-graphs", "value"),
# )
# def update_lineplot(column, contents, additional_graphs):
#     """
#     Update the line plot based on the selected column.
#     """
#     if contents is None or "line-plot" not in additional_graphs:
#         return ""
#     df = pd.read_csv(io.StringIO(contents))
#     if column is None or column not in df.columns:
#         return dcc.Graph(figure={})
#     fig = px.line(df, x=column, y=df.columns[-1])
#     return dcc.Graph(figure=fig)


# def update_summary_statistics(contents):
#     # Read the uploaded data
#     content_type, content_string = contents.split(",")
#     decoded = base64.b64decode(content_string)
#     df = pd.read_csv(StringIO(decoded.decode("utf-8")))

#     # Create the summary statistics
#     summary = df.describe().T

#     return dash_table.DataTable(
#         data=summary.to_dict("records"),
#         columns=[{"name": col, "id": col} for col in summary.columns],
#     )


# @app.callback(
#     Output("export-link", "href"),
#     Input("cleaning-options", "value"),
#     Input("upload-data", "contents"),
#     prevent_initial_call=True,
# )
#
# def export_data(cleaning_options, contents):
#     # Read the uploaded data
#     content_type, content_string = contents.split(",")
#     decoded = base64.b64decode(content_string)
#     df = pd.read_csv(StringIO(decoded.decode("utf-8")))
#
#     # Apply the cleaning options
#     if "remove-duplicates" in cleaning_options:
#         df = df.drop_duplicates()
#     if "fill-na" in cleaning_options:
#         df = df.fillna(0)
#
#     # Export the cleaned data
#     csv_string = df.to_csv(index=False, encoding="utf-8")
#     csv_string = "data:text/csv;charset=utf-8," + csv_string
#     return csv_string


if __name__ == '__main__':
    app.run_server(debug=True)