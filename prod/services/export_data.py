import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import io
import os

dash.register_page(__name__, path="/export_data", name="Data Export")

layout = html.Div(
    [
        dcc.Download(id="download-data"),
        html.Button("Download Data", id="btn-download", n_clicks=0),
    ]
)


@dash.callback(
    Output("download-data", "data"),
    Input("btn-download", "n_clicks"),
    prevent_initial_call=True,
)
def download_data(n_clicks):
    if n_clicks:
        df = pd.read_csv("local_data.csv")
        return dcc.send_data_frame(df.to_excel, "mydata.xlsx")
