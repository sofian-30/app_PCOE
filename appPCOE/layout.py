import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from dash import dcc,html
from app import app
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
from colors import *

import dash_mantine_components as dmc
import dash_daq as daq

# Import functions
# from index import get_auth

######################################################################################
#                                       Data                                         #
######################################################################################

## Chargement fichier csv : pour gérer infos principales des différentes applis
list_app = pd.read_csv("assets/list_app.csv", header=0, sep=';')
n_app = 1 # numéro de l'appli


# Charger le tableau Excel
# df = pd.read_excel(r"/mnt/c/CA_2023.xlsx", sheet_name='Maintenance SAP BusinessObjects',parse_dates=['Date anniversaire'], date_parser=pd.to_datetime)
df = pd.read_excel(r"C:\Users\SofianOUASS\Desktop\PCoE\Suivi CA licences et maintenance 2023.xlsx", sheet_name='Maintenance SAP BusinessObjects')

# On remplit la colonne renouvellement et alerte validation devis en fonction des critères donnés dans les SPECS
today=datetime.now()

# Remplacez les valeurs NaN par une date par défaut (par exemple, 1er janvier 1900)
    
df['Alerte renouvellement'] = (df['Date anniversaire'] - today).dt.days
df['Alerte validation devis'] = (df['Date anniversaire'] - today).dt.days

# Ajout des 4 nouvelles colonnes après colonne 'Date anniversaire'
new_columns = []
for col in df.columns:
    new_columns.append({'name': col, 'id': col, 'type': 'text'})
    if col == 'Date anniversaire':
        new_columns.append({'name': 'Alerte renouvellement', 'id': 'Alerte renouvellement', 'type': 'text'})
        new_columns.append({'name': 'Alerte validation devis', 'id': 'Alerte validation devis', 'type': 'text'})
        new_columns.append({'name': 'Nouveau prix d\'achat', 'id': 'input-nv-prix-achat', 'type': 'text'})
        new_columns.append({'name': 'Nouveau prix de vente', 'id': 'input-nv-prix-vente', 'type': 'text'})

#############################################################################################################
#                                          Appel API                                                        #
#############################################################################################################



#############################################################################################################
#                                                                                                           #
#############################################################################################################


##liste des noms de colonne: Informations contrats clients=
# ['Client', 'ERP Number \nRéf SAP', 'Date anniversaire', 'Code projet Boond', 'Resp\nCommercial', 'Type de contrat']

# #liste des noms de colonne: 
# ['Agence', 'Client', 'ERP_Number_Ref_SAP', 'Code projet Boond', 'Date anniversaire',
#   'CA maintenance facturé', 'Achat SAP Maintenance ou GBS ou NEED4VIZ', 'Marge maintenance ',
#     'Marge %', 'Montant vente annuel N+1', 'Montant annuel Achat N+1', "Mois d'imputation",
#       'Type de support SAP', 'Type de contrat', 'Parc/Techno', 'Numéro de facture',
#         'Date de facture', 'Resp\nCommercial', 'Proposition SAP reçue', 'Relance client**',
#           'Proposition Seenovate créée', 'Proposition Seenovate envoyée',
#             'Proposition signée par le client', 'Attente  N° Cde client avant facturation',
#               'Facture  créée', 'Commande faite SAP', 'Facture SAP reçue', 'Remarques',
#                 'Devis', 'Accord de principe', 'Signature client', 'Achat éditeur', 'Renouvelé',
#                   'Traitement comptable', 'Paiement SAP', 'Demande de résiliation', 
#                   'Communication éditeur', 'Résilié', 'Converti ou Extension']             

# Ajout d'un composant dcc.Store pour stocker les données de la ligne sélectionnée
stockage_ligne = dcc.Store(id='o1_store_row')
stockage_mis_a_jour = dcc.Store(id='o1_store_updated_data')  # Ajout de ce composant

