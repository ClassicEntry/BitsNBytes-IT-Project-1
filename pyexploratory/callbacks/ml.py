"""
Callbacks for the Machine Learning tab.

Handles task dropdown updates, ML control visibility,
and running clustering / classification / decision tree / random forest / regression.
"""

import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output, State

from pyexploratory.config import LIGHT_GREEN
from pyexploratory.core import action_log
from pyexploratory.core.data_store import (
    categorical_column_options,
    numeric_column_options,
    read_data,
)
from pyexploratory.core.ml_classification import run_svm
from pyexploratory.core.ml_clustering import compute_elbow, run_kmeans
from pyexploratory.core.ml_decision_tree import run_decision_tree
from pyexploratory.core.ml_random_forest import run_random_forest
from pyexploratory.core.ml_regression import run_linear_regression
from pyexploratory.core.validators import validate_ml_inputs

_DARK_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)

_HIDE = {"display": "none"}
_SHOW = {"display": "block"}


@dash.callback(
    [
        Output("clustering-controls", "style"),
        Output("classification-controls", "style"),
        Output("decision-tree-controls", "style"),
        Output("random-forest-controls", "style"),
        Output("regression-controls", "style"),
    ],
    Input("task-dropdown", "value"),
)
def toggle_ml_controls(task):
    """Show/hide the appropriate ML parameter controls."""
    styles = {
        "clustering": [_SHOW, _HIDE, _HIDE, _HIDE, _HIDE],
        "classification": [_HIDE, _SHOW, _HIDE, _HIDE, _HIDE],
        "decision_tree": [_HIDE, _HIDE, _SHOW, _HIDE, _HIDE],
        "random_forest": [_HIDE, _HIDE, _HIDE, _SHOW, _HIDE],
        "regression": [_HIDE, _HIDE, _HIDE, _HIDE, _SHOW],
    }
    return styles.get(task, [_HIDE] * 5)


@dash.callback(
    [
        Output("x-variable", "options"),
        Output("y-variable", "options"),
        Output("target-variable", "options"),
        Output("dt-target-variable", "options"),
        Output("rf-target-variable", "options"),
        Output("regression-target", "options"),
    ],
    [Input("task-dropdown", "value")],
)
def update_ml_dropdowns(task):
    """Populate feature and target dropdowns based on task type."""
    try:
        df = read_data()
    except FileNotFoundError:
        return [], [], [], [], [], []

    feature_opts = numeric_column_options(df)
    cat_opts = categorical_column_options(df)

    return feature_opts, feature_opts, cat_opts, cat_opts, cat_opts, feature_opts


