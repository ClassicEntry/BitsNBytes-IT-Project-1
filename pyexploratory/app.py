"""
PyExploratory — Dash application entry point.

Creates the Dash app with 3-zone layout:
- Sidebar (left, 200px)
- Main workspace (center, fluid)
- Step panel (right, 280px — only on data_analysis page)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from pyexploratory.components.step_panel import render as render_step_panel
from pyexploratory.components.styles import DOWNLOAD_BUTTON_STYLE
from pyexploratory.config import (
    BG_DEEP,
    BG_SURFACE,
    BORDER_COLOR,
    DATA_FILE,
    PRIMARY,
    PRIMARY_BUTTON_STYLE,
    SIDEBAR_STYLE_V2,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)

px.defaults.template = "plotly_dark"

app = Dash(
    __name__,
    pages_folder="pages",
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

# Sidebar
sidebar = html.Div(
    [
        html.Div(
            "PyExploratory",
            style={
                "fontSize": "18px", "fontWeight": "700", "color": TEXT_PRIMARY,
                "fontFamily": "'Inter', sans-serif", "padding": "0 0 40px 0",
            },
        ),
        dcc.Location(id="url", refresh=False),
        dbc.Nav(id="sidebar-nav", vertical=True, pills=True),
        html.Hr(style={"borderColor": BORDER_COLOR, "margin": "20px 0"}),
        dcc.Download(id="download-data"),
        html.Button(
            "Download Data", id="btn-download", n_clicks=0,
            style={**PRIMARY_BUTTON_STYLE, "width": "100%", "marginBottom": "8px"},
            className="btn-primary-glow",
        ),
        dcc.Download(id="download-script"),
        html.Button(
            "Export Script", id="btn-export-script", n_clicks=0,
            style={**PRIMARY_BUTTON_STYLE, "width": "100%", "marginBottom": "8px"},
            className="btn-primary-glow",
        ),
        dcc.Upload(
            id="upload-script",
            children=html.Button(
                "Import Script",
                style={**PRIMARY_BUTTON_STYLE, "width": "100%"},
                className="btn-primary-glow",
            ),
            accept=".py",
            max_size=5 * 1024 * 1024,
        ),
        html.Div(id="import-script-feedback", style={"marginTop": "8px"}),
    ],
    style=SIDEBAR_STYLE_V2,
)

# Layout
app.layout = html.Div(
    [
        sidebar,
        html.Div(id="step-panel-container"),
        html.Div(
            dash.page_container,
            id="main-content",
            style={
                "marginLeft": "200px",
                "minHeight": "100vh",
                "backgroundColor": BG_SURFACE,
            },
        ),
    ],
    style={"backgroundColor": BG_SURFACE, "margin": 0, "padding": 0},
)


@app.callback(Output("sidebar-nav", "children"), [Input("url", "pathname")])
def update_sidebar(pathname):
    return [
        dbc.NavLink(
            [html.Div(page["name"], style={"color": TEXT_PRIMARY, "fontSize": "13px"})],
            href=page["path"],
            active="exact",
            style={
                "backgroundColor": PRIMARY if page["path"] == pathname else "transparent",
                "borderRadius": "6px",
                "margin": "2px 0",
                "padding": "8px 12px",
            },
        )
        for page in dash.page_registry.values()
    ]


@app.callback(
    Output("step-panel-container", "children"),
    Output("main-content", "style"),
    Input("url", "pathname"),
)
def toggle_step_panel(pathname):
    if pathname == "/data_analysis":
        return render_step_panel(), {
            "marginLeft": "200px",
            "marginRight": "280px",
            "minHeight": "100vh",
            "backgroundColor": BG_SURFACE,
        }
    return html.Div(), {
        "marginLeft": "200px",
        "minHeight": "100vh",
        "backgroundColor": BG_SURFACE,
    }


@dash.callback(
    Output("download-data", "data"),
    Input("btn-download", "n_clicks"),
    prevent_initial_call=True,
)
def download_data(n_clicks):
    if n_clicks:
        df = pd.read_csv(DATA_FILE)
        return dcc.send_data_frame(df.to_excel, "mydata.xlsx")


import pyexploratory.callbacks  # noqa: E402, F401

if __name__ == "__main__":
    app.run(debug=True)
