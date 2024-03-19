import dash
from dash import html, dcc

dash.register_page(__name__, path='/Statistical_analysis', name='Statistical Analysis')

#-----------------------Page Layout----------------------------

layout = html.Div([
    html.Br(),
    html.P('Statistical Analysis', className="text-dark text-center fw-bold fs-1"),
    
    #Create a div to calculate the mean, median, mode, standard deviation and variance of the data
    html.Div([
        html.Label('Select Column'),
        dcc.Dropdown(
            id='select-column',
            options=[
                {'label': 'Mean', 'value': 'col1'},
                {'label': 'Median', 'value': 'col2'},
                {'label': 'Mode', 'value': 'col3'},],
            value='col1'
        ),
    ], className="col-6 mx-auto"),
], className="col-8 mx-auto")

#Creare a function to calculate the mean, median, mode, standard deviation and variance of the data
def calculate_statistics(data, column):
    mean = data[column].mean()
    median = data[column].median()
    mode = data[column].mode()
    std_dev = data[column].std()
    variance = data[column].var()
    return mean, median, mode, std_dev, variance