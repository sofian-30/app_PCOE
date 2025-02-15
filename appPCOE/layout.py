import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_mantine_components as dmc
import pandas as pd
from dash import dash_table, dcc, html
from dash.dash_table.Format import Format, Symbol, Scheme

from app import app
from db import connect_to_db, disconnect_from_db, sql_to_df
from utils import apply_calcul_sale_price, get_resp_commercial

# Import functions
# from index import get_auth

######################################################################################
#                                       Data                                         #
######################################################################################

# Chargement fichier csv : pour gérer infos principales des différentes applis
list_app = pd.read_csv("assets/list_app.csv", header=0, sep=';')
n_app = 1  # numéro de l'appli

# Charger les tables app_table et boond_table
conn = connect_to_db()
df_app = sql_to_df("SELECT * FROM app_table", conn=conn)
df_boond = sql_to_df("SELECT * FROM boond_table", conn=conn)
disconnect_from_db(conn)
df = pd.merge(df_boond, df_app, how='inner', on='code_projet_boond')

columns_to_convert = ['prix_achat_n1', 'prix_vente_n1', 'marge_n1']
for column in columns_to_convert:
    df[column] = df[column].astype(float)

df[['prix_achat_n1', 'prix_vente_n1', 'marge_n1']] = df.apply(apply_calcul_sale_price, axis=1)

df["date_anniversaire"] = df["date_anniversaire"].dt.date

# Obligé de forcer le str pour le conditionnal formatiing du datatable...
columns_to_convert = ['envoi_devis', 'accord_principe']
for column in columns_to_convert:
    df[column] = df[column].fillna('')
    df[column] = df[column].astype(str)

db_app_name_correspondance = {'agence': 'Agence',
                              'client': 'Client',
                              'num_ref_sap': 'ERP_Number_Ref_SAP',
                              'code_projet_boond': 'Code projet Boond',
                              'date_anniversaire': 'Date anniversaire',
                              'alerte_renouvellement': 'Alerte renouvellement',
                              'alerte_validation_devis': 'Alerte validation devis',
                              'prix_achat_n': "Prix d'achat année N",
                              'prix_vente_n': 'Prix de vente année N',
                              'marge_n': 'Marge année N',
                              'prix_achat_n1': "Prix d'achat année N+1",
                              'prix_vente_n1': 'Prix de vente année N+1',
                              'marge_n1': 'Marge année N+1',
                              'adresse': 'Adresse',
                              'ville': 'Ville',
                              'code_postal': 'Code postal',
                              # '': 'Editeur',
                              'type_support_sap': 'Type de support SAP',
                              'type_contrat': 'Type de contrat',
                              #'parc_techno': 'Parc/Techno',
                              # '': 'Numéro de facture',
                              # '': 'Date de facture',
                              'resp_commercial': 'Responsable commercial',
                              #'proposition_sap_recue': 'Proposition SAP reçue',
                              #'date_relance_client': 'Date de relance client',
                              #'proposition_seenovate_creee': 'Proposition Seenovate créée',
                              #'date_envoi_proposition': "Date d'envoi de la proposition",
                              #'date_signature_proposition': 'Date de signature par le client',
                              #'num_commande': 'Attente N° Cde client avant facturation',
                              #'date_creation_facture': 'Date de création de la facture',
                              #'commande_faite_sap': 'Commande faite SAP',
                              #'facture_sap_recue': 'Facture SAP reçue',
                              #'remarques': 'Remarques',
                              'devis': 'Devis',
                              'check_infos': 'Check infos',
                              'validation_erronee': 'Validation erronée',
                              'envoi_devis': 'Envoi devis',
                              'accord_principe': 'Accord de principe',
                              'signature_client': 'Signature client',
                              'achat_editeur': 'Achat éditeur',
                              'traitement_comptable': 'Traitement comptable',
                              'paiement_sap': 'Paiement SAP',
                              #'renouvele': 'Renouvelé',
                              #'demande_resiliation': 'Demande de résiliation',
                              #'communication_editeur': 'Communication éditeur',
                              'resilie': 'Résilié',
                              #'converti_extension': 'Converti ou Extension',
                              'condition_facturation': 'Condition de facturation',
                              'condition_paiement': 'Condition de paiement',
                              'parc_licence': 'Parc de licences'
                              }

