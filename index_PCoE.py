import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Charger le tableau Excel
df = pd.read_excel(r"C:\Users\SofianOUASS\Desktop\PCoE\Suivi CA licences et maintenance 2023.xlsx", sheet_name='Maintenance SAP BusinessObjects')

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

# Initialiser l'application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Ajout d'un composant dcc.Store pour stocker les données de la ligne sélectionnée
stockage_ligne = dcc.Store(id='o1_store_row')


# Mise en page de l'application
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Navbar([
                dbc.Row([
                    dbc.Col([], xs=2, sm=2, md=2, lg=2, xl=2),  # Colonne vide à gauche
                    dbc.Col([
                        html.Div(
                            "Tableau de bord de l'application PCoE",
                            id="titre",
                            className="text-white mx-auto",  # Ajouter la classe mx-auto pour centrer le texte horizontalement
                            style={"font-size": "15px", "text-align": "center"},
                        ),
                    ], xs=8, sm=8, md=8, lg=8, xl=8, align="center"),
                    dbc.Col([], xs=2, sm=2, md=2, lg=2, xl=2),  # Colonne vide à droite
                ]),
            ], color="#AAAD95"),
        ], xs=12, sm=12, md=12, lg=12, xl=12),
    ], justify='end'),


    # ... Le reste de votre mise en page ...

