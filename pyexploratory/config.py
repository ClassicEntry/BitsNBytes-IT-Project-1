"""
Centralized configuration for PyExploratory.

All colors, styles, ML defaults, and file paths in one place.
"""

import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(PROJECT_ROOT, "local_data.csv")

# ---------------------------------------------------------------------------
# Colors (SCREAMING_SNAKE_CASE constants)
# ---------------------------------------------------------------------------
LIGHT_GREEN = "#56D300"
DARK_GREEN = "#00a417"
NEW_GREEN = "#0f4d25"
GREY = "#3f3f3f"
LIGHT_BLUE = "#007BFF"
DARK_BLUE = "#1d06ca"
WHITE = "#f3f3f3"
BLACK = "#000000"
SIDEBAR_BG = "#282829"

# ---------------------------------------------------------------------------
# Tab styles
# ---------------------------------------------------------------------------
TAB_STYLE = {
    "backgroundColor": DARK_GREEN,
    "color": "white",
    "borderRadius": "15px",
    "margin": "10px",
}

SELECTED_TAB_STYLE = {
    "backgroundColor": LIGHT_GREEN,
    "color": "white",
    "borderRadius": "15px",
    "margin": "10px",
}

# ---------------------------------------------------------------------------
# Sidebar / Content layout styles
# ---------------------------------------------------------------------------
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "0rem",
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": SIDEBAR_BG,
    "z-index": "1",
}

CONTENT_STYLE = {
    "margin-left": "15.25rem",
    "position": "static",
    "top": "0rem",
    "right": "0rem",
    "bottom": "0rem",
    "left": "0rem",
    "background-color": GREY,
}

# ---------------------------------------------------------------------------
# ML defaults
# ---------------------------------------------------------------------------
KMEANS_DEFAULT_CLUSTERS = 3
KMEANS_RANDOM_STATE = 42
SVM_DEFAULT_KERNEL = "linear"
SVM_RANDOM_STATE = 42
DEFAULT_TEST_SIZE = 0.25
MESH_STEP_SIZE = 0.02

# ---------------------------------------------------------------------------
# Shared button style
# ---------------------------------------------------------------------------
GREEN_BUTTON_STYLE = {
    "backgroundColor": DARK_GREEN,
    "color": "white",
    "borderRadius": "10px",
    "padding": "5px",
    "textAlign": "center",
}

# ---------------------------------------------------------------------------
# Shared dropdown style
# ---------------------------------------------------------------------------
DROPDOWN_STYLE = {
    "borderRadius": "10px",
    "margin": "1px 10px 10px 0px",
    "width": "95.5%",
    "textAlign": "center",
}

# ---------------------------------------------------------------------------
# Shared input style
# ---------------------------------------------------------------------------
INPUT_STYLE = {
    "backgroundColor": DARK_GREEN,
    "color": WHITE,
    "borderRadius": "10px",
    "padding": "5px",
    "margin": "1px 10px 10px 10px",
    "width": "90%",
    "textAlign": "center",
}
