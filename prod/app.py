import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import base64
import io

# Create the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.Div(
        [
            html.H1("PyExploratory", style={'textAlign': 'center'}),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            dcc.Checklist(
                id='remove-duplicates',
                options=[{'label': 'Remove duplicates', 'value': 'RD'}],
                value=[]
            ),
            dcc.Input(
                id='fill-na',
                type='text',
                placeholder='Fill NA values with...'
            ),
            dcc.Dropdown(id="column-select", style={'width': '50%', 'margin': 'auto'}),
            dcc.Graph(id="data-visualization"),
        ],
        style={'maxWidth': '800px', 'margin': 'auto'}
    )
])

# Define the callback function to update the dropdown options after file upload
@app.callback(Output('column-select', 'options'), [Input('upload-data', 'contents'), Input('remove-duplicates', 'value'), Input('fill-na', 'value')])
def update_dropdown(contents, remove_duplicates, fill_na):
    if contents is not None:
        # Only use the first file
        content_type, content_string = contents[0].split(',')
        decoded = base64.b64decode(content_string)
        data = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        # Perform data cleaning operations
        if 'RD' in remove_duplicates:
            data = data.drop_duplicates()
        if fill_na is not None:
            data = data.fillna(fill_na)
        return [{'label': col, 'value': col} for col in data.columns]
    else:
        return []

# Define the callback function to update the graph after column selection
@app.callback(Output("data-visualization", "figure"), [Input("column-select", "value"), Input('upload-data', 'contents'), Input('remove-duplicates', 'value'), Input('fill-na', 'value')])
def update_visualization(selected_column, contents, remove_duplicates, fill_na):
    if contents is not None and selected_column is not None:
        # Only use the first file
        content_type, content_string = contents[0].split(',')
        decoded = base64.b64decode(content_string)
        data = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        # Perform data cleaning operations
        if 'RD' in remove_duplicates:
            data = data.drop_duplicates()
        if fill_na is not None:
            data = data.fillna(fill_na)
        return {
            "data": [{"x": data.index, "y": data[selected_column], "type": "scatter"}],
            "layout": {"title": f"Data Visualization for {selected_column}"},
        }
    else:
        return {}

if __name__ == "__main__":
    app.run_server(debug=True)