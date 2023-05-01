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
from pathlib import Path, PurePath
import pathlib
from PIL import Image
import plotly.express as px
import ants
import nibabel as nib
import time

from siemens_regist import Siemens_Registration_Dicom_to_Nifty

dicompath = 'path' #  Dummy
logoimagepath = Path(str(Path.cwd().parents[1]) + '/src/templates/first_Logo.png')
pil_img = Image.open(logoimagepath)

######################################################################################################################################

def selected_options():
    """
    für den callback mus ein Input geben, aber da ich kein Input habe, ist eine Funktion sehr hilfreich, der für den Dropdownmenu ein Output geben kann.
    Im app Layout wird es dann für options = selected_options() aufgerufen und eingefügt.
    """
    if dicompath.exists() == True:
        var = Siemens_Registration_Dicom_to_Nifty(dicompath)       
        options = var.option_list()
        return options
    
    else:
        return ['Error']

#######################################################################################################################################

dashapp = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP]) 

dashapp.layout = dbc.Container(fluid=True, children=[
    
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
            
            
            # Select ICP-Sheet
            dbc.Row(html.Div(children=[
                html.Div('RekonstruktionsMethoden')
                    ]), style = {'textAlign' : 'center'}),

            html.Div(style={'padding': 40}),

            dbc.Row([
                    dbc.Col(html.Div([
                    dcc.Dropdown(placeholder='Rekonstruktionsmethoden', options = selected_options(), id ='select_methode'), 
                    ]), style = {'textAlign' : 'center'})
                        
                        ]),
            
            html.Div(style={'padding': 40}),
            
            
            #########################
            # Start all my Analysis #
            #########################

            # Start Registration-Button
            dbc.Row(dbc.Col([dbc.Button('Show', outline=True, color='success', id='click_show', n_clicks=0)]), style = {'textAlign' : 'center'}),
            # dbc.Row(dbc.Col(dcc.Loading(
            #                 id="loading-1",
            #                 type="default",
            #                 children=html.Div(id="loading-output-1"))
            #                 )),
            html.Div(style={'padding': 40}),

            # selecting raw images
            dbc.Row([dbc.Col([
                            html.Div("raw Images"),
                            html.P(),
                            dcc.Dropdown(placeholder='sequences', id='raw_sequences', options = []),                                
                            html.P(),
                            html.Div([
                                dcc.Graph(id='raw_images')
                            ])],style={'textAlign': 'center'}),                  
                    ]),
            html.Div(style={'padding': 40}),

            dbc.Row(dbc.Col([dbc.Button('Start Registration', outline=True, color='success', id='click_reg', n_clicks=0)]), style = {'textAlign' : 'center'}),
            
            html.Div(style={'padding': 40}),
            
            # selecting registered images
            dbc.Row([dbc.Col([
                            html.Div("registered Images"),
                            html.P(),
                            dcc.Dropdown(placeholder='sequences', id='registered_sequences', options = []),                                
                            html.P(),
                            html.Div([
                                dcc.Graph(id='regist_images')
                            ])],style={'textAlign': 'center'})]
                    ),
            
            html.Div(style={'padding': 40}),
            
            # Displaying registered images

            ####################
            # saving in folder #
            ####################
            html.Div(style={'padding': 20}),
            dbc.Row([dbc.Col(html.Div([dbc.Button('Save', outline=True, color='success', id='export', n_clicks=0),
                        dcc.Download(id="download-text")])),
                    ],style = {'textAlign':'center'}),
            html.Div(style={'padding': 20}),                   
                ],)


@dashapp.callback(
    Output('raw_sequences','options'),
    State('select_methode','value'),
    Input('click_show', 'n_clicks'),
    )
def select_registration(methode, bool):
    if not bool:
        raise PreventUpdate
    
    var = Siemens_Registration_Dicom_to_Nifty(dicompath)

    methode_index = var.option_list().index(methode) # wenn zbsp 'WATER' gewählt wird, wird dann in der liste geschaut, welchen index dieser hat, der sucht dann die passenden
                                                     # DICOMs aus
    basename = var.nifti_filename(methode_index) # Die Namen der Bilder werden dann im Dropdownmenu angezeigt

    return basename 

