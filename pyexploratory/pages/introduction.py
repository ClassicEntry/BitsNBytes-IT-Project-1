"""
This file contains the code for the Introduction page of the Data Analysis App.
"""

import dash
import dash_bootstrap_components as dbc
from dash import html

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
                            "To get started, click on the Data Analysis Tab in the sidebar and click or drag to import a CSV, Excel, or JSON file. "
                            "Once you have imported the data, you can view your data.",
                            className="mb-4 text-light text-center",
                        ),
                        html.H3(
                            "You can perform data cleaning operations in the Table tab.",
                            className="mb-4 text-light text-center",
                        ),
                        html.H3(
                            "Additionally, explore machine learning capabilities in the Machine Learning tab.",
                            className="mb-4 text-light text-center",
                        ),
                        html.H3(
                            "To download your processed data, use the 'Download Data' button in the sidebar.",
                            className="mb-4 text-light text-center",
                        ),
                    ],
                    style={"padding": "20px"},  # Add padding to the column
                ),
            ],
            style={
                "margin": "0",
                "width": "80%",
            },  # Remove margin and set width to 100% for the row
        ),
    ],
    fluid=True,
    style={
        "height": "100vh",
        "background-color": "#3f3f3f",
        "padding": "1rem",
        "margin": "0",
        "position": "fixed",
    },  # Set background color and padding
)
