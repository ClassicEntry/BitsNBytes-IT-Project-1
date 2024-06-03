"""
This file controls the data analysis within the Dash application.

The file defines the layout and functionality for the "Data Analysis" page in 
the Dash application. 
It includes tabs for displaying summary statistics, a table view of the data, 
and various charts based on the user's selection.

Author: BitNBytes
"""

import base64
import io
import json
import time
import datetime
import os
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from scipy import stats

# Set environment variable to avoid memory leak issue with KMeans
os.environ["OMP_NUM_THREADS"] = "1"


# Register the page with Dash
dash.register_page(
    __name__,
    path="/data_analysis",
    name="Data Analysis",
    order=3,
)

# Define the styles
tab_style = {
    "backgroundColor": "#007BFF",
    "color": "white",
    "borderRadius": "15px",
    "margin": "10px",
}

selected_tab_style = {
    "backgroundColor": "#003366",
    "color": "white",
    "borderRadius": "15px",
    "margin": "10px",
}

# Define the layout of the page
layout = html.Div(
    [
        html.H1("Data Analysis", className="text-light text-center fw-bold fs-1"),
        dcc.Location(id="refresh", refresh=True),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Upload(
                            id="upload-data",
                            children=html.Div(
                                [
                                    "Drag and Drop or ",
                                    html.A("Select Files", style={"color": "white"}),
                                ],
                                style={"color": "white"},
                            ),
                            style={
                                "width": "50%",
                                "height": "60px",
                                "lineHeight": "60px",
                                "borderWidth": "3px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "textAlign": "center",
                                "margin": "10px auto",
                            },
                            multiple=True,
                        ),
                    ],
                ),
            ],
            className="row",
        ),
        html.Div(id="output-data-upload"),
        dcc.Tabs(
            id="tabs",
            value="tab-summary",
            children=[
                dcc.Tab(
                    label="Summary",
                    value="tab-summary",
                    style=tab_style,
                    selected_style=selected_tab_style,
                ),
                dcc.Tab(
                    label="Table",
                    value="tab-table",
                    style=tab_style,
                    selected_style=selected_tab_style,
                ),
                dcc.Tab(
                    label="Machine Learning",
                    value="tab-machine-learning",
                    style=tab_style,
                    selected_style=selected_tab_style,
                ),
                dcc.Tab(
                    label="Charts",
                    value="tab-charts",
                    style=tab_style,
                    selected_style=selected_tab_style,
                ),
            ],
            style={
                "width": "50%",
                "margin": "0 auto",
                "padding": "5px",
            },
        ),
        html.Div(id="tabs-content", style={"padding": "20px"}),
    ],
    style={"backgroundColor": "#4c4d4d"},
)


