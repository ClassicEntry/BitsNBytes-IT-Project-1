"""
Machine Learning tab layout builder.

Renders task selector, variable dropdowns, and ML parameter controls
for Clustering, Classification (SVM), Decision Tree, Random Forest,
and Linear Regression.
"""

import dash_bootstrap_components as dbc
from dash import dcc, html

from pyexploratory.config import (
    DEFAULT_TEST_SIZE,
    DT_DEFAULT_MAX_DEPTH,
    DROPDOWN_STYLE,
    KMEANS_DEFAULT_CLUSTERS,
    LIGHT_GREEN,
    RF_DEFAULT_ESTIMATORS,
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
                                            {"label": "Classification (SVM)", "value": "classification"},
                                            {"label": "Decision Tree", "value": "decision_tree"},
                                            {"label": "Random Forest", "value": "random_forest"},
                                            {"label": "Linear Regression", "value": "regression"},
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
            # Clustering controls
            html.Div(
                id="clustering-controls",
                style={"display": "none"},
                children=[
                    dbc.Card(
                        [
                            html.H6("Clustering Parameters", style={"color": LIGHT_GREEN, "fontWeight": "600"}),
                            html.Label("Number of Clusters:", style={"color": TEXT_MUTED, "margin": "10px 0 5px 0"}),
                            dcc.Slider(
                                id="n-clusters", min=2, max=10, step=1,
                                value=KMEANS_DEFAULT_CLUSTERS,
                                marks={i: str(i) for i in range(2, 11)},
                                tooltip={"placement": "bottom"},
                            ),
                        ],
                        style=SECTION_CARD_STYLE,
                    ),
                ],
            ),
            # Classification (SVM) controls
            html.Div(
                id="classification-controls",
                style={"display": "none"},
                children=[
                    dbc.Card(
                        [
                            html.H6("SVM Classification Parameters", style={"color": LIGHT_GREEN, "fontWeight": "600"}),
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Target Variable:", style={"color": TEXT_MUTED, "fontSize": "13px"}),
                                    dcc.Dropdown(
                                        id="target-variable", value="",
                                        placeholder="Select target variable...",
                                        style={**DROPDOWN_STYLE, "color": "black"},
                                    ),
                                ], md=4),
                                dbc.Col([
                                    html.Label("SVM Kernel:", style={"color": TEXT_MUTED, "fontSize": "13px"}),
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
                                ], md=4),
                                dbc.Col([
                                    html.Label("Test Size:", style={"color": TEXT_MUTED, "fontSize": "13px"}),
                                    dcc.Slider(
                                        id="test-size", min=0.1, max=0.5, step=0.05,
                                        value=DEFAULT_TEST_SIZE,
                                        marks={i / 10: f"{i / 10:.1f}" for i in range(1, 6)},
                                        tooltip={"placement": "bottom"},
                                    ),
                                ], md=4),
                            ]),
                        ],
                        style=SECTION_CARD_STYLE,
                    ),
                ],
            ),
            # Decision Tree controls
            html.Div(
                id="decision-tree-controls",
                style={"display": "none"},
                children=[
                    dbc.Card(
                        [
                            html.H6("Decision Tree Parameters", style={"color": LIGHT_GREEN, "fontWeight": "600"}),
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Target Variable:", style={"color": TEXT_MUTED, "fontSize": "13px"}),
                                    dcc.Dropdown(
                                        id="dt-target-variable", value="",
                                        placeholder="Select target variable...",
                                        style={**DROPDOWN_STYLE, "color": "black"},
                                    ),
                                ], md=4),
                                dbc.Col([
                                    html.Label("Max Depth:", style={"color": TEXT_MUTED, "fontSize": "13px"}),
                                    dcc.Slider(
                                        id="dt-max-depth", min=1, max=20, step=1,
                                        value=DT_DEFAULT_MAX_DEPTH,
                                        marks={i: str(i) for i in [1, 5, 10, 15, 20]},
                                        tooltip={"placement": "bottom"},
                                    ),
                                ], md=4),
                                dbc.Col([
                                    html.Label("Test Size:", style={"color": TEXT_MUTED, "fontSize": "13px"}),
                                    dcc.Slider(
                                        id="dt-test-size", min=0.1, max=0.5, step=0.05,
                                        value=DEFAULT_TEST_SIZE,
                                        marks={i / 10: f"{i / 10:.1f}" for i in range(1, 6)},
                                        tooltip={"placement": "bottom"},
                                    ),
                                ], md=4),
                            ]),
                        ],
                        style=SECTION_CARD_STYLE,
                    ),
                ],
            ),
            # Random Forest controls
            html.Div(
                id="random-forest-controls",
                style={"display": "none"},
                children=[
                    dbc.Card(
                        [
                            html.H6("Random Forest Parameters", style={"color": LIGHT_GREEN, "fontWeight": "600"}),
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Target Variable:", style={"color": TEXT_MUTED, "fontSize": "13px"}),
                                    dcc.Dropdown(
                                        id="rf-target-variable", value="",
                                        placeholder="Select target variable...",
                                        style={**DROPDOWN_STYLE, "color": "black"},
                                    ),
                                ], md=3),
                                dbc.Col([
                                    html.Label("Estimators:", style={"color": TEXT_MUTED, "fontSize": "13px"}),
                                    dcc.Slider(
                                        id="rf-n-estimators", min=10, max=500, step=10,
                                        value=RF_DEFAULT_ESTIMATORS,
                                        marks={i: str(i) for i in [10, 100, 200, 300, 500]},
                                        tooltip={"placement": "bottom"},
                                    ),
                                ], md=3),
                                dbc.Col([
                                    html.Label("Max Depth:", style={"color": TEXT_MUTED, "fontSize": "13px"}),
                                    dcc.Slider(
                                        id="rf-max-depth", min=1, max=20, step=1,
                                        value=DT_DEFAULT_MAX_DEPTH,
                                        marks={i: str(i) for i in [1, 5, 10, 15, 20]},
                                        tooltip={"placement": "bottom"},
                                    ),
                                ], md=3),
                                dbc.Col([
                                    html.Label("Test Size:", style={"color": TEXT_MUTED, "fontSize": "13px"}),
                                    dcc.Slider(
                                        id="rf-test-size", min=0.1, max=0.5, step=0.05,
                                        value=DEFAULT_TEST_SIZE,
                                        marks={i / 10: f"{i / 10:.1f}" for i in range(1, 6)},
                                        tooltip={"placement": "bottom"},
                                    ),
                                ], md=3),
                            ]),
                        ],
                        style=SECTION_CARD_STYLE,
                    ),
                ],
            ),
            # Regression controls
            html.Div(
                id="regression-controls",
                style={"display": "none"},
                children=[
                    dbc.Card(
                        [
                            html.H6("Linear Regression Parameters", style={"color": LIGHT_GREEN, "fontWeight": "600"}),
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Target (Y) Variable:", style={"color": TEXT_MUTED, "fontSize": "13px"}),
                                    dcc.Dropdown(
                                        id="regression-target", value="",
                                        placeholder="Select numeric target...",
                                        style={**DROPDOWN_STYLE, "color": "black"},
                                    ),
                                ], md=4),
                                dbc.Col([
                                    html.Label("Test Size:", style={"color": TEXT_MUTED, "fontSize": "13px"}),
                                    dcc.Slider(
                                        id="reg-test-size", min=0.1, max=0.5, step=0.05,
                                        value=DEFAULT_TEST_SIZE,
                                        marks={i / 10: f"{i / 10:.1f}" for i in range(1, 6)},
                                        tooltip={"placement": "bottom"},
                                    ),
                                ], md=4),
                            ]),
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
