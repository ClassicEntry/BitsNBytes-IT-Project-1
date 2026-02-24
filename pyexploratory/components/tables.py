"""
Shared DataTable styling constants.

Used by summary cards and the table tab to ensure consistent table appearance.
"""

from pyexploratory.config import DARK_GREEN, WHITE

TABLE_CELL_STYLE = {
    "textAlign": "center",
    "backgroundColor": WHITE,
    "color": "black",
    "border": "1px solid black",
}

TABLE_HEADER_STYLE = {
    "backgroundColor": DARK_GREEN,
    "fontWeight": "bold",
    "color": "white",
}

SUMMARY_TABLE_STYLE = {
    "overflowX": "auto",
    "overflowY": "auto",
    "padding": "15px 0px 0px 15px",
    "margin": "10px",
    "justifyContent": "center",
}

DATA_TABLE_STYLE = {
    "overflowX": "auto",
    "padding": "10px",
}

# Thicker border variant for the editable data table
DATA_TABLE_CELL_STYLE = {
    "whiteSpace": "normal",
    "height": "auto",
    "textAlign": "center",
    "backgroundColor": WHITE,
    "color": "black",
    "border": "2px solid black",
}
