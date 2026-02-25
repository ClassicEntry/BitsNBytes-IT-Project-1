"""
Summary tab layout builder.

Renders overview metrics row and per-column summary cards
with statistics and distribution charts.
"""

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dash_table, dcc, html

from pyexploratory.components.tables import (
    SUMMARY_DARK_CELL_STYLE,
    SUMMARY_DARK_HEADER_STYLE,
    SUMMARY_TABLE_STYLE,
)
from pyexploratory.config import PRIMARY, SECTION_CARD_STYLE, TEXT_MUTED, TEXT_SECONDARY
from pyexploratory.core.data_store import read_data


def _metric_tile(label: str, value: str) -> dbc.Col:
    """Build a single KPI tile for the overview row."""
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        label,
                        style={
                            "color": TEXT_MUTED,
                            "fontSize": "13px",
                            "marginBottom": "4px",
                        },
                    ),
                    html.Div(
                        value,
                        style={
                            "color": PRIMARY,
                            "fontSize": "24px",
                            "fontWeight": "700",
                        },
                    ),
                ]
            ),
            style={**SECTION_CARD_STYLE, "textAlign": "center"},
        ),
        xs=6,
        sm=6,
        lg=3,
    )


def render() -> html.Div:
    """Build the Summary tab content."""
    try:
        df = read_data()
    except FileNotFoundError:
        return html.Div(
            dbc.Alert(
                "Data file not found. Please upload data in the drop box.",
                color="warning",
            )
        )

    # --- Overview metrics row ---
    total_rows = len(df)
    total_cols = len(df.columns)
    missing_pct = (
        f"{(df.isnull().sum().sum() / (total_rows * total_cols)) * 100:.1f}%"
        if total_rows > 0
        else "0%"
    )
    memory_mb = f"{df.memory_usage(deep=True).sum() / (1024 * 1024):.2f} MB"

    overview = dbc.Row(
        [
            _metric_tile("Total Rows", f"{total_rows:,}"),
            _metric_tile("Total Columns", str(total_cols)),
            _metric_tile("Missing Values", missing_pct),
            _metric_tile("Memory Usage", memory_mb),
        ],
        className="mb-3",
    )

    # --- Per-column cards (separated by type) ---
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    categorical_cols = [c for c in df.columns if c not in numeric_cols]

    def _build_column_card(col):
        summary = df[col].describe().reset_index()
        summary.columns = ["Statistic", "Value"]

        additional_stats = pd.DataFrame(
            {
                "Statistic": [
                    "Data Type",
                    "Missing Values",
                    "Missing Values (%)",
                ],
                "Value": [
                    str(df[col].dtype),
                    df[col].isnull().sum(),
                    "{:.2f}%".format(
                        (df[col].isnull().sum() / len(df[col])) * 100
                        if len(df[col]) > 0
                        else 0
                    ),
                ],
            }
        )
        summary = pd.concat([summary, additional_stats], ignore_index=True)

        summary_table = dash_table.DataTable(
            data=summary.to_dict("records"),
            columns=[{"name": i, "id": i} for i in summary.columns],
            style_data={"whiteSpace": "normal", "height": "auto"},
            style_cell=SUMMARY_DARK_CELL_STYLE,
            style_header=SUMMARY_DARK_HEADER_STYLE,
            style_table=SUMMARY_TABLE_STYLE,
            fill_width=False,
        )

        if pd.api.types.is_numeric_dtype(df[col]):
            fig = px.histogram(
                df,
                x=col,
                title=f"Distribution of {col}",
                template="plotly_dark",
            )
        else:
            data = df[col].value_counts().reset_index()
            data.columns = [col, "count"]
            fig = px.bar(
                data,
                x=col,
                y="count",
                title=f"Distribution of {col}",
                template="plotly_dark",
                color_discrete_sequence=[PRIMARY],
            )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=40, b=10),
        )

        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H5(
                        col,
                        style={
                            "color": PRIMARY,
                            "fontWeight": "600",
                            "marginBottom": "12px",
                        },
                    ),
                    dcc.Graph(figure=fig, config={"displayModeBar": False}),
                    summary_table,
                ]
            ),
            style=SECTION_CARD_STYLE,
        )
        return dbc.Col(card, xs=12, sm=6, lg=4, xl=3, className="mb-3")

    _section_header_style = {
        "color": TEXT_SECONDARY,
        "fontSize": "14px",
        "fontWeight": "600",
        "textTransform": "uppercase",
        "letterSpacing": "1px",
        "marginBottom": "12px",
        "marginTop": "8px",
        "paddingBottom": "6px",
        "borderBottom": "1px solid #3a3a3b",
    }

    sections = [overview]

    if numeric_cols:
        sections.append(html.Div(
            f"Numeric Columns ({len(numeric_cols)})",
            style=_section_header_style,
        ))
        sections.append(dbc.Row([_build_column_card(c) for c in numeric_cols]))

    if categorical_cols:
        sections.append(html.Div(
            f"Categorical Columns ({len(categorical_cols)})",
            style=_section_header_style,
        ))
        sections.append(dbc.Row([_build_column_card(c) for c in categorical_cols]))

    return html.Div(
        sections,
        style={"maxHeight": "70vh", "overflowY": "auto", "paddingRight": "4px"},
    )
