"""
Callbacks for the step panel — toggle add-step menu, handle step
toggle/delete, refresh step list after operations.
"""

import dash
from dash import html, no_update
from dash.dependencies import Input, Output, State, ALL

from pyexploratory.components.step_panel import render as render_step_panel
from pyexploratory.core import action_log


@dash.callback(
    Output("add-step-menu", "style"),
    Input("add-step-btn", "n_clicks"),
    State("add-step-menu", "style"),
    prevent_initial_call=True,
)
def toggle_add_menu(n_clicks, current_style):
    """Toggle the + Add Step dropdown menu."""
    if not n_clicks:
        return no_update
    if current_style and current_style.get("display") == "block":
        return {"display": "none"}
    return {"display": "block", "marginTop": "8px"}


@dash.callback(
    Output("step-list", "children"),
    Input("add-step-btn", "n_clicks"),
    Input({"type": "step-toggle", "index": ALL}, "n_clicks"),
    Input({"type": "step-delete", "index": ALL}, "n_clicks"),
    Input("output-data-upload", "children"),
    Input("cleaning-result", "children"),
    Input("chart-container", "children"),
    Input("ml-results", "children"),
)
def refresh_step_list(*_):
    """Re-render the step list whenever the action log changes."""
    panel = render_step_panel()
    for child in panel.children:
        if hasattr(child, "id") and child.id == "step-list":
            return child.children
    return []


@dash.callback(
    Output("step-list", "children", allow_duplicate=True),
    Input({"type": "step-toggle", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def handle_step_toggle(n_clicks_list):
    """Toggle the disabled state of a step."""
    triggered = dash.ctx.triggered_id
    if (
        triggered
        and isinstance(triggered, dict)
        and triggered.get("type") == "step-toggle"
    ):
        step_id = triggered["index"]
        if any(n for n in n_clicks_list if n):
            action_log.toggle_step(step_id)
    return no_update


@dash.callback(
    Output("step-list", "children", allow_duplicate=True),
    Input({"type": "step-delete", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def handle_step_delete(n_clicks_list):
    """Delete a step from the action log."""
    triggered = dash.ctx.triggered_id
    if (
        triggered
        and isinstance(triggered, dict)
        and triggered.get("type") == "step-delete"
    ):
        step_id = triggered["index"]
        if any(n for n in n_clicks_list if n):
            action_log.delete_step(step_id)
    return no_update
