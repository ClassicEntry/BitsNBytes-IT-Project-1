"""
Callbacks for file upload and page refresh.
"""

import datetime

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

from pyexploratory.core.data_store import write_data
from pyexploratory.core.file_parser import parse_upload


def _parse_and_save(contents: str, filename: str, date: int) -> html.Div:
    """Parse an uploaded file, save to disk, and return feedback."""
    try:
        df = parse_upload(contents, filename)
    except Exception as e:
        return dbc.Alert(f"Error processing {filename}: {e}", color="danger")

    if df is None:
        return dbc.Alert("Unsupported file format.", color="warning")

    write_data(df)

    return dbc.Alert(
        [
            html.Strong(f"Successfully imported {filename}"),
            html.Br(),
            f"{len(df)} rows, {len(df.columns)} columns",
            html.Br(),
            f"Columns: {', '.join(df.columns[:8])}{'...' if len(df.columns) > 8 else ''}",
        ],
        color="success",
    )


@dash.callback(
    Output("output-data-upload", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    """Update the output area with parsed file info."""
    if list_of_contents is not None:
        return [
            _parse_and_save(c, n, d)
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]


@dash.callback(
    Output("refresh", "pathname"),
    [Input("upload-data", "contents")],
)
def refresh_page(contents):
    """Refresh to data_analysis page after upload."""
    if contents is not None:
        return "./data_analysis"
