"""
This file imports data within the Dash application.

The file defines the layout and functionality for the "Import data" page in the Dash application. 
It provides options to upload files, perform data cleaning operations on the uploaded data, 
and display the parsed contents of the file.

Author: BitNBytes
"""

import datetime
import base64
import io
import dash
import json
import pandas as pd
import numpy as np
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
import os


dash.register_page(
    __name__,
    path="/import_data",
    name="Import Data",
    order=2,
<<<<<<< HEAD
)

# -----------------------Page Layout-----------------------
layout = html.Div(
    [
        html.P("Import Data", className="text-dark text-left fw-bold fs-1"),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Select File"),
                        dcc.Upload(
                            id="upload-data",
                            children=html.Div(
                                ["Drag and Drop or ", html.A("Select Files")]
                            ),
                            style={
                                "width": "100%",
                                "height": "60px",
                                "lineHeight": "60px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "textAlign": "center",
                                "margin": "10px",
                            },
                            multiple=True,
                        ),
                    ],
                    className="col-6",
                ),
            ],
            className="row",
        ),
        html.Div(id="output-data-upload"),
    ],
    className="col-8 mx-auto",
)


def parse_contents(contents, filename, date):
=======
)


def get_layout():
    """
    Returns the layout for the import data page.

    Returns:
        layout (dash.html.Div): The layout for the import data page.
    """
    layout = html.Div(
        [
            html.H1("Import Data", className="text-dark text-center fw-bold fs-1"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Select File:"),
                            dcc.Upload(
                                id="upload-data",
                                children=html.Div(
                                    ["Drag and Drop or ", html.A("Select Files")]
                                ),
                                style={
                                    "width": "100%",
                                    "height": "60px",
                                    "lineHeight": "60px",
                                    "borderWidth": "1px",
                                    "borderStyle": "dashed",
                                    "borderRadius": "5px",
                                    "textAlign": "center",
                                    "margin": "10px",
                                },
                                multiple=True,
                            ),
                        ],
                    ),
                ],
                className="row",
            ),
            html.Div(id="output-data-upload"),
            html.Div(
                [
                    html.Label("Data Cleaning Options:"),
                    dcc.Input(
                        id="column-to-clean",
                        type="text",
                        placeholder="Column to clean...",
                    ),
                    dcc.Dropdown(
                        id="cleaning-operation",
                        options=[
                            {"label": "Strip value (left)", "value": "lstrip"},
                            {"label": "Strip value (right)", "value": "rstrip"},
                            {
                                "label": "Remove non-alphanumeric characters",
                                "value": "alnum",
                            },
                            {"label": "Drop NA", "value": "dropna"},
                            {"label": "Fill NA", "value": "fillna"},
                            {"label": "Convert to Numeric", "value": "to_numeric"},
                            {"label": "Convert to String", "value": "to_string"},
                            {"label": "Convert to DateTime", "value": "to_datetime"},
                            {"label": "Convert to Lowercase", "value": "lowercase"},
                            {"label": "Convert to Uppercase", "value": "uppercase"},
                            {"label": "Trim Whitespace", "value": "trim"},
                            {"label": "Drop Column", "value": "drop_column"},
                            {"label": "Rename Column", "value": "rename_column"},
                            {"label": "Normalize", "value": "normalize"},
                            {"label": "Remove Outliers", "value": "remove_outliers"},
                            {"label": "Drop Duplicates", "value": "drop_duplicates"},
                        ],
                        placeholder="Select Cleaning Operation...",
                        style={"margin-top": "10px"},
                    ),
                    dcc.Input(
                        id="fill-value",
                        type="text",
                        placeholder="Value to apply to cleaning operation/fill NA with...",
                        style={"margin-top": "10px"},
                    ),
                    dcc.Input(
                        id="new-column-name",
                        type="text",
                        placeholder="New column name...",
                        style={"margin-top": "10px"},
                    ),
                    html.Button(
                        "Apply Cleaning",
                        id="clean-data-btn",
                        n_clicks=0,
                        style={"margin-top": "10px"},
                    ),
                    html.Div(id="cleaning-result"),
                ],
                className="row",
            ),
        ],
        className="col-8 mx-auto",
    )
    return layout


layout = get_layout()


def parse_contents(contents, filename, date):
    """
    Parse the contents of an uploaded file.

    Parameters:
    - contents (str): The contents of the uploaded file.
    - filename (str): The name of the uploaded file.
    - date (int): The last modified date of the uploaded file.

    Returns:
    - html.Div: A Div element containing the parsed contents of the file.
    """
>>>>>>> 7ce10ef287e2b18a419c2c9f26a378b9c9bc282a
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    extension = os.path.splitext(filename)[1].lower()
    try:
<<<<<<< HEAD
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

        # Save the DataFrame to a CSV file
=======
        if extension == ".csv":
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif extension in [".xlsx", ".xls"]:
            df = pd.read_excel(io.BytesIO(decoded))
        elif extension == ".json":
            json_str = decoded.decode("utf-8")
            json_data = json.loads(json_str)
            df = pd.json_normalize(json_data)
        else:
            raise ValueError("Unsupported file extension")
    except FileNotFoundError as e:
        print(f"Error processing the file {filename}: {e}")
        return html.Div(["There was an error processing this file."])

