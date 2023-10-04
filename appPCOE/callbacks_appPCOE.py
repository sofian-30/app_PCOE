from app import app
from dash.dependencies import Input, Output, State
import pandas as pd
from dash.exceptions import PreventUpdate
import dash
from dash import ctx, html, dcc
import datetime
from appPCOE.src.generation_devis import remplir_devis
from datetime import datetime
import numpy as np  # Importez la bibliothèque NumPy

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
                'conditions_paiement','condition_parc',data_row['Prix d\'achat actuel'])#'Prix d\'achat actuel' ou' Achat SAP Maintenance ou GBS ou NEED4VIZ'

    return dcc.send_file('appPCOE/impressions/devis/devis_finalise.docx')


# Callback pour stocker les données de la ligne sélectionnée dans le dcc.Store
@app.callback(
    Output('o1_store_row', 'data'),
    Input('o1_data_table', 'selected_rows'),
    Input('o1_data_table','data'),
    prevent_initial_call=True,
)
def store_selected_row(selected_rows,dict_data):
    
    df=pd.DataFrame.from_dict(dict_data)
    if selected_rows:
        selected_row_data = df.iloc[selected_rows[0]].to_dict()
        return selected_row_data
    else:
        return {}
    

# Callback pour remplir les champs du modal pop-up "modifier la saisie" avec les données de la ligne sélectionnée dans la table
@app.callback(
    Output('input-client', 'children'),
    Output('input-erp-number', 'children'),
    Output('input-date-anniversaire', 'children'),#"date"
    Output('input-code-projet-boond', 'children'),
    Output('input-resp-commercial', 'children'),
    Output('input-editeur', 'children'),# card "informations générales"

    # Output('input-badge-generation-devis', 'color'),   #'children' or 'style' or 'color'
    # Output('input-badge-validation-devis', 'color'),
    # Output('input-badge-alerte-renouvellement', 'color'),
    # Output('input-badge-resilie', 'color'), # card "Alertes" (badge)

    Output('input-check-infos', 'children'),
    Output('input-validation-erronnes', 'children'),
    Output('input-envoi-devis', 'children'),
    Output('input-accord-de-principe', 'children'),
    Output('input-signature-client', 'children'),
    Output('input-achat-editeur', 'children'),
    Output('input-traitement-comptable', 'children'),
    Output('input-paiement-sap', 'children'), #card "Status et conditions financières"-status

    Output('input-prix-achat-actuel', 'value'),
    Output('input-prix-vente-actuel', 'value'),
    Output('input-Marge-pourcentage', 'value'),
    Output('input-nv-prix-vente', 'value'),
    Output('input-nv-prix-achat', 'value'),
    Output('input-Marge-N+1', 'value'), # card "Status et conditions financières"-cond. financières

    Output('input-type-contrat', 'value'),
    Output('input-type-support-sap', 'value'),
    Output('input-cond-fact', 'value'),
    Output('input-cond-paiement', 'value'),
    Output('input-adresse-client', 'value'),
    Output('input-parc-licences', 'value'), # card "Informations contractuelles"

    # Input('o1_filtre_resp_com', 'value'),# filtre resp. com.
    Input('o1_store_row', 'data'),#input du layout complet
    prevent_initial_call=True,
)

# def update_resp_commercial(selected_values):
#     if selected_values is None or len(selected_values) == 0:
#         # Si aucune valeur n'est sélectionnée, affiche "Tous les responsables"
#         return "Tous les responsables"
#     else:
#         # Filtrer la colonne "Resp. Commercial" en fonction des valeurs sélectionnées
#         # et afficher les valeurs sélectionnées
#         filtered_values = ', '.join(selected_values)
#         return filtered_values

