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
import pandas as pd
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
        html.H1("Data Analysis"),
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
                    label="Machine Learning",
                    value="tab-machine-learning",
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
            for col in df.columns:
            # Calculate summary statistics for the data
                summary = df[col].describe().reset_index()
                summary.columns = ["Statistic", "Value"]

                # Create a DataFrame for the additional statistics
                additional_stats = pd.DataFrame({
                    "Statistic": ["Data Type", "Missing Values", "Missing Values (%)"],
                    "Value": [
                        str(df[col].dtype),
                        df[col].isnull().sum(),
                        "{:.2f}%".format((df[col].isnull().sum() / len(df[col])) * 100)
                    ]
                })

                # Concatenate the summary and additional_stats DataFrames
                summary = pd.concat([summary, additional_stats], ignore_index=True)

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
            
                if df[col].dtype in ["float64", "int64"]:
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
                    card_content = dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(col, className="card-title"),
                                dcc.Graph(
                                    figure=px.bar(
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
                
                # Wrap the card content and summary table in a dbc.Col
                card = dbc.Col(
                    [dbc.Card(card_content, className="mb-3")], md=4
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
            return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

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
                    ],
                    value="",
                ),
                dcc.Dropdown(id="column-dropdown", options=column_options, value=""),
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
        return dcc.Graph(figure=px.line(df, x=df.index, y=column_name))
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


# Add a new callback function to perform the selected machine learning task
@dash.callback(
    Output("ml-results", "children"),
    [Input("task-dropdown", "value"), Input("target-variable-dropdown", "value")],
    prevent_initial_call=True,
)
def perform_ml_task(task, target_variable):
    # Read the data from the local_data.csv file
    df = pd.read_csv("local_data.csv")

    if task == "time_series":
        # Perform time series analysis
        df[target_variable] = pd.to_datetime(df[target_variable])
        df = df.set_index(target_variable)
        return dcc.Graph(figure=px.line(df, y=df.columns[0]))

    elif task == "feature_extraction":
        # Perform feature extraction using PCA
        features = df.drop(columns=[target_variable])
        pca = PCA(n_components=2)
        components = pca.fit_transform(features)
        return dcc.Graph(
            figure=px.scatter(
                components,
                x=0,
                y=1,
                title="PCA Feature Extraction",
                labels={"0": "PCA 1", "1": "PCA 2"},
            )
        )

    elif task == "clustering":
        # Perform clustering using KMeans
        features = df.drop(columns=[target_variable])
        kmeans = KMeans(n_clusters=3)
        df["Cluster"] = kmeans.fit_predict(features)
        return dcc.Graph(
            figure=px.scatter(
                df, x=features.columns[0], y=features.columns[1], color="Cluster"
            )
        )

    elif task == "classification":
        # Perform classification using RandomForestClassifier
        features = df.drop(columns=[target_variable])
        target = df[target_variable]
        X_train, X_test, y_train, y_test = train_test_split(
            features, target, test_size=0.3
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

    elif task == "feature_selection":
        # Perform feature selection using SelectKBest
        features = df.drop(columns=[target_variable])
        target = df[target_variable]
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
    else:
        # Return an error message if no task is selected
        return html.Div("Select a task.")
