"""
Callbacks for the Machine Learning tab.

Handles task dropdown updates, ML control visibility,
and running clustering / classification.
"""

import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output

from pyexploratory.config import LIGHT_GREEN
from pyexploratory.core.data_store import (
    categorical_column_options,
    numeric_column_options,
    read_data,
)
from pyexploratory.core.ml_classification import run_svm
from pyexploratory.core.ml_clustering import compute_elbow, run_kmeans


@dash.callback(
    [
        Output("clustering-controls", "style"),
        Output("classification-controls", "style"),
    ],
    Input("task-dropdown", "value"),
)
def toggle_ml_controls(task):
    """Show/hide the appropriate ML parameter controls."""
    if task == "clustering":
        return {"display": "block"}, {"display": "none"}
    elif task == "classification":
        return {"display": "none"}, {"display": "block"}
    return {"display": "none"}, {"display": "none"}


@dash.callback(
    [
        Output("x-variable", "options"),
        Output("y-variable", "options"),
        Output("target-variable", "options"),
    ],
    [Input("task-dropdown", "value")],
)
def update_ml_dropdowns(task):
    """Populate feature and target dropdowns based on task type."""
    try:
        df = read_data()
    except FileNotFoundError:
        return [], [], []

    feature_opts = numeric_column_options(df)

    if task == "classification":
        target_opts = categorical_column_options(df)
    else:
        target_opts = []

    return feature_opts, feature_opts, target_opts


@dash.callback(
    Output("ml-results", "children"),
    [
        Input("task-dropdown", "value"),
        Input("x-variable", "value"),
        Input("y-variable", "value"),
        Input("target-variable", "value"),
        Input("n-clusters", "value"),
        Input("svm-kernel", "value"),
        Input("test-size", "value"),
    ],
    prevent_initial_call=True,
)
def perform_machine_learning(
    task,
    x_variable,
    y_variable,
    target_variable,
    n_clusters,
    svm_kernel,
    test_size,
):
    """Run the selected ML task and return visualization."""
    try:
        df = read_data()
    except FileNotFoundError:
        return dbc.Alert("Data file not found. Please upload data.", color="warning")

    if task not in ("clustering", "classification"):
        return html.Div("Select a valid task.", style={"color": "white"})

    if not x_variable or x_variable not in df.columns:
        return html.Div("Select a valid x variable.", style={"color": "white"})
    if not y_variable or y_variable not in df.columns:
        return html.Div("Select a valid y variable.", style={"color": "white"})

    try:
        if task == "clustering":
            return _render_clustering(df, x_variable, y_variable, n_clusters or 3)
        else:
            if not target_variable or target_variable not in df.columns:
                return html.Div(
                    "Select a valid target variable for classification.",
                    style={"color": "white"},
                )
            return _render_classification(
                df,
                x_variable,
                y_variable,
                target_variable,
                svm_kernel or "linear",
                test_size or 0.25,
            )
    except Exception as e:
        return dbc.Alert(f"Error in {task}: {e}", color="danger")


# ---------------------------------------------------------------------------
# Private rendering helpers
# ---------------------------------------------------------------------------


def _render_clustering(df, x_variable, y_variable, n_clusters):
    """Build clustering visualization components."""
    result = run_kmeans(df, x_variable, y_variable, n_clusters)
    elbow = compute_elbow(df, x_variable, y_variable)

    # Main clustering figure
    fig = go.Figure()
    fig.add_trace(
        go.Contour(
            x=result.xx[0],
            y=result.yy[:, 0],
            z=result.Z,
            showscale=False,
            opacity=0.4,
            colorscale="Viridis",
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result.X_scaled[:, 0],
            y=result.X_scaled[:, 1],
            mode="markers",
            marker=dict(
                color=result.labels,
                colorscale="Viridis",
                line=dict(width=0.5, color="DarkSlateGrey"),
                showscale=True,
            ),
            text=[f"Cluster {label}" for label in result.labels],
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result.centroids[:, 0],
            y=result.centroids[:, 1],
            mode="markers",
            marker=dict(
                color="red",
                symbol="x",
                size=12,
                line=dict(width=2, color="DarkSlateGrey"),
            ),
            text=["Centroid"] * len(result.centroids),
        )
    )
    fig.update_layout(
        title="KMeans Clustering",
        xaxis_title=x_variable,
        yaxis_title=y_variable,
        margin=dict(l=0, r=0, t=40, b=0),
    )

    # Elbow method figure
    fig_elbow = go.Figure()
    fig_elbow.add_trace(
        go.Scatter(
            x=elbow["k_values"],
            y=elbow["inertias"],
            mode="lines+markers",
            marker=dict(color=LIGHT_GREEN),
        )
    )
    fig_elbow.update_layout(
        title="Elbow Method",
        xaxis_title="Number of Clusters (k)",
        yaxis_title="Inertia",
        margin=dict(l=0, r=0, t=40, b=0),
    )

    return html.Div(
        [
            dcc.Graph(figure=fig),
            html.Div(
                f"Silhouette Score: {result.silhouette:.3f}",
                style={"color": "white", "fontSize": "18px", "margin": "10px 0"},
            ),
            dcc.Graph(figure=fig_elbow),
        ]
    )


def _render_classification(
    df, x_variable, y_variable, target_variable, kernel, test_size
):
    """Build classification visualization components."""
    result = run_svm(df, x_variable, y_variable, target_variable, kernel, test_size)

    # Confusion matrix heatmap
    fig_cm = go.Figure()
    fig_cm.add_trace(
        go.Heatmap(
            z=result.cm,
            x=result.display_labels,
            y=result.display_labels,
            colorscale="Viridis",
            showscale=True,
        )
    )
    fig_cm.update_layout(title="Confusion Matrix")

    # Training scatter
    fig_train = px.scatter(
        x=result.X_train[:, 0],
        y=result.X_train[:, 1],
        color=result.y_pred_train.astype(str),
        title="Training Data Classification",
        labels={"color": "Predicted Class"},
    )
    fig_train.update_traces(marker=dict(line=dict(width=0.5, color="DarkSlateGrey")))

    # Testing scatter
    fig_test = px.scatter(
        x=result.X_test[:, 0],
        y=result.X_test[:, 1],
        color=result.y_pred_test.astype(str),
        title="Testing Data Classification",
        labels={"color": "Predicted Class"},
    )
    fig_test.update_traces(marker=dict(line=dict(width=0.5, color="DarkSlateGrey")))

    return html.Div(
        [
            html.H4("Classification Report", style={"color": "white"}),
            html.Pre(result.report, style={"color": "white"}),
            html.Div(
                [
                    html.Span(
                        f"Accuracy: {result.accuracy:.3f}",
                        style={
                            "color": "white",
                            "marginRight": "30px",
                            "fontSize": "16px",
                        },
                    ),
                    html.Span(
                        f"Weighted F1: {result.f1:.3f}",
                        style={"color": "white", "fontSize": "16px"},
                    ),
                ],
                style={"margin": "10px 0"},
            ),
            html.H4(
                "Confusion Matrix",
                style={
                    "color": "white",
                    "margin": "1px 10px 10px 0px",
                    "textAlign": "center",
                },
            ),
            dcc.Graph(figure=fig_cm, style={"margin": "1px 10px 10px 0px"}),
            dcc.Tabs(
                [
                    dcc.Tab(
                        label="Training Set", children=[dcc.Graph(figure=fig_train)]
                    ),
                    dcc.Tab(label="Testing Set", children=[dcc.Graph(figure=fig_test)]),
                ]
            ),
        ]
    )
