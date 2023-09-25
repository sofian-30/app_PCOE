from app import app
from dash.dependencies import Input, Output, State
import pandas as pd
from dash.exceptions import PreventUpdate
import dash
from dash import ctx, html, dcc
import datetime
from appPCOE.src.generation_devis import remplir_devis

# df = pd.read_excel(r"/mnt/c/CA_2023.xlsx", sheet_name='Maintenance SAP BusinessObjects')
df = pd.read_excel(r"C:\Users\SofianOUASS\Desktop\PCoE\Suivi CA licences et maintenance 2023.xlsx", sheet_name='Maintenance SAP BusinessObjects')


# Callback de génération de devis.
@app.callback(
    Output('download_devis', 'data'),
    Input('o1_btn_gener_devis', 'n_clicks'),
    State('o1_store_row','data'),
    prevent_initial_call=True
)
def export_devis(n0,data_row):
    
    # A faire : finir de rentrer les autres informations.
    # Faire une vérification avant l'envoi du devis
    remplir_devis('acces_devis',data_row['Client'],'adresse','CP','ville','editeur','type_support',data_row['Date anniversaire'],'code_boond','conditions_facturation',
                'conditions_paiement','condition_parc',data_row['Achat SAP Maintenance ou GBS ou NEED4VIZ'])

    return dcc.send_file('appPCOE/impressions/devis/devis_finalise.docx')


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
    

# Callback pour remplir les champs du modal pop-up avec les données de la ligne sélectionnée dans la table
@app.callback(
    Output('input-client', 'children'),
    Output('input-erp-number', 'children'),
    Output('input-date-anniversaire', 'children'),#"date"
    Output('input-code-projet-boond', 'children'),
    Output('input-resp-commercial', 'children'),
    Output('input-editeur', 'children'),# card "informations générales"

    Output('input-badge-generation-devis', 'children'),
    Output('input-badge-validation-devis', 'children'),
    Output('input-badge-alerte-renouvellement', 'children'),
    Output('input-badge-resilie', 'children'), # card "Alertes" (badge)

    Output('input-check-infos', 'children'),
    Output('input-validation-erronnes', 'children'),
    Output('input-envoi-devis', 'children'),
    Output('input-accord-de-principe', 'children'),
    Output('input-signature-client', 'children'),
    Output('input-achat-editeur', 'children'),
    Output('input-traitement-comptable', 'children'),
    Output('input-paiement-sap', 'children'), #card "Status et conditions financières"-status

    Output('input-nv-prix-achat', 'value'),
    Output('input-nv-prix-vente', 'value'),
    Output('input-Marge-pourcentage', 'value'),
    Output('input-Montant-vente-annuel-N+1', 'value'),
    Output('input-Montant-annuel-Achat-N+1', 'value'),
    Output('input-Marge-N+1', 'value'), # card "Status et conditions financières"-cond. financières

    Output('input-type-contrat', 'value'),
    Output('input-type-support-sap', 'value'),
    Output('input-cond-fact', 'value'),
    Output('input-cond-paiement', 'value'),
    Output('input-adresse-client', 'value'),
    Output('input-parc-licences', 'value'), # card "Informations contractuelles"

    #Input("o1_modal", 'data'), #input du modal pop-up complet
    Input('o1_store_row', 'data'),#input du layout complet
    prevent_initial_call=True,
)
def update_modal_pop_up(selected_row_data):

    client = selected_row_data.get('Client', '') # card "informations générales"
    erp_number = selected_row_data.get('ERP_Number_Ref_SAP', '') #'ERP Number \nRéf SAP'
    date_anniversaire = selected_row_data.get('Date anniversaire', '')
    code_projet_boond = selected_row_data.get('Code projet Boond', '') # via API
    resp_commercial = selected_row_data.get('Resp\nCommercial', '')
    editeur = selected_row_data.get('Editeur', '')  # Editeur à Cf.avec ACA pour faire le lien, je ne vois pas où il est dans xls!

    badge_generation_devis = selected_row_data.get('Génération devis', '') # card "Alertes" (badge)
    badge_validation_devis = selected_row_data.get('Validation devis', '')
    badge_alerte_renouvellement = selected_row_data.get('Renouvellement', '')
    badge_resilie = selected_row_data.get('Résilié', '')

    check_infos = selected_row_data.get('Check Infos', '') #card "Status et conditions financières"-status
    validation_erronees = selected_row_data.get('Validation erronées', '')
    envoi_devis = selected_row_data.get('Envoi devis', '')
    accord_principe = selected_row_data.get('Accord de principe', '')
    signature_client = selected_row_data.get('Signature client', '')
    achat_editeur = selected_row_data.get('Achat éditeur', '')
    traitement_comptable = selected_row_data.get('Traitement comptable', '')
    paiement_sap = selected_row_data.get('Paiement SAP', '')

    nv_prix_achat = selected_row_data.get('Nouveau prix d\'achat', '') # card "Status et conditions financières"-cond. financières
    nv_prix_vente = selected_row_data.get('Nouveau prix de vente', '')
    marge_pourcentage = selected_row_data.get('Marge %', '')
    montant_vente_annuel = selected_row_data.get('Montant vente annuel N+1', '')
    montant_annuel_achat = selected_row_data.get('Montant annuel Achat N+1', '')
    marge_annuel = selected_row_data.get('Marge N+1 (%)', '') 

    type_contrat = selected_row_data.get('Type de contrat', '')     # card "Informations contractuelles"
    type_support_sap = selected_row_data.get('Type de support SAP', '')
    condition_facturation = selected_row_data.get('Condition de facturation', '')
    condition_paiement = selected_row_data.get('Condition de Paiement', '')
    adresse_client = selected_row_data.get('Adresse', '')
    ville = selected_row_data.get('ville', '')
    cp = selected_row_data.get('CP', '')
    parc_licences = selected_row_data.get('Parc de licences', '')

    # Composition de l'adresse avec saut de ligne
    adresse_client = adresse_client +"\n " + cp + "\n " + ville

    # Conditions "Type de contrat" par rapport à l'éditeur
    if type_contrat is None and editeur == 'SAP':
        type_contrat = "SAP BOBJ"

    # Convertion en % et arrondi à 2 chiffres après virgule
    marge_pourcentage = round(marge_pourcentage * 100, 2)

    
         
    return (client, erp_number, date_anniversaire, code_projet_boond,resp_commercial, editeur,
            badge_generation_devis,badge_validation_devis,badge_alerte_renouvellement,badge_resilie,
            check_infos,validation_erronees,envoi_devis,accord_principe,signature_client,achat_editeur,traitement_comptable,paiement_sap,
            nv_prix_achat,nv_prix_vente,marge_pourcentage,montant_vente_annuel,montant_annuel_achat,marge_annuel,
            type_contrat,type_support_sap,condition_facturation,condition_paiement,adresse_client,parc_licences
                
            )

