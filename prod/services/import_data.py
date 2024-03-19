import dash
from dash import html, dcc

dash.register_page(__name__, path="/import_data", name="Import Data")

# -----------------------Page Layout-----------------------
layout = html.Div(
    [
        html.Br(),
        html.P("Import Data", className="text-dark text-center fw-bold fs-1"),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Select File"),
                        dcc.Upload(
                            id="upload-data",
                            children=html.Div(
                                ["Drag and Drop or ", html.A("Select Files")]
                            ),
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
                            multiple=True,
                        ),
                    ],
                    className="col-6",
                ),
                html.Div(
                    [
                        html.Label("Select Data Source"),
                        dcc.Dropdown(
                            id="data-source",
                            options=[
                                {"label": "CSV", "value": "csv"},
                                {"label": "Excel", "value": "excel"},
                                {"label": "JSON", "value": "JSON"},
                            ],
                            value="csv",
                        ),
                    ],
                    className="col-6",
                ),
            ],
            className="row",
        ),
        html.Div(id="output-data-upload"),
    ],
    className="col-8 mx-auto",
)
