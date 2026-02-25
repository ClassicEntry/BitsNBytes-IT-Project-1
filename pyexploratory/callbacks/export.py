"""
Callback for exporting the session as a standalone Python script.
"""

import dash
from dash import dcc
from dash.dependencies import Input, Output

from pyexploratory.core import action_log
from pyexploratory.core.script_generator import generate_script


@dash.callback(
    Output("download-script", "data"),
    Input("btn-export-script", "n_clicks"),
    prevent_initial_call=True,
)
def export_script(n_clicks):
    """Generate a standalone Python script from the action log and trigger download."""
    if not n_clicks:
        return dash.no_update
    log = action_log.get_log()
    script = generate_script(log)
    return dcc.send_string(script, "pyexploratory_session.py")
