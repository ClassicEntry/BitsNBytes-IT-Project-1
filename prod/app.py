from dash import Dash, html, dcc
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import atexit
import os

px.defaults.template = "plotly_dark"

external_css = [dbc.themes.BOOTSTRAP]

app = Dash(
    __name__,
    pages_folder="services",
    use_pages=True,
    external_stylesheets=external_css,
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
}
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
# Sidebar
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
right_sidebar = html.Div(
    [
        html.H2("Right Sidebar"),
        html.Hr(),
        html.P("This is a right sidebar."),
        dbc.NavLink("Generate Script", href="/script_generation"),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "right": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#4c4d4d",
    },
)

content = html.Div(id="page-content", children={}, style=CONTENT_STYLE)

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
