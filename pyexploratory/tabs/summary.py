"""
Summary tab layout builder.

Renders per-column summary cards with statistics and distribution charts.
"""

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dash_table, dcc, html

from pyexploratory.components.tables import (
    SUMMARY_TABLE_STYLE,
    TABLE_CELL_STYLE,
    TABLE_HEADER_STYLE,
)
from pyexploratory.config import DARK_GREEN, LIGHT_BLUE, WHITE
from pyexploratory.core.data_store import read_data


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

    cards = []
    for col in df.columns:
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
                    "{:.2f}%".format((df[col].isnull().sum() / len(df[col])) * 100),
                ],
            }
        )

        summary = pd.concat([summary, additional_stats], ignore_index=True)

        summary_table = dash_table.DataTable(
            data=summary.to_dict("records"),
            columns=[{"name": i, "id": i} for i in summary.columns],
            style_data={"whiteSpace": "normal", "height": "auto"},
            style_cell=TABLE_CELL_STYLE,
            style_header=TABLE_HEADER_STYLE,
            style_table=SUMMARY_TABLE_STYLE,
            fill_width=False,
        )

        if pd.api.types.is_numeric_dtype(df[col]):
            card_content = dbc.Card(
                dbc.CardBody(
                    [
                        html.H4(col, className="card-title"),
                        dcc.Graph(
                            figure=px.histogram(
                                df,
                                x=col,
                                title=f"Distribution of {col}",
                                template="seaborn",
                            )
                        ),
                        summary_table,
                    ]
                ),
                style={"backgroundColor": WHITE, "color": "black", "margin": "10px"},
            )
        else:
            data = df[col].value_counts().reset_index()
            data.columns = [col, "count"]
            card_content = dbc.Card(
                dbc.CardBody(
                    [
                        html.H4(col, className="card-title"),
                        dcc.Graph(
                            figure=px.bar(
                                data,
                                x=col,
                                y="count",
                                title=f"Distribution of {col}",
                                template="seaborn",
                                color_discrete_sequence=[LIGHT_BLUE],
                            )
                        ),
                        summary_table,
                    ]
                ),
                style={"backgroundColor": WHITE, "color": "black"},
            )

        cards.append(dbc.Col([dbc.Card(card_content, className="mb-3")], md=4))

    return html.Div(dbc.Row(cards))