# Fenêtre modale pour la modification de saisie (Avec Accordion)
modal_pop_up= dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle("Modifier la saisie")),
                dbc.ModalBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader("Informations générales"),
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Label("Client", width=6),
                                                dbc.Label(id='input-client')
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("ERP Number", width=6),
                                                dbc.Label(id='input-erp-number')
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Date anniversaire", width=6),
                                                dbc.Label(id='input-date-anniversaire')  # Utilisation de dbc.Label pour afficher la date
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Code projet Boond", width=6),
                                                dbc.Label(id='input-code-projet-boond') # En attente de Boond
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Resp. Commercial", width=6),
                                                dbc.Label(id='input-resp-commercial')
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Editeur", width=6),
                                                dbc.Label(id='input-editeur') # possibilité de faire dropdown cf. excel specs App PCoE
                                            ], width={"size": 6}),
                                        ]),
                                    ])
                                ]),
                            ],width={"size": 9}),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader("Alertes"),
                                    dbc.CardBody([
                                        dbc.Row([
                                            dmc.Badge("Génération devis", id= 'input-badge-generation-devis',color='grey')
                                            ], className="mb-2"),
                                        dbc.Row([
                                            dmc.Badge("Validation devis", id= 'input-badge-validation-devis', color='grey')
                                            ], className="mb-2"),
                                        dbc.Row([
                                            dmc.Badge("Renouvellement", id= 'input-badge-alerte-renouvellement', color='grey')
                                            ], className="mb-2"),
                                        dbc.Row([
                                            dmc.Badge("Résilié", id= 'input-badge-resilie', color='grey')
                                            ], className="mb-2"),
                                        ])
                                    ])
                            ],width={"size": 3}),
                        ]),

                # Créez un Accordion pour chaque section
            dmc.Accordion(
    children=[
        dmc.AccordionItem(
            [
                dmc.AccordionControl("Status et conditions financières"),
                dmc.AccordionPanel(
                                    [dbc.Row([dbc.Col([dbc.Card(
                                        dbc.CardBody([
                                        # Contenu de la section 'Status'
                            dbc.Row([
                            dbc.Col([html.Label("Check Infos")], width={"size": 6}),
                            dbc.Col([daq.ToggleSwitch(
                                id='input-check-infos',
                                color="green",  # Couleur du bouton ON
                                # label=['Non', 'Oui'],  # Texte pour les positions OFF et ON
                                size=40,  # Taille du bouton
                                value=False  # Par défaut, OFF
                            )],width={"size": 6}         
                            ), 
                            dbc.Col([html.Label("Validation erronées")],width={"size": 6}),
                            dbc.Col([daq.ToggleSwitch(
                                id='input-validation-erronnes',
                                color="red",  # Couleur du bouton ON
                                size=40,  # Taille du bouton
                                value=False  # Par défaut, OFF
                            )],width={"size": 6}
                            ),  
                            dbc.Col([html.Label("Envoi devis")],width={"size": 6}),
                            dbc.Col([daq.ToggleSwitch(
                                id='input-envoi-devis',
                                color="green",  # Couleur du bouton ON
                                size=40,  # Taille du bouton
                                value=False  # Par défaut, OFF
                            )],width={"size": 6}
                            ),      
                            dbc.Col([html.Label("Accord de principe")],width={"size": 6}),
                            dbc.Col([daq.ToggleSwitch(
                                id='input-accord-de-principe',
                                color="green",  # Couleur du bouton ON
                                size=40,  # Taille du bouton
                                value=False  # Par défaut, OFF
                            )],width={"size": 6}
                            ),
                             dbc.Col([html.Label("Signature client")],width={"size": 6}),
                             dbc.Col([daq.ToggleSwitch(
                                 id='input-signature-client',
                                 color="green",
                                 size=40,
                                 value=False
                             )],width={"size": 6}
                             ),
                             dbc.Col([html.Label("Achat éditeur")],width={"size": 6}),
                             dbc.Col([daq.ToggleSwitch(
                                 id='input-achat-editeur',
                                 color="green",
                                 size=40,
                                 value=False
                             )],width={"size": 6}
                             ),
                            dbc.Col([html.Label("Traitement comptable")],width={"size": 6}),
                             dbc.Col([daq.ToggleSwitch(
                                 id='input-traitement-comptable',
                                 color="green",
                                 size=40,
                                 value=False
                                 )],width={"size": 6}
                             ),
                             dbc.Col([html.Label("Paiement SAP")],width={"size": 6}),
                             dbc.Col([daq.ToggleSwitch(
                                 id='input-paiement-sap',
                                 color="green",
                                 size=40,
                                 value=False
                            )],width={"size": 6}
                            ) ]
                            ),
                                        ]),
                                    )], width={"size": 6}),
                                    dbc.Col([dbc.Card(
                                        dbc.CardBody([
                                            
                                            dbc.Row([
                                            dbc.Col([
                                                dbc.Label('Nouveau prix d\'achat')], width={"size": 6}),
                                            dbc.Col([
                                                dcc.Input(id='input-nv-prix-achat' , type='number', placeholder='Entrez le NV prix d\'achat'),
                                                html.Span('€', style={'margin-left': '5px'})  # Ajoutez le symbole "€" après la case d'entrée
                                            ], width={"size": 6})]),
                                            dbc.Row([
                                            dbc.Col([
                                                dbc.Label('Nouveau prix de vente')], width={"size": 6}),
                                            dbc.Col([
                                                dcc.Input(id='input-nv-prix-vente', type='number', placeholder='Entrez le NV prix de vente '),
                                                html.Span('€', style={'margin-left': '5px'})
                                            ], width={"size": 6})]),
                                            dbc.Row([
                                            dbc.Col([
                                                dbc.Label("Marge %")], width={"size": 6}),
                                            dbc.Col([
                                                dcc.Input(id='input-Marge-pourcentage', type='number', placeholder='Entrez la Marge %'),
                                                html.Span('%', style={'margin-left': '5px'})
                                            ], width={"size": 6})]),
                                            dbc.Row([
                                            dbc.Col([
                                                dbc.Label("Montant vente annuel N+1")], width={"size": 6}),
                                            dbc.Col([
                                                dcc.Input(id='input-Montant-vente-annuel-N+1', type='number', placeholder='Entrez le Montant vente annuel N+1'),
                                                html.Span('€', style={'margin-left': '5px'})
                                            ], width={"size": 6})]),
                                            dbc.Row([
                                            dbc.Col([
                                                dbc.Label("Montant annuel Achat N+1")], width={"size": 6}),
                                            dbc.Col([
                                                dcc.Input(id='input-Montant-annuel-Achat-N+1', type='number', placeholder='Entrez le Montant annuel Achat N+1'),
                                                html.Span('€', style={'margin-left': '5px'})
                                            ], width={"size": 6})]),
                                            dbc.Row([
                                            dbc.Col([
                                                dbc.Label("Marge N+1 (%)")], width={"size": 6}),
                                            dbc.Col([
                                                dcc.Input(id='input-Marge-N+1', type='number', placeholder='Entrez la Marge N+1'),
                                                html.Span('%', style={'margin-left': '5px'})
                                            ], width={"size": 6})]),
                                            # Ajoutez d'autres éléments de contenu ici
                                        ]),
                                    )], width={"size": 6})]),
                         # Ajoutez d'autres éléments de contenu ici
                     ], id='status-content'  # Ajout ID à l'ensemble de contenu
                 ),
                 ],
                value="Status",
                        ),
                        dmc.Accordion(
                            children=[
                                dmc.AccordionItem(
                                    
                            value="Conditions financières",
                        ),
                        dmc.Accordion(
                            children=[
                                dmc.AccordionItem(
                                    [
                                        dmc.AccordionControl("Informations contractuelles"),
                                        dmc.AccordionPanel(
                                    [
                                        # Contenu de la section 'Informations contractuelles'
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Label("Type de contrat")],
                                                width={"size": 2,"offset":1}),
                                            dbc.Col([
                                                dcc.Dropdown(
                                                    id='input-type-contrat',
                                                    options=[
                                                        {'label': 'SAP BOBJ', 'value': 'SAP BOBJ'},
                                                        {'label': 'SAP PAPER', 'value': 'SAP PAPER'},
                                                        {'label': '', 'value': ''},
                                                    ],
                                                    placeholder='Sélectionnez le Type de contrat',
                                                ),
                                            ], width={"size": 2,"offset":-1}),
                                            dbc.Col([
                                                dbc.Label("Type de Support SAP")],
                                                width={"size": 2,"offset":1}),
                                            dbc.Col([
                                                dcc.Dropdown(
                                                    id='input-type-support-sap',
                                                    options=[
                                                        {'label': 'Enterprise', 'value': 'Enterprise'},
                                                        {'label': 'Standard', 'value': 'Standard'},
                                                        {'label': '', 'value': ''},
                                                    ],
                                                    placeholder='Sélectionnez le Type de support SAP',
                                                ),
                                            ], width={"size": 2,"offset":-1}),
                                            ], className="mb-2"),
                                                                                                                        
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Label("Condition de facturation")],
                                                width={"size": 2,"offset":1}),
                                            dbc.Col([
                                                dcc.Input(
                                                    id='input-cond-fact',
                                                    type='text',
                                                    placeholder='Conditions Facturation',
                                                ),
                                                ], width={"size": 2,"offset":-1}),
                                            dbc.Col([
                                                dbc.Label("Condition de Paiement")],
                                                width={"size": 2,"offset":1}),
                                            dbc.Col([
                                                dcc.Input(
                                                    id='input-cond-paiement',
                                                    type='text',
                                                    placeholder='Conditions de paiement',
                                                ),
                                            ], width={"size": 2,"offset":-1}),
                                        ], className="mb-2"),

                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Label('Adresse')],
                                                width={"size": 2,"offset":1}),
                                            dbc.Col([                                              
					                        dcc.Input(id='input-adresse-client', type='text',style={
                                            'width': '200px',  # Largeur du champ de saisie
                                            'height': '60px',  # Hauteur du champ de saisie
                                            'border': '1px solid #ccc',  # Bordure du champ de saisie
                                            'border-radius': '5px',  # Coins arrondis
                                            'padding': '5px',  # Espacement intérieur
                                        }, placeholder='adresse client'),
                                        ], {"size": 2,"offset":-1}),
                                            
                                         ], className="mb-2"),

                                         
                                        dbc.Row([dbc.Col([
                                                dbc.Label("Parc de licences")],
                                                width={"size": 2,"offset":1}),
                                            dbc.Col([
                                                dcc.Input(
                                                    id='input-parc-licences',
                                                    type='text',style={
                                            'width': '400px',  # Largeur du champ de saisie
                                            'height': '30px',  # Hauteur du champ de saisie
                                            'border': '1px solid #ccc',  # Bordure du champ de saisie
                                            'border-radius': '3px',  #'5px' Coins arrondis
                                            'padding': '5px',  # Espacement intérieur
                                        },
                                                    placeholder='Entrez le nom et la quantité du parc de licences (ex. Licence A: 10)',
                                                ),
                                            ], width={"size": 2,"offset":-1}),])
                                    ]
                                ),
                            ],
                            value="Informations contractuelles",
                        ),
                    ],
                ),
            ])])]),
            dbc.ModalFooter([
                dbc.Button("Valider", id="o1_btn_submit_validate", className="me-1", color="success"),
                dbc.Button("Annuler", id="o1_btn_submit_cancel", className="me-1", n_clicks=0, color="warning"),
                dbc.Button("Résilier", id="o1_btn_submit_resiliation", className="me-1", n_clicks=0, color="danger")
            ]),
        ],
        id="o1_modal",
        size="xl",
        is_open=False,
    )

    # Ajoutez d'autres éléments de votre mise en page ici


