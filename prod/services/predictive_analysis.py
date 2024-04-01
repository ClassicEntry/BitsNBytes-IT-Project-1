# import dash
# from dash import html, dcc

# dash.register_page(__name__, path="/Predictive_analysis", name=" Predictive Analysis")

# # -----------------------Page Layout-----------------------

# layout = html.Div(
#     [
#         html.Br(),
#         html.P("Predictive Analysis", className="text-dark text-center fw-bold fs-1"),
#         # Create a div to select the model and the column to predict
#         html.Div(
#             [
#                 html.Label("Select Model"),
#                 dcc.Dropdown(
#                     id="select-model",
#                     options=[
#                         {"label": "Linear Regression", "value": "linear_regression"},
#                         {
#                             "label": "Logistic Regression",
#                             "value": "logistic_regression",
#                         },
#                         {"label": "Decision Tree", "value": "decision_tree"},
#                     ],
#                     value="linear_regression",
#                 ),
#             ],
#             className="col-6 mx-auto",
#         ),
#         html.Div(
#             [
#                 html.Label("Select Column to Predict"),
#                 dcc.Dropdown(
#                     id="select-column-to-predict",
#                     options=[
#                         {"label": "Column 1", "value": "col1"},
#                         {"label": "Column 2", "value": "col2"},
#                         {"label": "Column 3", "value": "col3"},
#                     ],
#                     value="col1",
#                 ),
#             ],
#             className="col-6 mx-auto",
#         ),
#     ],
#     className="col-8 mx-auto",
# )


# # Create a function to predict the data
# def predict_data(data, model, column) -> list:
#     if model == "linear_regression":
#         # Code to predict using linear regression

#         pass
#     elif model == "logistic_regression":
#         # Code to predict using logistic regression
#         pass
#     elif model == "decision_tree":
#         # Code to predict using decision tree
#         pass
#     return list


# # Create a function to use linear regression to predict the data