def update_modal_pop_up(selected_row_data):

    client = selected_row_data.get('Client', '') # card "informations générales"
    erp_number = selected_row_data.get('ERP_Number_Ref_SAP', '') #'ERP Number \nRéf SAP'
    date_anniversaire = selected_row_data.get('Date anniversaire', '')
    code_projet_boond = selected_row_data.get('Code projet Boond', '') # via API
    resp_commercial = selected_row_data.get('Resp\nCommercial', '')
    editeur = selected_row_data.get('Editeur', '')  # Editeur à Cf.avec ACA pour faire le lien, je ne vois pas où il est dans xls!

    # badge_generation_devis = selected_row_data.get('Génération devis', '') # card "Alertes" (badge)
    # badge_validation_devis = selected_row_data.get('Validation devis', '')
    # badge_alerte_renouvellement = selected_row_data.get('Renouvellement', '')
    # badge_resilie = selected_row_data.get('Résilié', '')

    check_infos = selected_row_data.get('Check Infos', '') #card "Status et conditions financières"-status
    validation_erronees = selected_row_data.get('Validation erronées', '')
    envoi_devis = selected_row_data.get('Envoi devis', '')
    accord_principe = selected_row_data.get('Accord de principe', '')
    signature_client = selected_row_data.get('Signature client', '')
    achat_editeur = selected_row_data.get('Achat éditeur', '')
    traitement_comptable = selected_row_data.get('Traitement comptable', '')
    paiement_sap = selected_row_data.get('Paiement SAP', '')

    prix_achat_actuel = selected_row_data.get('Prix d\'achat actuel', '') # card "Status et conditions financières"-cond. financières
    prix_vente_actuel = selected_row_data.get('Prix de vente actuel', '')
    marge_pourcentage = selected_row_data.get('Marge %', '')
    nv_prix_vente = selected_row_data.get('Nouveau prix de vente', '')
    nv_prix_achat = selected_row_data.get("Nouveau prix d'achat", '')
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
    # adresse_client = adresse_client +"\n " + str(cp) + "\n " + ville

    if adresse_client is not None:
        adresse_client = str(adresse_client) + "\n "
    else:
        adresse_client = ""

    if cp is not None:
        adresse_client += str(cp) + "\n "

    if ville is not None:
        adresse_client += ville


    # Conditions "Type de contrat" par rapport à l'éditeur
    if type_contrat is None and editeur == 'SAP':
        type_contrat = "SAP BOBJ"


   # Vérifiez d'abord si marge_pourcentage est None avant de faire le calcul
    if marge_pourcentage is not None:
        marge_pourcentage = round(marge_pourcentage * 100, 2)

# Vérifiez si marge_annuel est None avant de faire le calcul
    if marge_annuel is not None:
        marge_annuel = round(marge_annuel * 100, 2)

# Vérifiez si prix_achat_actuel est None avant de faire le calcul
    if prix_achat_actuel is not None:
        prix_achat_actuel = round(prix_achat_actuel, 2)

# Vérifiez si prix_vente_actuel est None avant de faire le calcul
    if prix_vente_actuel is not None:
        prix_vente_actuel = round(prix_vente_actuel, 2)


# #Calcul Nouveau prix d'achat et de vente selon condition: type de contrat
#     # Obtenez la date du jour
#     today = datetime.now()

#     # Calculez la différence en jours entre la date anniversaire et la date du jour
#     df['Différence de jours'] = (df['Date anniversaire'] - today).dt.days

#     # Utilisez une boucle pour parcourir chaque ligne du DataFrame
#     for index, row in df.iterrows():
#         if row['Différence de jours'] < 120:
#             print("La date d'anniversaire est dans moins de 4 mois")
#             df.at[index, 'Nouveau prix d\'achat'] = ""
#         else:
#             type_contrat = row['Type de contrat']
#             if type_contrat == 'SAP PAPER':
#                 coeff_evolution = 0.06
#             elif type_contrat == 'SAP BOBJ':
#                 coeff_evolution = 0.08
#             elif type_contrat == 'N4V':
#                 coeff_evolution = 0.05
#             elif type_contrat in ['360', 'wiiisdom']:
#                 coeff_evolution = 0.02
#             else:
#                 coeff_evolution = 0.0  # Valeur par défaut si le type de contrat n'est pas reconnu
            
