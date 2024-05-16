"""
This file controls the data analysis within the Dash application.

The file defines the layout and functionality for the "Data Analysis" page in 
the Dash application. 
It includes tabs for displaying summary statistics, a table view of the data, 
and various charts based on the user's selection.

Author: BitNBytes
"""

# Import necessary libraries
import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.decomposition import PCA

# Register the page with Dash
dash.register_page(__name__, path="/data_analysis", name="Data Analysis", order=3)

# Define the layout of the page
layout = html.Div(
    [
        html.H1("Data Analysis", className="text-dark text-center fw-bold fs-1"),
        dcc.Tabs(
            id="tabs",
            value="tab-summary",
            children=[
                dcc.Tab(
                    label="Summary",
                    value="tab-summary",
                    style={
                        "backgroundColor": "#007BFF",
                        "color": "white",
                        "borderRadius": "15px",
                        "margin": "10px",
                    },
                ),
                dcc.Tab(
                    label="Table",
                    value="tab-table",
                    style={
                        "backgroundColor": "#007BFF",
                        "color": "white",
                        "borderRadius": "15px",
                        "margin": "10px",
                    },
                ),
                dcc.Tab(
                    label="Charts",
                    value="tab-charts",
                    style={
                        "backgroundColor": "#007BFF",
                        "color": "white",
                        "borderRadius": "15px",
                        "margin": "10px",
                    },
                ),
                dcc.Tab(
                    label="Machine Learning",
                    value="tab-machine-learning",
                    style={
                        "backgroundColor": "#007BFF",
                        "color": "white",
                        "borderRadius": "15px",
                        "margin": "10px",
                    },
                ),
            ],
            style={
                "width": "50%",
                "margin": "auto",
                "padding": "10px",
                "backgroundColor": "#343A40",
            },  # Center the tabs, set their width to 50%, add some padding, and set the background color to dark
        ),
        html.Div(id="tabs-content"),
    ]
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

            # Generate histograms for numeric columns and bar charts for categorical columns
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    # Generate histogram for numeric data
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
                            ]
                        ),
                        className="mb-3",  # add some bottom margin for each card
                        style={
                            "backgroundColor": "#343A40",
                            "color": "white",
                        },  # Set the background color to dark and the text color to white
                    )

                # Calculate summary statistics for the data
                summary = df[col].describe().reset_index()
                summary["data_type"] = str(df[col].dtype)
                # show the missing values as a values and percentage in brackets
                summary["missing_values"] = df[col].isnull().sum()
                summary["missing_values_percentage"] = (
                    df[col].isnull().sum() / len(df[col])
                ) * 100
                summary["missing_values_percentage"] = summary[
                    "missing_values_percentage"
                ].map("{:.2f}%".format)
                summary.columns = [
                    "Statistic",
                    "Value",
                    "Data Type",
                    "Missing Values",
                    "Missing Values (%)",
                ]

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

                # Wrap the card content and summary table in a dbc.Col
                card = dbc.Col(
                    [dbc.Card(card_content, className="mb-3"), summary_table], md=4
                )

                cards.append(card)
            # Wrap the cards in a dbc.Row
            cards_row = dbc.Row(cards)

            # Return the generated cards
            return html.Div(cards_row)

        except FileNotFoundError:
            # Return an error message if the data file is not found
            return html.Div(
                "Data file not found. Please upload data in the 'Import Data' section."
            )

    elif tab == "tab-table":
        try:
            # Read the data from the local_data.csv file
            df = pd.read_csv("local_data.csv")

            # Create a DataTable component to display the data as a table
            return dash_table.DataTable(
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
                },
            )
        except FileNotFoundError:
            # Return an error message if the data file is not found
            return html.Div(
                "Data file not found. Please upload data in the 'Import Data' section."
            )

    elif tab == "tab-charts":
        # Read the data from the local_data.csv file
        df = pd.read_csv("local_data.csv")

        # Create options for the column dropdown based on the columns in the data
        column_options = [{"label": col, "value": col} for col in df.columns]

        # Return a Div component with dropdowns for chart type and column selection
        return html.Div(
            [
                html.H3("Chart Types"),
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
            {"label": "Time Series Analysis", "value": "time_series"},
            {"label": "Feature Extraction", "value": "feature_extraction"},
            {"label": "Clustering", "value": "clustering"},
            {"label": "Classification", "value": "classification"},
            {"label": "Feature Selection", "value": "feature_selection"},
        ]
        target_variable_options = [{"label": col, "value": col} for col in df.columns]

        # Return a Div component with dropdowns for task and target variable selection
        return html.Div(
            [
                dcc.Dropdown(id="task-dropdown", options=task_options, value=""),
                dcc.Dropdown(
                    id="target-variable-dropdown",
                    options=target_variable_options,
                    value="",
                ),
                html.Div(id="ml-results"),
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
                dcc.Dropdown(id="y-axis-dropdown", options=column_options, value=""),
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
    df = pd.read_csv("local_data.csv")
    fig = px.scatter(df, x=x_axis, y=y_axis)
    return dcc.Graph(figure=fig)


@dash.callback(
    Output("ml-results", "children"),
    [Input("task-dropdown", "value"), Input("target-variable-dropdown", "value")],
    prevent_initial_call=True,
)
def perform_ml_task(task, target_variable):
    # Read the data from the local_data.csv file
    try:
        df = pd.read_csv("local_data.csv")
    except FileNotFoundError:
        return html.Div(
            "Data file not found. Please upload data in the 'Import Data' section."
        )

    if target_variable not in df.columns:
        return html.Div("Target variable not found in the dataset.")

    if task == "time_series":
        try:
            # Perform time series analysis
            df[target_variable] = pd.to_datetime(df[target_variable])
            df = df.set_index(target_variable)
            return dcc.Graph(
                figure=px.line(df, y=df.columns[0], title="Time Series Analysis")
            )
        except Exception as e:
            return html.Div(f"Error in time series analysis: {str(e)}")

    elif task == "feature_extraction":
        try:
            # Perform feature extraction using PCA
            features = df.drop(columns=[target_variable])
            if not all(features.dtypes.apply(lambda x: np.issubdtype(x, np.number))):
                return html.Div("Feature extraction requires numeric data.")
            pca = PCA(n_components=2)
            components = pca.fit_transform(features)
            components_df = pd.DataFrame(data=components, columns=["PCA 1", "PCA 2"])
            return dcc.Graph(
                figure=px.scatter(
                    components_df, x="PCA 1", y="PCA 2", title="PCA Feature Extraction"
                )
            )
        except Exception as e:
            return html.Div(f"Error in feature extraction: {str(e)}")

    elif task == "clustering":
        try:
            # Perform clustering using KMeans
            features = df.drop(columns=[target_variable])
            if not all(features.dtypes.apply(lambda x: np.issubdtype(x, np.number))):
                return html.Div("Clustering requires numeric data.")
            kmeans = KMeans(n_clusters=3)
            df["Cluster"] = kmeans.fit_predict(features)
            return dcc.Graph(
                figure=px.scatter(
                    df,
                    x=features.columns[0],
                    y=features.columns[1],
                    color="Cluster",
                    title="KMeans Clustering",
                )
            )
        except Exception as e:
            return html.Div(f"Error in clustering: {str(e)}")

    elif task == "classification":
        try:
            # Perform classification using RandomForestClassifier
            features = df.drop(columns=[target_variable])
            target = df[target_variable]
            if target.nunique() <= 1:
                return html.Div(
                    "Classification requires more than one class in the target variable."
                )
            X_train, X_test, y_train, y_test = train_test_split(
                features, target, test_size=0.3, random_state=42
            )
            scaler = StandardScaler().fit(X_train)
            X_train_scaled = scaler.transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            clf = RandomForestClassifier()
            clf.fit(X_train_scaled, y_train)
            y_pred = clf.predict(X_test_scaled)
            report = classification_report(y_test, y_pred, output_dict=True)
            report_df = pd.DataFrame(report).transpose()
            return dash_table.DataTable(
                data=report_df.to_dict("records"),
                columns=[{"name": i, "id": i} for i in report_df.columns],
                style_cell={"textAlign": "left"},
                style_header={"backgroundColor": "white", "fontWeight": "bold"},
                fill_width=False,
            )
        except Exception as e:
            return html.Div(f"Error in classification: {str(e)}")

    elif task == "feature_selection":
        try:
            # Perform feature selection using SelectKBest
            features = df.drop(columns=[target_variable])
            target = df[target_variable]
            if not np.issubdtype(target.dtype, np.number):
                return html.Div("Feature selection requires a numeric target variable.")
            selector = SelectKBest(score_func=chi2, k=2)
            selector.fit(features, target)
            scores = pd.DataFrame(
                selector.scores_, index=features.columns, columns=["Score"]
            )
            scores = scores.sort_values(by="Score", ascending=False).reset_index()
            return dash_table.DataTable(
                data=scores.to_dict("records"),
                columns=[{"name": i, "id": i} for i in scores.columns],
                style_cell={"textAlign": "left"},
                style_header={"backgroundColor": "white", "fontWeight": "bold"},
                fill_width=False,
            )
        except Exception as e:
            return html.Div(f"Error in feature selection: {str(e)}")

    return html.Div("Select a valid task.")
