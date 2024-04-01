import dash
from dash import html, dcc

dash.register_page(__name__, path="/", name="Dashboard", order=4)


# -----------------------Page Layout-----------------------

layout = html.Div(
    [
        html.Br(),
        html.P("Dashboard", className="text-dark text-center fw-bold fs-1"),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id="example-graph",
                            figure={
                                "data": [
                                    {
                                        "x": [1, 2, 3],
                                        "y": [4, 1, 2],
                                        "type": "bar",
                                        "name": "SF",
                                    },
                                    {
                                        "x": [1, 2, 3],
                                        "y": [2, 4, 5],
                                        "type": "bar",
                                        "name": "Montréal",
                                    },
                                ],
                                "layout": {"title": "Dash Data Visualization"},
                            },
                        ),
                    ],
                    className="col-6",
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="example-graph-2",
                                figure={
                                    "data": [
                                        {
                                            "labels": ["SF", "Montréal"],
                                            "values": [1, 2],
                                            "type": "pie",
                                            "name": "Cities",
                                        },
                                    ],
                                    "layout": {"title": "Data Visualization"},
                                },
                        ),
                    ],
                    className="col-6",
                ),
            ],
            className="row",
        ),
    ],
    className="col-8 mx-auto",
)
