# Import packages
import base64
import io
from dash import Dash, html, dash_table, dcc
import pandas as pd
from dash.dependencies import Input, Output, State


# Incorporate data
# df = pd.read_csv(
#     "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
# )

# Initialize the app
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    title="My PyExploratory Dashboard App",
    update_title="Loading...",
    external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"],
    background_callback_manager=True,
)

# App layout
# Create a Dash layout
app.layout = html.Div(
    [
        html.Div(html.H1("PyExploratory", style={"textAlign": "center", "color": "Red","background-color": "blue"})),
        html.H3("Import Data"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
                "background-color": "lightblue",
            },
            # Allow multiple csv and json to be uploaded
            multiple=True,
        ),
         #Display the data in a table
        html.Div(id="output-data-upload", ) ,
      
           
    ]
    # create a  button to another page
)
# Define the callback function to update the dropdown options after file upload
@app.callback(
    Output("column-select", "options"),
    [
        Input("upload-data", "contents"),
       
    ],
)

def preview_data(contents):
    if contents is not None:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        try:
            if "csv" in content_type:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            elif "json" in content_type:
                # Assume that the user uploaded a JSON file
                df = pd.read_json(io.StringIO(decoded.decode("utf-8")))
        except Exception as e:
            print(e)
            return html.Div(["There was an error processing this file."])
        return html.Div(
            [
                dash_table.DataTable(
                    data=df.to_dict("records"),
                    columns=[{"name": i, "id": i} for i in df.columns],
                ),
                html.Hr(),  # add a horizontal rule
                html.Div("Raw Content"),
                html.Pre(
                    contents[0:200] + "...", style={"whiteSpace": "pre-wrap", "wordBreak": "break-all"}
                ),
            ]
        )
    else:
        return html.Div(["Upload a csv or json file to start"])

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
