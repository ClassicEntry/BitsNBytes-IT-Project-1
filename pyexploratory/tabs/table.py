"""
Table tab layout builder.

Renders the editable data table with cleaning controls,
undo/redo buttons, and history log.
"""

import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html

from pyexploratory.components.styles import CLEAN_BUTTON_STYLE, SAVE_BUTTON_STYLE
from pyexploratory.components.tables import (
    DATA_TABLE_CELL_STYLE,
    DATA_TABLE_STYLE,
    TABLE_HEADER_STYLE,
)
from pyexploratory.config import (
    CARD_BG,
    DROPDOWN_STYLE,
    INPUT_STYLE,
    LIGHT_GREEN,
    SECTION_CARD_STYLE,
    TEXT_MUTED,
    WHITE,
)
from pyexploratory.core.data_store import read_data

# Operations that delete data — require confirmation
DESTRUCTIVE_OPS = {"drop_column", "dropna", "drop_duplicates", "remove_outliers"}

# Cleaning operation dropdown options
CLEANING_OPTIONS = [
    {"label": "Strip value (left)", "value": "lstrip"},
    {"label": "Strip value (right)", "value": "rstrip"},
    {"label": "Remove non-alphanumeric characters", "value": "alnum"},
    {"label": "Drop NA", "value": "dropna"},
    {"label": "Fill NA", "value": "fillna"},
    {"label": "Convert to Numeric", "value": "to_numeric"},
    {"label": "Convert to String", "value": "to_string"},
    {"label": "Convert to DateTime", "value": "to_datetime"},
    {"label": "Convert to Lowercase", "value": "lowercase"},
    {"label": "Convert to Uppercase", "value": "uppercase"},
    {"label": "Trim Whitespace", "value": "trim"},
    {"label": "Drop Column", "value": "drop_column"},
    {"label": "Rename Column", "value": "rename_column"},
    {"label": "Normalize", "value": "normalize"},
    {"label": "Remove Outliers", "value": "remove_outliers"},
    {"label": "Drop Duplicates", "value": "drop_duplicates"},
    {"label": "Sort Ascending", "value": "sort_asc"},
    {"label": "Sort Descending", "value": "sort_desc"},
]

_UNDO_REDO_BTN = {
    "borderRadius": "8px",
    "border": "none",
    "padding": "6px 16px",
    "fontWeight": "600",
    "cursor": "pointer",
    "marginRight": "8px",
}


