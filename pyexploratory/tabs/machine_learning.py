"""
Machine Learning tab layout builder.

Renders task selector, variable dropdowns, and ML parameter controls.
"""

from dash import dcc, html

from pyexploratory.config import (
    DEFAULT_TEST_SIZE,
    DROPDOWN_STYLE,
    KMEANS_DEFAULT_CLUSTERS,
    LIGHT_GREEN,
)


def render() -> html.Div:
    """Build the Machine Learning tab content."""
    return html.Div(
        [
            html.H3("Machine Learning Task Selector", style={"color": "white"}),
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
            # Clustering controls
            html.Div(
                id="clustering-controls",
                style={"display": "none"},
                children=[
                    html.Label(
                        "Number of Clusters:",
                        style={"color": "white", "margin": "10px 0 5px 0"},
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
            ),
            # Classification controls
            html.Div(
                id="classification-controls",
                style={"display": "none"},
                children=[
                    dcc.Dropdown(
                        id="target-variable",
                        value="",
                        placeholder="Select target variable...",
                        style={**DROPDOWN_STYLE, "color": "black"},
                    ),
                    html.Label(
                        "SVM Kernel:",
                        style={"color": "white", "margin": "10px 0 5px 0"},
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
                    html.Label(
                        "Test Size:",
                        style={"color": "white", "margin": "10px 0 5px 0"},
                    ),
                    dcc.Slider(
                        id="test-size",
                        min=0.1,
                        max=0.5,
                        step=0.05,
                        value=DEFAULT_TEST_SIZE,
                        marks={i / 10: f"{i / 10:.1f}" for i in range(1, 6)},
                        tooltip={"placement": "bottom"},
                    ),
                ],
            ),
            # Shared feature selectors
            dcc.Dropdown(
                id="x-variable",
                value="",
                placeholder="Select x-axis...",
                style={**DROPDOWN_STYLE, "color": "black"},
            ),
            dcc.Dropdown(
                id="y-variable",
                value="",
                placeholder="Select y-axis...",
                style={**DROPDOWN_STYLE, "color": "black"},
            ),
            dcc.Loading(
                id="loading-ml",
                type="circle",
                color=LIGHT_GREEN,
                children=html.Div(id="ml-results", style={"minHeight": "200px"}),
            ),
        ]
    )
