from app import app
from dash.dependencies import Input, Output, State
import pandas as pd
from dash.exceptions import PreventUpdate
import dash
from dash import ctx

df = pd.read_excel(r"C:\Users\SofianOUASS\Desktop\PCoE\Suivi CA licences et maintenance 2023.xlsx", sheet_name='Maintenance SAP BusinessObjects')



# Callback pour stocker les données de la ligne sélectionnée dans le dcc.Store
@app.callback(
    Output('o1_store_row', 'data'),
    Input('o1_data_table', 'selected_rows'),
    Input('o1_data_table','data'),
    prevent_initial_call=True,
)
def store_selected_row(selected_rows,dict_data):
    # print(selected_rows)
    # print(dict_data)
    df=pd.DataFrame.from_dict(dict_data)
    if selected_rows:
        selected_row_data = df.iloc[selected_rows[0]].to_dict()
        return selected_row_data
    else:
        return {}
    
    
#callback pour préremplir le type support sap du pop up
@app.callback(
    Output('input-type-support-sap', 'value'),
    Input('o1_store_row', 'data'),
    prevent_initial_call=True,
)
def update_type_support_sap(selected_row_data):
    Type_de_support_sap = selected_row_data.get('Type de support SAP', '')
    return Type_de_support_sap


# Callback pour remplir les champs de la card avec les données de la ligne sélectionnée
@app.callback(
    Output('input-client', 'children'),
    Output('input-erp-number', 'children'),
    Output('input-date-anniversaire', 'date'),
    Output('input-code-projet', 'children'),
    Output('input-resp-commercial', 'children'),
    Output('input-editeur', 'children'),
    
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
    Output('input-facture-creee', 'date'), #'value'
    Output('input-commande-faite-sap', 'value'),
    Output('input-facture-sap-recue', 'value'),
    Output('input-remarques', 'value'),
    Output('input-Parc-Techno', 'value'),
    Output("input-Numero-de-facture", "value"),
    Output("input-mois-imputation", "value"),
    # Output('input-coeff-evolution-prix-achat', 'value'),
    # Output('input-coeff-marge', 'value'),

    Input('o1_store_row', 'data'),
    prevent_initial_call=True,
)
def update_card_fields(selected_row_data):
    client = selected_row_data.get('Client', '')
    erp_number = selected_row_data.get('ERP_Number_Ref_SAP', '') #'ERP Number \nRéf SAP'
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
    attente_Cde_client = selected_row_data.get('Attente  N° Cde client avant facturation', '')
    facture_creee = selected_row_data.get('Facture  créée', '')
    commande_faite_sap = selected_row_data.get('Commande faite SAP', '')
    facture_sap_recue = selected_row_data.get('Facture SAP reçue', '')
    remarques = selected_row_data.get('Remarques', '')
    Parc_Techno = selected_row_data.get('Parc/Techno', '')
    Numero_de_facture = selected_row_data.get('Numéro de facture', '')
    mois_imputation = selected_row_data.get("Mois d'imputation", "")
    # coeff_evolution_prix_achat = selected_row_data.get('Coeff évolution prix achat', 0.00)
    # coeff_marge = selected_row_data.get('Coeff marge', 0.00)
    
         
    return (client, erp_number, date_anniversaire, code_projet_boond,
             resp_commercial, editeur,CA_maintenance_facture,
               Achat_SAP_Maintenance_GBS_NEED4VIZ,Marge_maintenance,marge_pourcentage,
                 montant_vente_annuel, montant_annuel_achat,date_facture,proposition_sap_recue,
                 relance_client,proposition_seenovate_creee,proposition_seenovate_envoyee,
                proposition_signee_par_le_client,attente_Cde_client,facture_creee,commande_faite_sap,
                facture_sap_recue,remarques,Parc_Techno,Numero_de_facture,mois_imputation, #Type_de_support_sap
    )


# ...............................
#callback pour ouvrir le pop-up et valider les données saisies ou modifiées
@app.callback(
    Output("o1_modal", "is_open"),  # Ouvrir le modal
    Input("o1_btn_modif_ech", "n_clicks"),
    Input("o1_btn_submit_validate", "n_clicks"),
    prevent_initial_call=True,
)
def update_modal_open_state(n_btn_modif_ech, n_btn_submit_validate):
    if ctx.triggered_id == "o1_btn_modif_ech":
        return True  # Ouvrir la fenêtre modale
    elif ctx.triggered_id == "o1_btn_submit_validate":
        return False  # Fermer la fenêtre modale après validation
    return dash.no_update