def render() -> html.Div:
    """Build the Table tab content."""
    try:
        df = read_data()
    except FileNotFoundError:
        return html.Div(
            dbc.Alert(
                "Data file not found. Please upload data in the drop box.",
                color="warning",
            )
        )

    return html.Div(
        [
            # Hidden stores
            dcc.Store(id="pending-operation", data=None),
            dcc.Store(id="history-trigger", data=0),
            # Confirmation modal
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Confirm Operation")),
                    dbc.ModalBody(id="confirm-modal-body"),
                    dbc.ModalFooter(
                        [
                            dbc.Button(
                                "Cancel",
                                id="confirm-cancel",
                                className="ms-auto",
                                color="secondary",
                            ),
                            dbc.Button(
                                "Confirm",
                                id="confirm-execute",
                                color="danger",
                            ),
                        ]
                    ),
                ],
                id="confirm-modal",
                is_open=False,
            ),
            # Preview modal
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Operation Preview")),
                    dbc.ModalBody(id="preview-modal-body"),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="preview-close", color="secondary"),
                    ),
                ],
                id="preview-modal",
                is_open=False,
            ),
            # Toast for operation feedback
            dbc.Toast(
                id="cleaning-toast",
                header="Cleaning Result",
                is_open=False,
                dismissable=True,
                duration=4000,
                icon="success",
                style={
                    "position": "fixed",
                    "top": 20,
                    "right": 20,
                    "width": 350,
                    "zIndex": 9999,
                },
            ),
            # Data table
            dash_table.DataTable(
                id="table",
                data=df.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df.columns],
                page_action="native",
                page_size=50,
                style_table=DATA_TABLE_STYLE,
                style_cell=DATA_TABLE_CELL_STYLE,
                style_header=TABLE_HEADER_STYLE,
                editable=True,
            ),
            # Save + Undo/Redo buttons row
            html.Div(
                [
                    html.Button(
                        "Save Changes",
                        id="save-button",
                        style=SAVE_BUTTON_STYLE,
                    ),
                    html.Button(
                        "Undo",
                        id="undo-btn",
                        n_clicks=0,
                        style={
                            **_UNDO_REDO_BTN,
                            "backgroundColor": "#e67e22",
                            "color": "white",
                        },
                    ),
                    html.Button(
                        "Redo",
                        id="redo-btn",
                        n_clicks=0,
                        style={
                            **_UNDO_REDO_BTN,
                            "backgroundColor": "#3498db",
                            "color": "white",
                        },
                    ),
                    html.Div(
                        id="output-container-button",
                        children='Enter your inputs and press "Save Changes"',
                        style={"color": TEXT_MUTED, "marginTop": "8px"},
                    ),
                ],
                style={"margin": "10px 0", "display": "flex", "alignItems": "center", "flexWrap": "wrap", "gap": "4px"},
            ),
            # Data Cleaning card
            dbc.Card(
                [
                    html.H5(
                        "Data Cleaning",
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
                                        "Operation:",
                                        style={"color": WHITE, "fontSize": "13px"},
                                    ),
                                    dcc.Dropdown(
                                        id="cleaning-operation",
                                        options=CLEANING_OPTIONS,
                                        placeholder="Select Cleaning Operation...",
                                        style=DROPDOWN_STYLE,
                                    ),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    html.Label(
                                        "Column:",
                                        style={"color": WHITE, "fontSize": "13px"},
                                    ),
                                    dcc.Input(
                                        id="column-to-clean",
                                        type="text",
                                        placeholder="Column to clean...",
                                        style=INPUT_STYLE,
                                    ),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    html.Label(
                                        "Fill Value:",
                                        style={"color": WHITE, "fontSize": "13px"},
                                    ),
                                    dcc.Input(
                                        id="fill-value",
                                        type="text",
                                        placeholder="Value for operation...",
                                        style=INPUT_STYLE,
                                    ),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    html.Label(
                                        "New Name:",
                                        style={"color": WHITE, "fontSize": "13px"},
                                    ),
                                    dcc.Input(
                                        id="new-column-name",
                                        type="text",
                                        placeholder="New column name...",
                                        style=INPUT_STYLE,
                                    ),
                                ],
                                md=3,
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            html.Button(
                                "Apply Cleaning",
                                id="clean-data-btn",
                                n_clicks=0,
                                style=CLEAN_BUTTON_STYLE,
                            ),
                            html.Button(
                                "Preview",
                                id="preview-btn",
                                n_clicks=0,
                                style={
                                    **_UNDO_REDO_BTN,
                                    "backgroundColor": "#8e44ad",
                                    "color": "white",
                                },
                            ),
                        ],
                        style={"display": "flex", "alignItems": "center", "gap": "8px"},
                    ),
                    html.Div(id="cleaning-result", style={"marginTop": "10px"}),
                ],
                style=SECTION_CARD_STYLE,
            ),
            # History log card
            dbc.Card(
                [
                    html.H6(
                        "Cleaning History",
                        style={"color": LIGHT_GREEN, "fontWeight": "600", "marginBottom": "8px"},
                    ),
                    html.Div(
                        id="history-log",
                        style={"color": TEXT_MUTED, "fontSize": "13px", "maxHeight": "200px", "overflowY": "auto"},
                    ),
                ],
                style=SECTION_CARD_STYLE,
            ),
        ]
    )