## def update_toggle_switch_color(value):
##    if value == 'Oui':
##        return "green"  # Si la valeur est "Oui", la couleur est verte
##     else:
##         return "default"  # Sinon, utilisez la couleur par défaut

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

##########################################################################################################
#callback pour mettre à jour les données du tableau
@app.callback(
    Output("o1_data_table", "data"),  # Mettez à jour les données du tableau
    Input("o1_btn_submit_validate", "n_clicks"),
    State('o1_data_table', 'selected_rows'),

    State("input-client", "value"),
    State("input-erp-number", "value"),
    State("input-date-anniversaire", "value"), #"date"
    State("input-code-projet-boond", "value"),                                          #"children" ou "value"?!!!
    State("input-resp-commercial", "value"),
    State("input-editeur", "value"), # card "informations générales"                                

    # State('input-badge-generation-devis', 'children'),
    # State('input-badge-validation-devis', 'children'),
    # State('input-badge-alerte-renouvellement', 'children'),
    # State('input-badge-resilie', 'children'), # card "Alertes" (badge)

    State('input-check-infos', 'children'),
    State('input-validation-erronnes', 'children'),
    State('input-envoi-devis', 'children'),
    State('input-accord-de-principe', 'children'),
    State('input-signature-client', 'children'),
    State('input-achat-editeur', 'children'),
    State('input-traitement-comptable', 'children'),
    State('input-paiement-sap', 'children'), #card "Status et conditions financières"-status

    State('input-nv-prix-achat', 'value'),
    State('input-nv-prix-vente', 'value'),
    State('input-Marge-pourcentage', 'value'),
    State('input-Montant-vente-annuel-N+1', 'value'),
    State('input-Montant-annuel-Achat-N+1', 'value'),
    State('input-Marge-N+1', 'value'), # card "Status et conditions financières"-cond. financières

    State('input-type-contrat', 'value'),
    State('input-type-support-sap', 'value'),
    State('input-cond-fact', 'value'),
    State('input-cond-paiement', 'value'),
    State('input-adresse-client', 'value'),
    State('input-parc-licences', 'value'), # card "Informations contractuelles"


    State("o1_data_table", "data"),
    State('data-store', 'data'),
    prevent_initial_call=True,
)#     ## State('status-content', 'data'),


