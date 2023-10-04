import dash_bootstrap_components as dbc
from dash import dash_table
from dash import dcc, html
from app import app
import pandas as pd

import dash_mantine_components as dmc
import dash_daq as daq
from db import connect_to_db, disconnect_from_db, sql_to_df
from utils import apply_calcul_sale_price

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
df[['prix_achat_n1', 'prix_vente_n1', 'marge_n1']] = df.apply(apply_calcul_sale_price, axis=1)

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
                              'parc_techno': 'Parc/Techno',
                              # '': 'Numéro de facture',
                              # '': 'Date de facture',
                              'resp_commercial': 'Responsable commercial',
                              'proposition_sap_recue': 'Proposition SAP reçue',
                              'date_relance_client': 'Date de relance client',
                              'proposition_seenovate_creee': 'Proposition Seenovate créée',
                              'date_envoi_proposition': "Date d'envoi de la proposition",
                              'date_signature_proposition': 'Date de signature par le client',
                              'num_commande': 'Attente N° Cde client avant facturation',
                              'date_creation_facture': 'Date de création de la facture',
                              'commande_faite_sap': 'Commande faite SAP',
                              'facture_sap_recue': 'Facture SAP reçue',
                              'remarques': 'Remarques',
                              'devis': 'Devis',
                              'check_infos': 'Check infos',
                              'validation_erronee': 'Validation erronée',
                              'envoi_devis': 'Envoi devis',
                              'accord_principe': 'Accord de principe',
                              'signature_client': 'Signature client',
                              'achat_editeur': 'Achat éditeur',
                              'traitement_comptable': 'Traitement comptable',
                              'paiement_sap': 'Paiement SAP',
                              'renouvele': 'Renouvelé',
                              'demande_resiliation': 'Demande de résiliation',
                              'communication_editeur': 'Communication éditeur',
                              'resilie': 'Résilié',
                              'converti_extension': 'Converti ou Extension',
                              # '': 'Condition de facturation',
                              # '': 'Condition de paiement',
                              'parc_licence': 'Parc de licences'
                              }

data_table_columns = []
for name_db, name_app in db_app_name_correspondance.items():
    data_table_columns.append({'name': name_app, 'id': name_db, 'type': 'text'})

#############################################################################################################
#                                          Appel API                                                        #
#############################################################################################################


#############################################################################################################
#                                                                                                           #
#############################################################################################################