#callback pour mettre à jour les données du tableau
@app.callback(
    Output("o1_data_table", "data"),  # Mettez à jour les données du tableau
    Input("o1_btn_submit_validate", "n_clicks"),
    State('o1_data_table', 'selected_rows'),
    State("input-client", "value"),
    State("input-erp-number", "value"),
    State("input-date-anniversaire", "date"),
    State("input-code-projet", "value"),
    State("input-resp-commercial", "value"),
    State("input-editeur", "value"),
    State("input-CA-maintenance-facture", "value"),
    State("input-Achat-SAP-Maintenance-GBS-NEED4VIZ", "value"),
    State("input-Marge-maintenance", "value"),
    State("input-Marge-pourcentage", "value"),
    State("input-Montant-vente-annuel-N+1", "value"),
    State("input-Montant-annuel-Achat-N+1", "value"),
    State("input-Date-de-facture", "date"),
    State("input-Proposition-SAP-reçue", "value"),
    State("input-relance-client", "date"),
    State("input-Proposition-Seenovate-creee", "value"),
    State("input-Proposition-Seenovate-envoyee", "date"),
    State("input-Proposition-signee-par-le-client", "date"),
    State("input-attente-Cde-client", "value"),
    State("input-facture-creee", "date"),
    State("input-commande-faite-sap", "value"),
    State("input-facture-sap-recue", "value"),
    State("input-remarques", "value"),
    State("input-Parc-Techno", "value"),
    State("input-Numero-de-facture", "value"),
    State("input-mois-imputation", "value"),
    State("o1_data_table", "data"),
    State('input-type-support-sap', 'value'),
    # State('data-store', 'data'),
    prevent_initial_call=True,
)
def update_table_data(n_btn_submit_validate, selected_row_number, client, erp_number, 
                     date_anniversaire, code_projet_boond, resp_commercial, editeur,
                     CA_maintenance_facture, Achat_SAP_Maintenance_GBS_NEED4VIZ, 
                     Marge_maintenance, marge_pourcentage, montant_vente_annuel, 
                     montant_annuel_achat, date_facture, proposition_sap_recue, 
                     relance_client, proposition_seenovate_creee, proposition_seenovate_envoyee,
                     proposition_signee_par_le_client, attente_Cde_client, facture_creee, 
                     commande_faite_sap, facture_sap_recue, remarques, Parc_Techno, 
                     Numero_de_facture, mois_imputation, data_main_table, Type_de_support_sap):
    if n_btn_submit_validate:
        # Validez les données ici (effectuez des vérifications si nécessaire)

        # Construisez le dictionnaire des données mises à jour
        updated_data = {
            "Client": client,
            "ERP_Number_Ref_SAP": erp_number,
            "Date anniversaire": date_anniversaire,
            "Code projet Boond": code_projet_boond,
            "Resp\nCommercial": resp_commercial,
            "Type de contrat": editeur,
            "CA maintenance facturé": CA_maintenance_facture,
            "Achat SAP Maintenance ou GBS ou NEED4VIZ": Achat_SAP_Maintenance_GBS_NEED4VIZ,
            "Marge maintenance ": Marge_maintenance,
            "Marge %": marge_pourcentage,
            "Montant vente annuel N+1": montant_vente_annuel,
            "Montant annuel Achat N+1": montant_annuel_achat,
            "Date de facture": date_facture,
            "Proposition SAP reçue": proposition_sap_recue,
            "Relance client**": relance_client,
            "Proposition Seenovate créée": proposition_seenovate_creee,
            "Proposition Seenovate envoyée": proposition_seenovate_envoyee,
            "Proposition signée par le client": proposition_signee_par_le_client,
            "Attente  N° Cde client avant facturation": attente_Cde_client,
            "Facture  créée": facture_creee,
            "Commande faite SAP": commande_faite_sap,
            "Facture SAP reçue": facture_sap_recue,
            "Remarques": remarques,
            "Parc/Techno": Parc_Techno,
            "Numéro de facture": Numero_de_facture,
            "Mois d'imputation": mois_imputation,
            "Type de support SAP": Type_de_support_sap
            
        }
        # data_main_table[selected_row_number[0]]["Client"] = client
        # data_main_table[selected_row_number[0]]["ERP_Number_Ref_SAP"] = erp_number
        # data_main_table[selected_row_number[0]]["Date anniversaire"] = date_anniversaire
        # data_main_table[selected_row_number[0]]["Code projet Boond"] = code_projet_boond
        # data_main_table[selected_row_number[0]]["Resp\nCommercial"] = resp_commercial
        # data_main_table[selected_row_number[0]]["Type de contrat"] = editeur
        # data_main_table[selected_row_number[0]]["CA maintenance facturé"] = CA_maintenance_facture
        # data_main_table[selected_row_number[0]]["Achat SAP Maintenance ou GBS ou NEED4VIZ"] = Achat_SAP_Maintenance_GBS_NEED4VIZ
        # data_main_table[selected_row_number[0]]["Marge maintenance "] = Marge_maintenance
        # data_main_table[selected_row_number[0]]["Marge %"] = marge_pourcentage
        # data_main_table[selected_row_number[0]]["Montant vente annuel N+1"] = montant_vente_annuel
        # data_main_table[selected_row_number[0]]["Montant annuel Achat N+1"] = montant_annuel_achat
        # data_main_table[selected_row_number[0]]["Date de facture"] = date_facture
        # data_main_table[selected_row_number[0]]["Proposition SAP reçue"] = proposition_sap_recue
        # data_main_table[selected_row_number[0]]["Relance client**"] = relance_client
        # data_main_table[selected_row_number[0]]["Proposition Seenovate créée"] = proposition_seenovate_creee
        # data_main_table[selected_row_number[0]]["Proposition Seenovate envoyée"] = proposition_seenovate_envoyee
        # data_main_table[selected_row_number[0]]["Proposition signée par le client"] = proposition_signee_par_le_client
        # data_main_table[selected_row_number[0]]["Facture  créée"] = facture_creee
        # data_main_table[selected_row_number[0]]["Commande faite SAP"] = commande_faite_sap
        # data_main_table[selected_row_number[0]]["Facture SAP reçue"] = facture_sap_recue
        # data_main_table[selected_row_number[0]]["Remarques"] = remarques
        # data_main_table[selected_row_number[0]]["Parc/Techno"] = Parc_Techno
        # data_main_table[selected_row_number[0]]["Numéro de facture"] = Numero_de_facture
        # data_main_table[selected_row_number[0]]["Mois d'imputation"] = mois_imputation
        # data_main_table[selected_row_number[0]]["Type de support SAP"] = Type_de_support_sap
        

        # Mettez à jour les données de la ligne sélectionnée dans data_main_table
        for key, value in updated_data.items():
            data_main_table[selected_row_number[0]][key] = value
                

        return data_main_table

       







