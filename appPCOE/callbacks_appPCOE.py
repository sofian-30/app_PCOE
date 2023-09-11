from app import app
from dash.dependencies import Input, Output, State
import pandas as pd

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
    State('o1_data_table','data'),
    prevent_initial_call=True,
)
def store_selected_row(selected_rows,dict_data):
    print(selected_rows)
    print(dict_data)
    df=pd.DataFrame.from_dict(dict_data)
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