import dash
import pandas as pd
from dash import dcc
from dash.dependencies import Input, Output, State
import numpy as np
import zipfile
import os

from app import app
from appPCOE.src.generation_devis import remplir_devis
from db import connect_to_db, sql_to_df, disconnect_from_db, execute_sql_request
from utils import update_app_table, update_app_table_resiliation, apply_calcul_sale_price

# df = pd.read_excel("./data/Suivi CA licences et maintenance 2023.xlsx", sheet_name='Maintenance SAP BusinessObjects')


@app.callback(
    Output('o1_btn_modif_ech', 'disabled'),
    Output('o1_btn_modif_ech', 'color'),
    Input('o1_data_table', 'selected_rows'),
    prevent_initial_call=True# Déclencheur du callback (clics sur le bouton)
)
def rendre_bouton_incliquable(n_row):
    if np.size(n_row)==1:
        return [False,'success']  
    else:
        return [True,'secondary']  
    
@app.callback(
    Output('o1_btn_gener_devis', 'disabled'),
    Output('o1_btn_gener_devis', 'color'),
    Input('o1_data_table', 'selected_rows'),
    prevent_initial_call=True# Déclencheur du callback (clics sur le bouton)
)
def rendre_bouton_incliquable(n_row):
    if np.size(n_row)>=1:
        return [False,'warning']
    else:
        return [True,'secondary']

# Callback de génération de devis.
@app.callback(
    Output('download_devis', 'data'),
    Input('o1_btn_gener_devis', 'n_clicks'),
    State('o1_data_table', 'selected_rows'),
    State('o1_data_table', 'data'),
    prevent_initial_call=True
)
def export_devis(n0, n_row,dict_data):
    df=pd.DataFrame.from_dict(dict_data)
    
    nom_archive = 'appPCOE/impressions/devis/devis_archive.zip'
    
    # Vérifier si le fichier ZIP existe déjà, et si c'est le cas, supprimez-le.
    if os.path.exists(nom_archive):
        os.remove(nom_archive)
    
    conn = connect_to_db()
    
    with zipfile.ZipFile(nom_archive, 'w') as myzip:
    # Ajoutez des fichiers à l'archive en utilisant la méthode `write`.
        for i in n_row :
            data_row=df.iloc[i].to_dict()
            nom_devis='devis_'+str(data_row['code_projet_boond'])+'_'+str(data_row['client'])
            # A faire : finir de rentrer les autres informations.
            # Faire une vérification avant l'envoi du devis
            update_request=f"""UPDATE app_table SET devis=True WHERE code_projet_boond={data_row['code_projet_boond']}"""
            execute_sql_request(update_request, conn)
            remplir_devis(nom_devis, data_row['client'], data_row['adresse'], data_row['code_postal'], data_row['ville'], 'editeur', 'type_support',
                data_row['date_anniversaire'], data_row['code_projet_boond'], data_row['parc_licence'], 'conditions_facturation',
                'conditions_paiement', data_row['prix_vente_n1'],np.round(data_row['prix_vente_n1']*1.2,2))  # 'Prix d\'achat actuel' ou' Achat SAP Maintenance ou GBS ou NEED4VIZ'
            myzip.write('appPCOE/impressions/devis/'+nom_devis+'.docx',nom_devis+'.docx')

    disconnect_from_db(conn)

    return dcc.send_file('appPCOE/impressions/devis/devis_archive.zip')


# Callback pour stocker les données de la ligne sélectionnée dans le dcc.Store
@app.callback(
    Output('o1_store_row', 'data'),
    Input('o1_data_table', 'selected_rows'),
    Input('o1_data_table', 'data'),
    prevent_initial_call=True,
)
def store_selected_row(selected_rows, dict_data):
    df = pd.DataFrame.from_dict(dict_data)
    if df.empty:
        return {}
    elif selected_rows:
        selected_row_data = df.iloc[selected_rows[0]].to_dict()
        return selected_row_data
    else:
        return {}


