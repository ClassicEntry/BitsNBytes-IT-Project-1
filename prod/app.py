import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import base64
import io
import plotly.express as px

# Create the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("PyExploratory", style={"textAlign": "center"}),
                dcc.Upload(
                    id="upload-data",
                    children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
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
                    multiple=True,  # Allow multiple files to be uploaded
                ),
                dcc.Checklist(
                    id="remove-duplicates",
                    options=[{"label": "Remove duplicates", "value": "RD"}],
                    value=[],
                ),
                dcc.Input(
                    id="fill-na", type="text", placeholder="Fill NA values with..."
                ),
                dcc.Dropdown(
                    id="column-select", style={"width": "50%", "margin": "auto"}
                ),
                dcc.Dropdown(
                    id="plot-type",
                    style={"width": "50%", "margin": "auto"},
                    options=[
                        {"label": "Scatter Plot", "value": "scatter"},
                        {"label": "Histogram", "value": "histogram"},
                        {"label": "Bar Chart", "value": "bar"},
                    ],
                ),
                dcc.Graph(id="data-visualization"),
                dcc.Markdown(id="summary-stats"),
                html.Button(id="export-data", children="Export Data", n_clicks=0),
                dcc.Download(id="download-data"),
            ],
            style={"maxWidth": "800px", "margin": "auto"},
        )
    ]
)


# Define the callback function to update the dropdown options after file upload
@app.callback(
    Output("column-select", "options"),
    [
        Input("upload-data", "contents"),
        Input("remove-duplicates", "value"),
        Input("fill-na", "value"),
    ],
)
def update_dropdown(contents, remove_duplicates, fill_na):
    if contents is not None:
        # Only use the first file
        content_type, content_string = contents[0].split(",")
        decoded = base64.b64decode(content_string)
        data = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

        # Perform data cleaning operations
        if "RD" in remove_duplicates:
            data = data.drop_duplicates()
        if fill_na is not None:
            data = data.fillna(fill_na)

        return [{"label": col, "value": col} for col in data.columns]
    else:
        return []


def update_visualization(
    selected_column, contents, remove_duplicates, fill_na, plot_type
):
    if contents is not None and selected_column is not None:
        # Only use the first file
        content_type, content_string = contents[0].split(",")
        decoded = base64.b64decode(content_string)
        data = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

        # Perform data cleaning operations
        if "RD" in remove_duplicates:
            data = data.drop_duplicates()
        if fill_na is not None:
            data = data.fillna(fill_na)

        if plot_type == "scatter":
            return px.scatter(
                data, x=data.index, y=data[selected_column]
            ).update_layout(title=f"Data Visualization for {selected_column}")
        elif plot_type == "histogram":
            return px.histogram(data, x=data[selected_column]).update_layout(
                title=f"Histogram for {selected_column}"
            )
        elif plot_type == "bar":
            return px.bar(data, x=data.index, y=data[selected_column]).update_layout(
                title=f"Bar Chart for {selected_column}"
            )
    else:
        return {}


# Define the callback function to update the summary statistics
@app.callback(
    Output("summary-stats", "children"),
    [
        Input("upload-data", "contents"),
        Input("remove-duplicates", "value"),
        Input("fill-na", "value"),
    ],
)
def update_summary_stats(contents, remove_duplicates, fill_na):
    if contents is not None:
        # Only use the first file
        content_type, content_string = contents[0].split(",")
        decoded = base64.b64decode(content_string)
        data = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

        # Perform data cleaning operations
        if "RD" in remove_duplicates:
            data = data.drop_duplicates()
        if fill_na is not None:
            data = data.fillna(fill_na)

        return f"Summary Statistics:\n\n{data.describe().to_markdown()}"
    else:
        return "No data loaded yet."


# Add a button to the app layout
html.Button("Download data", id="export-data", n_clicks=0),
dcc.Download(id="download-data"),


# Modify the export_data callback
@app.callback(
    Output("download-data", "data"),
    [Input("export-data", "n_clicks")],
    [
        State("upload-data", "contents"),
        State("remove-duplicates", "value"),
        State("fill-na", "value"),
    ],
    prevent_initial_call=True,
)
def export_data(n_clicks, contents, remove_duplicates, fill_na):
    if n_clicks > 0 and contents is not None:
        # Only use the first file
        content_type, content_string = contents[0].split(",")
        decoded = base64.b64decode(content_string)
        data = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

        # Perform data cleaning operations
        if "RD" in remove_duplicates:
            data = data.drop_duplicates()
        if fill_na is not None:
            data = data.fillna(fill_na)

        return dcc.send_data_frame(data.to_csv, "data.csv", index=False)


if __name__ == "__main__":
    app.run_server(debug=True)
