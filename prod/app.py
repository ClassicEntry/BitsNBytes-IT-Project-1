"""
This file defines the layout and configuration of the Dash application.

It creates a Dash app with a sidebar and the content area. 
The sidebar contains navigation links to different pages of the app.
The content area displays the selected page content.

The app layout is structured using Bootstrap grid system.

To run the app, execute this script.

Author: BitNBytes
"""

from dash import Dash, html, dcc
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

# Set the default template for Plotly Express
px.defaults.template = "plotly_dark"

# Define external CSS stylesheets
external_css = [dbc.themes.BOOTSTRAP]

# Create an instance of the Dash app
app = Dash(
    __name__,
    pages_folder="services",
    use_pages=True,
    external_stylesheets=external_css,
    suppress_callback_exceptions=True,
)

# Styling for sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "0rem",
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#282829",
    "z-index": "1",
}

# Styling for content area
CONTENT_STYLE = {
    "margin-left": "15rem",
    "position": "absolute",
    "top": "0rem",
    "right": "0rem",
    "bottom": "0rem",
    "left": "0rem",
    "padding": "2rem 1rem",
    
}

# Create the sidebar navigation hierarchy
sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(
                    page["name"],
                ),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
)


# Create the content area
content = html.Div(id="page-content", children={}, style=CONTENT_STYLE)

# Configure the app layout hierarchy
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            "PyExploratory",
                            style={
                                "fontSize": 20,
                                "textAlign": "Left",
                                "fontWeight:": "Bold",
                                "color": "#ffffff ",
                                "fontFamily": "Arial Black",
                                "padding": "10px 10px 80px 10px",
                            },
                        ),
                        sidebar,
                    ],
                    xs=4,
                    sm=4,
                    md=2,
                    lg=2,
                    xl=2,
                    xxl=2,
                    style=SIDEBAR_STYLE,
                ),
                dbc.Col(
                    [dash.page_container],
                    xs=8,
                    sm=8,
                    md=10,
                    lg=10,
                    xl=10,
                    xxl=10,
                    style=CONTENT_STYLE,
                ),
            ]
        )
    ],
    fluid=True,
    style={"position": "relative"},
)

if __name__ == "__main__":
    app.run(debug=True)