# Callback pour remplir les champs du modal pop-up "modifier la saisie" avec les données de la ligne sélectionnée dans la table
@app.callback(
    Output('input-client', 'children'),
    Output('input-erp-number', 'children'),
    Output('input-date-anniversaire', 'children'),  # "date"
    Output('input-code-projet-boond', 'children'),
    Output('input-resp-commercial', 'children'),
    Output('input-editeur', 'children'),  # card "informations générales"

    # Output('input-badge-generation-devis', 'color'),   #'children' or 'style' or 'color'
    # Output('input-badge-validation-devis', 'color'),
    # Output('input-badge-alerte-renouvellement', 'color'),
    # Output('input-badge-resilie', 'color'), # card "Alertes" (badge)

    Output('input-check-infos', 'checked'),
    Output('input-validation-erronnes', 'checked'),
    Output('input-envoi-devis', 'checked'),
    Output('input-accord-de-principe', 'checked'),
    Output('input-signature-client', 'checked'),
    Output('input-achat-editeur', 'checked'),
    Output('input-traitement-comptable', 'checked'),
    Output('input-paiement-sap', 'checked'),  # card "Status et conditions financières"-status

    Output('input-prix-achat-actuel', 'value'),
    Output('input-prix-vente-actuel', 'value'),
    Output('input-Marge-pourcentage', 'value'),
    Output('input-nv-prix-achat', 'value'),
    Output('input-nv-prix-vente', 'value'),
    Output('input-Marge-N+1', 'value'),  # card "Status et conditions financières"-cond. financières

    Output('input-type-contrat', 'value'),
    Output('input-type-support-sap', 'value'),
    Output('input-cond-fact', 'value'),
    Output('input-cond-paiement', 'value'),
    Output('input-adresse-client', 'value'),
    Output('input-parc-licences', 'value'),  # card "Informations contractuelles"

    # Input("o1_modal", 'data'), #input du modal pop-up complet
    Input('o1_store_row', 'data'),  # input du layout complet
    prevent_initial_call=True,
)

def update_modal_pop_up(selected_row_data):
    client = selected_row_data.get('client', '')  # card "informations générales"
    erp_number = selected_row_data.get('num_ref_sap', '')  # 'ERP Number \nRéf SAP'
    date_anniversaire = selected_row_data.get('date_anniversaire', '')
    code_projet_boond = selected_row_data.get('code_projet_boond', '')  # via API
    resp_commercial = selected_row_data.get('resp_commercial', '')
    editeur = selected_row_data.get('Editeur', '')  # Editeur à Cf.avec ACA pour faire le lien, je ne vois pas où il est dans xls!

    # badge_generation_devis = selected_row_data.get('Génération devis', '') # card "Alertes" (badge)
    # badge_validation_devis = selected_row_data.get('Validation devis', '')
    # badge_alerte_renouvellement = selected_row_data.get('Renouvellement', '')
    # badge_resilie = selected_row_data.get('Résilié', '')

    check_infos = selected_row_data.get('check_infos', '')  # card "Status et conditions financières"-status
    validation_erronees = selected_row_data.get('validation_erronee', '')
    envoi_devis = selected_row_data.get('envoi_devis', '')
    if envoi_devis=='False':
        envoi_devis=False
    accord_principe = selected_row_data.get('accord_principe', '')
    if accord_principe=='False':
        accord_principe=False
    signature_client = selected_row_data.get('signature_client', '')
    achat_editeur = selected_row_data.get('achat_editeur', '')
    traitement_comptable = selected_row_data.get('traitement_comptable', '')
    paiement_sap = selected_row_data.get('paiement_sap', '')

    prix_achat_n = selected_row_data.get("prix_achat_n", 0)  # card "Status et conditions financières"-cond. financières
    prix_vente_n = selected_row_data.get('prix_vente_n', 0)
    marge_n = selected_row_data.get('marge_n', 0)
    prix_achat_n1 = selected_row_data.get("prix_achat_n1", 0)
    prix_vente_n1 = selected_row_data.get('prix_vente_n1', 0)
    marge_n1 = selected_row_data.get('marge_n1', 0)

    type_contrat = selected_row_data.get('type_contrat', '')  # card "Informations contractuelles"
    type_support_sap = selected_row_data.get('type_support_sap', '')
    condition_facturation = selected_row_data.get('Condition de facturation', '')
    condition_paiement = selected_row_data.get('Condition de Paiement', '')
    adresse_client = selected_row_data.get('adresse', '')
    ville = selected_row_data.get('ville', '')
    cp = selected_row_data.get('code_postal', '')
    parc_licences = selected_row_data.get('parc_licence', '')

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
    if marge_n is not None:
        marge_n = round(marge_n * 100, 2)

    # Vérifiez si marge_annuel est None avant de faire le calcul
    if marge_n1 is not None:
        marge_n1 = round(marge_n1 * 100, 2)

    # Vérifiez si prix_achat_actuel est None avant de faire le calcul
    if prix_achat_n is not None:
        prix_achat_n = round(prix_achat_n, 2)

    # Vérifiez si prix_vente_actuel est None avant de faire le calcul
    if prix_vente_n is not None:
        prix_vente_n = round(prix_vente_n, 2)

    return (client, erp_number, date_anniversaire, code_projet_boond, resp_commercial, editeur,
            # badge_generation_devis,badge_validation_devis,badge_alerte_renouvellement,badge_resilie,
            check_infos, validation_erronees, envoi_devis, accord_principe, signature_client, achat_editeur,
            traitement_comptable, paiement_sap,
            prix_achat_n, prix_vente_n, marge_n, prix_achat_n1, prix_vente_n1, marge_n1,
            type_contrat, type_support_sap, condition_facturation, condition_paiement, adresse_client, parc_licences
            )