#             prix_achat_actuel = row['Prix d\'achat actuel']
#             print('prix_achat_actuel:',prix_achat_actuel)
            
#             #Vérifiez si prix_achat_actuel n'est pas nulle (None) avant de l'arrondir
#             if prix_achat_actuel is not None:
#                 prix_achat_actuel = round(prix_achat_actuel, 2)
            
#             nv_prix_achat = prix_achat_actuel + prix_achat_actuel * coeff_evolution
#             df.at[index, 'Nouveau prix d\'achat'] = nv_prix_achat

#             print("nv_prix_achat:",nv_prix_achat)

#     # Supprimez la colonne 'Différence de jours' si vous n'en avez plus besoin
#     df.drop(columns=['Différence de jours'], inplace=True)

#     # Affichez le DataFrame mis à jour
#     print(df)

        
    


    #date_anniversaire= date_anniversaire.strftime("%d/%m")
    
         
    return (client, erp_number, date_anniversaire, code_projet_boond,resp_commercial, editeur,
            # badge_generation_devis,badge_validation_devis,badge_alerte_renouvellement,badge_resilie,
            check_infos,validation_erronees,envoi_devis,accord_principe,signature_client,achat_editeur,traitement_comptable,paiement_sap,
            prix_achat_actuel,prix_vente_actuel,marge_pourcentage,nv_prix_vente,nv_prix_achat,marge_annuel,
            type_contrat,type_support_sap,condition_facturation,condition_paiement,adresse_client,parc_licences
                
            )

# ...............................

#callback pour ouvrir le pop-up "modifier la saisie" 
#  "valider" et/ou "Annuler" les données saisies ou modifiées
@app.callback(
    Output("o1_modal", "is_open"),  # Open the modal
    Input("o1_btn_modif_ech", "n_clicks"),
    Input("o1_btn_submit_validate", "n_clicks"),
    Input("o1_btn_submit_cancel", "n_clicks"),
    State("o1_modal", "is_open"),
    prevent_initial_call=True,
)
def update_modal_open_state(n_btn_modif_ech, n_btn_submit_validate, n_btn_submit_cancel, is_open):
    ctx = dash.callback_context

    if ctx.triggered_id == "o1_btn_modif_ech":
        return True  # Open the modal
    elif ctx.triggered_id == "o1_btn_submit_validate":
        return False  # Close the modal after validation
    elif ctx.triggered_id == "o1_btn_submit_cancel":
        return False  # Close the modal when "Annuler" is clicked
    return is_open


##########################################################################################################
#callback pour mettre à jour les données du tableau (callback retour)
@app.callback(
    Output("o1_data_table", "data"),  # Mettez à jour les données du tableau
    Input("o1_btn_submit_validate", "n_clicks"),
    State('o1_data_table', 'selected_rows'),
    State("o1_data_table", "data"),

    State("input-client", "value"),
    State("input-erp-number", "value"),
    State("input-date-anniversaire", "value"), 
    State("input-code-projet-boond", "value"),                                          
    State("input-resp-commercial", "value"),
    State("input-editeur", "value"), # card "informations générales"                                

    # State('input-badge-generation-devis', 'value'),   #'children' or 'style' or 'color'
    # State('input-badge-validation-devis', 'value'),
    # State('input-badge-alerte-renouvellement', 'value'),
    # State('input-badge-resilie', 'value'), # card "Alertes" (badge)

    State('input-check-infos', 'value'),
    State('input-validation-erronnes', 'value'),
    State('input-envoi-devis', 'value'),
    State('input-accord-de-principe', 'value'),
    State('input-signature-client', 'value'),
    State('input-achat-editeur', 'value'),
    State('input-traitement-comptable', 'value'),
    State('input-paiement-sap', 'value'), #card "Status et conditions financières"-status

    State('input-prix-achat-actuel', 'value'),
    State('input-prix-vente-actuel', 'value'),
    State('input-Marge-pourcentage', 'value'),
    State('input-nv-prix-vente', 'value'),
    State('input-nv-prix-achat', 'value'),
    State('input-Marge-N+1', 'value'), # card "Status et conditions financières"-cond. financières

    State('input-type-contrat', 'value'),
    State('input-type-support-sap', 'value'),
    State('input-cond-fact', 'value'),
    State('input-cond-paiement', 'value'),
    State('input-adresse-client', 'value'),
    State('input-parc-licences', 'value'), # card "Informations contractuelles"

    
        prevent_initial_call=True,
)

