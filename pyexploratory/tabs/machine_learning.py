"""
Machine Learning tab layout builder.

Renders task selector, variable dropdowns, and ML parameter controls.
"""

import dash_bootstrap_components as dbc
from dash import dcc, html

from pyexploratory.config import (
    DEFAULT_TEST_SIZE,
    DROPDOWN_STYLE,
    KMEANS_DEFAULT_CLUSTERS,
    LIGHT_GREEN,
    SECTION_CARD_STYLE,
    TEXT_MUTED,
)


def render() -> html.Div:
    """Build the Machine Learning tab content."""
    return html.Div(
        [
            # ML Task Selection card
            dbc.Card(
                [
                    html.H5(
                        "Machine Learning Task Selector",
                        style={
                            "color": LIGHT_GREEN,
                            "fontWeight": "600",
                            "marginBottom": "16px",
                        },
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label(
                                        "Task:",
                                        style={"color": TEXT_MUTED, "fontSize": "13px"},
                                    ),
                                    dcc.Dropdown(
                                        id="task-dropdown",
                                        options=[
                                            {"label": "Clustering", "value": "clustering"},
                                            {"label": "Classification", "value": "classification"},
                                        ],
                                        value="",
                                        placeholder="Select a task...",
                                        style={**DROPDOWN_STYLE, "color": "black"},
                                    ),
                                ],
                                md=4,
                            ),
                            dbc.Col(
                                [
                                    html.Label(
                                        "X Variable:",
                                        style={"color": TEXT_MUTED, "fontSize": "13px"},
                                    ),
                                    dcc.Dropdown(
                                        id="x-variable",
                                        value="",
                                        placeholder="Select x-axis...",
                                        style={**DROPDOWN_STYLE, "color": "black"},
                                    ),
                                ],
                                md=4,
                            ),
                            dbc.Col(
                                [
                                    html.Label(
                                        "Y Variable:",
                                        style={"color": TEXT_MUTED, "fontSize": "13px"},
                                    ),
                                    dcc.Dropdown(
                                        id="y-variable",
                                        value="",
                                        placeholder="Select y-axis...",
                                        style={**DROPDOWN_STYLE, "color": "black"},
                                    ),
                                ],
                                md=4,
                            ),
                        ],
                    ),
                ],
                style=SECTION_CARD_STYLE,
            ),
            # Clustering controls card
            html.Div(
                id="clustering-controls",
                style={"display": "none"},
                children=[
                    dbc.Card(
                        [
                            html.H6(
                                "Clustering Parameters",
                                style={"color": LIGHT_GREEN, "fontWeight": "600"},
                            ),
                            html.Label(
                                "Number of Clusters:",
                                style={"color": TEXT_MUTED, "margin": "10px 0 5px 0"},
                            ),
                            dcc.Slider(
                                id="n-clusters",
                                min=2,
                                max=10,
                                step=1,
                                value=KMEANS_DEFAULT_CLUSTERS,
                                marks={i: str(i) for i in range(2, 11)},
                                tooltip={"placement": "bottom"},
                            ),
                        ],
                        style=SECTION_CARD_STYLE,
                    ),
                ],
            ),
            # Classification controls card
            html.Div(
                id="classification-controls",
                style={"display": "none"},
                children=[
                    dbc.Card(
                        [
                            html.H6(
                                "Classification Parameters",
                                style={"color": LIGHT_GREEN, "fontWeight": "600"},
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Label(
                                                "Target Variable:",
                                                style={"color": TEXT_MUTED, "fontSize": "13px"},
                                            ),
                                            dcc.Dropdown(
                                                id="target-variable",
                                                value="",
                                                placeholder="Select target variable...",
                                                style={**DROPDOWN_STYLE, "color": "black"},
                                            ),
                                        ],
                                        md=4,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Label(
                                                "SVM Kernel:",
                                                style={"color": TEXT_MUTED, "fontSize": "13px"},
                                            ),
                                            dcc.Dropdown(
                                                id="svm-kernel",
                                                options=[
                                                    {"label": "Linear", "value": "linear"},
                                                    {"label": "RBF", "value": "rbf"},
                                                    {"label": "Polynomial", "value": "poly"},
                                                    {"label": "Sigmoid", "value": "sigmoid"},
                                                ],
                                                value="linear",
                                                style={**DROPDOWN_STYLE, "color": "black"},
                                            ),
                                        ],
                                        md=4,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Label(
                                                "Test Size:",
                                                style={"color": TEXT_MUTED, "fontSize": "13px"},
                                            ),
                                            dcc.Slider(
                                                id="test-size",
                                                min=0.1,
                                                max=0.5,
                                                step=0.05,
                                                value=DEFAULT_TEST_SIZE,
                                                marks={
                                                    i / 10: f"{i / 10:.1f}"
                                                    for i in range(1, 6)
                                                },
                                                tooltip={"placement": "bottom"},
                                            ),
                                        ],
                                        md=4,
                                    ),
                                ],
                            ),
                        ],
                        style=SECTION_CARD_STYLE,
                    ),
                ],
            ),
            # Results area
            dcc.Loading(
                id="loading-ml",
                type="circle",
                color=LIGHT_GREEN,
                children=html.Div(id="ml-results", style={"minHeight": "200px"}),
            ),
        ]
    )
