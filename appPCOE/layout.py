import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from dash import dcc,html
from app import app
import pandas as pd
import plotly.graph_objs as go
from datetime import date
from colors import *
# import dash_mantine_components as dmc
import dash_mantine_components as dmc


# Import functions
# from index import get_auth

######################################################################################
#                                       Data                                         #
######################################################################################

## Chargement fichier csv : pour gérer infos principales des différentes applis
list_app = pd.read_csv("assets/list_app.csv", header=0, sep=';')
n_app = 1 # numéro de l'appli


# Charger le tableau Excel
# df = pd.read_excel(r"/mnt/c/CA_2023.xlsx", sheet_name='Maintenance SAP BusinessObjects')
df = pd.read_excel(r"C:\Users\SofianOUASS\Desktop\PCoE\Suivi CA licences et maintenance 2023.xlsx", sheet_name='Maintenance SAP BusinessObjects')


# Ajout des 4 nouvelles colonnes après 'Achat SAP Maintenance ou GBS ou NEED4VIZ'
new_columns = []
for col in df.columns:
    new_columns.append({'name': col, 'id': col, 'type': 'text'})
    if col == 'Achat SAP Maintenance ou GBS ou NEED4VIZ':
        new_columns.append({'name': 'Alerte renouvellement', 'id': 'Alerte renouvellement', 'type': 'text'})
        new_columns.append({'name': 'Alerte validation devis', 'id': 'Alerte validation devis', 'type': 'text'})
        new_columns.append({'name': 'Nouveau prix d\'achat', 'id': 'Nouveau prix d\'achat', 'type': 'text'})
        new_columns.append({'name': 'Nouveau prix de vente', 'id': 'Nouveau prix de vente', 'type': 'text'})


#############################################################################################################
#                                          Appel API                                                        #
#############################################################################################################



#############################################################################################################
#                                                                                                           #
#############################################################################################################


##liste des noms de colonne: Informations contrats clients=
# ['Client', 'ERP Number \nRéf SAP', 'Date anniversaire', 'Code projet Boond', 'Resp\nCommercial', 'Type de contrat']

# #liste des noms de colonne: Autres infos =['CA maintenance facturé', 'Achat SAP Maintenance ou GBS ou NEED4VIZ',
#   'Marge maintenance ', 'Marge %', 'Montant vente annuel N+1', 'Montant annuel Achat N+1',
#     "Mois d'imputation", 'Type de support SAP', 'Parc/Techno', 'Numéro de facture',
#       'Date de facture', 'Proposition SAP reçue', 'Relance client**', 'Proposition Seenovate créée',
#         'Proposition Seenovate envoyée', 'Proposition signée par le client', 'Attente  N° Cde client avant facturation',
#           'Facture  créée', 'Commande faite SAP', 'Facture SAP reçue', 'Remarques',
#             'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'décembre',
#               'janvier.1', 'février.1', 'mars.1', 'avril.1', 'mai.1', 'juin.1', 'juillet.1', 'aout.1', 'septembre.1', 'octobre.1',
#                 'novembre.1', 'décembre.1']

# Ajout d'un composant dcc.Store pour stocker les données de la ligne sélectionnée
stockage_ligne = dcc.Store(id='o1_store_row')
stockage_mis_a_jour = dcc.Store(id='o1_store_updated_data')  # Ajout de ce composant