@dash.callback(
    Output("ml-results", "children"),
    Input("task-dropdown", "value"),
    Input("x-variable", "value"),
    Input("y-variable", "value"),
    # SVM inputs
    Input("target-variable", "value"),
    Input("n-clusters", "value"),
    Input("svm-kernel", "value"),
    Input("test-size", "value"),
    # DT inputs
    Input("dt-target-variable", "value"),
    Input("dt-max-depth", "value"),
    Input("dt-test-size", "value"),
    # RF inputs
    Input("rf-target-variable", "value"),
    Input("rf-n-estimators", "value"),
    Input("rf-max-depth", "value"),
    Input("rf-test-size", "value"),
    # Regression inputs
    Input("regression-target", "value"),
    Input("reg-test-size", "value"),
    prevent_initial_call=True,
)
def perform_machine_learning(
    task, x_variable, y_variable,
    target_variable, n_clusters, svm_kernel, test_size,
    dt_target, dt_max_depth, dt_test_size,
    rf_target, rf_n_estimators, rf_max_depth, rf_test_size,
    reg_target, reg_test_size,
):
    """Run the selected ML task and return visualization."""
    try:
        df = read_data()
    except FileNotFoundError:
        return dbc.Alert("Data file not found. Please upload data.", color="warning")

    valid_tasks = {"clustering", "classification", "decision_tree", "random_forest", "regression"}
    if task not in valid_tasks:
        return html.Div("Select a valid task.", style={"color": "white"})

    # Regression uses x-variable and regression-target (both numeric)
    if task == "regression":
        if not x_variable or not reg_target:
            return html.Div("Select X variable and target.", style={"color": "white"})
        try:
            action_log.log_action({
                "action_type": "ml",
                "task": "regression",
                "x_col": x_variable,
                "target_col": reg_target,
                "test_size": reg_test_size or 0.25,
            })
            return _render_regression(df, x_variable, reg_target, reg_test_size or 0.25)
        except Exception as e:
            return dbc.Alert(f"Regression error: {e}", color="danger")

    # All other tasks need x and y variables
    if not x_variable or not y_variable:
        return html.Div("Select x and y variables.", style={"color": "white"})

    error = validate_ml_inputs(df, x_variable, y_variable)
    if error:
        return dbc.Alert(error, color="warning")

    try:
        if task == "clustering":
            action_log.log_action({
                "action_type": "ml",
                "task": "clustering",
                "x_col": x_variable,
                "y_col": y_variable,
                "n_clusters": n_clusters or 3,
            })
            return _render_clustering(df, x_variable, y_variable, n_clusters or 3)
        elif task == "classification":
            if not target_variable or target_variable not in df.columns:
                return html.Div("Select a valid target variable.", style={"color": "white"})
            action_log.log_action({
                "action_type": "ml",
                "task": "classification",
                "x_col": x_variable,
                "y_col": y_variable,
                "target_col": target_variable,
                "kernel": svm_kernel or "linear",
                "test_size": test_size or 0.25,
            })
            return _render_classification(
                df, x_variable, y_variable, target_variable,
                svm_kernel or "linear", test_size or 0.25,
            )
        elif task == "decision_tree":
            if not dt_target or dt_target not in df.columns:
                return html.Div("Select a target variable for Decision Tree.", style={"color": "white"})
            action_log.log_action({
                "action_type": "ml",
                "task": "decision_tree",
                "x_col": x_variable,
                "y_col": y_variable,
                "target_col": dt_target,
                "max_depth": dt_max_depth or 5,
                "test_size": dt_test_size or 0.25,
            })
            return _render_decision_tree(
                df, x_variable, y_variable, dt_target,
                dt_max_depth or 5, dt_test_size or 0.25,
            )
        elif task == "random_forest":
            if not rf_target or rf_target not in df.columns:
                return html.Div("Select a target variable for Random Forest.", style={"color": "white"})
            action_log.log_action({
                "action_type": "ml",
                "task": "random_forest",
                "x_col": x_variable,
                "y_col": y_variable,
                "target_col": rf_target,
                "n_estimators": rf_n_estimators or 100,
                "max_depth": rf_max_depth or 5,
                "test_size": rf_test_size or 0.25,
            })
            return _render_random_forest(
                df, x_variable, y_variable, rf_target,
                rf_n_estimators or 100, rf_max_depth or 5, rf_test_size or 0.25,
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

    fig = go.Figure()
    fig.add_trace(
        go.Contour(
            x=result.xx[0], y=result.yy[:, 0], z=result.Z,
            showscale=False, opacity=0.4, colorscale="Viridis", hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result.X_scaled[:, 0], y=result.X_scaled[:, 1], mode="markers",
            marker=dict(color=result.labels, colorscale="Viridis",
                        line=dict(width=0.5, color="DarkSlateGrey"), showscale=True),
            text=[f"Cluster {label}" for label in result.labels],
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result.centroids[:, 0], y=result.centroids[:, 1], mode="markers",
            marker=dict(color="red", symbol="x", size=12,
                        line=dict(width=2, color="DarkSlateGrey")),
            text=["Centroid"] * len(result.centroids),
        )
    )
    fig.update_layout(
        title="KMeans Clustering", xaxis_title=x_variable, yaxis_title=y_variable,
        margin=dict(l=0, r=0, t=40, b=0), **_DARK_LAYOUT,
    )

    fig_elbow = go.Figure()
    fig_elbow.add_trace(
        go.Scatter(
            x=elbow["k_values"], y=elbow["inertias"], mode="lines+markers",
            marker=dict(color=LIGHT_GREEN),
        )
    )
    fig_elbow.update_layout(
        title="Elbow Method", xaxis_title="Number of Clusters (k)", yaxis_title="Inertia",
        margin=dict(l=0, r=0, t=40, b=0), **_DARK_LAYOUT,
    )

    return html.Div([
        dcc.Graph(figure=fig),
        html.Div(f"Silhouette Score: {result.silhouette:.3f}",
                 style={"color": "white", "fontSize": "18px", "margin": "10px 0"}),
        dcc.Graph(figure=fig_elbow),
    ])


def _render_classification(df, x_variable, y_variable, target_variable, kernel, test_size):
    """Build SVM classification visualization components."""
    result = run_svm(df, x_variable, y_variable, target_variable, kernel, test_size)

    fig_cm = go.Figure(go.Heatmap(
        z=result.cm, x=result.display_labels, y=result.display_labels,
        colorscale="Viridis", showscale=True,
    ))
    fig_cm.update_layout(title="Confusion Matrix", **_DARK_LAYOUT)

    fig_train = px.scatter(
        x=result.X_train[:, 0], y=result.X_train[:, 1],
        color=result.y_pred_train.astype(str),
        title="Training Data Classification", labels={"color": "Predicted Class"},
    )
    fig_train.update_traces(marker=dict(line=dict(width=0.5, color="DarkSlateGrey")))
    fig_train.update_layout(**_DARK_LAYOUT)

    fig_test = px.scatter(
        x=result.X_test[:, 0], y=result.X_test[:, 1],
        color=result.y_pred_test.astype(str),
        title="Testing Data Classification", labels={"color": "Predicted Class"},
    )
    fig_test.update_traces(marker=dict(line=dict(width=0.5, color="DarkSlateGrey")))
    fig_test.update_layout(**_DARK_LAYOUT)

    return html.Div([
        html.H4("Classification Report", style={"color": "white"}),
        html.Pre(result.report, style={"color": "white"}),
        _metrics_row(f"Accuracy: {result.accuracy:.3f}", f"Weighted F1: {result.f1:.3f}"),
        html.H4("Confusion Matrix", style={"color": "white", "textAlign": "center"}),
        dcc.Graph(figure=fig_cm),
        dcc.Tabs([
            dcc.Tab(label="Training Set", children=[dcc.Graph(figure=fig_train)]),
            dcc.Tab(label="Testing Set", children=[dcc.Graph(figure=fig_test)]),
        ]),
    ])


def _render_decision_tree(df, x_variable, y_variable, target, max_depth, test_size):
    """Build Decision Tree visualization components."""
    result = run_decision_tree(df, x_variable, y_variable, target, max_depth, test_size)

    fig_cm = go.Figure(go.Heatmap(
        z=result.cm, x=result.display_labels, y=result.display_labels,
        colorscale="Viridis", showscale=True,
    ))
    fig_cm.update_layout(title="Confusion Matrix", **_DARK_LAYOUT)

    fig_imp = go.Figure(go.Bar(
        x=result.feature_importances, y=result.feature_names,
        orientation="h", marker_color=LIGHT_GREEN,
    ))
    fig_imp.update_layout(title="Feature Importances", **_DARK_LAYOUT)

    return html.Div([
        html.H4("Decision Tree Report", style={"color": "white"}),
        html.Pre(result.report, style={"color": "white"}),
        _metrics_row(f"Accuracy: {result.accuracy:.3f}", f"Weighted F1: {result.f1:.3f}"),
        dcc.Graph(figure=fig_cm),
        dcc.Graph(figure=fig_imp),
    ])


def _render_random_forest(df, x_variable, y_variable, target, n_estimators, max_depth, test_size):
    """Build Random Forest visualization components."""
    result = run_random_forest(df, x_variable, y_variable, target, n_estimators, max_depth, test_size)

    fig_cm = go.Figure(go.Heatmap(
        z=result.cm, x=result.display_labels, y=result.display_labels,
        colorscale="Viridis", showscale=True,
    ))
    fig_cm.update_layout(title="Confusion Matrix", **_DARK_LAYOUT)

    fig_imp = go.Figure(go.Bar(
        x=result.feature_importances, y=result.feature_names,
        orientation="h", marker_color=LIGHT_GREEN,
    ))
    fig_imp.update_layout(title="Feature Importances", **_DARK_LAYOUT)

    oob_text = f"OOB Score: {result.oob_score:.3f}" if result.oob_score is not None else "OOB Score: N/A"

    return html.Div([
        html.H4("Random Forest Report", style={"color": "white"}),
        html.Pre(result.report, style={"color": "white"}),
        _metrics_row(
            f"Accuracy: {result.accuracy:.3f}",
            f"Weighted F1: {result.f1:.3f}",
            oob_text,
        ),
        dcc.Graph(figure=fig_cm),
        dcc.Graph(figure=fig_imp),
    ])


def _render_regression(df, x_col, y_col, test_size):
    """Build Linear Regression visualization components."""
    result = run_linear_regression(df, x_col, y_col, test_size)

    # Actual vs Predicted scatter
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(
        x=result.y_test, y=result.y_pred_test, mode="markers",
        name="Predictions", marker=dict(color=LIGHT_GREEN, size=8),
    ))
    # Perfect prediction line
    min_val = min(result.y_test.min(), result.y_pred_test.min())
    max_val = max(result.y_test.max(), result.y_pred_test.max())
    fig_pred.add_trace(go.Scatter(
        x=[min_val, max_val], y=[min_val, max_val], mode="lines",
        name="Perfect Prediction", line=dict(color="red", dash="dash"),
    ))
    fig_pred.update_layout(
        title="Actual vs Predicted", xaxis_title="Actual", yaxis_title="Predicted",
        **_DARK_LAYOUT,
    )

    # Residual plot
    fig_resid = go.Figure(go.Scatter(
        x=result.y_pred_test, y=result.residuals, mode="markers",
        marker=dict(color=LIGHT_GREEN, size=8),
    ))
    fig_resid.add_hline(y=0, line_dash="dash", line_color="red")
    fig_resid.update_layout(
        title="Residual Plot", xaxis_title="Predicted", yaxis_title="Residuals",
        **_DARK_LAYOUT,
    )

    return html.Div([
        html.H4("Linear Regression Results", style={"color": "white"}),
        _metrics_row(f"R-squared: {result.r2:.4f}", f"MSE: {result.mse:.4f}"),
        html.Div([
            html.Span(f"Coefficient: {result.coefficients[0]:.4f}", style={"color": "white", "marginRight": "30px"}),
            html.Span(f"Intercept: {result.intercept:.4f}", style={"color": "white"}),
        ], style={"margin": "10px 0"}),
        dcc.Graph(figure=fig_pred),
        dcc.Graph(figure=fig_resid),
    ])


def _metrics_row(*items):
    """Build a row of metric spans."""
    spans = []
    for item in items:
        spans.append(html.Span(item, style={"color": "white", "marginRight": "30px", "fontSize": "16px"}))
    return html.Div(spans, style={"margin": "10px 0"})
