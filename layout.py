# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 17:12:51 2021

@author: SEENOVATE
"""

import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
# from index import username
from app import app

# Chargement fichier csv : pour gérer infos principales des différentes applis
list_app = pd.read_csv("assets/list_app.csv", header=0, sep=';')

# Fichier layout "principal" : on retrouve le composant "page-content" géré dans le fichier "callbacks.py" pour faire
# afficher la page adéquate.
layout_template = html.Div([
    dcc.Location(id='url2', refresh=False),
    # permet de stocker l'URL de la page affichée (pour le callbacks de gestion des applis)
    html.Div(id='page-content', className='content'),
    html.P(id='placeholder_index')
], style={'overflow-x':'hidden'})

######################################################################################################
#                                    LAYOUT PAGE d'ACCUEIL                                           #
######################################################################################################


children = [dbc.Col(width=1)]

for i in list_app["ind"]:
    child_group_form = dbc.Col([
        dbc.Card([
            dbc.CardHeader(
                dbc.CardLink(
                    html.H1(list_app["name"].loc[list_app["ind"] == i].iloc[0],
                            style={"color": "#024c97", "font-weight": "bold", "font-size": "1.65vh",
                                   # change color => Belongs csv file ?
                                   "padding-top": "15px"}),
                    href=list_app["link"].loc[list_app["ind"] == i].iloc[0],
                    # id={'type':'LinkGroup','id_group':i},
                ),
                className='text-center',
                style={"background-color": "transparent"}
            ),
            html.Div(
                dbc.CardLink(
                    dbc.CardImg(src=list_app["link_image"].loc[list_app["ind"] == i].iloc[0],
                                style={"height": "12vh", "width": "auto", "margin-top": "2vh"},
                                className="img-fluid rounded-start"
                                ),
                    href=list_app["link"].loc[list_app["ind"] == i].iloc[0],
                    # id={'type':'LinkGroup2','id_group':i},
                )
            ),
        ], style={"height": "25vh", "width": "25vh", 'margin-left': '1vw',
                  "box-shadow": " 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                  'border-color': 'transparent', "border-radius": " 10px 100px / 120px"}),
    ], xs=12, sm=12, md=12, lg=1, xl=1, align="center")
    children.append(dbc.Col(width=1))
    children.append(child_group_form)

children.append(dbc.Col(width=3))

home_page = html.Div([

    # -------- HEADER --------- #

    # dbc.Row([
    #     dbc.Col([
    #         dbc.Navbar([
    #             dbc.Col([html.Img(src='/assets/logo_seenovate.png', height="40px", style={'margin-left': '1vw'})], xs=2,
    #                     sm=2, md=2, lg=2, xl=2),
    #             dbc.Col([html.Div(dbc.NavbarBrand("Titre page d'accueil", id="titre"),
    #                               style={"color": "grey", "font-size": "1.65vh", "textAlign": "center"})
    #                      # ,className="text-white"
    #                      ], xs=8, sm=8, md=8, lg=8, xl=8, align="center"),
    #             dbc.Col([html.Div(html.Img(src=app.get_asset_url('user2.png'), height="40px"))], xs=1, sm=1, md=1, lg=1,
    #                     xl=1, align="right"),
    #             dbc.Col([dbc.NavbarBrand("Logo Client")], xs=1, sm=1, md=1, lg=1, xl=1,
    #                     style={"color": "grey", "font-size": "1.65vh"}, align="center")  # className="ml-5 text-white"
    #         ], color = "-webkit-gradient(linear, right bottom, left top, from(#80DEEA), to(#1A77BD))")

    #     ], xs=12, sm=12, md=12, lg=12, xl=12, style={"height": "100%"})
    # ]),
    dbc.Row([
        dbc.Col([
            dbc.Navbar([
                dbc.Col([html.Img(src=app.get_asset_url("logo_seenovate.png"), height="30px",
                                style={'margin-left': '1vw'})], xs=2, sm=2, md=2, lg=2, xl=2),
                dbc.Col([html.Div(dbc.NavbarBrand("Accueil", id="titre",
                                                className="text-white", style = {'fontSize':'1.7vh'}), style={"textAlign": "center"})
                        ], xs=8, sm=8, md=8, lg=8, xl=8, align="center"),
                # dbc.Col([
                #     html.Div([
                #         html.Img(src=app.get_asset_url("user.png"), height="30px"),
                #         dbc.Label('')
                #     ])
                # ])
            ], color="primary", style={"backgroundImage":"-webkit-gradient(linear, right bottom, left top, from(#80DEEA), to(#1A77BD))"})
        ], xs=12, sm=12, md=12, lg=12, xl=12, className="justify-content-center")
    ]),

    # --------- BODY --------- #

    # --------- ROW1 ---------#
    # First image
    dbc.Row(
        dbc.Col(
            html.Img(src=app.get_asset_url("logo_seenovate_bleu.png"), style={"height": "10vh"})
        ),
        style={"paddingTop": "6vh", "paddingBottom": "6vh", 'textAlign': 'center'}),

    # --------- ROW2 ---------#
    # Second image
    dbc.Row(
        dbc.Col(
            html.Img(src=app.get_asset_url("Image3.jpeg"),
                     style={"border-radius": "20% / 50%", "height": "42vh", "width": "102vh"}),
            width=12
        ),
        style={"height": "auto", 'textAlign': 'center'}),

    # --------- ROW3 ---------#

    dbc.Row(
        children=children
        , style={'padding-left': "5vh", 'margin-top': "-15vh",
                 'padding-bottom': "5vh", 'padding-right': "5vh", "textAlign": "center"},
        justify="center"),

], style={'overflow-x': 'hidden'})