data_table_columns = []
for name_db, name_app in db_app_name_correspondance.items():
    if name_db in ['prix_achat_n', 'prix_vente_n',  'prix_achat_n1', 'prix_vente_n1']:
        data_table_columns.append({'name': name_app, 'id': name_db, 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=2, symbol=Symbol.yes, symbol_suffix='€')})
    elif name_db in ['alerte_renouvellement', 'alerte_validation_devis']:
        data_table_columns.append({'name': name_app, 'id': name_db, 'type': 'numeric', 'format':Format(precision=2, scheme=Scheme.decimal_integer)})
    elif name_db in ['marge_n','marge_n1']:
        data_table_columns.append({'name': name_app, 'id': name_db, 'type': 'numeric', 'format':Format(precision=2, scheme=Scheme.percentage)})
    else:
        data_table_columns.append({'name': name_app, 'id': name_db, 'type': 'text'})
        
value_resp_commercial = get_resp_commercial()
options_resp_commercial = [{'label': resp, 'value': resp} for resp in value_resp_commercial]

#############################################################################################################
#                                          Appel API                                                        #
#############################################################################################################

stockage_ligne = dcc.Store(id='o1_store_row')
stockage_mis_a_jour = dcc.Store(id='o1_store_updated_data')
stockage_popup_evprix = dcc.Store(id='excel_data')