# # Mise en page de l'application
# app.layout = dbc.Container([
#     html.H1("Tableau de bord de l'application PCoE"),
#     # En-tête avec logo
#     html.Div([
#         html.Img(src='logo.png', style={'width': '200px', 'height': '50px'})
#     ], style={'text-align': 'center'}),
    dash_table.DataTable(
        columns=[
            {
                'name': col,
                'id': col,
                'type': 'text'  # Remplacez 'text' par le type de données correct si nécessaire
            }
            for col in df.columns
        ],
        data=df.to_dict('records'),  # Convertir le DataFrame en dictionnaire de records
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

    # Fenêtre modale pour la modification de saisie
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Modifier la saisie")),
            dbc.ModalBody([
                dbc.Card([
                    dbc.CardHeader("Informations contrats clients"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Client", width=6),
                                dcc.Input(id='input-client', type='text', placeholder='Entrez le Client'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("ERP Number", width=6),
                                dcc.Input(id='input-erp-number', type='text', placeholder='Entrez l\'ERP Number'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Date anniversaire", width=6),
                                dcc.DatePickerSingle(id='input-date-anniversaire',display_format='DD/MM', placeholder='Sélectionnez une date'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Code projet Boond", width=6),
                                dcc.Input(id='input-code-projet', type='text', placeholder='Entrez le Code projet Boond'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Resp. Commercial", width=6),
                                dcc.Input(id='input-resp-commercial', type='text', placeholder='Entrez le Resp. Commercial'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Editeur", width=6),
                                dcc.Input(id='input-editeur', type='text', placeholder='Entrez l\'Editeur'),#possibilité de faire dropdown cf. excel specs App PCoE
                            ], width={"size": 6}),
                        ]),
                    ])
                ]),
                dbc.Card([
                    dbc.CardHeader("Autres informations"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("CA maintenance facturé", width=6),
                                dcc.Input(id='input-CA-maintenance-facture', type='text', placeholder='Entrez le CA maintenance facturé'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Achat SAP Maintenance ou GBS ou NEED4VIZ", width=6),
                                dcc.Input(id='input-Achat-SAP-Maintenance-GBS-NEED4VIZ', type='text', placeholder='Entrez le Achat SAP Maintenance ou GBS ou NEED4VIZ'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Marge maintenance", width=6),
                                dcc.Input(id='input-Marge-maintenance', type='text', placeholder='Entrez la Marge maintenance'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Marge %", width=6),
                                dcc.Input(id='input-Marge-pourcentage', type='text', placeholder='Entrez la Marge %'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Montant vente annuel N+1", width=6),
                                dcc.Input(id='input-Montant-vente-annuel-N+1', type='text', placeholder='Entrez le Montant vente annuel N+1'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Montant annuel Achat N+1", width=6),
                                dcc.Input(id='input-Montant-annuel-Achat-N+1', type='text', placeholder='Entrez le Montant annuel Achat N+1'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Mois d'imputation", width=6),
                                dcc.DatePickerSingle(id='input-mois-imputation', display_format='MM', placeholder='Sélectionnez une date'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Type de support SAP", width=6),
                                dcc.Dropdown(
                                    id='input-type-support-sap',
                                    options=[
                                        {'label': 'Enterprise', 'value': 'Enterprise'},
                                        {'label': 'Standard', 'value': 'Standard'},
                                        {'label': '', 'value': ''},
                                    ],
                                    placeholder='Sélectionnez le Type de support SAP',
                                ),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Parc/Techno", width=6),
                                dcc.Input(id='input-Parc-Techno', type='text', placeholder='Entrez le Parc/Techno'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Numéro de facture", width=6),
                                dcc.Input(id='input-Numero-de-facture', type='text', placeholder='Entrez le Numéro de facture'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Date de facture", width=6),
                                dcc.DatePickerSingle(id='input-Date-de-facture', display_format='DD/MM/YYYY', placeholder='Sélectionnez une date'),
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
                                dcc.Input(id='input-facture-creee', type='text', placeholder='Entrez la Facture créée'),
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

                            # dbc.Col([
                            #     dbc.Label("Champ 2", width=6),
                            #     dcc.Input(id='input-champ-2', type='text', placeholder='Entrez le Champ 2'),
                            # ], width={"size": 6}),
                        ]),
                    ])
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Valider", id="o1_btn_submit_validate", type="submit", outline=True, color="success"),
                dbc.Button("Enregistrer", id="o1_btn_submit_save", type="submit", outline=True, color="warning"),
            ]),
        ],
        id="o1_modal",
        size="lg",
        is_open=False,
    ),
    stockage_ligne
])

# Callback pour afficher la fenêtre modale lors du clic sur le bouton "Modifier une saisie"
@app.callback(
    Output("o1_modal", "is_open"),
    Input("o1_btn_modif_ech", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_modal(n):
    if n:
        return True
    return False

# Callback pour stocker les données de la ligne sélectionnée dans le dcc.Store
@app.callback(
    Output('o1_store_row', 'data'),
    Input('o1_data_table', 'selected_rows'),
    prevent_initial_call=True,
)
def store_selected_row(selected_rows):
    if selected_rows:
        selected_row_data = df.iloc[selected_rows[0]].to_dict()
        return selected_row_data
    else:
        return {}

## Callback pour mettre à jour la valeur du dropdown "Type de support SAP" en fonction de "Editeur"('Type de contrat'??!!)
# @app.callback(
#     Output('input-type-support-sap', 'value'),
#     Input('o1_store_row', 'data'),
#     prevent_initial_call=True,
# )
# def update_support_sap_dropdown(selected_row_data):
#     editeur = selected_row_data.get('Type de contrat', '')
#     if editeur.startswith('SAP'): 
#         return 'Enterprise'
#     else:
#         return ''


# Callback pour remplir les champs de la card avec les données de la ligne sélectionnée
@app.callback(
    Output('input-client', 'value'),
    Output('input-erp-number', 'value'),
    Output('input-date-anniversaire', 'date'),
    Output('input-code-projet', 'value'),
    Output('input-resp-commercial', 'value'),
    Output('input-editeur', 'value'),
    Output('input-relance-client', 'date'),

    Output('input-CA-maintenance-facture', 'value'),
    Output('input-Achat-SAP-Maintenance-GBS-NEED4VIZ', 'value'),
    Output('input-Marge-maintenance', 'value'),
    Output('input-Marge-pourcentage', 'value'),
    Output('input-Montant-vente-annuel-N+1', 'value'),
    Output('input-Montant-annuel-Achat-N+1', 'value'),
    
    # Output('input-coeff-evolution-prix-achat', 'value'),
    # Output('input-coeff-marge', 'value'),

    Input('o1_store_row', 'data'),
    prevent_initial_call=True,
)
def update_card_fields(selected_row_data):
    client = selected_row_data.get('Client', '')
    erp_number = selected_row_data.get('ERP Number \nRéf SAP', '')
    date_anniversaire = selected_row_data.get('Date anniversaire', '')
    code_projet_boond = selected_row_data.get('Code projet Boond', '') # ACA doit le mettre sur excel pour faire le lien!!!
    resp_commercial = selected_row_data.get('Resp\nCommercial', '')
    editeur = selected_row_data.get('Type de contrat', '')  # Editeur à Cf.avec ACA pour faire le lien, je ne vois pas où il est dans xls!
    relance_client_date = selected_row_data.get('Relance client**', None)

    CA_maintenance_facture = selected_row_data.get('CA maintenance facturé', '')
    Achat_SAP_Maintenance_GBS_NEED4VIZ = selected_row_data.get('Achat SAP Maintenance ou GBS ou NEED4VIZ', '')
    Marge_maintenance = selected_row_data.get('Marge maintenance ', '')
    marge_pourcentage = selected_row_data.get('Marge %', '')
    montant_vente_annuel = selected_row_data.get('Montant vente annuel N+1', '')
    montant_annuel_achat = selected_row_data.get('Montant annuel Achat N+1', '')
    # coeff_evolution_prix_achat = selected_row_data.get('Coeff évolution prix achat', 0.00)
    # coeff_marge = selected_row_data.get('Coeff marge', 0.00)
        
    return client, erp_number, date_anniversaire, code_projet_boond, resp_commercial, editeur, relance_client_date,CA_maintenance_facture, Achat_SAP_Maintenance_GBS_NEED4VIZ,Marge_maintenance,marge_pourcentage, montant_vente_annuel, montant_annuel_achat

if __name__ == '__main__':
    app.run_server(debug=True)
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Charger le tableau Excel
df = pd.read_excel(r"C:\Users\SofianOUASS\Desktop\PCoE\Suivi CA licences et maintenance 2023.xlsx", sheet_name='Maintenance SAP BusinessObjects')

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

# Initialiser l'application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Ajout d'un composant dcc.Store pour stocker les données de la ligne sélectionnée
stockage_ligne = dcc.Store(id='o1_store_row')


# Mise en page de l'application
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Navbar([
                dbc.Row([
                    dbc.Col([], xs=2, sm=2, md=2, lg=2, xl=2),  # Colonne vide à gauche
                    dbc.Col([
                        html.Div(
                            "Tableau de bord de l'application PCoE",
                            id="titre",
                            className="text-white mx-auto",  # Ajouter la classe mx-auto pour centrer le texte horizontalement
                            style={"font-size": "15px", "text-align": "center"},
                        ),
                    ], xs=8, sm=8, md=8, lg=8, xl=8, align="center"),
                    dbc.Col([], xs=2, sm=2, md=2, lg=2, xl=2),  # Colonne vide à droite
                ]),
            ], color="#AAAD95"),
        ], xs=12, sm=12, md=12, lg=12, xl=12),
    ], justify='end'),


    # ... Le reste de votre mise en page ...

# # Mise en page de l'application
# app.layout = dbc.Container([
#     html.H1("Tableau de bord de l'application PCoE"),
#     # En-tête avec logo
#     html.Div([
#         html.Img(src='logo.png', style={'width': '200px', 'height': '50px'})
#     ], style={'text-align': 'center'}),
    dash_table.DataTable(
        columns=[
            {
                'name': col,
                'id': col,
                'type': 'text'  # Remplacez 'text' par le type de données correct si nécessaire
            }
            for col in df.columns
        ],
        data=df.to_dict('records'),  # Convertir le DataFrame en dictionnaire de records
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

    # Fenêtre modale pour la modification de saisie
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Modifier la saisie")),
            dbc.ModalBody([
                dbc.Card([
                    dbc.CardHeader("Informations contrats clients"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Client", width=6),
                                dcc.Input(id='input-client', type='text', placeholder='Entrez le Client'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("ERP Number", width=6),
                                dcc.Input(id='input-erp-number', type='text', placeholder='Entrez l\'ERP Number'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Date anniversaire", width=6),
                                dcc.DatePickerSingle(id='input-date-anniversaire',display_format='DD/MM', placeholder='Sélectionnez une date'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Code projet Boond", width=6),
                                dcc.Input(id='input-code-projet', type='text', placeholder='Entrez le Code projet Boond'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Resp. Commercial", width=6),
                                dcc.Input(id='input-resp-commercial', type='text', placeholder='Entrez le Resp. Commercial'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Editeur", width=6),
                                dcc.Input(id='input-editeur', type='text', placeholder='Entrez l\'Editeur'),#possibilité de faire dropdown cf. excel specs App PCoE
                            ], width={"size": 6}),
                        ]),
                    ])
                ]),
                dbc.Card([
                    dbc.CardHeader("Autres informations"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("CA maintenance facturé", width=6),
                                dcc.Input(id='input-CA-maintenance-facture', type='text', placeholder='Entrez le CA maintenance facturé'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Achat SAP Maintenance ou GBS ou NEED4VIZ", width=6),
                                dcc.Input(id='input-Achat-SAP-Maintenance-GBS-NEED4VIZ', type='text', placeholder='Entrez le Achat SAP Maintenance ou GBS ou NEED4VIZ'),
                            ], width={"size": 6}),
                        ]),dbc.Row([
                            dbc.Col([
                                dbc.Label("Marge maintenance", width=6),
                                dcc.Input(id='input-Marge-maintenance', type='text', placeholder='Entrez la Marge maintenance'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Marge %", width=6),
                                dcc.Input(id='input-Marge-pourcentage', type='text', placeholder='Entrez la Marge %'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Montant vente annuel N+1", width=6),
                                dcc.Input(id='input-Montant-vente-annuel-N+1', type='text', placeholder='Entrez le Montant vente annuel N+1'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Montant annuel Achat N+1", width=6),
                                dcc.Input(id='input-Montant-annuel-Achat-N+1', type='text', placeholder='Entrez le Montant annuel Achat N+1'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Mois d'imputation", width=6),
                                dcc.DatePickerSingle(id='input-mois-imputation', display_format='MM', placeholder='Sélectionnez une date'),
                            ], width={"size": 6}),
                            dbc.Col([
                                dbc.Label("Type de support SAP", width=6),],width={"size": 3}),
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
                                dcc.Input(id='input-Numero-de-facture', type='text', placeholder='Entrez le Numéro de facture'),
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
                                dcc.Input(id='input-facture-creee', type='text', placeholder='Entrez la Facture créée'),
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

                            # dbc.Col([
                            #     dbc.Label("Champ 2", width=6),
                            #     dcc.Input(id='input-champ-2', type='text', placeholder='Entrez le Champ 2'),
                            # ], width={"size": 6}),
                        ]),
                    ])
                ]),
            ]),
            dbc.ModalFooter([
                dbc.Button("Valider", id="o1_btn_submit_validate", type="submit", outline=True, color="success"),
                dbc.Button("Enregistrer", id="o1_btn_submit_save", type="submit", outline=True, color="warning"),
            ]),
        ],
        id="o1_modal",
        size="xl",
        is_open=False,
    ),
    stockage_ligne
])