def update_table_data(n_btn_submit_validate, selected_row_number,
                     client, erp_number,date_anniversaire, code_projet_boond, resp_commercial, editeur,
                     badge_generation_devis,badge_validation_devis,badge_alerte_renouvellement,badge_resilie,
                     check_infos,validation_erronnes,envoi_devis,accord_de_principe,signature_client,achat_editeur,traitement_comptable,paiement_sap,
                     nv_prix_achat,nv_prix_vente,marge_pourcentage,montant_vente_annuel,montant_annuel_achat,marge_annuel,
                     type_contrat,type_support_sap,condition_facturation,condition_paiement,adresse_client,parc_licences,

                     data_main_table

                     ): 

    if selected_row_number is not None and selected_row_number:  # Vérifiez si une ligne a été sélectionnée
        # Validez les données ici (effectuez des vérifications si nécessaire)

        # Construisez le dictionnaire des données mises à jour
        updated_data = {
            "Client": client,
            "ERP_Number_Ref_SAP": erp_number,
            "Date anniversaire": date_anniversaire,
            "Code projet Boond": code_projet_boond,
            "Resp\nCommercial": resp_commercial,
            "Type de contrat": editeur,

            "Génération devis": badge_generation_devis,
            "Validation devis": badge_validation_devis,
            "Renouvellement": badge_alerte_renouvellement,
            "Résilié": badge_resilie,

            "Check Infos": check_infos,
            "Validation erronées": validation_erronnes,
            "Envoi devis": envoi_devis,
            "Accord de principe":accord_de_principe,
            "Signature client":signature_client,
            "Achat éditeur":achat_editeur,
            'Traitement comptable': traitement_comptable,
            "Paiement SAP":paiement_sap,

            'Nouveau prix d\'achat': nv_prix_achat,
            'Nouveau prix de vente':nv_prix_vente,
            "Marge %" : marge_pourcentage,
            "Montant vente annuel N+1": montant_vente_annuel,
            "Montant annuel Achat N+1": montant_annuel_achat,
            "Marge N+1 (%)": marge_annuel,

             "Type de contrat": type_contrat,
             "Type de Support SAP": type_support_sap,
             "Condition de facturation": condition_facturation,
             "Condition de Paiement": condition_paiement,
             'adresse client': adresse_client,
             "Parc de licences": parc_licences
                                    
            
        }

        # Mettez à jour les données de la ligne sélectionnée dans data_main_table
        for key, value in updated_data.items():
            data_main_table[selected_row_number[0]][key] = value

    return data_main_table

  ###############################################################################################################  
    

# #transformer le format de la date d'anniversaire      
# from datetime import datetime

# # La date d'anniversaire au format initial
# date_anniversaire_str = '2023-12-31T00:00:00'

# # Convertir la chaîne de caractères en objet datetime
# date_obj = datetime.strptime(date_anniversaire_str, '%Y-%m-%dT%H:%M:%S')

# # Formater la date au format 'DD/MM'
# date_formatee = date_obj.strftime('%d/%m')

# # Afficher la date au format souhaité
# print(date_formatee)

# @app.callback(
#     Output('input-accord-de-principe', 'children'),# Sortie pour afficher le texte
#     Output('input-signature-client', 'children'),
#     Output('input-achat-editeur', 'children'),
#     Output('input-paiement-sap', 'children'),
#     Input('status-content', 'children')  # Utilisez l'ID de l'ensemble de contenu
# )
# def update_toggle_switch_color(value):
#     if value == 'Oui':
#         return "green"  # Si la valeur est "Oui", la couleur est verte
#     else:
#         return "default"  # Sinon, utilisez la couleur par défaut
