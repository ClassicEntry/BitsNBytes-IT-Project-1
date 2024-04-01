import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import dash_table
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path="/Introduction",
    name="Introduction",
    order=1,
)

# -----------------------Page Layout-----------------------

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
                            "You will also be able create a script to generate the dashboard.",
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
    style={"height": "100vh", "background-color": "#4c4d4d"},
)
