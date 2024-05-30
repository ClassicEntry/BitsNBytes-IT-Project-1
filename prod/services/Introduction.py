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
                        html.H1("Introduction", className="mb-4 text-light"),
                        html.P(
                            "This is a Data Analysis App for exploring the data in a CSV file. "
                            "You can import data, clean data, and visualise data. "
                            "You will also be able to create the dashboard.",
                            className="mb-4 text-light",
                        ),
                        html.P(
                            "To get started, click on the Import Data link in the sidebar to import a CSV file."
                            + "Once you have imported the data, you can click on the Clean Data link to clean the data with the techniques off.",
                            className="text-light",
                        ),
                    ],
                    md=6,
                ),
            ],
        ),
    ],
    fluid=True,
    # Set background color
    style={"height": "100vh", "background-color": "#4c4d4d"},
)
