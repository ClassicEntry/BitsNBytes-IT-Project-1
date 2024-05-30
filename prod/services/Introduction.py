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
                            "PyExploratory is a Data Analysis App written in Python using Dash and Plotly. "
                            "You can import data, clean data, and visualise data. ",
                            className="mb-4 text-light text-center",
                        ),
                        html.H3(
                            "To get started, click on the Import Data tab in the sidebar and click or drag to import a CSV, Excel or JSON file. "
                            + "Once you have imported the data, you can click on Data Analysis Tab to view your data.",
                            "You can perform data cleaning operations in the Import Data tab. ",
                            className="mb-4 text-light text-center",
                        ),
                        html.H3(
                            "You can perform machine learning operations on your data in the Machine Learning tab.",
                            "",
                            className="mb-4 text-light text-center",
                        ),
                    ],
                    style={"padding": "20px"},  # Add padding to the column
                ),
            ],
            style={"margin": "0", "width": "80%"},  # Remove margin and set width to 100% for the row
        ),
    ],
    fluid=True,
    style={"height": "100vh", "background-color": "#4c4d4d", "padding": "1rem", "margin": "0", "position": "fixed"},  # Remove padding and margin from the container
)