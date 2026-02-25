"""
Shared DataTable styling constants.

Used by summary cards and the table tab to ensure consistent table appearance.
"""

from pyexploratory.config import CARD_BG, CARD_BORDER, DARK_GREEN, LIGHT_GREEN, WHITE

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

# Dark-themed summary table styles
SUMMARY_DARK_CELL_STYLE = {
    "textAlign": "left",
    "backgroundColor": CARD_BG,
    "color": "#e0e0e0",
    "border": f"1px solid {CARD_BORDER}",
    "padding": "8px 12px",
}

SUMMARY_DARK_HEADER_STYLE = {
    "backgroundColor": "#1a3a1a",
    "fontWeight": "600",
    "color": LIGHT_GREEN,
    "padding": "10px 12px",
}
