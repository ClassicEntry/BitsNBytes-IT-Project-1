"""
Callback for importing a previously exported PyExploratory script.

Parses the script back into action log entries and replays cleaning
operations on the currently loaded dataset.
"""

import base64
import os

import dash
from dash import html
from dash.dependencies import Input, Output, State

from pyexploratory.config import DATA_FILE
from pyexploratory.core import action_log
from pyexploratory.core.cleaning_ops import apply_operation
from pyexploratory.core.data_store import read_data, write_data
from pyexploratory.core.script_parser import parse_script


@dash.callback(
    Output("import-script-feedback", "children"),
    Input("upload-script", "contents"),
    State("upload-script", "filename"),
    prevent_initial_call=True,
)
def import_script(contents, filename):
    """Decode uploaded .py file, parse it, replay cleaning ops, and log all entries."""
    if contents is None:
        return dash.no_update

    # --- Guard: data must be loaded first ---
    if not os.path.exists(DATA_FILE):
        return html.Div(
            "Please upload a dataset before importing a script.",
            style={"color": "#ff6b6b", "marginTop": "6px", "fontSize": "13px"},
        )

    # --- Decode base64 upload ---
    try:
        _, content_string = contents.split(",", 1)
        script_text = base64.b64decode(content_string).decode("utf-8")
    except Exception:
        return html.Div(
            "Failed to read the uploaded file.",
            style={"color": "#ff6b6b", "marginTop": "6px", "fontSize": "13px"},
        )

    # --- Parse script into action entries ---
    entries = parse_script(script_text)
    if not entries:
        return html.Div(
            "No actions found in the script.",
            style={"color": "#ff6b6b", "marginTop": "6px", "fontSize": "13px"},
        )

    # --- Reset log and replay ---
    # Find the upload entry (if any) and use it to reset the log
    upload_entry = next(
        (e for e in entries if e.get("action_type") == "upload"), None
    )
    if upload_entry:
        action_log.reset_on_upload(
            upload_entry["filename"], upload_entry["file_format"]
        )
    else:
        action_log.clear_log()

    cleaning_count = 0
    chart_count = 0
    ml_count = 0
    errors: list = []

    for entry in entries:
        at = entry.get("action_type")

        if at == "upload":
            # Already handled above via reset_on_upload
            continue

        if at == "cleaning":
            # Replay on actual data
            try:
                df = read_data()
                df = apply_operation(
                    df,
                    operation=entry["operation"],
                    column=entry["column"],
                    fill_value=entry.get("fill_value"),
                    new_name=entry.get("new_name"),
                )
                write_data(df)
                action_log.log_action(entry)
                cleaning_count += 1
            except Exception as exc:
                errors.append(f"{entry.get('operation')} on {entry.get('column')}: {exc}")

        elif at == "chart":
            action_log.log_action(entry)
            chart_count += 1

        elif at == "ml":
            action_log.log_action(entry)
            ml_count += 1

    # --- Build success message ---
    parts = []
    if cleaning_count:
        parts.append(f"{cleaning_count} cleaning")
    if chart_count:
        parts.append(f"{chart_count} chart")
    if ml_count:
        parts.append(f"{ml_count} ML")

    summary = ", ".join(parts) if parts else "0"
    msg = f"Imported {summary} actions from {filename or 'script'}."

    children = [
        html.Div(
            msg,
            style={"color": "#56D300", "marginTop": "6px", "fontSize": "13px"},
        )
    ]

    if errors:
        children.append(
            html.Div(
                f"{len(errors)} error(s): {'; '.join(errors)}",
                style={"color": "#ff6b6b", "marginTop": "4px", "fontSize": "12px"},
            )
        )

    return html.Div(children)
