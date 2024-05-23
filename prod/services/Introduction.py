<<<<<<< HEAD
=======
"""
This file contains the code for the Introduction page of the Data Analysis App.
"""

>>>>>>> 7ce10ef287e2b18a419c2c9f26a378b9c9bc282a
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import dash_table
import dash_bootstrap_components as dbc

<<<<<<< HEAD
dash.register_page(
    __name__,
    path="/Introduction",
=======
# Register the page with Dash
dash.register_page(
    __name__,
    path="/",
>>>>>>> 7ce10ef287e2b18a419c2c9f26a378b9c9bc282a
    name="Introduction",
    order=1,
)

<<<<<<< HEAD
# -----------------------Page Layout-----------------------

=======
# Define the layout for the Introduction page
>>>>>>> 7ce10ef287e2b18a419c2c9f26a378b9c9bc282a
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
<<<<<<< HEAD
                        html.H1("Introduction", className="mb-4 text-light"),
                        html.P(
                            "This is a Data Analysis App for exploring the data in a CSV file. "
                            "You can import data, clean data, and visualise data. "
                            "You will also be able to create the dashboard.",
                            className="mb-4 text-light",
                        ),
                        html.P(
                            "To get started, click on the Import Data link in the sidebar to import a CSV file."+
                            "Once you have imported the data, you can click on the Clean Data link to clean the data with the techniques off.",
                            className="text-light",
                        ),
                    ],
                    md=6,
                ),
            ],
            
        ),
    ],
    fluid=True,
    #set backgroud colour to blue
=======
                        html.H1(
                            "Introduction",
                            className="mb-4 text-light text-center fw-bold fs-1",
                        ),
                        html.H3(
                            "PyExploratory is a Data Analysis App written in Python using Dash and Plotly. "
                            "You can import data, clean data, and visualise data. "
                            "You will also be able to create the dashboard.",
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
                ),
            ],
        ),
    ],
    fluid=True,
>>>>>>> 7ce10ef287e2b18a419c2c9f26a378b9c9bc282a
    style={"height": "100vh", "background-color": "#4c4d4d"},
)
