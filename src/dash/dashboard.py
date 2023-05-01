"""Instantiate a Dash app."""
import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from .data import create_dataframe
from .layout import html_layout


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[
            "/static/dist/css/styles.css",
            "https://fonts.googleapis.com/css?family=Lato",
        ],
    )

    # Load DataFrame
    df = create_dataframe()

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = serve_layout

    # Callback to update the output area with the selected option
    @dash_app.callback(
        Output("output-area", "children"),
        [Input("dropdown-menu", "value")],
    )
    def update_output_area(selected_option):
        return f"Selected option: {selected_option}"

    return dash_app.server

def serve_layout():
    # Load DataFrame
    df = create_dataframe()

    # Create Layout
    layout = html.Div(
        children=[
            dcc.Dropdown(  # Add a dropdown menu
                id="dropdown-menu",
                options=[
                    {"label": option, "value": option}
                    for option in df["city"].unique()
                ],
                value="",
            ),
            html.Div(id="output-area"),
            dcc.Graph(
                id="histogram-graph",
                figure={
                    "data": [
                        {
                            "x": df["complaint_type"],
                            "text": df["complaint_type"],
                            "customdata": df["key"],
                            "name": "311 Calls by region.",
                            "type": "histogram",
                        }
                    ],
                    "layout": {
                        "title": "NYC 311 Calls category.",
                        "height": 500,
                        "padding": 150,
                    },
                },
            ),
            create_data_table(df),
        ],
        id="dash-container",
    )
    return layout


def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id="database-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        sort_action="native",
        sort_mode="native",
        page_size=300,
    )
    return table