import dash
import datetime
import base64
import pandas as pd
import numpy as np
import io
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
from scipy import stats
from sklearn.preprocessing import MinMaxScaler



dash.register_page(
    __name__,
    path="/import_data",
    name="Import Data",
    order=2,
)


def get_layout():
    """
    Returns the layout for the import data page.
    """
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
            html.Div(
                [
                    html.Label("Data Cleaning Options:"),
                    dcc.Input(id='column-to-clean', type='text', placeholder='Column to clean...'),
                    dcc.Dropdown(
                        id='cleaning-operation',
                        options=[
                            {'label': 'Strip spaces (left)', 'value': 'lstrip'},
                            {'label': 'Strip spaces (right)', 'value': 'rstrip'},
                            {'label': 'Remove non-alphanumeric characters', 'value': 'alnum'},
                            {'label': 'Drop NA', 'value': 'dropna'},
                            {'label': 'Fill NA', 'value': 'fillna'},
                            {'label': 'Convert to Numeric', 'value': 'to_numeric'},
                            {'label': 'Convert to String', 'value': 'to_string'},
                            {'label': 'Convert to DateTime', 'value': 'to_datetime'},
                            {'label': 'Convert to Lowercase', 'value': 'lowercase'},
                            {'label': 'Convert to Uppercase', 'value': 'uppercase'},
                            {'label': 'Trim Whitespace', 'value': 'trim'},
                            {'label': 'Drop Column', 'value': 'drop_column'},
                            {'label': 'Rename Column', 'value': 'rename_column'},
                            {'label': 'Normalize', 'value': 'normalize'},
                            {'label': 'Remove Outliers', 'value': 'remove_outliers'},
                            {'label': 'Drop Duplicates', 'value': 'drop_duplicates'},
                            # Add more options here as needed
                        ],
                        value='lstrip'
                    ),
                    dcc.Input(id='fill-value', type='text', placeholder='Value to fill NA with...'),
                    dcc.Input(id='new-column-name', type='text', placeholder='New column name...'),  # Added line
                    html.Button('Apply Cleaning', id='clean-data-btn', n_clicks=0),
                    html.Div(id='cleaning-result')  # Placeholder for showing cleaning results or status
                ],
                className="row"
            ),
        ],
        className="col-8 mx-auto",
    )
    return layout



layout = get_layout()


def parse_contents(contents, filename, date, column_to_clean=None, operation=None):
    """
    Parse the contents of an uploaded file.

    Parameters:
    - contents (str): The contents of the uploaded file.
    - filename (str): The name of the uploaded file.
    - date (int): The last modified date of the uploaded file.

    Returns:
    - html.Div: A Div element containing the parsed contents of the file.
    """
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except FileNotFoundError as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    # Data cleaning logic
    if column_to_clean and column_to_clean in df.columns:
        if operation == 'lstrip':
            df[column_to_clean] = df[column_to_clean].str.lstrip()
        elif operation == 'rstrip':
            df[column_to_clean] = df[column_to_clean].str.rstrip()
        elif operation == 'alnum':
            df[column_to_clean] = df[column_to_clean].str.replace('[^a-zA-Z0-9]','', regex=True)

    # Save the DataFrame to a CSV file
    df.to_csv("local_data.csv", index=False)

    return html.Div(
        [
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),
            dash_table.DataTable(
                df.to_dict("records"), [{"name": i, "id": i} for i in df.columns]
            ),
            html.Hr(),  # horizontal line
            # For debugging, display the raw contents provided by the web browser
            html.Div("Raw Content"),
            html.Pre(
                contents[0:200] + "...",
                style={"whiteSpace": "pre-wrap", "wordBreak": "break-all"},
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
    else:
        return []  # Fix the return statement



@dash.callback(
    Output('cleaning-result', 'children'),
    Input('clean-data-btn', 'n_clicks'),
    State('column-to-clean', 'value'),
    State('cleaning-operation', 'value'),
    State('fill-value', 'value'),
    State('new-column-name', 'value'),
    prevent_initial_call=True
)
def apply_data_cleaning(n_clicks, column_to_clean, operation, fill_value=None, new_column_name=None):
    if n_clicks > 0:
        df = pd.read_csv("local_data.csv")
        
        if column_to_clean in df.columns:
            if operation == 'lstrip':
                df[column_to_clean] = df[column_to_clean].str.lstrip()
            elif operation == 'rstrip':
                df[column_to_clean] = df[column_to_clean].str.rstrip()
            elif operation == 'alnum':
                df[column_to_clean] = df[column_to_clean].str.replace('[^a-zA-Z0-9]', '', regex=True)
            elif operation == 'dropna':
                df = df.dropna(subset=[column_to_clean])
            elif operation == 'fillna':
                if fill_value is None:
                    if df[column_to_clean].dtype == 'object':
                        fill_value = df[column_to_clean].mode()[0]
                    else:
                        fill_value = df[column_to_clean].mean()
                df[column_to_clean] = df[column_to_clean].fillna(fill_value)
            elif operation == 'to_numeric':
                df[column_to_clean] = pd.to_numeric(df[column_to_clean], errors='coerce')
            elif operation == 'to_string':
                df[column_to_clean] = df[column_to_clean].astype(str)
            elif operation == 'to_datetime':
                df[column_to_clean] = pd.to_datetime(df[column_to_clean], errors='coerce')
            elif operation == 'lowercase':
                df[column_to_clean] = df[column_to_clean].str.lower()
            elif operation == 'uppercase':
                df[column_to_clean] = df[column_to_clean].str.upper()
            elif operation == 'trim':
                df[column_to_clean] = df[column_to_clean].str.strip()
            elif operation == 'drop_column':
                df = df.drop(columns=[column_to_clean])
            elif operation == 'rename_column':
                df = df.rename(columns={column_to_clean: new_column_name})
            elif operation == 'normalize':
                scaler = MinMaxScaler()
                df[column_to_clean] = scaler.fit_transform(df[[column_to_clean]])
            elif operation == 'remove_outliers':
                df = df[(np.abs(stats.zscore(df[column_to_clean])) < 3)]
            elif operation == 'drop_duplicates':
                df = df.drop_duplicates(subset=[column_to_clean])

            df.to_csv("local_data.csv", index=False)
            return "Data cleaning applied and saved."
    return "No cleaning applied or column not found."
