"""
This file contains the code for the Introduction page of the Data Analysis App.
"""

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import dash_table
import dash_bootstrap_components as dbc

# Register the page with Dash
dash.register_page(
    __name__,
    path="/",
    name="Introduction",
    order=1,
)

# Define the layout for the Introduction page
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            "Introduction",
                            className="mb-4 text-light text-center fw-bold fs-1",
                        ),
                        html.H3(
                            "This is a Data Analysis App for exploring the data in a CSV file. "
                            "You can import data, clean data, and visualise data. "
                            "You will also be able to create the dashboard.",
                            className="mb-4 text-light text-center",
                        ),
                        html.H3(
                            "To get started, click on the Data Analysis tab in the sidebar and click on the Table tab to import a CSV or Excel file. "
                            + "Once you have imported the data, you can click on the Summary Tab to clean the data with the techniques off.",
                            className="mb-4 text-light text-center",
                        ),
                    ],
                ),
            ],
        ),
    ],
    fluid=True,
    style={"height": "100vh", "background-color": "#4c4d4d"},
)