@dashapp.callback(
    Output('raw_images','figure'),
    Input('raw_sequences','value'),
    Input('select_methode', 'value')
    )
def show_raw_images(raw, methode):
    if not raw and methode:
        raise PreventUpdate
    
    var = Siemens_Registration_Dicom_to_Nifty(dicompath)
    methode_index = var.option_list().index(methode) # 'Water' als Index
    list_nifti_to_ants = var.nifti_to_antspy(methode_index) # meine Antspy Dateien in einer liste
    basename = var.nifti_filename(methode_index)

    rot = -1 # Variable um das Bild zu drehen

    list_ants_to_np = [np.rot90(list_nifti_to_ants[x].numpy(),rot) for x in range(len(list_nifti_to_ants))] # die Bilder sind nämlich hier bei Jost Schweine umgedreht

    dict_npants = {} # die Filenames mit den rotierten in Numpy-Arrays convertierte Bilder
    for i in range(len(basename)):
        dict_npants[basename[i]] = list_ants_to_np[i]  


    # die MRT Bilder wurden in drei Richtungen aufgenommen (x, y und z sclices)
    # .shape[2] ist dann die z Richtung sagt dann wie viele Schichten da sich beinhaltet (88)
    # in [baseline[:,:,i] werden die 88 Slices in z-Richtung in einer Liste übergeben
    antsy = np.array(dict_npants[raw])
    z_array = np.asarray([antsy[:,:,i] for i in range(antsy.shape[2])])

    fig = px.imshow(z_array, animation_frame=0, zmin = antsy.min() , zmax = antsy.max(), binary_string=False,color_continuous_scale='gray') # binary_string =False, weil dash sonst nicht so prickelnd läuft

    return fig

@dashapp.callback(
    Output('registered_sequences','options'),
    State('select_methode','value'),
    Input('click_reg', 'n_clicks'),
    )
def select_registration(methode, bool):
    if not bool:
        raise PreventUpdate
    
    var = Siemens_Registration_Dicom_to_Nifty(dicompath)

    methode_index = var.option_list().index(methode) # wenn zbsp 'WATER' gewählt wird, wird dann in der liste geschaut, welchen index dieser hat, der sucht dann die passenden
                                                     # DICOMs aus
    list_nifti_to_ants = var.nifti_to_antspy(methode_index) # meine Antspy Dateien in einer liste
    basename = var.nifti_filename(methode_index)
    reg_folderpath = var.reg_folder()   


    # Das erste Bild ist das Baselinebild und die anderen sind die Bilder, die auf das Baselinebild registriert werden soll.
    # Da das erste Bild nicht auf das erste Bild registriert werden soll, musst der index fürs reg +1 sein aber der range -1, damit wenn man 1 raufaddiert, auch das letzte Bild mit registriert werden
    # kann
    reg_ants = [ants.registration(fixed=list_nifti_to_ants[0], moving=list_nifti_to_ants[i+1], type_of_transform = 'Affine' ) for i in range(len(list_nifti_to_ants)-1)]

    reg_filename = []
    for save in range(len(reg_ants)):
        addfile = reg_folderpath/('reg_'+ basename[save + 1])
        reg_filename.append('reg_'+ basename[save + 1])
        nifti_reg = ants.to_nibabel(reg_ants[save]['warpedmovout'])
        nib.save(nifti_reg, addfile)

    return reg_filename


### TO DO
# Iwas muss ich wegen der Registrierung machen.
# Dieses Callback hat die Registrierung drin, aber wenn ich ein neuen callback aufmache, kann ich nicht darauf zu gegreifen..




    




if __name__ == '__main__':
    dashapp.run_server(debug=False, host='0.0.0.0', port='8050')