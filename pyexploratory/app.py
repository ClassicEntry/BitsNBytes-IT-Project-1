"""
PyExploratory — Dash application entry point.

Creates the Dash app, defines sidebar/content layout, and registers callbacks.
Run with: python pyexploratory/app.py
"""

import os
import sys

# Ensure project root is on sys.path so `pyexploratory` is importable as a package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from pyexploratory.components.styles import DOWNLOAD_BUTTON_STYLE
from pyexploratory.config import (
    CONTENT_STYLE,
    DARK_GREEN,
    DATA_FILE,
    GREY,
    SIDEBAR_BG,
    SIDEBAR_STYLE,
)

# Set the default template for Plotly Express
px.defaults.template = "plotly_dark"

# Create the Dash app
app = Dash(
    __name__,
    pages_folder="pages",
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

# Sidebar navigation
sidebar = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dbc.Nav(id="sidebar-nav", vertical=True, pills=True),
    ]
)

# App layout
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
                                "fontWeight": "bold",
                                "color": "#ffffff",
                                "fontFamily": "Arial Black",
                                "padding": "10px 10px 80px 10px",
                            },
                        ),
                        sidebar,
                        dcc.Download(id="download-data"),
                        html.Button(
                            "Download Data",
                            id="btn-download",
                            n_clicks=0,
                            style=DOWNLOAD_BUTTON_STYLE,
                        ),
                        dcc.Download(id="download-script"),
                        html.Button(
                            "Export Script",
                            id="btn-export-script",
                            n_clicks=0,
                            style=DOWNLOAD_BUTTON_STYLE,
                        ),
                        dcc.Upload(
                            id="upload-script",
                            children=html.Button(
                                "Import Script",
                                style=DOWNLOAD_BUTTON_STYLE,
                            ),
                            accept=".py",
                            max_size=5 * 1024 * 1024,
                        ),
                        html.Div(id="import-script-feedback"),
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
    style={"position": "relative", "background-color": GREY},
)


# ---------------------------------------------------------------------------
# App-level callbacks (use @app.callback since they need the app instance)
# ---------------------------------------------------------------------------


@app.callback(Output("sidebar-nav", "children"), [Input("url", "pathname")])
def update_sidebar(pathname):
    """Update sidebar navigation links based on current pathname."""
    return [
        dbc.NavLink(
            [html.Div(page["name"], style={"color": "#ffffff"})],
            href=page["path"],
            active="exact",
            style={
                "background-color": (
                    DARK_GREEN if page["path"] == pathname else SIDEBAR_BG
                ),
                "margin": "10px",
            },
        )
        for page in dash.page_registry.values()
    ]


@dash.callback(
    Output("download-data", "data"),
    Input("btn-download", "n_clicks"),
    prevent_initial_call=True,
)
def download_data(n_clicks):
    """Download current data as Excel."""
    if n_clicks:
        df = pd.read_csv(DATA_FILE)
        return dcc.send_data_frame(df.to_excel, "mydata.xlsx")


# Import callback modules to trigger their @dash.callback() registrations
import pyexploratory.callbacks  # noqa: E402, F401

if __name__ == "__main__":
    app.run(debug=True)