# ...............................

# callback pour ouvrir le pop-up et valider les données saisies ou modifiées
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
# callback pour mettre à jour les données du tableau
@app.callback(
    Output("o1_data_table", "data"), 
    Input("o1_btn_submit_validate", "n_clicks"),
    Input('o1_filtre_resp_com', 'value'),
    State('o1_data_table', 'selected_rows'),
    State("o1_data_table", "data"),

    State("input-client", "value"),
    State("input-erp-number", "value"),
    State("input-date-anniversaire", "value"),
    State("input-code-projet-boond", "value"),
    State("input-resp-commercial", "value"),
    State("input-editeur", "value"),  # card "informations générales"

    # State('input-badge-generation-devis', 'value'),   #'children' or 'style' or 'color'
    # State('input-badge-validation-devis', 'value'),
    # State('input-badge-alerte-renouvellement', 'value'),
    # State('input-badge-resilie', 'value'),  # card "Alertes" (badge)

    State('input-check-infos', 'checked'),
    State('input-validation-erronnes', 'checked'),
    State('input-envoi-devis', 'checked'),
    State('input-accord-de-principe', 'checked'),
    State('input-signature-client', 'checked'),
    State('input-achat-editeur', 'checked'),
    State('input-traitement-comptable', 'checked'),
    State('input-paiement-sap', 'checked'),  # card "Status et conditions financières"-status

    State('input-prix-achat-actuel', 'value'),
    State('input-prix-vente-actuel', 'value'),
    State('input-Marge-pourcentage', 'value'),
    State('input-nv-prix-vente', 'value'),
    State('input-nv-prix-achat', 'value'),
    State('input-Marge-N+1', 'value'),  # card "Status et conditions financières"-cond. financières

    State('input-type-contrat', 'value'),
    State('input-type-support-sap', 'value'),
    State('input-cond-fact', 'value'),
    State('input-cond-paiement', 'value'),
    State('input-adresse-client', 'value'),
    State('input-parc-licences', 'value'),  # card "Informations contractuelles"
    prevent_initial_call=False
)
def update_table_data(n_btn_submit_validate, resp_comm_list, selected_row_number, data_main_table,
                      client, erp_number, date_anniversaire, code_projet_boond, resp_commercial, editeur,
                      #  badge_generation_devis,badge_validation_devis,badge_alerte_renouvellement, badge_resilie,
                      check_infos, validation_erronnes, envoi_devis, accord_de_principe, signature_client,
                      achat_editeur, traitement_comptable, paiement_sap,
                      prix_achat_actuel, prix_vente_actuel, marge_pourcentage, nv_prix_vente, nv_prix_achat,
                      marge_annuel,
                      type_contrat, type_support_sap, condition_facturation, condition_paiement, adresse_client,
                      parc_licences                      ):
    conn = connect_to_db()
    df_app = sql_to_df("SELECT * FROM app_table", conn=conn)
    df_boond = sql_to_df("SELECT * FROM boond_table", conn=conn)
    disconnect_from_db(conn)
    df = pd.merge(df_boond, df_app, how='inner', on='code_projet_boond')
    df = df[df['resp_commercial'].isin(resp_comm_list)]
    df["date_anniversaire"] = df["date_anniversaire"].dt.date
    
    columns_to_convert = ['prix_achat_n1', 'prix_vente_n1', 'marge_n1']
    for column in columns_to_convert:
        df[column] = df[column].astype(float)

    df[['prix_achat_n1', 'prix_vente_n1', 'marge_n1']] = df.apply(apply_calcul_sale_price, axis=1)
    
    # Obligé de forcer le str pour le conditionnal formatiing du datatable...
    columns_to_convert = ['envoi_devis', 'accord_principe']
    for column in columns_to_convert:
        df[column] = df[column].fillna('')
        df[column] = df[column].astype(str)
    
    data_main_table = df.to_dict('records')
    if df.empty:
        return data_main_table

    if selected_row_number is not None and selected_row_number:  # Vérifiez si une ligne a été sélectionnée
        # Validez les données ici (effectuez des vérifications si nécessaire)

        # Construisez le dictionnaire des données mises à jour
        updated_data = {
            "Client": client,
            "ERP_Number_Ref_SAP": erp_number,
            "Date anniversaire": date_anniversaire,
            "Code projet Boond": code_projet_boond,
            "Responsable commercial": resp_commercial,
            "Editeur": editeur,

            # "Génération devis": badge_generation_devis,
            # "Validation devis": badge_validation_devis,
            # "Renouvellement": badge_alerte_renouvellement,
            # "Résilié": badge_resilie,

            "Check Infos": check_infos,
            "Validation erronées": validation_erronnes,
            "Envoi devis": envoi_devis,
            "Accord de principe": accord_de_principe,
            "Signature client": signature_client,
            "Achat éditeur": achat_editeur,
            'Traitement comptable': traitement_comptable,
            "Paiement SAP": paiement_sap,

            "Prix d'achat année N": prix_achat_actuel,
            'Prix de vente année N': prix_vente_actuel,
            'Marge année N': marge_pourcentage,
            "Prix d'achat année N+1": nv_prix_achat,
            'Prix de vente année N+1': nv_prix_vente,
            'Marge année N+1': marge_annuel,

            "Type de contrat": type_contrat,
            "Type de Support SAP": type_support_sap,
            "Condition de facturation": condition_facturation,
            "Condition de Paiement": condition_paiement,
            'Adresse': adresse_client,
            "Parc de licences": parc_licences
        }

        # Mettez à jour les données de la ligne sélectionnée dans data_main_table
        try:
            for key, value in updated_data.items():
                data_main_table[selected_row_number[0]][key] = value
        except IndexError as indexerror:
            print('indexerror:',indexerror)

        # Mettre à jour en BDD
        update_app_table(data_main_table[selected_row_number[0]]['code_projet_boond'],
                         nv_prix_achat, nv_prix_vente, marge_annuel, parc_licences,
                         check_infos, validation_erronnes, envoi_devis, accord_de_principe, signature_client,
                         achat_editeur, traitement_comptable, paiement_sap)
        

        #une fois la modification effectué, cela sert à recharger la data_main_table
        conn = connect_to_db()
        df_app = sql_to_df("SELECT * FROM app_table", conn=conn)
        df_boond = sql_to_df("SELECT * FROM boond_table", conn=conn)
        disconnect_from_db(conn)
        df = pd.merge(df_boond, df_app, how='inner', on='code_projet_boond')
        df = df[df['resp_commercial'].isin(resp_comm_list)]
        data_main_table = df.to_dict('records')



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