modal_pop_up= dbc.Modal(
         [
            dbc.ModalHeader(dbc.ModalTitle("Modifier la saisie")),
            dbc.ModalBody([
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
                                dbc.Label(id='input-code-projet') # En attente de Boond
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
                # Créez un Accordion pour chaque section
                dmc.Accordion(
    children=[
        dmc.AccordionItem(
            [
                dmc.AccordionControl("Status"),
                dmc.AccordionPanel(
                                    [
                                        # Contenu de la section 'Status'
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Label("Accord de principe", width=6),
                                                dcc.Dropdown(
                                                    id='input-accord-de-principe',
                                                    options=[
                                                        {'label': 'Oui', 'value': 'Oui'},
                                                        {'label': 'Non', 'value': 'Non'},
                                                    ],
                                                    placeholder='Sélectionnez une option',
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Signature client", width=6),
                                                dcc.Dropdown(
                                                    id='input-signature-client',
                                                    options=[
                                                        {'label': 'Oui', 'value': 'Oui'},
                                                        {'label': 'Non', 'value': 'Non'},
                                                    ],
                                                    placeholder='Sélectionnez une option',
                                                ),
                                            ], width={"size": 6}),
                                        ]),
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Label("Achat éditeur", width=6),
                                                dcc.Dropdown(
                                                    id='input-achat-editeur',
                                                    options=[
                                                        {'label': 'Oui', 'value': 'Oui'},
                                                        {'label': 'Non', 'value': 'Non'},
                                                    ],
                                                    placeholder='Sélectionnez une option',
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Paiement SAP", width=6),
                                                dcc.Dropdown(
                                                    id='input-paiement-sap',
                                                    options=[
                                                        {'label': 'Oui', 'value': 'Oui'},
                                                        {'label': 'Non', 'value': 'Non'},
                                                    ],
                                                    placeholder='Sélectionnez une option',
                                                ),
                                            ], width={"size": 6}),
                                            # Ajoutez d'autres éléments de contenu ici
                                        ]),
                                    ]
                                ),
                            ],
                            value="Status",
                        ),
                        dmc.Accordion(
                            children=[
                                dmc.AccordionItem(
                                    [
                                        dmc.AccordionControl("Conditions financières"),
                                        dmc.AccordionPanel(
                                    [
                                        # Contenu de la section 'Conditions financières'
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Label('Nouveau prix d\'achat', width=6),
                                                dcc.Input(id='Nouveau prix d\'achat', type='number', placeholder='Entrez le NV prix d\'achat'),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label('Nouveau prix de vente', width=6),
                                                dcc.Input(id='Nouveau prix de vente', type='number', placeholder='Entrez le NV prix de vente '),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Marge maintenance", width=6),
                                                dcc.Input(id='input-Marge-maintenance', type='number', placeholder='Entrez la Marge maintenance'),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Marge %", width=6),
                                                dcc.Input(id='input-Marge-pourcentage', type='number', placeholder='Entrez la Marge %'),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Montant vente annuel N+1", width=6),
                                                dcc.Input(id='input-Montant-vente-annuel-N+1', type='number', placeholder='Entrez le Montant vente annuel N+1'),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Montant annuel Achat N+1", width=6),
                                                dcc.Input(id='input-Montant-annuel-Achat-N+1', type='number', placeholder='Entrez le Montant annuel Achat N+1'),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Mois d'imputation", width=6),
                                                dcc.Input(id='input-mois-imputation', type='text', placeholder='Sélectionnez une date'),
                                            ], width={"size": 6}),
                                            # Ajoutez d'autres éléments de contenu ici
                                        ]),
                                    ]
                                ),
                            ],
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
                                                dbc.Label('CA maintenance facturé', width=6),
                                                dcc.Input(id='input-CA-maintenance-facture', type='number', placeholder='Entrez le CA maintenance facturé'),
                                            ], width={"size": 6}), # step='0.01' arrondi à 2 chiffre après la virgule
                                            dbc.Col([
                                                dbc.Label('Achat SAP Maintenance ou GBS ou NEED4VIZ', width=6),
                                                dcc.Input(id='input-Achat-SAP-Maintenance-GBS-NEED4VIZ', type='number', placeholder='Entrez le Achat SAP Maintenance ou GBS ou NEED4VIZ'),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Type de support SAP", width=6)],
                                                width={"size": 3}),
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
                                            ], width={"size": 3}),
                                            dbc.Col([
                                                dbc.Label("Parc/Techno", width=6),
                                                dcc.Input(id='input-Parc-Techno', type='text', placeholder='Entrez le Parc/Techno'),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Numéro de facture", width=6),
                                                dcc.Input(id='input-Numero-de-facture', type='number', placeholder='Entrez le Numéro de facture'),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Date de facture", width=6),
                                                dcc.DatePickerSingle(id='input-Date-de-facture', display_format='DD/MM/YYYY', placeholder='Sélectionnez une date'),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Parc de licences", width=6),
                                                dcc.Input(
                                                    id='input-parc-licences',
                                                    type='text',
                                                    placeholder='Entrez le nom et la quantité du parc de licences (ex. Licence A: 10)',
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Coeff évolution prix achat", width=6),
                                                dcc.Input(
                                                    id='input-coeff-evolution-prix-achat',
                                                    type='number',
                                                    placeholder='Entrez le Coeff évolution prix achat',
                                                    step=0.01,  # 2 chiffres après la virgule
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Coeff marge", width=6),
                                                dcc.Input(
                                                    id='input-coeff-marge',
                                                    type='number',
                                                    placeholder='Entrez le Coeff marge',
                                                    step=0.01,  # 2 chiffres après la virgule
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Proposition SAP reçue", width=6),
                                                dcc.Dropdown(
                                                    id='input-Proposition-SAP-reçue',
                                                    options=[
                                                        {'label': 'OK', 'value': 'OK'},
                                                        {'label': ' ', 'value': ' '}
                                                    ],
                                                    placeholder='Sélectionnez une option',
                                                    value='',  # Vous pouvez définir une valeur par défaut si nécessaire
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Relance client**", width=6),
                                                dcc.DatePickerSingle(
                                                    id='input-relance-client',
                                                    display_format='DD/MM/YYYY',  # Format jour, mois et année
                                                    placeholder='Sélectionnez une date de relance',
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Proposition Seenovate créée", width=6),
                                                dcc.Dropdown(
                                                    id='input-Proposition-Seenovate-creee',
                                                    options=[
                                                        {'label': 'OK', 'value': 'OK'},
                                                        {'label': ' ', 'value': ' '}
                                                    ],
                                                    placeholder='Sélectionnez une option',
                                                    value='',  # Vous pouvez définir une valeur par défaut si nécessaire
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Proposition Seenovate envoyée", width=6),
                                                dcc.DatePickerSingle(
                                                    id='input-Proposition-Seenovate-envoyee',
                                                    display_format='DD/MM/YYYY',  # Format jour, mois et année
                                                    placeholder='Sélectionnez une date',
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Proposition signée par le client", width=6),
                                                dcc.DatePickerSingle(
                                                    id='input-Proposition-signee-par-le-client',
                                                    display_format='DD/MM/YYYY',  # Format jour, mois et année
                                                    placeholder='Sélectionnez une date',
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Attente N° Cde client avant facturation", width=6),
                                                dcc.Input(id='input-attente-Cde-client', type='text', placeholder='Entrez le N° Cde client avant facturation'),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Facture créée", width=6),
                                                dcc.DatePickerSingle(id='input-facture-creee', display_format='DD/MM/YYYY', placeholder='Entrez la Facture créée'),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Commande faite SAP", width=6),
                                                dcc.Input(id='input-commande-faite-sap', type='text', placeholder='Entrez la Commande faite SAP'),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Facture SAP reçue", width=6),
                                                dcc.Input(id='input-facture-sap-recue', type='text', placeholder='Entrez la Facture SAP reçue'),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Remarques", width=6),
                                                dcc.Input(id='input-remarques', type='text', placeholder='Entrez les Remarques'),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Conditions contractuelles et facturation", width=6),
                                                dcc.Input(id='input-conditions-contractuelles', type='text', placeholder='Entrez les conditions contractuelles et facturation'),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Devis", width=6),
                                                dcc.Dropdown(
                                                    id='input-devis',
                                                    options=[
                                                        {'label': 'Oui', 'value': 'Oui'},
                                                        {'label': 'Non', 'value': 'Non'},
                                                    ],
                                                    placeholder='Sélectionnez une option',
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Renouvelé", width=6),
                                                dcc.Dropdown(
                                                    id='input-renouvele',
                                                    options=[
                                                        {'label': 'Oui', 'value': 'Oui'},
                                                        {'label': 'Non', 'value': 'Non'},
                                                    ],
                                                    placeholder='Sélectionnez une option',
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Traitement comptable", width=6),
                                                dcc.Dropdown(
                                                    id='input-traitement-comptable',
                                                    options=[
                                                        {'label': 'Oui', 'value': 'Oui'},
                                                        {'label': 'Non', 'value': 'Non'},
                                                    ],
                                                    placeholder='Sélectionnez une option',
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Demande de résiliation", width=6),
                                                dcc.Dropdown(
                                                    id='input-demande-resiliation',
                                                    options=[
                                                        {'label': 'Oui', 'value': 'Oui'},
                                                        {'label': 'Non', 'value': 'Non'},
                                                    ],
                                                    placeholder='Sélectionnez une option',
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Communication éditeur", width=6),
                                                dcc.Dropdown(
                                                    id='input-communication-editeur',
                                                    options=[
                                                        {'label': 'Oui', 'value': 'Oui'},
                                                        {'label': 'Non', 'value': 'Non'},
                                                    ],
                                                    placeholder='Sélectionnez une option',
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Résilié", width=6),
                                                dcc.Dropdown(
                                                    id='input-resilie',
                                                    options=[
                                                        {'label': 'Oui', 'value': 'Oui'},
                                                        {'label': 'Non', 'value': 'Non'},
                                                    ],
                                                    placeholder='Sélectionnez une option',
                                                ),
                                            ], width={"size": 6}),
                                            dbc.Col([
                                                dbc.Label("Converti ou Extension", width=6),
                                                dcc.Dropdown(
                                                    id='input-converti-extension',
                                                    options=[
                                                        {'label': ' ', 'value': ' '},
                                                        {'label': 'Converti', 'value': 'Converti'},
                                                        {'label': 'Extension', 'value': 'Extension'},
                                                    ],
                                                    placeholder='Sélectionnez une option',
                                                ),
                                            ], width={"size": 6}),
                                            # Ajoutez d'autres éléments de contenu ici
                                        ]),
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
                dbc.Button("Enregistrer", id="o1_btn_submit_save", className="me-1", n_clicks=0, color="warning"),
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
    }],
    sort_action='native',
    sort_mode='single',
    filter_action='native',
    row_selectable='single',
    export_format="xlsx"
),
    
    # Bouton "Modifier une saisie"
dbc.Row([
    dbc.Col([
        dbc.Button('Modifier une saisie', id="o1_btn_modif_ech", className="me-1", n_clicks=0, color='warning'),
    ], width={"size": 6, "offset": 3})  # Offset de 3 pour centrer le bouton
], className="pb-3"),

 modal_pop_up, stockage_ligne, stockage_mis_a_jour
    
])