# Callback pour afficher la fenêtre modale lors du clic sur le bouton "Modifier une saisie"
@app.callback(
    Output("o1_modal", "is_open"),
    Input("o1_btn_modif_ech", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_modal(n):
    if n:
        return True
    return False

# Callback pour stocker les données de la ligne sélectionnée dans le dcc.Store
@app.callback(
    Output('o1_store_row', 'data'),
    Input('o1_data_table', 'selected_rows'),
    prevent_initial_call=True,
)
def store_selected_row(selected_rows):
    if selected_rows:
        selected_row_data = df.iloc[selected_rows[0]].to_dict()
        return selected_row_data
    else:
        return {}

## Callback pour mettre à jour la valeur du dropdown "Type de support SAP" en fonction de "Editeur"('Type de contrat'??!!)
# @app.callback(
#     Output('input-type-support-sap', 'value'),
#     Input('o1_store_row', 'data'),
#     prevent_initial_call=True,
# )
# def update_support_sap_dropdown(selected_row_data):
#     editeur = selected_row_data.get('Type de contrat', '')
#     if editeur.startswith('SAP'): 
#         return 'Enterprise'
#     else:
#         return ''


# Callback pour remplir les champs de la card avec les données de la ligne sélectionnée
@app.callback(
    Output('input-client', 'value'),
    Output('input-erp-number', 'value'),
    Output('input-date-anniversaire', 'date'),
    Output('input-code-projet', 'value'),
    Output('input-resp-commercial', 'value'),
    Output('input-editeur', 'value'),
    

    Output('input-CA-maintenance-facture', 'value'),
    Output('input-Achat-SAP-Maintenance-GBS-NEED4VIZ', 'value'),
    Output('input-Marge-maintenance', 'value'),
    Output('input-Marge-pourcentage', 'value'),
    Output('input-Montant-vente-annuel-N+1', 'value'),
    Output('input-Montant-annuel-Achat-N+1', 'value'),
    Output('input-Date-de-facture', 'date'),
    Output('input-Proposition-SAP-reçue', 'value'),
    Output('input-relance-client', 'date'),
    Output('input-Proposition-Seenovate-creee', 'value'),
    Output('input-Proposition-Seenovate-envoyee', 'date'),
    Output('input-Proposition-signee-par-le-client', 'date'),
    Output('input-attente-Cde-client', 'value'),
    Output('input-facture-creee', 'value'),
    Output('input-commande-faite-sap', 'value'),
    Output('input-facture-sap-recue', 'value'),
    Output('input-remarques', 'value'),
    Output('input-Parc-Techno', 'value'),
    Output("input-Numero-de-facture", "value"),
    # Output('input-coeff-evolution-prix-achat', 'value'),
    # Output('input-coeff-marge', 'value'),

    Input('o1_store_row', 'data'),
    prevent_initial_call=True,
)
def update_card_fields(selected_row_data):
    client = selected_row_data.get('Client', '')
    erp_number = selected_row_data.get('ERP Number \nRéf SAP', '')
    date_anniversaire = selected_row_data.get('Date anniversaire', '')
    code_projet_boond = selected_row_data.get('Code projet Boond', '') # ACA doit le mettre sur excel pour faire le lien!!!
    resp_commercial = selected_row_data.get('Resp\nCommercial', '')
    editeur = selected_row_data.get('Type de contrat', '')  # Editeur à Cf.avec ACA pour faire le lien, je ne vois pas où il est dans xls!
    

    CA_maintenance_facture = selected_row_data.get('CA maintenance facturé', '')
    Achat_SAP_Maintenance_GBS_NEED4VIZ = selected_row_data.get('Achat SAP Maintenance ou GBS ou NEED4VIZ', '')
    Marge_maintenance = selected_row_data.get('Marge maintenance ', '')
    marge_pourcentage = selected_row_data.get('Marge %', '')
    montant_vente_annuel = selected_row_data.get('Montant vente annuel N+1', '')
    montant_annuel_achat = selected_row_data.get('Montant annuel Achat N+1', '')
    date_facture = selected_row_data.get('Date de facture', None)
    proposition_sap_recue = selected_row_data.get('Proposition SAP reçue', ' ')
    relance_client = selected_row_data.get('Relance client**', None)
    proposition_seenovate_creee = selected_row_data.get('Proposition Seenovate créée', '')
    proposition_seenovate_envoyee = selected_row_data.get('Proposition Seenovate envoyée', None)
    proposition_signee_par_le_client = selected_row_data.get('Proposition signée par le client', None)
    attente_Cde_client = selected_row_data.get('Attente N° Cde client avant facturation', '')
    facture_creee = selected_row_data.get('Facture créée', '')
    commande_faite_sap = selected_row_data.get('Commande faite SAP', '')
    facture_sap_recue = selected_row_data.get('Facture SAP reçue', '')
    remarques = selected_row_data.get('Remarques', '')
    Parc_Techno = selected_row_data.get('Parc/Techno', '')
    Numero_de_facture = selected_row_data.get('Numero de facture', '')
    # coeff_evolution_prix_achat = selected_row_data.get('Coeff évolution prix achat', 0.00)
    # coeff_marge = selected_row_data.get('Coeff marge', 0.00)
    #print(selected_row_data)
    
        
    return (client, erp_number, date_anniversaire, code_projet_boond,
             resp_commercial, editeur,CA_maintenance_facture,
               Achat_SAP_Maintenance_GBS_NEED4VIZ,Marge_maintenance,marge_pourcentage,
                 montant_vente_annuel, montant_annuel_achat,date_facture,proposition_sap_recue,
                 relance_client,proposition_seenovate_creee,proposition_seenovate_envoyee,
                proposition_signee_par_le_client,attente_Cde_client,facture_creee,commande_faite_sap,
                facture_sap_recue,remarques,Parc_Techno,Numero_de_facture
    )
if __name__ == '__main__':
    app.run_server(debug=True)