# Fenêtre modale pour la modification de saisie (Avec Accordion)
modal_pop_up = dbc.Modal(
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
                                    dbc.Label("Client")
                                ], width=3),
                                dbc.Col([
                                    dbc.Label(id='input-client')
                                ], width=3),
                                dbc.Col([
                                    dbc.Label("ERP Number")
                                ], width=3),
                                dbc.Col([
                                    dbc.Label(id='input-erp-number')
                                ], width=3)
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Date anniversaire")
                                ], width=3),
                                dbc.Col([
                                    dbc.Label(id='input-date-anniversaire')
                                ], width=3),
                                dbc.Col([
                                    dbc.Label("Code projet Boond")
                                ], width=3),
                                dbc.Col([
                                    dbc.Label(id='input-code-projet-boond')
                                ], width=3)
                            ]), 
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Resp. Commercial")
                                ], width=3),
                                dbc.Col([
                                    dbc.Label(id='input-resp-commercial')
                                ], width=3),
                                dbc.Col([
                                    dbc.Label("Editeur")
                                ], width=3),
                                dbc.Col([
                                    dbc.Label(id='input-editeur')
                                ], width=3)
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Type de contrat")],
                                    width={"size": 3}),
                                dbc.Col([
                                    dcc.Input(
                                        id='input-type-contrat',
                                        type='text', value='Valeur non modifiable',
                                        style={'border': 'none', 'pointer-events': 'none'},
                                        placeholder='Type de contrat',
                                    ),
                                ], width={"size": 3}),
                                dbc.Col([
                                    dbc.Label("Type de Support SAP")],
                                    width={"size": 3}),
                                dbc.Col([
                                    dcc.Input(
                                        id='input-type-support-sap', value='Valeur non modifiable',
                                        style={'border': 'none', 'pointer-events': 'none'},
                                        type='text',
                                        placeholder='Type de Support SAP',
                                    ),
                                ], width={"size": 3}),
                            ], className="mb-2"),

                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Condition de facturation")],
                                    width={"size": 3}),
                                dbc.Col([
                                    dcc.Input(
                                        id='input-cond-fact',
                                        type='text', value='Valeur non modifiable',
                                        style={'border': 'none', 'pointer-events': 'none'},
                                        placeholder='Conditions Facturation',
                                    ),
                                ], width={"size": 3}),
                                dbc.Col([
                                    dbc.Label("Condition de Paiement")],
                                    width={"size": 3}),
                                dbc.Col([
                                    dcc.Input(
                                        id='input-cond-paiement', value='Valeur non modifiable',
                                        style={'border': 'none', 'pointer-events': 'none'},
                                        type='text',
                                        placeholder='Conditions de paiement',
                                    ),
                                ], width={"size": 3}),
                            ], className="mb-2"),

                            dbc.Row([
                                dbc.Col([
                                    dbc.Label('Adresse')],
                                    width={"size": 3}),
                                dbc.Col([
                                    dcc.Textarea(
                                        id='input-adresse-client', readOnly=True,
                                        style={
                                            'width': '200px',  # Largeur du champ de saisie
                                            'height': '100px',  # Hauteur du champ de saisie
                                            'border': 'none',  # Bordure du champ de saisie
                                            'border-radius': '5px',  # Coins arrondis
                                            'padding': '5px',  # Espacement intérieur
                                        },
                                        placeholder='adresse client'
                                    ),
                                ], {"size": 2}),
                            ], className="mb-2"),
                        ])
                    ]),
                ], width={"size": 9}),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Alertes"),
                        dbc.CardBody([
                            dbc.Row([
                                dmc.Badge("Renouvellement", id='input-badge-alerte-renouvellement', color='blue')
                            ], className="mb-2"),
                            dbc.Row([
                                dmc.Badge("Génération devis", id='input-badge-generation-devis', color='blue')
                            ], className="mb-2"),
                            dbc.Row([
                                dmc.Badge("Validation devis", id='input-badge-validation-devis', color='blue')
                            ], className="mb-2"),
                            dbc.Row([
                                dmc.Badge("Résilié", id='input-badge-resilie', color='blue')
                            ], className="mb-2"),
                        ])
                    ])
                ], width={"size": 3}),
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
                                            dbc.Col([dmc.Switch(
                                                id='input-check-infos',
                                                color="green",  # Couleur du bouton ON
                                                # label=['Non', 'Oui'],  # Texte pour les positions OFF et ON
                                                size=20,  # Taille du bouton
                                                checked=False,  # Par défaut, OFF
                                            ),
                                                dbc.Col([
                                                    html.Div(id='check-infos-date',
                                                            style={'padding-top': '10px', 'text-align': 'left',
                                                                    'font-weight': 'bold'}), ], width={"size": 6}
                                                )]),
                                            dbc.Col([html.Label("Validation erronées")], width={"size": 6}),
                                            dbc.Col([dmc.Switch(
                                                id='input-validation-erronnes',
                                                color="red",  # Couleur du bouton ON
                                                size=20,  # Taille du bouton
                                                checked=False  # Par défaut, OFF
                                            )], width={"size": 6}
                                            ),
                                            dbc.Col([html.Label("Envoi devis")], width={"size": 6}),
                                            dbc.Col([dmc.Switch(
                                                id='input-envoi-devis',
                                                color="green",  # Couleur du bouton ON
                                                size=20,  # Taille du bouton
                                                checked=False  # Par défaut, OFF
                                            )], width={"size": 6}
                                            ),
                                            dbc.Col([html.Label("Accord de principe")], width={"size": 6}),
                                            dbc.Col([dmc.Switch(
                                                id='input-accord-de-principe',
                                                color="green",  # Couleur du bouton ON
                                                size=20,  # Taille du bouton
                                                checked=False  # Par défaut, OFF
                                            )], width={"size": 6}
                                            ),
                                            dbc.Col([html.Label("Signature client")], width={"size": 6}),
                                            dbc.Col([dmc.Switch(
                                                id='input-signature-client',
                                                color="green",
                                                size=20,
                                                checked=False
                                            )], width={"size": 6}
                                            ),
                                            dbc.Col([html.Label("Achat éditeur")], width={"size": 6}),
                                            dbc.Col([dmc.Switch(
                                                id='input-achat-editeur',
                                                color="green",
                                                size=20,
                                                checked=False
                                            )], width={"size": 6}
                                            ),
                                            dbc.Col([html.Label("Traitement comptable")], width={"size": 6}),
                                            dbc.Col([dmc.Switch(
                                                id='input-traitement-comptable',
                                                color="green",
                                                size=20,
                                                checked=False
                                            )], width={"size": 6}
                                            ),
                                            dbc.Col([html.Label("Paiement SAP")], width={"size": 6}),
                                            dbc.Col([dmc.Switch(
                                                id='input-paiement-sap',
                                                color="green",
                                                size=20,
                                                checked=False
                                            )], width={"size": 6}
                                            )]
                                        ),
                                    ]),
                                )], width={"size": 6}),
                                    dbc.Col([dbc.Card(
                                        dbc.CardBody([

                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Label('Prix d\'achat actuel')], width={"size": 6}),
                                                dbc.Col([
                                                    dcc.Input(id='input-prix-achat-actuel', type='number',
                                                            value='Valeur non modifiable',
                                                            style={'border': 'none', 'pointer-events': 'none'},
                                                            placeholder='Entrez prix d\'achat N'),
                                                    html.Span('€', style={'margin-left': '5px'})
                                                    # Ajoutez le symbole "€" après la case d'entrée
                                                ], width={"size": 6})]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Label('Prix de vente actuel')], width={"size": 6}),
                                                dbc.Col([
                                                    dcc.Input(id='input-prix-vente-actuel', type='number',
                                                            value='Valeur non modifiable',
                                                            style={'border': 'none', 'pointer-events': 'none'},
                                                            placeholder='Entrez prix de vente N '),
                                                    html.Span('€', style={'margin-left': '5px'})
                                                ], width={"size": 6})]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Label("Marge %")], width={"size": 6}),
                                                dbc.Col([
                                                    dcc.Input(id='input-Marge-pourcentage', type='number',
                                                            value='Valeur non modifiable',
                                                            style={'border': 'none', 'pointer-events': 'none'},
                                                            placeholder='Entrez la Marge %'),
                                                    html.Span('%', style={'margin-left': '5px'})
                                                ], width={"size": 6})]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Label("Nouveau prix d'achat")], width={"size": 6}),
                                                dbc.Col([
                                                    dcc.Input(id='input-nv-prix-achat', type='number',
                                                            placeholder='Entrez prix achat N+1',debounce=False),
                                                    html.Span('€', style={'margin-left': '5px'})
                                                ], width={"size": 6})]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Label("Nouveau prix de vente")], width={"size": 6}),
                                                dbc.Col([
                                                    dcc.Input(id='input-nv-prix-vente', type='number',
                                                            placeholder='Entrez prix vente N+1',debounce=False),
                                                    html.Span('€', style={'margin-left': '5px'})
                                                ], width={"size": 6})]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Label("Marge N+1 (%)")], width={"size": 6}),
                                                dbc.Col([
                                                    dbc.Label(id='input-Marge-N+1'),
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
                                            dmc.AccordionControl("Parc de licences"),
                                            dmc.AccordionPanel(
                                                [
                                                    dbc.Row([
                                                         dbc.Col([
                                                            dcc.Textarea(
                                                                id='input-parc-licences',
                                                                style={
                                                                    'width': '100%',  # Largeur du champ de texte
                                                                    'height': 200,
                                                                    # Hauteur du champ de texte (ajustez-la selon vos besoins)
                                                                    'border': '1px solid #ccc',
                                                                    # Bordure du champ de texte
                                                                    'border-radius': '3px',  # Coins arrondis
                                                                    'padding': '5px',  # Espacement intérieur
                                                                },
                                                                placeholder='Entrez le nom et la quantité du parc de licences (ex. Licence A: 10)',
                                                            ),
                                                        ],  # width={"size": 2, "offset": -1}
                                                        ),
                                                    ])  #
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
            html.Div([
                dbc.Button("Résilier", id="o1_btn_submit_resiliation", className="me-1", n_clicks=0, color="danger"),
                dcc.ConfirmDialog(
                    id="confirm-resiliation",
                    message="Souhaitez-vous réellement saisir une résiliation client?",
                ),
            ]),

        ]),
    ],
    id="o1_modal",
    size="xl",
    is_open=False,
)

