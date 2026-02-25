"""
Shared component styles for buttons, inputs, and dropdowns.

Import from here rather than duplicating inline dicts.
"""

from pyexploratory.config import (
    DARK_GREEN,
    DROPDOWN_STYLE,
    GHOST_BUTTON_STYLE,
    GREEN_BUTTON_STYLE,
    INPUT_STYLE,
    PRIMARY_BUTTON_STYLE,
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
    "PRIMARY_BUTTON_STYLE",
    "GHOST_BUTTON_STYLE",
]

SAVE_BUTTON_STYLE = {**PRIMARY_BUTTON_STYLE, "width": "auto"}
DOWNLOAD_BUTTON_STYLE = {**PRIMARY_BUTTON_STYLE, "width": "100%", "marginBottom": "8px"}
CLEAN_BUTTON_STYLE = {**PRIMARY_BUTTON_STYLE, "width": "auto"}
