"""
Introduction page — welcome screen for PyExploratory.
"""

import dash
from dash import html

from pyexploratory.config import BG_SURFACE, PRIMARY, TEXT_PRIMARY, TEXT_SECONDARY

dash.register_page(
    __name__,
    path="/",
    name="Introduction",
    order=1,
)


def _step_item(number: str, title: str, description: str) -> html.Div:
    """Render a single getting-started step."""
    return html.Div(
        [
            html.Div(
                number,
                style={
                    "width": "32px",
                    "height": "32px",
                    "borderRadius": "50%",
                    "background": f"linear-gradient(135deg, {PRIMARY}, #00a85a)",
                    "color": "white",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "fontSize": "14px",
                    "fontWeight": "700",
                    "flexShrink": "0",
                },
            ),
            html.Div(
                [
                    html.Span(title, style={"color": TEXT_PRIMARY, "fontWeight": "600", "fontSize": "14px"}),
                    html.Span(
                        f" — {description}",
                        style={"color": TEXT_SECONDARY, "fontSize": "14px"},
                    ),
                ],
            ),
        ],
        style={
            "display": "flex",
            "alignItems": "center",
            "gap": "16px",
            "padding": "12px 0",
            "borderBottom": "1px solid #3a3a3b",
            "textAlign": "left",
        },
    )


layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "PyExploratory",
                    style={
                        "color": TEXT_PRIMARY,
                        "fontWeight": "700",
                        "fontSize": "48px",
                        "fontFamily": "'Inter', sans-serif",
                        "marginBottom": "24px",
                    },
                ),
                html.P(
                    "An interactive data analysis app built with Python, Dash, and Plotly. "
                    "Import data, clean it, visualize it, and run machine learning tasks.",
                    style={
                        "color": TEXT_SECONDARY,
                        "fontSize": "18px",
                        "lineHeight": "1.6",
                        "maxWidth": "600px",
                        "marginBottom": "32px",
                    },
                ),
                html.Div(
                    [
                        _step_item("1", "Upload", "Import a CSV, Excel, or JSON file from the Data Analysis page"),
                        _step_item("2", "Explore", "View summary stats, edit data in the table, and clean with 18 operations"),
                        _step_item("3", "Visualize", "Build from 14 chart types including scatter, heatmap, and treemap"),
                        _step_item("4", "Analyze", "Run KMeans, SVM, Decision Tree, Random Forest, or Linear Regression"),
                        _step_item("5", "Export", "Download your data or export your session as a replayable Python script"),
                    ],
                    style={"maxWidth": "600px"},
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "justifyContent": "center",
                "textAlign": "center",
                "padding": "80px 40px",
                "minHeight": "100vh",
            },
        ),
    ],
    style={"backgroundColor": BG_SURFACE, "minHeight": "100vh"},
)