# ..................................................................................................
# callback pour gérer l'ouverture du pop-up "résilier" et la gestion des boutons "Oui" et "Non"
@app.callback(
    Output("confirm-resiliation", "displayed"),
    Output("confirm-resiliation", "message"),
    Output("o1_btn_submit_resiliation", "disabled"),
    Output("input-badge-resilie", "color"),  # Ajout de la sortie pour le badge
    Input("o1_btn_submit_resiliation", "n_clicks"),
    Input("confirm-resiliation", "submit_n_clicks"),
    Input("confirm-resiliation", "cancel_n_clicks"),
    State('o1_data_table', 'selected_rows'),
    State("o1_data_table", "data"),
    prevent_initial_call=True,
)
def confirm_resiliation(n_resiliation_clicks, submit_n_clicks, cancel_n_clicks, selected_row_number, data_main_table):
    if n_resiliation_clicks > 0:
        if submit_n_clicks is None and cancel_n_clicks is None:
            return True, "Souhaitez-vous réellement saisir une résiliation client?", True, 'blue'  # Initialiser la couleur du badge à bleu
        elif submit_n_clicks is not None and submit_n_clicks > 0:
            # Traitement à effectuer lorsque "Oui" est cliqué
            # Vous pouvez insérer ici la logique de résiliation client
            # Mettre à jour la couleur du badge en rouge
            update_app_table_resiliation(data_main_table[selected_row_number[0]]['code_projet_boond'])
            return False, "", False, 'red'
        else:
            # Traitement à effectuer lorsque "Non" est cliqué
            return False, "", False, 'blue'  # Réinitialiser la couleur du badge à bleu

    return False, "", False, 'blue'  # Réinitialiser la couleur du badge à bleu


