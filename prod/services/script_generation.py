import dash
from dash import html, dcc

dash.register_page(__name__, path="/script_generation", name="Generate Script")

# -----------------------Page Layout-----------------------

layout = html.Div(
    [
        html.Br(),
        html.P("Generate Script", className="text-dark text-center fw-bold fs-1"),
        # Create a div to generate the code used to make the visualisation
        html.Div(
            [
                html.Label("Select Script Type"),
                dcc.Dropdown(
                    id="select-script-type",
                    options=[
                        {"label": "Python", "value": "python"},
                    ],
                    value="python",
                ),
            ],
            className="col-6 mx-auto",
        ),
    ],
    className="col-8 mx-auto",
)
