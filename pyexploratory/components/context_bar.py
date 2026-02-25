"""
Context bar layout builder.

Always-visible bar at the top of the main workspace showing dataset metadata.
"""

import os

from dash import html

from pyexploratory.config import (
    CONTEXT_BAR_STYLE,
    DATA_FILE,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


def render() -> html.Div:
    """Build the context bar showing current dataset info."""
    try:
        from pyexploratory.core.data_store import read_data

        df = read_data()
        filename = os.path.basename(DATA_FILE)
        rows = len(df)
        cols = len(df.columns)
        memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

        return html.Div(
            [
                html.Span(
                    [
                        "\U0001f4c4 ",
                        html.Span(
                            filename,
                            style={"color": TEXT_PRIMARY, "fontWeight": "500"},
                        ),
                    ],
                    className="context-bar-item",
                ),
                html.Span(
                    f"{rows:,} rows \u00d7 {cols} cols",
                    className="context-bar-item",
                ),
                html.Span(
                    f"{memory_mb:.1f} MB",
                    className="context-bar-item",
                ),
            ],
            id="context-bar",
            style=CONTEXT_BAR_STYLE,
        )
    except (FileNotFoundError, Exception):
        return html.Div(
            "No dataset loaded",
            id="context-bar",
            style={**CONTEXT_BAR_STYLE, "color": "#666666"},
        )