# ...........................................................................................
# callback carte "Alertes"
@app.callback(
    Output('input-badge-validation-devis', 'color'),  # 'color' ou 'style'
    Output('input-badge-alerte-renouvellement', 'color'),
    Output('input-badge-generation-devis','color'),
    Input('o1_btn_modif_ech', 'n_clicks'),  # Utilisez le bouton comme déclencheur
    Input('o1_store_row', 'data'),
    prevent_initial_call=True,
)
def update_badge_colors(n_clicks, selected_row_data):
    if selected_row_data is None:
        # Gérez le cas où selected_row_data est None
        return 'gray', 'gray'  # {'color': 'gray'}, {'color': 'gray'}

    # Initialisez les styles par défaut
    validation_devis_style = 'blue'  # {'color': 'blue'}  # Style par défaut pour "Validation devis"
    alerte_renouvellement_style = 'blue'  # {'color': 'blue'}  # Style par défaut pour "Renouvellement"

    # Valeurs de "Validation devis" et "Renouvellement" à partir des données de la ligne sélectionnée
    validation_devis = selected_row_data.get('alerte_validation_devis', '')
    alerte_renouvellement = selected_row_data.get('alerte_renouvellement', '')
    etat_envoi_devis=selected_row_data.get('envoi_devis', '')
    etat_devis=selected_row_data.get('devis', '')
    etat_accord_principe=selected_row_data.get('accord_principe', '')

    # Convertir en float pour permettre la comparaison avec les entiers
    validation_devis = float(validation_devis) if validation_devis else 0.0
    alerte_renouvellement = float(alerte_renouvellement) if alerte_renouvellement else 0.0

    # Mettre à jour les styles en fonction des conditions
    if validation_devis > 56 or etat_envoi_devis=='True':
        validation_devis_style = 'green'
    elif 21 < validation_devis <= 56:
        validation_devis_style = 'orange'
    else:
        validation_devis_style = 'red'

    if alerte_renouvellement > 120 or etat_accord_principe=='True':
        alerte_renouvellement_style = 'green'
    elif 45 <= alerte_renouvellement <= 120:
        alerte_renouvellement_style = 'orange'
    else:
        alerte_renouvellement_style = 'red'
        
    if etat_devis=='true':
        alerte_generation_devis='green'
    else :
        alerte_generation_devis='orange'
        
    return validation_devis_style, alerte_renouvellement_style,alerte_generation_devis


######################################################################################################

# Callback pour mettre à jour le nombre de lignes validées - 'check_infos' depuis la data_table et affichage sur la carte
@app.callback(
    Output('o1_nb_lignes_validees', 'children'),  # Utilisez 'children' pour modifier le texte
    Input('o1_data_table', 'data')
)

def update_valid_check_infos_count(data):
    # Convertissez la liste de dictionnaires en un DataFrame pandas
    df = pd.DataFrame(data)
    
    # Comptez les lignes valides dans la colonne 'check_infos' du DataFrame
    count = len(df[df['check_infos'] == True])
    print('count:', count)

    return count
    
# ...
 