>>>>>>> 7ce10ef287e2b18a419c2c9f26a378b9c9bc282a
    df.to_csv("local_data.csv", index=False)

    return html.Div(
        [
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),
            dash_table.DataTable(
<<<<<<< HEAD
                df.to_dict("records"), [{"name": i, "id": i} for i in df.columns],
                style_table={'overflowX': 'auto'},
                style_cell={
                    # all three widths are needed
                    'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                }
            ),
            html.Hr(),  # horizontal line
            # For debugging, display the raw contents provided by the web browser
            html.Div("Raw Content"),
            html.Pre(
                contents[0:200] + "...",
                style={"whiteSpace": "pre-wrap", "wordBreak": "break-all"},
=======
                data=df.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df.columns],
                page_action="native",
                page_size=50,
                style_table={
                    "overflowX": "scroll",
                },
                style_cell={
                    "whiteSpace": "normal",
                    "height": "auto",
                },
>>>>>>> 7ce10ef287e2b18a419c2c9f26a378b9c9bc282a
            ),
        ]
    )


@dash.callback(
    Output("output-data-upload", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    """
    Update the output based on the uploaded files.

    Parameters:
    - list_of_contents (list): A list of file contents.
    - list_of_names (list): A list of file names.
    - list_of_dates (list): A list of last modified dates.

    Returns:
    - list: A list of Div elements containing the parsed contents of the files.
    """
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d)
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children
<<<<<<< HEAD
=======
    else:
        return []


@dash.callback(
    Output("cleaning-result", "children"),
    Input("clean-data-btn", "n_clicks"),
    State("column-to-clean", "value"),
    State("cleaning-operation", "value"),
    State("fill-value", "value"),
    State("new-column-name", "value"),
    prevent_initial_call=True,
)
def apply_data_cleaning(
    n_clicks, column_to_clean, operation, fill_value=None, new_column_name=None
):
    """
    Apply data cleaning operations on a specified column of a DataFrame.

    Parameters:
    - n_clicks (int): The number of times the "clean-data-btn" button has been clicked.
    - column_to_clean (str): The name of the column to be cleaned.
    - operation (str): The data cleaning operation to be applied.
    - fill_value (optional): The value to fill missing values with (default: None).
    - new_column_name (optional): The new name for the column after renaming (default: None).

    Returns:
    - str: A message indicating whether the data cleaning was applied and saved or not.

    """
    if n_clicks > 0:
        df = pd.read_csv("local_data.csv")

        if column_to_clean in df.columns:
            if operation == "lstrip":
                df[column_to_clean] = df[column_to_clean].str.lstrip(fill_value)
            elif operation == "rstrip":
                df[column_to_clean] = df[column_to_clean].str.rstrip(fill_value)
            elif operation == "alnum":
                df[column_to_clean] = df[column_to_clean].str.replace(
                    "[^a-zA-Z0-9]", "", regex=True
                )
            elif operation == "dropna":
                df[column_to_clean] = (
                    df[column_to_clean].dropna().reset_index(drop=True)
                )
            elif operation == "fillna":
                if fill_value is None:
                    if df[column_to_clean].dtype == "object":
                        fill_value = df[column_to_clean].mode()[0]
                    else:
                        fill_value = df[column_to_clean].mean()
                df[column_to_clean] = df[column_to_clean].fillna(fill_value)
            elif operation == "to_numeric":
                df[column_to_clean] = pd.to_numeric(
                    df[column_to_clean], errors="coerce"
                )
            elif operation == "to_string":
                df[column_to_clean] = df[column_to_clean].astype(str)
            elif operation == "to_datetime":
                df[column_to_clean] = pd.to_datetime(
                    df[column_to_clean], errors="coerce"
                )
            elif operation == "lowercase":
                df[column_to_clean] = df[column_to_clean].str.lower()
            elif operation == "uppercase":
                df[column_to_clean] = df[column_to_clean].str.upper()
            elif operation == "trim":
                df[column_to_clean] = df[column_to_clean].str.strip()
            elif operation == "drop_column":
                df = df.drop(columns=[column_to_clean])
            elif operation == "rename_column":
                df = df.rename(columns={column_to_clean: new_column_name})
            elif operation == "normalize":
                # Convert column to numeric, coercing errors
                df[column_to_clean] = pd.to_numeric(
                    df[column_to_clean], errors="coerce"
                )
                df[column_to_clean] = df[column_to_clean].fillna(
                    0
                )  # Replace NaNs with 0 for scaling
                scaler = MinMaxScaler()
                df[column_to_clean] = scaler.fit_transform(df[[column_to_clean]])
            elif operation == "remove_outliers":
                # Convert column to numeric, coercing errors
                df[column_to_clean] = pd.to_numeric(
                    df[column_to_clean], errors="coerce"
                )
                # Calculate z-scores, exclude NaNs
                z_scores = np.abs(stats.zscore(df[column_to_clean].dropna()))
                # Create a full-length boolean mask
                full_mask = df[
                    column_to_clean
                ].notna()  # Create a mask for non-NaN values
                full_mask.loc[df[column_to_clean].notna()] = (
                    z_scores >= 3
                )  # Apply the z-score mask
                # Set outliers to None
                df.loc[full_mask, column_to_clean] = None
            elif operation == "drop_duplicates":
                df[column_to_clean] = (
                    df[column_to_clean].drop_duplicates().reset_index(drop=True)
                )

            df.to_csv("local_data.csv", index=False)
            return "Data cleaning applied and saved."
    return "No cleaning applied or column not found."
>>>>>>> 7ce10ef287e2b18a419c2c9f26a378b9c9bc282a