# liste des noms de colonne: Informations contrats clients=
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
                                    dbc.Label("Client", width=6),
                                    dbc.Label(id='input-client')
                                ], width={"size": 6}),
                                dbc.Col([
                                    dbc.Label("ERP Number", width=6),
                                    dbc.Label(id='input-erp-number')
                                ], width={"size": 6}),
                                dbc.Col([
                                    dbc.Label("Date anniversaire", width=6),
                                    dbc.Label(id='input-date-anniversaire')
                                    # Utilisation de dbc.Label pour afficher la date
                                ], width={"size": 6}),
                                dbc.Col([
                                    dbc.Label("Code projet Boond", width=6),
                                    dbc.Label(id='input-code-projet-boond')  # En attente de Boond
                                ], width={"size": 6}),
                                dbc.Col([
                                    dbc.Label("Resp. Commercial", width=6),
                                    dbc.Label(id='input-resp-commercial')
                                ], width={"size": 6}),
                                dbc.Col([
                                    dbc.Label("Editeur", width=6),
                                    dbc.Label(id='input-editeur')
                                    # possibilité de faire dropdown cf. excel specs App PCoE
                                ], width={"size": 6}),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Type de contrat")],
                                        width={"size": 3, "offset": 0}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='input-type-contrat',
                                            options=[
                                                {'label': 'SAP BOBJ', 'value': 'SAP BOBJ'},
                                                {'label': 'SAP PAPER', 'value': 'SAP PAPER'},
                                                {'label': '', 'value': ''},
                                            ],
                                            placeholder='Sélectionnez le Type de contrat',
                                            disabled=True,  # Rendre le dropdown en lecture seule
                                            style={'border': 'none', 'width': '120px'}
                                            # Supprimer l'encadrure de la donnée
                                        ),
                                    ], width={"size": 3, "offset": 0}),
                                    dbc.Col([
                                        dbc.Label("Type de Support SAP")],
                                        width={"size": 3, "offset": -4}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='input-type-support-sap',
                                            options=[
                                                {'label': 'Enterprise', 'value': 'Enterprise'},
                                                {'label': 'Standard', 'value': 'Standard'},
                                                {'label': '', 'value': ''},
                                            ],
                                            placeholder='Sélectionnez le Type de support SAP',
                                            disabled=True,  # Rendre le dropdown en lecture seule
                                            style={'border': 'none', 'width': '120px'}
                                            # Supprimer l'encadrure de la donnée
                                        ),
                                    ], width={"size": 3, "offset": -5}),
                                ], className="mb-2"),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Condition de facturation")],
                                        width={"size": 3, "offset": -1}),
                                    dbc.Col([
                                        dcc.Input(
                                            id='input-cond-fact',
                                            type='text', value='Valeur non modifiable',
                                            style={'border': 'none', 'pointer-events': 'none'},
                                            placeholder='Conditions Facturation',
                                        ),
                                    ], width={"size": 3, "offset": -3}),
                                    dbc.Col([
                                        dbc.Label("Condition de Paiement")],
                                        width={"size": 3, "offset": -3}),
                                    dbc.Col([
                                        dcc.Input(
                                            id='input-cond-paiement', value='Valeur non modifiable',
                                            style={'border': 'none', 'pointer-events': 'none'},
                                            type='text',
                                            placeholder='Conditions de paiement',
                                        ),
                                    ], width={"size": 3, "offset": -3}),
                                ], className="mb-2"),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label('Adresse')],
                                        width={"size": 3, "offset": -3}),
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
                                    ], {"size": 2, "offset": -1}),
                                ], className="mb-2"),
                            ]),
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
                                            dbc.Col([daq.ToggleSwitch(
                                                id='input-check-infos',
                                                color="green",  # Couleur du bouton ON
                                                # label=['Non', 'Oui'],  # Texte pour les positions OFF et ON
                                                size=40,  # Taille du bouton
                                                value=False,  # Par défaut, OFF
                                            ),
                                                dbc.Col([
                                                    html.Div(id='check-infos-date',
                                                             style={'padding-top': '10px', 'text-align': 'left',
                                                                    'font-weight': 'bold'}), ], width={"size": 6}
                                                )]),
                                            dbc.Col([html.Label("Validation erronées")], width={"size": 6}),
                                            dbc.Col([daq.ToggleSwitch(
                                                id='input-validation-erronnes',
                                                color="red",  # Couleur du bouton ON
                                                size=40,  # Taille du bouton
                                                value=False  # Par défaut, OFF
                                            )], width={"size": 6}
                                            ),
                                            dbc.Col([html.Label("Envoi devis")], width={"size": 6}),
                                            dbc.Col([daq.ToggleSwitch(
                                                id='input-envoi-devis',
                                                color="green",  # Couleur du bouton ON
                                                size=40,  # Taille du bouton
                                                value=False  # Par défaut, OFF
                                            )], width={"size": 6}
                                            ),
                                            dbc.Col([html.Label("Accord de principe")], width={"size": 6}),
                                            dbc.Col([daq.ToggleSwitch(
                                                id='input-accord-de-principe',
                                                color="green",  # Couleur du bouton ON
                                                size=40,  # Taille du bouton
                                                value=False  # Par défaut, OFF
                                            )], width={"size": 6}
                                            ),
                                            dbc.Col([html.Label("Signature client")], width={"size": 6}),
                                            dbc.Col([daq.ToggleSwitch(
                                                id='input-signature-client',
                                                color="green",
                                                size=40,
                                                value=False
                                            )], width={"size": 6}
                                            ),
                                            dbc.Col([html.Label("Achat éditeur")], width={"size": 6}),
                                            dbc.Col([daq.ToggleSwitch(
                                                id='input-achat-editeur',
                                                color="green",
                                                size=40,
                                                value=False
                                            )], width={"size": 6}
                                            ),
                                            dbc.Col([html.Label("Traitement comptable")], width={"size": 6}),
                                            dbc.Col([daq.ToggleSwitch(
                                                id='input-traitement-comptable',
                                                color="green",
                                                size=40,
                                                value=False
                                            )], width={"size": 6}
                                            ),
                                            dbc.Col([html.Label("Paiement SAP")], width={"size": 6}),
                                            dbc.Col([daq.ToggleSwitch(
                                                id='input-paiement-sap',
                                                color="green",
                                                size=40,
                                                value=False
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
                                                              placeholder='Entrez prix achat N+1'),
                                                    html.Span('€', style={'margin-left': '5px'})
                                                ], width={"size": 6})]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Label("Nouveau prix de vente")], width={"size": 6}),
                                                dbc.Col([
                                                    dcc.Input(id='input-nv-prix-vente', type='number',
                                                              placeholder='Entrez prix vente N+1'),
                                                    html.Span('€', style={'margin-left': '5px'})
                                                ], width={"size": 6})]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Label("Marge N+1 (%)")], width={"size": 6}),
                                                dbc.Col([
                                                    dcc.Input(id='input-Marge-N+1', type='number',
                                                              placeholder='Entrez Marge N+1'),
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
                                                        # dbc.Col([
                                                        #     dbc.Label("Parc de licences")],
                                                        #     # width={"size": 2, "offset": 1}
                                                        #     ),
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
                dbc.Col([dcc.Link(dbc.Button(html.Img(src=app.get_asset_url("accueil.png"), style={"height": "30px"}),
                                             id="bouton_accueil",
                                             style={'border': '2px solid white', 'margin-left': '-1vw'}, color='white'),
                                  href='/'),
                         html.Img(src=app.get_asset_url("logo_seenovate.png"), height="30px",
                                  style={'margin-left': '1vw'})], xs=2, sm=2, md=2, lg=2, xl=2),
                dbc.Col([html.Div(dbc.NavbarBrand(list_app["name"].loc[list_app["ind"] == n_app].iloc[0], id="titre",
                                                  className="text-white"), style={"textAlign": "center"})
                         ], xs=9, sm=9, md=9, lg=9, xl=9, align="center"),
                dbc.Col([html.Div(html.Img(src=app.get_asset_url("user.png"), height="30px"))])
            ], color="dark")
        ], xs=12, sm=12, md=12, lg=12, xl=12)
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
                                html.H4('Responsable commercial', style={'color': '#191970'}),
                                dbc.Row([
                                    dbc.Col([
                                        html.Div(
                                            dcc.Dropdown(
                                                id='o1_filtre_resp_com',
                                                options=[
                                                    {'label': 'ACA', 'value': 'ACA'},
                                                    {'label': 'ARE', 'value': 'ARE'},
                                                    {'label': 'ATA', 'value': 'ATA'},
                                                    {'label': 'ATA - ACA', 'value': 'ATA - ACA'},
                                                    {'label': 'BDE', 'value': 'BDE'},
                                                    {'label': 'GLE', 'value': 'GLE'},
                                                    {'label': 'JDK', 'value': 'JDK'},
                                                    {'label': 'JPW', 'value': 'JPW'},
                                                    {'label': 'NBE', 'value': 'NBE'},
                                                    {'label': 'TCH', 'value': 'TCH'},
                                                    {'label': 'TCH - ACA', 'value': 'TCH - ACA'},
                                                ],
                                                multi=True,
                                            ),
                                            style={'fontSize': '20px', 'font-weight': 'bold', 'text-align': 'center'}),
                                    ], width=10),
                                    dbc.Col([
                                        dbc.Spinner(html.Div(id="o1_spinner_resp_com")),
                                    ], width=2)
                                ], className="mb-2")
                            ]
                        )
                    ),
                ], className="mt-4 shadow mx-auto"),
            ], xs=4, sm=4, md=4, lg=4, xl=4, align="start"),
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4('Nombre de lignes validées', style={'color': '#191970'}),
                                html.Div(html.H2(id='o1_nb_lignes_validees'),
                                         style={'fontSize': '20px', 'font-weight': 'bold', 'text-align': 'center'}),
                            ]
                        )
                    ),
                    dbc.Card(
                        html.Div(className="fa fa-check-square",
                                 style={'color': 'white', 'text-align': 'center', 'font-size': 30, 'margin': 'auto'}),
                        className="bg-success",
                        style={"maxWidth": 75},
                    ),

                ], className="mt-4 shadow mx-auto"),
            ], xs=4, sm=4, md=4, lg=4, xl=4, align="start"),
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
        ]),
    ], fluid=True),

    # Le reste de votre mise en page...

    # Création de la DataTable + ajout nouvelles colonnes
    dash_table.DataTable(
        columns=data_table_columns,
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
        },  # Alerte renouvellement(feux tricolores)
            {'if': {
                'filter_query': '{Alerte renouvellement}>120',
                'column_id': 'Alerte renouvellement'
            },
                'backgroundColor': 'green'
            },
            {'if': {
                'filter_query': '{Alerte renouvellement}<120',
                'column_id': 'Alerte renouvellement'
            },
                'backgroundColor': 'orange'
            },
            {'if': {
                'filter_query': '{Alerte renouvellement}<45',
                'column_id': 'Alerte renouvellement'
            },
                'backgroundColor': 'red'
            },  # Alerte validation devis (feux tricolores)
            {'if': {
                'filter_query': '{Alerte validation devis}>240',
                'column_id': 'Alerte validation devis'
            },
                'backgroundColor': 'green'
            },
            {'if': {
                'filter_query': '{Alerte validation devis}<240',
                'column_id': 'Alerte validation devis'
            },
                'backgroundColor': 'orange'
            },
            {'if': {
                'filter_query': '{Alerte validation devis}<90',
                'column_id': 'Alerte validation devis'
            },
                'backgroundColor': 'red'
            },

        ],
        sort_action='native',
        sort_mode='single',
        filter_action='native',
        row_selectable='single'
    ),

    # Boutons: "Modifier une saisie", "Générer Devis"
    dbc.Row([
        dbc.Col([
            dbc.Button('Modifier une saisie', id="o1_btn_modif_ech", className="me-1", n_clicks=0, color='warning'),
        ], width={"size": 3}),
        dbc.Col([
            dbc.Button('Générer Devis', id="o1_btn_gener_devis", className="me-1", n_clicks=0, color='success'),
        ], width={"size": 3}),
    ], className="pb-3 d-flex justify-content-center"),

    modal_pop_up, stockage_ligne, stockage_mis_a_jour,
    modal_pop_up_evol_prix, stockage_popup_evprix
])
