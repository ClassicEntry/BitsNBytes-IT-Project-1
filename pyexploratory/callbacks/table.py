"""
Callbacks for the Table tab — save edits, cleaning with confirmation for destructive ops.
"""

import json

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, no_update
from dash.dependencies import Input, Output, State

from pyexploratory.core.cleaning_ops import OPERATIONS, apply_operation
from pyexploratory.core.data_store import read_data, write_data
from pyexploratory.tabs.table import DESTRUCTIVE_OPS

# ---------------------------------------------------------------------------
# Save inline table edits
# ---------------------------------------------------------------------------


@dash.callback(
    Output("table", "data"),
    Input("save-button", "n_clicks"),
    State("table", "data"),
)
def save_changes(n_clicks, rows):
    """Save inline table edits back to CSV."""
    if n_clicks is not None and n_clicks > 0:
        write_data(pd.DataFrame(rows))
    return rows


@dash.callback(
    Output("output-container-button", "children"),
    [Input("save-button", "n_clicks")],
)
def save_table_feedback(n_clicks):
    """Show confirmation after saving."""
    if n_clicks is not None:
        return "Changes have been saved."


# ---------------------------------------------------------------------------
# Cleaning: click Apply → either execute directly or open confirmation modal
# ---------------------------------------------------------------------------


@dash.callback(
    Output("cleaning-result", "children"),
    Output("pending-operation", "data"),
    Output("confirm-modal", "is_open"),
    Output("confirm-modal-body", "children"),
    Input("clean-data-btn", "n_clicks"),
    State("column-to-clean", "value"),
    State("cleaning-operation", "value"),
    State("fill-value", "value"),
    State("new-column-name", "value"),
    prevent_initial_call=True,
)
def handle_clean_click(
    n_clicks, column_to_clean, operation, fill_value, new_column_name
):
    """Route cleaning request: destructive ops get a confirmation modal, others run immediately."""
    if not n_clicks:
        return no_update, no_update, no_update, no_update

    # Validate inputs first
    try:
        df = read_data()
    except FileNotFoundError:
        return (
            dbc.Alert("Data file not found. Upload data first.", color="warning"),
            None,
            False,
            "",
        )

    if not column_to_clean or column_to_clean not in df.columns:
        return (
            dbc.Alert(
                f"Column '{column_to_clean}' not found in data.", color="warning"
            ),
            None,
            False,
            "",
        )

    if not operation or operation not in OPERATIONS:
        return (
            dbc.Alert("Select a valid cleaning operation.", color="warning"),
            None,
            False,
            "",
        )

    # Destructive? → open confirmation modal
    if operation in DESTRUCTIVE_OPS:
        op_label = next(
            (o["label"] for o in _get_op_labels() if o["value"] == operation),
            operation,
        )
        pending = json.dumps(
            {
                "column": column_to_clean,
                "operation": operation,
                "fill_value": fill_value,
                "new_name": new_column_name,
            }
        )
        body = f'Are you sure you want to apply "{op_label}" on column "{column_to_clean}"? This may remove data.'
        return no_update, pending, True, body

    # Non-destructive → execute immediately
    return (
        _execute_cleaning(df, operation, column_to_clean, fill_value, new_column_name),
        None,
        False,
        "",
    )


def _get_op_labels():
    """Import lazily to avoid circular import."""
    from pyexploratory.tabs.table import CLEANING_OPTIONS

    return CLEANING_OPTIONS


# ---------------------------------------------------------------------------
# Confirmation modal: confirm or cancel
# ---------------------------------------------------------------------------


@dash.callback(
    Output("cleaning-toast", "children"),
    Output("cleaning-toast", "icon"),
    Output("cleaning-toast", "is_open"),
    Output("confirm-modal", "is_open", allow_duplicate=True),
    Input("confirm-execute", "n_clicks"),
    Input("confirm-cancel", "n_clicks"),
    State("pending-operation", "data"),
    prevent_initial_call=True,
)
def handle_confirm(confirm_clicks, cancel_clicks, pending_data):
    """Execute or cancel the pending destructive operation."""
    triggered = dash.ctx.triggered_id

    if triggered == "confirm-cancel" or not pending_data:
        return "Operation cancelled.", "warning", True, False

    # Execute the stored operation
    try:
        op = json.loads(pending_data)
        df = read_data()
        df = apply_operation(
            df, op["operation"], op["column"], op["fill_value"], op["new_name"]
        )
        write_data(df)
        return "Data cleaning applied and saved.", "success", True, False
    except Exception as e:
        return f"Cleaning error: {e}", "danger", True, False


# ---------------------------------------------------------------------------
# Helper to run a non-destructive cleaning operation
# ---------------------------------------------------------------------------


def _execute_cleaning(df, operation, column, fill_value, new_name):
    """Run cleaning and return an alert."""
    try:
        df = apply_operation(df, operation, column, fill_value, new_name)
        write_data(df)
        return dbc.Alert("Data cleaning applied and saved.", color="success")
    except Exception as e:
        return dbc.Alert(f"Cleaning error: {e}", color="danger")
