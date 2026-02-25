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
# ---------------------------------------------------------------------------
# Colors — Design System v2
# ---------------------------------------------------------------------------
BG_DEEP = "#111113"
BG_SURFACE = "#1a1a1d"
BG_CARD = "#222226"
BG_HOVER = "#2a2a30"
BG_ACTIVE = "#333338"
PRIMARY = "#00c46a"
PRIMARY_DIM = "#00c46a33"
TEXT_PRIMARY = "#f0f0f0"
TEXT_SECONDARY = "#a0a0a0"
TEXT_MUTED_V2 = "#666666"
STEP_UPLOAD_COLOR = "#4a9eff"
STEP_CLEAN_COLOR = "#00c46a"
STEP_CHART_COLOR = "#ff9f43"
STEP_ML_COLOR = "#a855f7"
BORDER_COLOR = "#3a3a3b"
ERROR_COLOR = "#ff6b6b"
WARNING_COLOR = "#e67e22"
INFO_COLOR = "#3498db"

SIDEBAR_BG = BG_DEEP

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
# Upload limits
# ---------------------------------------------------------------------------
MAX_UPLOAD_SIZE_MB = 50

# ---------------------------------------------------------------------------
# ML defaults
# ---------------------------------------------------------------------------
KMEANS_DEFAULT_CLUSTERS = 3
KMEANS_RANDOM_STATE = 42
SVM_DEFAULT_KERNEL = "linear"
SVM_RANDOM_STATE = 42
DEFAULT_TEST_SIZE = 0.25
MESH_STEP_SIZE = 0.02
DT_DEFAULT_MAX_DEPTH = 5
DT_RANDOM_STATE = 42
RF_DEFAULT_ESTIMATORS = 100
RF_RANDOM_STATE = 42

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

# ---------------------------------------------------------------------------
# Card / UI enhancement styles
# ---------------------------------------------------------------------------
CARD_BG = BG_CARD
CARD_BORDER = BORDER_COLOR
TEXT_MUTED = TEXT_SECONDARY

SECTION_CARD_STYLE = {
    "backgroundColor": CARD_BG,
    "borderRadius": "12px",
    "border": f"1px solid {CARD_BORDER}",
    "padding": "20px",
    "marginBottom": "16px",
}

UPLOAD_STYLE = {
    "width": "80%",
    "height": "120px",
    "lineHeight": "40px",
    "borderWidth": "2px",
    "borderStyle": "dashed",
    "borderColor": LIGHT_GREEN,
    "borderRadius": "12px",
    "textAlign": "center",
    "margin": "20px auto",
    "backgroundColor": CARD_BG,
    "cursor": "pointer",
    "padding": "20px",
}

# ---------------------------------------------------------------------------
# Design System v2 — Layout styles
# ---------------------------------------------------------------------------
SIDEBAR_STYLE_V2 = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "200px",
    "padding": "20px 16px",
    "background": f"linear-gradient(180deg, {BG_DEEP}, #0d0d10)",
    "zIndex": 10,
    "overflowY": "auto",
    "borderRight": f"1px solid {BORDER_COLOR}",
}

CONTEXT_BAR_STYLE = {
    "background": f"linear-gradient(90deg, {BG_SURFACE}, #1e1e22)",
    "padding": "12px 20px",
    "borderBottom": f"1px solid {BORDER_COLOR}",
    "display": "flex",
    "alignItems": "center",
    "gap": "16px",
    "color": TEXT_SECONDARY,
    "fontSize": "13px",
    "fontFamily": "'Inter', sans-serif",
}

MAIN_WORKSPACE_STYLE = {
    "marginLeft": "200px",
    "marginRight": "280px",
    "minHeight": "100vh",
    "backgroundColor": BG_SURFACE,
    "padding": "0",
}

STEP_PANEL_STYLE = {
    "position": "fixed",
    "top": 0,
    "right": 0,
    "bottom": 0,
    "width": "280px",
    "background": f"linear-gradient(180deg, {BG_DEEP}, #0d0d10)",
    "borderLeft": f"1px solid {BORDER_COLOR}",
    "padding": "20px 12px",
    "overflowY": "auto",
    "zIndex": 10,
}

GLASS_CARD_STYLE = {
    "backgroundColor": "rgba(34, 34, 38, 0.8)",
    "backdropFilter": "blur(12px)",
    "WebkitBackdropFilter": "blur(12px)",
    "border": "1px solid rgba(255, 255, 255, 0.06)",
    "borderRadius": "8px",
    "padding": "16px",
    "marginBottom": "12px",
}

PRIMARY_BUTTON_STYLE = {
    "background": "linear-gradient(135deg, #00c46a, #00a85a)",
    "color": "white",
    "border": "none",
    "borderRadius": "6px",
    "padding": "8px 20px",
    "fontWeight": "600",
    "cursor": "pointer",
    "fontFamily": "'Inter', sans-serif",
    "fontSize": "13px",
    "transition": "all 0.15s ease",
}

GHOST_BUTTON_STYLE = {
    "backgroundColor": "transparent",
    "color": TEXT_SECONDARY,
    "border": f"1px solid {BORDER_COLOR}",
    "borderRadius": "6px",
    "padding": "8px 16px",
    "fontWeight": "500",
    "cursor": "pointer",
    "fontFamily": "'Inter', sans-serif",
    "fontSize": "13px",
    "transition": "all 0.15s ease",
}