# Ajoutez d'autres éléments de votre mise en page ici

# Modal pour afficher le tableau Excel "Tableau coefficient des prix"
modal_pop_up_evol_prix = dbc.Modal([
    dbc.ModalHeader("Tableau coefficient des prix"),
    dcc.Loading(
        id="loading-excel-table",
        type="default",
        children=[
            dash_table.DataTable(
                id='excel_table',
                columns=[
                    {"name": str(col), "id": col} for col in df.columns
                ],
                data=df.to_dict('records'),
                page_size=10,  # Nombre d'entrées par page
            ),
        ]
    ),
    dbc.ModalFooter(
        dbc.Button("Fermer", id="close_excel_modal", className="ml-auto")
    ),
], id="excel_modal", is_open=False, style={'max-width': '80%'})

# Mise en page de l'application
layout_PCOE = html.Div([

    dbc.Row([
        dbc.Col([
            dbc.Navbar([
                dbc.Col([dcc.Link(dbc.Button(html.Img(src=app.get_asset_url("accueil_white.png"), style={"height": "30px"}),
                                            id="bouton_accueil",
                                            style={'border': '2px solid white', 'margin-left': '1%'}, color='white'),
                                href='/'),
                        # html.Img(src=app.get_asset_url("logo_seenovate.png"), height="30px",
                        #         style={'margin-left': '1vw'})
                        ], xs=2, sm=2, md=2, lg=2, xl=2),
                dbc.Col([html.Div(dbc.NavbarBrand(list_app["name"].loc[list_app["ind"] == n_app].iloc[0], id="titre",
                                                className="text-white", style = {'fontSize':'1.5vh'}), style={"textAlign": "center"})
                        ], xs=8, sm=8, md=8, lg=8, xl=8, align="center"),
                dbc.Col([html.Img(src=app.get_asset_url("logo_seenovate.png"), height="30px",
                                style={'margin-left': '70%'})], width={'size':'1','offset':'1'})
                # dbc.Col([html.Div(html.Img(src=app.get_asset_url("user.png"), height="30px"))])
            ], color="dark")
        ], xs=12, sm=12, md=12, lg=12, xl=12, className="justify-content-center")
    ]),

    # Ajoutez un dcc.Store pour stocker les données du tableau
    dcc.Store(id='data-store', data=[]),
    # gestion du téléchargement
    dcc.Download(id="download_devis"),


    # Intégration des 3 boutons de la mise en page (check infos..)
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H3('Responsable commercial', style={'color': '#191970'}),
                            dbc.Row([
                                dbc.Col([
                                    html.Div(
                                        dcc.Dropdown(
                                            id='o1_filtre_resp_com',
                                            options=options_resp_commercial,
                                            value=value_resp_commercial,
                                            multi=True,
                                        ),
                                        style={'fontSize': '20px', 'font-weight': 'bold', 'text-align': 'center'}),
                                ], width=10),
                                dbc.Col([
                                    dbc.Spinner(html.Div(id="o1_spinner_resp_com")),
                                ], width=2)
                            ], className="mb-2")
                        ]
                    ), className="mt-4 shadow mx-auto", style = {"height":'10vh'}
                ),
            ]),
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3('Nombre de lignes validées - check infos', style={'color': '#191970'}),
                                html.Div(html.H2(id='o1_nb_lignes_validees'),
                                        style={'fontSize': '20px', 'font-weight': 'bold', 'text-align': 'center'}),
                            ]
                        ), className="shadow mx-auto"
                    ),
                    dbc.Card(
                        html.Div(className="fa fa-check-square",
                                style={'color': 'white', 'text-align': 'center', 'font-size': 30, 'margin': 'auto'}),
                        className="bg-success shadow mx-auto",
                        style={"maxWidth": 75},
                    ),

                ], className="mt-4",  style = {"height":'10vh'}),
            ]),
            # dbc.Col([
            #     dbc.CardGroup([
            #         dbc.Card(
            #             dbc.CardBody(
            #                 [
            #                     html.H4('Nombre de lignes non validées', style={'color': '#191970'}),
            #                     html.Div(html.H2(id='o1_nb_lignes_non_validees'), style={'fontSize': '20px','font-weight': 'bold','text-align':'center'}),
            #                 ]
            #             )
            #         ),
            #         dbc.Card(
            #             html.Div(className="fa fa-floppy-o", style={'color':'white','text-align': 'center','font-size': 30,'margin': 'auto'}),

            #             className="bg-warning",
            #             style={"maxWidth": 75},
            #         ),

            #     ],className="mt-4 shadow"),
            # ],xs=4,sm=4,md=4,lg=4,xl=4,align="start"),
        ], style = {"height":'12vh','marginTop':"1vh"}),
    ], fluid=True),

    # Le reste de votre mise en page...

    # Création de la DataTable + ajout nouvelles colonnes
    dash_table.DataTable(
        columns=data_table_columns,
        data=df.to_dict('records'),
        id='o1_data_table',
        style_header={
            'backgroundColor': '#555',
            'color': 'white'
        },
        style_table={'height': '60vh',
                    'overflowX': 'auto',
                    'overflowY': 'auto',
                    'margin-left': '20px',
                    'margin-top': '4vh',
                    'margin-right': '20px',
                    'width':'98.5%'},
        style_cell={'font_family': 'calibri',
                    'height': 'auto',
                    'textAlign': 'center'},
        style_data={'font-family': 'Bahnschrift Light',
                    'height':'auto',
                    'whiteSpace': 'normal'},
        style_data_conditional=[
            {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
            },
            {
            "if": {"state": "selected"},
            "backgroundColor": "rgba(0, 116, 217, .03)",
            "border": "1px solid black",
            },  # Alerte renouvellement(feux tricolores)
            {'if': {
                'filter_query': '{alerte_renouvellement}<=120',
                'column_id': 'alerte_renouvellement'
            },
                'backgroundColor': '#fd7e14'
            },
            {'if': {
                'filter_query': '{alerte_renouvellement}<=45',
                'column_id': 'alerte_renouvellement'
            },
                'backgroundColor': '#ff4136'
            },  # Alerte validation devis (feux tricolores)
            {'if': {
                'filter_query': '{alerte_renouvellement}>120 || {envoi_devis} eq True' ,
                'column_id': 'alerte_renouvellement'
            },
                'backgroundColor': '#28b62c'
            },
            {'if': {
                'filter_query': '{alerte_validation_devis}<=56',
                'column_id': 'alerte_validation_devis'
            },
                'backgroundColor': '#fd7e14'
            },
            {'if': {
                'filter_query': '{alerte_validation_devis}<=21',
                'column_id': 'alerte_validation_devis'
            },
                'backgroundColor': '#ff4136'
            },
            {'if': {
                'filter_query': '{alerte_validation_devis}>56 || {accord_principe} eq True',
                'column_id': 'alerte_validation_devis'
            },
                'backgroundColor': '#28b62c'
            },

        ],
        sort_action='native',
        sort_mode='single',
        filter_action='native',
        row_selectable='multi'
    ),

    # Boutons: "Modifier une saisie", "Générer Devis"
    dbc.Row([
        dbc.Col([
            dbc.Button('Modifier une saisie', id="o1_btn_modif_ech", className="me-1", color='secondary',disabled=True,style={'fontSize':'1.5vh','height':'4vh'}),
        ], width={"size": 3,"offset":2}),
        dbc.Col([
            dbc.Button('Générer Devis', id="o1_btn_gener_devis", className="me-1",  color='secondary',disabled=True,style={'fontSize':'1.5vh','height':'4vh'}),
        ], width={"size": 3,"offset":2}),
    ], className="pb-3 d-flex justify-content-center", style = {"marginTop":'5vh'}),

    modal_pop_up, stockage_ligne, stockage_mis_a_jour,
    modal_pop_up_evol_prix, stockage_popup_evprix
], style = {"overflox-x":'hidden'})
