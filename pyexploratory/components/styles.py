"""
Shared component styles for buttons, inputs, and dropdowns.

Import from here rather than duplicating inline dicts.
"""

from pyexploratory.config import (
    DARK_GREEN,
    DROPDOWN_STYLE,
    GREEN_BUTTON_STYLE,
    INPUT_STYLE,
    WHITE,
)

# Re-export for convenience
__all__ = [
    "GREEN_BUTTON_STYLE",
    "DROPDOWN_STYLE",
    "INPUT_STYLE",
    "SAVE_BUTTON_STYLE",
    "DOWNLOAD_BUTTON_STYLE",
    "CLEAN_BUTTON_STYLE",
]

SAVE_BUTTON_STYLE = {
    **GREEN_BUTTON_STYLE,
    "margin": "1px 0px 0px 10px",
    "width": "90%",
}

DOWNLOAD_BUTTON_STYLE = {
    **GREEN_BUTTON_STYLE,
    "margin": "10px 10px 0px 0px",
    "width": "100%",
}

CLEAN_BUTTON_STYLE = {
    **GREEN_BUTTON_STYLE,
    "margin": "1px 10px 10px 10px",
    "width": "90%",
}
