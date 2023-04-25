"""Instantiate a Dash app."""
import dash_bootstrap_components as dbc
from siemens_regist import Siemens_Registration_Dicom_to_Nifty
import itertools
import pandas as pd
import numpy as np
import base64
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output, State
from dash import Dash, dcc, html, dash_table
from pathlib import Path
import pathlib
from PIL import Image

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

    return dash_app.server

def serve_layout():

    logoimagepath = Path(str(Path.cwd()) + '/src/templates/first_Logo.png')
    pil_img = Image.open(logoimagepath)

    layout = dbc.Container(fluid=True, children=[
    
                # die Überschrift
                dbc.Row(dbc.Col(html.Div([
                         html.P(),  # empty row
                         html.Img(src=pil_img, style={'height':'5%', 'width':'5%','textAlign': 'center' }),
                         
                    
                    
                ], style= {'textAlign': 'center'} )
                )),
                html.Div(style={'padding': 20}),  # empty paragraph
                
                dbc.Row(dbc.Col(html.Div(children=[html.H1(children='',style={'font-family': 'Arial','color': 'black', 'fontSize': 28}),
                    html.P(),
                    html.Div("",style={'font-family': 'Courier New','color': 'black', 'fontSize': 20,'textAlign': 'center'}),
                    html.P()]))
                        ),
                
                # Uploadbutton
            
                dbc.Row([dbc.Col(html.Div(dbc.Button('Upload File',color = 'primary',outline=True), id='upload-data',className = 'uploadtest/uploads.js', n_clicks=0),width=1),
                         dbc.Col(html.Div(id='output-image-upload')),
                         dbc.Col(html.P())
                        ]),
                html.Div(style={'padding': 20}),  # empty paragraph
                
                
                
                # Select ICP-Sheet
                dbc.Row(html.Div(children=[
                    html.Div('RekonstruktionsMethoden')
                     ]), style = {'textAlign' : 'center'}),
                dbc.Row([
                        dbc.Col(html.Div([
                        dcc.Dropdown(placeholder='Rekonstruktionsmethoden', options = [], id='option'), 
                        ]), style = {'textAlign' : 'center'})
                            
                            ]),
                
                html.Div(style={'padding': 40}),
                
                
                #########################
                # Start all my Analysis #
                #########################
                
                # Displaying registered images
                dbc.Row([dbc.Col([
                                html.Div("raw Images"),
                                html.P(),
                                dcc.Dropdown(placeholder='sequences', id='raw_sequences', options = []),                                
                                html.P()],style={'textAlign': 'center'}),
                        dbc.Col([
                                html.Div("registered Images"),
                                html.P(),
                                dcc.Dropdown(placeholder='sequences', id='registered_sequences', options = []),                                
                                html.P()],style={'textAlign': 'center'})]
                        ),
                
                html.Div(style={'padding': 40}),
                

                ####################
                # saving in folder #
                ####################
                html.Div(style={'padding': 20}),
                dbc.Row([dbc.Col(html.Div([dbc.Button('Save', outline=True, color='success', id='export', n_clicks=0),
                         dcc.Download(id="download-text")])),
                        ],style = {'textAlign':'center'}),
                html.Div(style={'padding': 20}),                   
                    ],)

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