@dash.callback(Output("tabs-content", "children"), Input("tabs", "value"))
def render_tab_content(tab):
    """
    Renders the content for the selected tab.

    Parameters:
    - tab (str): The value of the selected tab.

    Returns:
    - html.Div: The rendered content for the selected tab.
    """

    if tab == "tab-summary":
        try:
            # Read the data from the local_data.csv file
            df = pd.read_csv("local_data.csv")

            cards = []
            for col in df.columns:
                # Calculate summary statistics for the data
                summary = df[col].describe().reset_index()
                summary.columns = ["Statistic", "Value"]

                # Create a DataFrame for the additional statistics
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
                            ),
                        ],
                    }
                )

                # Concatenate the summary and additional_stats DataFrames
                summary = pd.concat([summary, additional_stats], ignore_index=True)

                # Create a DataTable component to display the summary statistics
                summary_table = dash_table.DataTable(
                    data=summary.to_dict("records"),
                    columns=[{"name": i, "id": i} for i in summary.columns],
                    style_data={
                        "whiteSpace": "normal",
                        "height": "auto",
                    },  # Wrap the cell content and adjust the cell height
                    style_cell={
                        "textAlign": "left",
                        "backgroundColor": "#1e2130",  # Set the cell background color to dark
                        "color": "white",  # Set the cell text color to white
                        "border": "1px solid white",  # Add a border to the cells
                    },
                    style_header={
                        "backgroundColor": "#007BFF",  # Set the header background color to blue
                        "fontWeight": "bold",  # Make the header text bold
                        "color": "white",  # Set the header text color to white
                    },
                    style_table={
                        "overflowX": "auto",  # Add a horizontal scrollbar if the content overflows
                        "maxHeight": "300px",  # Set a maximum height for the table
                        "overflowY": "auto",  # Add a vertical scrollbar if the content overflows
                    },
                    fill_width=False,
                )

                # Generate histograms for numeric columns and bar charts for categorical columns
                if pd.api.types.is_numeric_dtype(df[col]):
                    # Generate histogram for numerical data
                    card_content = dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(col, className="card-title"),
                                dcc.Graph(
                                    figure=px.histogram(
                                        df,
                                        x=col,
                                        title=f"Distribution of {col}",
                                        template="plotly_dark",
                                    )
                                ),
                                summary_table,  # Add the summary table here
                            ]
                        ),
                        className="mb-3",  # add some bottom margin for each card
                        style={
                            "backgroundColor": "#343A40",
                            "color": "white",
                        },  # Set the background color to dark and the text color to white
                    )
                else:
                    # Generate bar chart for categorical data
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
                                        template="plotly_dark",
                                    )
                                ),
                                summary_table,  # Add the summary table here
                            ]
                        ),
                        className="mb-3",  # add some bottom margin for each card
                        style={
                            "backgroundColor": "#343A40",
                            "color": "white",
                        },  # Set the background color to dark and the text color to white
                    )

                # Wrap the card content and summary table in a dbc.Col

                card = dbc.Col([dbc.Card(card_content, className="mb-3")], md=4)

                cards.append(card)
            # Wrap the cards in a dbc.Row
            cards_row = dbc.Row(cards)

            # Return the generated cards
            return html.Div(cards_row)

        except FileNotFoundError:
            # Return an error message if the data file is not found
            return html.Div("Data file not found. Please upload data in the drop box.")

    elif tab == "tab-table":

        try:
            # Read the data from the local_data.csv file
            df = pd.read_csv("local_data.csv")
            return html.Div(
                [
                    # Create a DataTable component to display the data as a table
                    dash_table.DataTable(
                        id="table",
                        data=df.to_dict("records"),
                        columns=[{"name": i, "id": i} for i in df.columns],
                        page_action="native",
                        page_size=50,
                        style_table={
                            "overflowX": "auto",
                            "padding": "10px",
                        },
                        style_cell={
                            "whiteSpace": "normal",
                            "height": "auto",
                            "textAlign": "left",
                            "backgroundColor": "#1e2130",  # Set the cell background color to dark
                            "color": "white",  # Set the cell text color to white
                            "border": "1px solid white",  # Add a border to the cells
                        },
                        style_header={
                            "backgroundColor": "#007BFF",  # Set the header background color to blue
                            "fontWeight": "bold",  # Make the header text bold
                            "color": "white",  # Set the header text color to white
                        },
                        editable=True,
                    ),
                    html.Div(
                        [
                            html.Button(
                                "Save Changes",
                                id="save-button",
                                style={
                                    "backgroundColor": "#007BFF",
                                    "color": "white",
                                    "borderRadius": "10px",
                                    "padding": "5px",
                                    "margin": "10px 10px 0px 0px",
                                    "width": "100%",
                                    "textAlign": "center",
                                },
                            ),
                            html.Div(
                                id="output-container-button",
                                children='Enter your inputs and press "Save Changes"',
                            ),
                        ]
                    ),
                    html.Div(
                        [
                            html.Label(
                                "Data Cleaning Options:", style={"color": "white"}
                            ),
                            dcc.Input(
                                id="column-to-clean",
                                type="text",
                                placeholder="Column to clean...",
                                style={
                                    "backgroundColor": "#007BFF",
                                    "color": "white",
                                    "borderRadius": "10px",
                                    "padding": "5px",
                                    "margin": "10px 10px 0px 0px",
                                    "width": "100%",
                                    "textAlign": "center",
                                },
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
                                    {
                                        "label": "Convert to Numeric",
                                        "value": "to_numeric",
                                    },
                                    {
                                        "label": "Convert to String",
                                        "value": "to_string",
                                    },
                                    {
                                        "label": "Convert to DateTime",
                                        "value": "to_datetime",
                                    },
                                    {
                                        "label": "Convert to Lowercase",
                                        "value": "lowercase",
                                    },
                                    {
                                        "label": "Convert to Uppercase",
                                        "value": "uppercase",
                                    },
                                    {"label": "Trim Whitespace", "value": "trim"},
                                    {"label": "Drop Column", "value": "drop_column"},
                                    {
                                        "label": "Rename Column",
                                        "value": "rename_column",
                                    },
                                    {"label": "Normalize", "value": "normalize"},
                                    {
                                        "label": "Remove Outliers",
                                        "value": "remove_outliers",
                                    },
                                    {
                                        "label": "Drop Duplicates",
                                        "value": "drop_duplicates",
                                    },
                                    {"label": "Sort Ascending", "value": "sort_asc"},
                                    {"label": "Sort Descending", "value": "sort_desc"},
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
                            # dcc.Location(id="refresh", refresh=True),
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
                ]
            )
        except FileNotFoundError:
            # Return an error message if the data file is not found
            return html.Div("Data file not found. Please upload data in the drop box.")

    elif tab == "tab-charts":
        # Read the data from the local_data.csv file
        df = pd.read_csv("local_data.csv")

        # Create options for the column dropdown based on the columns in the data
        column_options = [{"label": col, "value": col} for col in df.columns]

        # Return a Div component with dropdowns for chart type and column selection
        return html.Div(
            [
                html.H3("Chart Types", style={"color": "white"}),
                dcc.Dropdown(
                    id="chart-type-dropdown",
                    options=[
                        {"label": "Histogram", "value": "histogram"},
                        {"label": "Box Plot", "value": "boxplot"},
                        {"label": "Scatter Plot", "value": "scatter"},
                        {"label": "Line Plot", "value": "line"},
                        {"label": "Bar Chart", "value": "bar"},
                        {"label": "Pie Chart", "value": "pie"},
                    ],
                    value="",
                    placeholder="Select a chart type...",
                ),
                dcc.Dropdown(
                    id="column-dropdown",
                    options=column_options,
                    value="",
                    placeholder="Select a column...",
                    style={
                        "margin-top": "10px",
                    },
                ),
                html.Div(id="chart-container"),
            ]
        )
    # Add a new case in the render_tab_content function
    elif tab == "tab-machine-learning":
        # Read the data from the local_data.csv file
        df = pd.read_csv("local_data.csv")

        # Create options for the task and target variable dropdowns
        task_options = [
            {"label": "Clustering", "value": "clustering"},
            {"label": "Classification", "value": "classification"},
        ]
        # Get only categorical columns
        categorical_columns = df.select_dtypes(include=["object", "category"]).columns

        # Create options for target variable dropdown
        target_variable_options = [
            {"label": col, "value": col} for col in categorical_columns
        ]

        # Return a Div component with dropdowns for task and target variable selection
        return html.Div(
            [
                html.H1("Machine Learning Task Selector"),
                dcc.Dropdown(
                    id="task-dropdown",
                    options=task_options,
                    value="",
                    placeholder="Select a task...",
                ),
                dcc.Dropdown(
                    id="target-variable-dropdown",
                    options=target_variable_options,
                    value="",
                    style={"margin-top": "10px"},
                    placeholder="Select a target variable...",
                ),
                html.Div(id="ml-results"),
                dcc.Dropdown(
                    id="x-variable",
                    options=[{"label": i, "value": i} for i in df.columns],
                    value="",
                    placeholder="Select x-axis...",
                ),
                dcc.Dropdown(
                    id="y-variable",
                    options=[{"label": i, "value": i} for i in df.columns],
                    style={"margin-top": "10px"},
                    value="",
                    placeholder="Select y-axis...",
                ),
            ]
        )


@dash.callback(
    Output("chart-container", "children"),
    [Input("chart-type-dropdown", "value"), Input("column-dropdown", "value")],
    prevent_initial_call=True,
)
def update_chart(chart_type, column_name):
    """
    Update the chart based on the selected chart type and column name.

    Parameters:
    - chart_type (str): The selected chart type.
    - column_name (str): The selected column name.

    Returns:
    - chart_container (dash.html.Div or dcc.Graph): The updated chart container.
    """
    # Read the data from the local_data.csv file
    df = pd.read_csv("local_data.csv")
    if not column_name or column_name not in df.columns:
        return html.Div("Select a valid column.")
    if chart_type == "histogram":
        # Generate a histogram for the selected column
        return dcc.Graph(figure=px.histogram(df, x=column_name))
    elif chart_type == "boxplot":
        # Generate a box plot for the selected column
        return dcc.Graph(figure=px.box(df, y=column_name))
    elif chart_type == "scatter":
        # Create options for the scatter plot axes dropdowns based on the columns in the data
        column_options = [{"label": col, "value": col} for col in df.columns]
        return html.Div(
            [
                html.H3("Scatter plot axes"),
                dcc.Dropdown(id="x-axis-dropdown", options=column_options, value=""),
                dcc.Dropdown(
                    id="y-axis-dropdown",
                    options=column_options,
                    value="",
                    style={"margin-top": "10px"},
                ),
                html.Div(id="scatter-chart-container"),
            ]
        )
    elif chart_type == "line":
        # Generate a line plot for the selected column
        if pd.api.types.is_numeric_dtype(df[column_name]):
            return dcc.Graph(
                figure=px.line(
                    df, x=df.index, y=column_name, title=f"Line Plot of {column_name}"
                )
            )
        else:
            # For categorical columns
            data = df[column_name].value_counts().reset_index()
            data.columns = [column_name, "count"]
            return dcc.Graph(
                figure=px.line(
                    data, x=column_name, y="count", title=f"Line Plot of {column_name}"
                )
            )
    elif chart_type == "bar":
        if pd.api.types.is_numeric_dtype(df[column_name]):
            # For numeric columns, use binning
            bins = 10  # or any number of bins you want
            data = pd.cut(df[column_name], bins).value_counts().reset_index()
            data.columns = [column_name, "count"]
            data = data.sort_values(by=column_name)
            # Convert intervals to strings
            data[column_name] = data[column_name].astype(str)
            return dcc.Graph(
                figure=px.bar(
                    data,
                    x=column_name,
                    y="count",
                    title=f"Distribution of {column_name}",
                )
            )
        else:
            # For categorical columns
            data = df[column_name].value_counts().reset_index()
            data.columns = [column_name, "count"]
            return dcc.Graph(
                figure=px.bar(
                    data,
                    x=column_name,
                    y="count",
                    title=f"Distribution of {column_name}",
                )
            )
    elif chart_type == "pie":
        # Check if the column is numeric
        if pd.api.types.is_numeric_dtype(df[column_name]):
            return "Error: Pie chart cannot be created for numeric data"
        else:
            # Generate a pie chart for the selected column
            return dcc.Graph(
                figure=px.pie(
                    df, names=column_name, title=f"Pie chart of {column_name}"
                )
            )
    else:
        # Return an error message if no chart type is selected
        return html.Div("Select a chart type.")


@dash.callback(
    Output("scatter-chart-container", "children"),
    [Input("x-axis-dropdown", "value"), Input("y-axis-dropdown", "value")],
    prevent_initial_call=True,
)
def update_scatter_chart(x_axis, y_axis):
    """
    Update the scatter chart based on the selected x-axis and y-axis values.

    Parameters:
    - x_axis (str): The selected x-axis value.
    - y_axis (str): The selected y-axis value.

    Returns:
    - dash_html_components.Div: The scatter chart container with the updated scatter chart.
    """
    if not x_axis or not y_axis:
        return html.Div("Select valid x-axis and y-axis values.")
    df = pd.read_csv("local_data.csv")
    fig = px.scatter(df, x=x_axis, y=y_axis)
    return dcc.Graph(figure=fig)


@dash.callback(
    Output("ml-results", "children"),
    [
        Input("task-dropdown", "value"),
        Input("target-variable-dropdown", "value"),
        Input("x-variable", "value"),
        Input("y-variable", "value"),
    ],
    prevent_initial_call=True,
)
def perform_ml_task(task, target_variable, x_variable, y_variable):
    """
    Perform the selected machine learning task based on the user's selection.

    Parameters:
    - task (str): The selected machine learning task.
    - target_variable (str): The selected target variable.

    Returns:
    - html.Div: The results of the machine learning task.
    """
    # Read the data from the local_data.csv file
    try:
        df = pd.read_csv("local_data.csv")
    except FileNotFoundError:
        return html.Div("Data file not found. Please upload data in the drop box.")

    if target_variable not in df.columns:
        return html.Div("Target variable not found in the dataset.")

    if task == "clustering":
        try:
            # Remove the label column
            X = df.drop(columns=[target_variable])

            # Ensure all feature columns are numerical
            for col in X.columns:
                if X[col].dtype == "object":
                    label_encoder = LabelEncoder()
                    X[col] = label_encoder.fit_transform(X[col])

            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(
                X, df[target_variable], test_size=0.25, random_state=42
            )

            # Apply K-Means clustering
            kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
            kmeans.fit(X_train)

            # Predict clusters for training and testing sets
            train_clusters = kmeans.predict(X_train)
            test_clusters = kmeans.predict(X_test)

            # Map clusters to original class names based on majority voting
            cluster_labels = {}
            for i in range(3):
                mask = train_clusters == i
                cluster_labels[i] = y_train[mask].mode()[0]

            # Apply the mapping to the cluster labels
            train_cluster_names = pd.Series(train_clusters).map(cluster_labels)
            test_cluster_names = pd.Series(test_clusters).map(cluster_labels)

            # Visualization
            visuals = []
            if x_variable in X.columns and y_variable in X.columns:
                x_min, x_max = (
                    X_train[x_variable].min() - 1,
                    X_train[x_variable].max() + 1,
                )
                y_min, y_max = (
                    X_train[y_variable].min() - 1,
                    X_train[y_variable].max() + 1,
                )

                # Create plotly figure for training data
                fig_train = px.scatter(
                    x=X_train[x_variable],
                    y=X_train[y_variable],
                    color=train_cluster_names.astype(str),
                    title="Training Data Clusters",
                )
                fig_train.update_traces(
                    marker=dict(line=dict(width=0.5, color="DarkSlateGrey"))
                )
                visuals.append(dcc.Graph(figure=fig_train, id="train-plot"))

                # Create plotly figure for test data
                fig_test = px.scatter(
                    x=X_test[x_variable],
                    y=X_test[y_variable],
                    color=test_cluster_names.astype(str),
                    title="Test Data Clusters",
                )
                fig_test.update_traces(
                    marker=dict(line=dict(width=0.5, color="DarkSlateGrey"))
                )
                visuals.append(dcc.Graph(figure=fig_test, id="test-plot"))
            else:
                visuals = [
                    html.Div(
                        "Selected features for visualization are not in the dataset."
                    )
                ]

            return html.Div(
                [
                    html.H1("Clustering Results"),
                    dcc.Tabs(
                        [
                            dcc.Tab(
                                label="Training Set",
                                children=visuals[
                                    :1
                                ],  # Only include train-plot if available
                            ),
                            dcc.Tab(
                                label="Testing Set",
                                children=visuals[
                                    1:
                                ],  # Only include test-plot if available
                            ),
                        ]
                    ),
                ]
            )
        except Exception as e:
            return html.Div(f"Error in clustering: {str(e)}")

    elif task == "classification":
        try:
            # Initialize the label encoder
            label_encoder = LabelEncoder()
            # Encode the target variable if it's categorical
            if df[target_variable].dtype == "object":
                df[target_variable] = label_encoder.fit_transform(df[target_variable])
                target_names = label_encoder.classes_

            # Features and target
            X = df[[x_variable, y_variable]]
            y = df[target_variable]

            # Ensure all feature columns are numerical
            for col in X.columns:
                if X[col].dtype == "object":
                    X[col] = label_encoder.fit_transform(X[col])

            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.3, random_state=42
            )

            # Create an instance of the SVC class with a linear kernel
            svm_model = SVC(kernel="linear", C=1.0)

            # Fit the model to the training data
            svm_model.fit(X_train, y_train)

            # Predictions
            train_predictions = svm_model.predict(X_train)
            test_predictions = svm_model.predict(X_test)

            # Reverse the label encoding for the classification report
            y_train_names = label_encoder.inverse_transform(y_train)
            y_test_names = label_encoder.inverse_transform(y_test)
            train_predictions_names = label_encoder.inverse_transform(train_predictions)
            test_predictions_names = label_encoder.inverse_transform(test_predictions)

            # Classification reports
            train_report = classification_report(
                y_train_names,
                train_predictions_names,
                target_names=target_names,
                zero_division=0,
                output_dict=True,
            )
            test_report = classification_report(
                y_test_names,
                test_predictions_names,
                target_names=target_names,
                zero_division=0,
                output_dict=True,
            )

            # Visualization
            visuals = []
            if x_variable in X.columns and y_variable in X.columns:
                x_min, x_max = (
                    X_train[x_variable].min() - 1,
                    X_train[x_variable].max() + 1,
                )
                y_min, y_max = (
                    X_train[y_variable].min() - 1,
                    X_train[y_variable].max() + 1,
                )
                xx, yy = np.meshgrid(
                    np.arange(x_min, x_max, 0.01), np.arange(y_min, y_max, 0.01)
                )
                Z = svm_model.predict(np.c_[xx.ravel(), yy.ravel()])
                Z = Z.reshape(xx.shape)

                # Create plotly figure for training data
                fig_train = px.scatter(
                    x=X_train[x_variable],
                    y=X_train[y_variable],
                    color=pd.Series(y_train_names).astype(str),
                    title="Training Data",
                )
                fig_train.update_traces(
                    marker=dict(line=dict(width=0.5, color="DarkSlateGrey"))
                )
                fig_train.add_contour(
                    x=np.arange(x_min, x_max, 0.01),
                    y=np.arange(y_min, y_max, 0.01),
                    z=Z,
                    colorscale="Viridis",
                    opacity=0.3,
                )
                visuals.append(dcc.Graph(figure=fig_train, id="train-plot"))

                # Create plotly figure for test data
                fig_test = px.scatter(
                    x=X_test[x_variable],
                    y=X_test[y_variable],
                    color=pd.Series(y_test_names).astype(str),
                    title="Test Data",
                )
                fig_test.update_traces(
                    marker=dict(line=dict(width=0.5, color="DarkSlateGrey"))
                )
                fig_test.add_contour(
                    x=np.arange(x_min, x_max, 0.01),
                    y=np.arange(y_min, y_max, 0.01),
                    z=Z,
                    colorscale="Viridis",
                    opacity=0.3,
                )
                visuals.append(dcc.Graph(figure=fig_test, id="test-plot"))
            else:
                visuals = [
                    html.Div(
                        "Selected features for visualization are not in the dataset."
                    )
                ]

            return html.Div(
                [
                    html.H1("SVM Classification Report"),
                    dcc.Tabs(
                        [
                            dcc.Tab(
                                label="Training Set",
                                children=[
                                    html.Pre(
                                        id="train-report",
                                        children=json.dumps(train_report, indent=2),
                                    ),
                                    *visuals[
                                        :1
                                    ],  # Only include train-plot if available
                                ],
                            ),
                            dcc.Tab(
                                label="Testing Set",
                                children=[
                                    html.Pre(
                                        id="test-report",
                                        children=json.dumps(test_report, indent=2),
                                    ),
                                    *visuals[1:],  # Only include test-plot if available
                                ],
                            ),
                        ]
                    ),
                ]
            )
        except Exception as e:
            return html.Div(f"Error in classification: {str(e)}")

    return html.Div("Select a valid task.")


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
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    extension = os.path.splitext(filename)[1].lower()
    try:
        if extension == ".csv":
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif extension in [".xlsx", ".xls"]:
            df = pd.read_excel(io.BytesIO(decoded))
        elif extension == ".json":
            json_str = decoded.decode("utf-8")
            json_data = json.loads(json_str)
            df = pd.json_normalize(json_data)
        else:
            return html.H5(["Unsupported file extension"])
    except FileNotFoundError as e:
        print(f"Error processing the file {filename}: {e}")
        return html.H5(["There was an error processing this file."])

    df.to_csv("local_data.csv", index=False)

    return html.Div(
        [
            html.H5("Successfully imported " + filename),
            html.H6("Last Modified: " + str(datetime.datetime.fromtimestamp(date))),
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


@dash.callback(
    Output("refresh", "pathname"),
    [Input("upload-data", "contents")],
)
def refresh_page(contents):
    """
    Refreshes the page after a delay of 2 seconds.

    Args:
        contents: The contents of the page.

    Returns:
        The path to the refreshed page.

    """
    if contents is not None:
        time.sleep(2)
        return "./data_analysis"


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
            elif operation == "sort_asc":
                df = df.sort_values(by=column_to_clean, ascending=True)
            elif operation == "sort_desc":
                df = df.sort_values(by=column_to_clean, ascending=False)

            df.to_csv("local_data.csv", index=False)
            return "Data cleaning applied and saved."
    return "No cleaning applied or column not found."


@dash.callback(
    Output("table", "data"), Input("save-button", "n_clicks"), State("table", "data")
)
def save_changes(n_clicks, rows):
    """
    Save the changes made to the table data.

    Parameters:
    - n_clicks (int): The number of times the "save-button" has been clicked.
    - rows (list): The current data in the table.

    Returns:
    - list: The updated data in the table.
    """
    if n_clicks is not None and n_clicks > 0:
        pd.DataFrame(rows).to_csv("local_data.csv", index=False)
    return rows


@dash.callback(
    Output("output-container-button", "children"), [Input("save-button", "n_clicks")]
)
def save_table_data(n_clicks):
    """
    Saves the table data.

    Parameters:
    - n_clicks (int): The number of clicks.

    Returns:
    - str: A message indicating that the changes have been saved.
    """
    if n_clicks is not None:
        return "Changes have been saved."