# Mise en page de l'application
layout_PCOE = html.Div([
    
    dbc.Row([
        dbc.Col([   
            dbc.Navbar([
                    dbc.Col([dcc.Link(dbc.Button(html.Img(src=app.get_asset_url("accueil.png"),style={"height":"30px"}), id="bouton_accueil", style={'border':'2px solid white','margin-left':'-1vw'},color='white'), href = '/'),
                        html.Img(src=app.get_asset_url("logo_seenovate.png"), height="30px",style={'margin-left':'1vw'})],xs=2,sm=2,md=2,lg=2,xl=2),
                    dbc.Col([html.Div(dbc.NavbarBrand(list_app["name"].loc[list_app["ind"]==n_app].iloc[0], id="titre",className="text-white"),style={"textAlign":"center"})
                    ],xs=9,sm=9,md=9,lg=9,xl=9,align="center"),
                    dbc.Col([html.Div(html.Img(src=app.get_asset_url("user.png"), height="30px"))])
            ],color="dark")
        ],xs=12,sm=12,md=12,lg=12,xl=12)
    ]),
     
    
    
# Ajoutez un dcc.Store pour stocker les données du tableau
    dcc.Store(id='data-store', data=[]),
    # gestion du téléchargement
    dcc.Download(id="download_devis"),

    # ... Le reste de votre mise en page ...


    # Intégration des 3 boutons de la mise en page (check infos..)
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4('Check infos', style={'color': '#191970'}),
                                dbc.Row([
                                    dbc.Col([
                                        html.Div(
                                            dcc.Dropdown(
                                                id='o1_tannerie',
                                                options=[
                                                    {'label': 'Non réalisé', 'value': 'non-realise'},
                                                    {'label': 'OK', 'value': 'ok'},
                                                    {'label': 'KO', 'value': 'ko'},
                                                ],
                                                multi=True,    
                                            ), style={'fontSize': '20px','font-weight': 'bold','text-align':'center'}),
                                    ],width=10),
                                    dbc.Col([    
                                        dbc.Spinner(html.Div(id="o1_spinner_tannerie")),
                                    ],width=2)
                                ],className="mb-2")
                            ]
                        )
                    ),
                ],className="mt-4 shadow"),
            ],xs=4,sm=4,md=4,lg=4,xl=4,align="start"), 
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4('Nombre de lignes validées', style={'color': '#191970'}),
                                html.Div(html.H2(id='o1_nb_lignes_validees'), style={'fontSize': '20px','font-weight': 'bold','text-align':'center'}),
                            ]
                        )
                    ),
                    dbc.Card(
                        html.Div(className="fa fa-check-square", style={'color':'white','text-align': 'center','font-size': 30,'margin': 'auto'}),
                        className="bg-success",
                        style={"maxWidth": 75},
                    ),
                
                ],className="mt-4 shadow"),
            ],xs=4,sm=4,md=4,lg=4,xl=4,align="start"),  
            dbc.Col([    
                dbc.CardGroup([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4('Nombre de lignes non validées', style={'color': '#191970'}),
                                html.Div(html.H2(id='o1_nb_lignes_non_validees'), style={'fontSize': '20px','font-weight': 'bold','text-align':'center'}),
                            ]
                        )
                    ),
                    dbc.Card(
                        html.Div(className="fa fa-floppy-o", style={'color':'white','text-align': 'center','font-size': 30,'margin': 'auto'}),
                    
                        className="bg-warning",
                        style={"maxWidth": 75},
                    ),
                
                ],className="mt-4 shadow"),
            ],xs=4,sm=4,md=4,lg=4,xl=4,align="start"),  
        ]),
    ], fluid=True),
    
    # Le reste de votre mise en page...
    