def update_table_data(n_btn_submit_validate, selected_row_number, data_main_table, 
                      
                     client, erp_number,date_anniversaire, code_projet_boond, resp_commercial, editeur,
                    #  badge_generation_devis,badge_validation_devis,badge_alerte_renouvellement,badge_resilie,
                     check_infos,validation_erronnes,envoi_devis,accord_de_principe,signature_client,achat_editeur,traitement_comptable,paiement_sap,
                     prix_achat_actuel,prix_vente_actuel,marge_pourcentage,nv_prix_vente,nv_prix_achat,marge_annuel,
                     type_contrat,type_support_sap,condition_facturation,condition_paiement,adresse_client,parc_licences

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
            "Editeur": editeur, #"Type de contrat"

            # "Génération devis": badge_generation_devis,
            # "Validation devis": badge_validation_devis,
            # "Renouvellement": badge_alerte_renouvellement,
            # "Résilié": badge_resilie,

            "Check Infos": check_infos,
            "Validation erronées": validation_erronnes,
            "Envoi devis": envoi_devis,
            "Accord de principe":accord_de_principe,
            "Signature client":signature_client,
            "Achat éditeur":achat_editeur,
            'Traitement comptable': traitement_comptable,
            "Paiement SAP":paiement_sap,

            'Prix d\'achat actuel': prix_achat_actuel,
            'Prix de vente actuel':prix_vente_actuel,
            "Marge %" : marge_pourcentage,
            "Nouveau prix de vente": nv_prix_vente,
            "Nouveau prix d'achat": nv_prix_achat,
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

# #Callback pour activer la date quand switch "on" sur accordion "status et conditions financières"
# @app.callback(
#     Output('check-infos-date', 'children'),
#     Input('input-check-infos', 'value')
# )
# def update_check_infos_date(value):
#     if value:
#         return f"{datetime.date.today().strftime('%d/%m/%Y')}"
#     else:
#         return ""
    

#..................................................................................................
#callback pour gérer l'ouverture du pop-up "résilier" et la gestion des boutons "Oui" et "Non"
@app.callback(
    Output("confirm-resiliation", "displayed"),
    Output("confirm-resiliation", "message"),
    Output("o1_btn_submit_resiliation", "disabled"),
    Output("input-badge-resilie", "color"),  # Ajout de la sortie pour le badge
    Input("o1_btn_submit_resiliation", "n_clicks"),
    Input("confirm-resiliation", "submit_n_clicks"),
    Input("confirm-resiliation", "cancel_n_clicks"),
    prevent_initial_call=True,
)
def confirm_resiliation(n_resiliation_clicks, submit_n_clicks, cancel_n_clicks):
    if n_resiliation_clicks > 0:
        if submit_n_clicks is None and cancel_n_clicks is None:
            return True, "Souhaitez-vous réellement saisir une résiliation client?", True, 'blue'  # Initialiser la couleur du badge à bleu
        elif submit_n_clicks is not None and submit_n_clicks > 0:
            # Traitement à effectuer lorsque "Oui" est cliqué
            # Vous pouvez insérer ici la logique de résiliation client
            # Mettre à jour la couleur du badge en rouge
            return False, "", False, 'red'
        else:
            # Traitement à effectuer lorsque "Non" est cliqué
            return False, "", False, 'blue'  # Réinitialiser la couleur du badge à bleu

    return False, "", False, 'blue'  # Réinitialiser la couleur du badge à bleu



#...........................................................................................
#callback carte "Alertes"
@app.callback(
    Output('input-badge-validation-devis', 'color'), #'color' ou 'style'
    Output('input-badge-alerte-renouvellement', 'color'),
    Input('o1_btn_modif_ech', 'n_clicks'),  # Utilisez le bouton comme déclencheur
    Input('o1_store_row', 'data'),
    prevent_initial_call=True,
)
def update_badge_colors(n_clicks,selected_row_data):
    if selected_row_data is None:
        # Gérez le cas où selected_row_data est None
        return 'gray', 'gray'#{'color': 'gray'}, {'color': 'gray'}
   # print("Selected Row Data:", selected_row_data)
    
    # Initialisez les styles par défaut
    validation_devis_style = 'blue' #{'color': 'blue'}  # Style par défaut pour "Validation devis"
    alerte_renouvellement_style = 'blue'#{'color': 'blue'}  # Style par défaut pour "Renouvellement"

    # Obtenez les valeurs de "Validation devis" et "Renouvellement" à partir des données de la ligne sélectionnée
    validation_devis = selected_row_data.get('Alerte validation devis', '')
    #print('Validation Devis:', validation_devis)

    alerte_renouvellement = selected_row_data.get('Alerte renouvellement', '')
    #print('Alerte Renouvellement:', alerte_renouvellement)

    # Convertissez en float pour permettre la comparaison avec les entiers
    validation_devis = float(validation_devis) if validation_devis else 0.0
    alerte_renouvellement = float(alerte_renouvellement) if alerte_renouvellement else 0.0

    # Mettez à jour les styles en fonction des conditions
    if validation_devis > 240:
        validation_devis_style = 'green'
    elif 90 < validation_devis <= 240:
        validation_devis_style = 'orange'
    else:
        validation_devis_style = 'red'

    if alerte_renouvellement > 120:
        alerte_renouvellement_style = 'green'
    elif 45 <= alerte_renouvellement <= 120:
        alerte_renouvellement_style = 'orange'
    else:
        alerte_renouvellement_style = 'red'

    # print("Validation Devis Style:", validation_devis_style)
    # print("Alerte Renouvellement Style:", alerte_renouvellement_style)

    return validation_devis_style, alerte_renouvellement_style


@app.callback(
    Output('input-badge-generation-devis', 'color'),  # Change the badge's color
    Input('o1_btn_gener_devis', 'n_clicks'),
    prevent_initial_call=True
)
def change_badge_color(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        # If the button is clicked, change the badge color to 'success' (green)
        return 'green'
    else:
        # If the button is not clicked, keep the badge color as 'blue'
        return 'blue'



#..................................................................................

# # Callback pour ouvrir/fermer le modal_pop_up_evol_prix lorsque le bouton est cliqué
# @app.callback(
#     Output("excel_modal", "is_open"),
#     [Input("o1_btn_evol_prix", "n_clicks"),
#      Input("close_excel_modal", "n_clicks")],
#     [State("excel_modal", "is_open")]
# )
# def toggle_excel_modal(btn_click, close_click, is_open):
#     if btn_click or close_click:
#         return not is_open
#     return is_open

# # Callback pour charger et afficher le tableau Excel dans le modal_pop_up_evol_prix
# @app.callback(
#     [Output("excel_table", "data"), Output("excel_table", "columns")],
#     [Input("o1_btn_evol_prix", "n_clicks")]
# )
# def load_excel_table(btn_click):
#     if btn_click:
#         # Chargez votre fichier Excel et convertissez-le en un DataFrame Pandas
#         excel_file_path = r'appPCOE\src\tableau_calcul_evolution_prix.xlsx'
        
#         try:
#             df = pd.read_excel(excel_file_path)
#             columns = [{"name": str(col), "id": str(col)} for col in df.columns]
#             data = df.to_dict('records')

#             return data, columns
#         except Exception as e:
#             return [], []  # Retourne une liste vide pour les données et les colonnes en cas d'erreur


#C:\Users\SofianOUASS\Documents\Dev\app-pcoe\appPCOE\src\tableau_calcul_evolution_prix.xlsx
######################################################################################################


# ...


