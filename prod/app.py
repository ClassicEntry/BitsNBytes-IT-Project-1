from dash import Dash, dcc, html, Output, Input, dash_table
import dash
import plotly.express as px

px.defaults.template = "plotly_dark"

external_css = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css",
]

app = Dash(
    __name__, pages_folder="services", use_pages=True, external_stylesheets=external_css,
)

app.layout = html.Div(
    [
        dcc.Store(id='stored-data'),
        html.Br(),
        html.P("PyExploratory App", className="text-dark text-center fw-bold fs-1"),
        html.Div(
            children=[
                dcc.Link(
                    page["name"],
                    href=page["relative_path"],
                    className="btn btn-dark m-2 fs-5",
                )
                for page in dash.page_registry.values()
                    #arrange the buttons in a specific order of dashboard, clean data, visualise data and predictive analysis
            ]
        ),
        dash.page_container,
    ],
    className="col-10 mx-auto",


)

if __name__ == "__main__":
    app.run(debug=True)