# Création de la DataTable + ajout nouvelles colonnes
dash_table.DataTable(
    columns=new_columns,
    data=df.to_dict('records'),
    id='o1_data_table',
    style_table={'height': '60vh',
                'overflowX': 'auto',
                'overflowY': 'auto',
                'margin-left': '20px',
                'margin-top': '20px',
                'margin-right': '20px'},
    style_cell={'font_family': 'calibri',
                'height': 'auto',
                'textAlign': 'center',
                'minWidth': 50,
                'maxWidth': 150},
    style_data={'font-family': 'Bahnschrift Light'},
    style_data_conditional=[{
        "if": {"state": "selected"},
        "backgroundColor": "rgba(0, 116, 217, .03)",
        "border": "1px solid black",
    },#Alerte renouvellement(feux tricolores)
    {'if':{
            'filter_query':'{Alerte renouvellement}>120',
            'column_id':'Alerte renouvellement'
        },
      'backgroundColor':'green'
      },                         
    {'if':{
            'filter_query':'{Alerte renouvellement}<120',
            'column_id':'Alerte renouvellement'
        },
      'backgroundColor':'orange'
      },
    {'if':{
            'filter_query':'{Alerte renouvellement}<45',
            'column_id':'Alerte renouvellement'
        },
      'backgroundColor':'red'
      },#Alerte validation devis (feux tricolores)
    {'if':{
            'filter_query':'{Alerte validation devis}>240',
            'column_id':'Alerte validation devis'
        },
      'backgroundColor':'green'
      },                         
    {'if':{
            'filter_query':'{Alerte validation devis}<240',
            'column_id':'Alerte validation devis'
        },
      'backgroundColor':'orange'
      },
    {'if':{
            'filter_query':'{Alerte validation devis}<90',
            'column_id':'Alerte validation devis'
        },
      'backgroundColor':'red'
      },

     ],
    sort_action='native',
    sort_mode='single',
    filter_action='native',
    row_selectable='single'
),
    
    # Bouton "Modifier une saisie"
dbc.Row([
    dbc.Col([
        dbc.Button('Modifier une saisie', id="o1_btn_modif_ech", className="me-1", n_clicks=0, color='warning'),
    ], width={"size": 3, "offset": 3}),
    dbc.Col([
        dbc.Button('Générer Devis', id="o1_btn_gener_devis", className="me-1", n_clicks=0, color='success'),
        ],width={"size": 3, "offset": 0})
], className="pb-3"),

 modal_pop_up, stockage_ligne, stockage_mis_a_jour
    
])
