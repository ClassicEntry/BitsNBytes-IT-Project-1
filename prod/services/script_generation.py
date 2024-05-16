"""
This file provides functionality for generating scripts using Dash.

It defines a Dash page for script generation, including a dropdown to select the script type.
"""

import dash
from dash import html, dcc

dash.register_page(__name__, path="/script_generation", name="Generate Script")

layout = html.Div(
    [
        html.Br(),
        html.H1("Generate Script", className="text-dark text-center fw-bold fs-1"),
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
