"""
Data Analysis page — layout and tab routing.

This page provides the upload area, tab navigation, and delegates
tab rendering to the individual tab modules.
"""

import os

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc

from pyexploratory.config import (
    GREY,
    LIGHT_GREEN,
    MAX_UPLOAD_SIZE_MB,
    SECTION_CARD_STYLE,
    SELECTED_TAB_STYLE,
    TAB_STYLE,
    UPLOAD_STYLE,
)
from pyexploratory.tabs import charts, machine_learning, summary, table

# Set environment variable to avoid memory leak issue with KMeans
os.environ["OMP_NUM_THREADS"] = "1"

# Register the page with Dash
dash.register_page(
    __name__,
    path="/data_analysis",
    name="Data Analysis",
    order=3,
)

# Tab renderer dispatch
TAB_RENDERERS = {
    "tab-summary": summary.render,
    "tab-table": table.render,
    "tab-charts": charts.render,
    "tab-machine-learning": machine_learning.render,
}

# Page layout
layout = html.Div(
    [
        html.H1("Data Analysis", className="text-light text-center fw-bold fs-1"),
        dcc.Location(id="refresh", refresh=True),
        dbc.Card(
            dcc.Upload(
                id="upload-data",
                children=html.Div(
                    [
                        html.Div(
                            "Upload Your Data",
                            style={
                                "fontSize": "18px",
                                "fontWeight": "600",
                                "color": LIGHT_GREEN,
                                "marginBottom": "8px",
                            },
                        ),
                        html.Div(
                            [
                                "Drag and Drop or ",
                                html.A(
                                    "Browse Files",
                                    style={
                                        "color": "white",
                                        "textDecoration": "underline",
                                    },
                                ),
                            ],
                            style={"color": "#cccccc"},
                        ),
                        html.Small(
                            f"Supports CSV, Excel, JSON — max {MAX_UPLOAD_SIZE_MB}MB",
                            style={"color": "#aaaaaa", "marginTop": "4px"},
                        ),
                    ],
                ),
                style=UPLOAD_STYLE,
                max_size=MAX_UPLOAD_SIZE_MB * 1024 * 1024,
                multiple=True,
            ),
            style=SECTION_CARD_STYLE,
        ),
        dcc.Loading(
            id="loading-upload",
            type="circle",
            color=LIGHT_GREEN,
            children=html.Div(id="output-data-upload"),
        ),
        dcc.Tabs(
            id="tabs",
            value="tab-summary",
            children=[
                dcc.Tab(
                    label="Summary",
                    value="tab-summary",
                    style=TAB_STYLE,
                    selected_style=SELECTED_TAB_STYLE,
                ),
                dcc.Tab(
                    label="Table",
                    value="tab-table",
                    style=TAB_STYLE,
                    selected_style=SELECTED_TAB_STYLE,
                ),
                dcc.Tab(
                    label="Machine Learning",
                    value="tab-machine-learning",
                    style=TAB_STYLE,
                    selected_style=SELECTED_TAB_STYLE,
                ),
                dcc.Tab(
                    label="Charts",
                    value="tab-charts",
                    style=TAB_STYLE,
                    selected_style=SELECTED_TAB_STYLE,
                ),
            ],
            style={
                "width": "100%",
                "margin": "0 auto",
                "padding": "5px",
            },
        ),
        dcc.Loading(
            id="loading-tabs",
            type="circle",
            color="#56D300",
            children=html.Div(id="tabs-content", style={"padding": "20px"}),
        ),
    ],
    style={
        "background-color": GREY,
        "position": "relative",
        "margin": "0px",
        "padding": "10px",
    },
)


@dash.callback(Output("tabs-content", "children"), Input("tabs", "value"))
def render_tab_content(tab):
    """Route to the appropriate tab renderer."""
    renderer = TAB_RENDERERS.get(tab)
    if renderer:
        return renderer()
    return html.Div("Unknown tab.")
