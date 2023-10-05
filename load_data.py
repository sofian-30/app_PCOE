from datetime import datetime

import pandas as pd

from config import logger
from db import connect_to_db, disconnect_from_db, insert_df_to_table
from utils import process_monitoring


def execute_script(python_script: str) -> None:
    logger.info(f"Start execution of script {python_script}")
    try:
        with open(python_script) as f:
            exec(f.read())
        logger.info(f"Execution of {python_script} terminated")
    except Exception as e:
        logger.error(f"Error executing {python_script}: {str(e)}")


def load_data_from_boond() -> None:
    # Créer les fichiers CSV nécessaires avec l'API Boond
    script_to_execute = ['load_projet.py', 'load_profil.py', 'load_crmsociete.py', 'load_achat.py',
                         'load_projet_achat.py',
                         'load_bondecommande.py']
    for script in script_to_execute:
        execute_script('ods/' + script)

    # Charger les fichiers CSV
    df_projet = pd.read_csv("data/projet.csv", sep=",", quotechar='"', index_col=0)
    df_profil = pd.read_csv("data/profil.csv", sep=",", quotechar='"', index_col=0)
    df_crmsociete = pd.read_csv("data/crmsociete.csv", sep=",", quotechar='"', index_col=0)
    df_achat = pd.read_csv("data/achat.csv", sep=",", quotechar='"', index_col=0)
    df_projet_achat = pd.read_csv("data/projet_achat.csv", sep=",", quotechar='"', index_col=0)
    df_bdc = pd.read_csv("data/bondecommande.csv", sep=",", quotechar='"', index_col=0)

    # PROJET
    logger.debug("PROJET")
    # Filtrer les lignes dans projet où prj_etat est égal à 1 et prj_typeref est dans [6, 12]
    df_boond = df_projet[(df_projet['prj_etat'] == 1) & (df_projet['prj_typeref'].isin([6, 12]))]
    logger.debug(f"df_boond.shape = {df_boond.shape}")

    # CRM SOCIETE
    logger.debug("CRM SOCIETE")
    df_boond = pd.merge(df_boond, df_crmsociete, on='id_crmsociete', how='left')
    logger.debug(f"df_boond.shape = {df_boond.shape}")

    # BON DE COMMANDE
    logger.debug("BON DE COMMANDE")
    df_bdc = df_bdc.drop_duplicates()
    # Trier bdc par ordre décroissant de id_bondecommande et garder les premiers enregistrements pour chaque id_projet
    df_bdc = df_bdc.sort_values(by='id_bondecommande', ascending=False)
    df_bdc = df_bdc.groupby('id_projet').first().reset_index()
    # Fusionner projet_achat avec derniers_bdc sur la colonne 'id_projet' (équivalent d'un LEFT JOIN en SQL)
    df_boond = pd.merge(df_boond, df_bdc, on='id_projet', how='left')
    logger.debug(f"df_boond.shape = {df_boond.shape}")

    # PROFIL
    logger.debug("PROFIL")
    # Garder uniquement l'id et le trigramme dans le profil
    df_profil['profil_trigramme'] = df_profil['profil_prenom'].str[0] + df_profil['profil_nom'].str[:2]
    df_profil = df_profil[['id_profil', 'profil_trigramme']]
    # Fusionner projet_update avec profil sur la colonne 'id_profilcdp' et 'id_profil' (équivalent d'un LEFT JOIN en SQL)
    df_boond = pd.merge(df_boond, df_profil, left_on='id_profilcdp', right_on='id_profil', how='left')
    logger.debug(f"df_boond.shape = {df_boond.shape}")

    # PROJET ACHAT
    logger.debug("PROJET ACHAT")
    df_projet_achat = df_projet_achat.drop_duplicates()
    df_boond = pd.merge(df_boond, df_projet_achat, on='id_projet', how='left')
    logger.debug(f"df_boond.shape = {df_boond.shape}")

    # ACHAT
    logger.debug("ACHAT")
    df_achat = df_achat.drop_duplicates()
    # Convertir la colonne 'achat_date' en date et prendre le dernier achat en date sur chaque projet
    df_achat['achat_date'] = pd.to_datetime(df_achat['achat_date'])
    df_boond = pd.merge(df_boond, df_achat, on='id_achat', how='left')
    df_boond = df_boond.sort_values(by=['id_projet', 'achat_date'], ascending=[True, False])
    df_boond = df_boond.drop_duplicates(subset='id_projet', keep='first')
    logger.debug(f"df_boond.shape = {df_boond.shape}")

    # Écrire le résultat dans un fichier CSV
    df_boond.to_csv('./data/boond.csv', index=False, sep=';')

    # Ecrire le résultat en BDD
    table_name = "boond_table"

    conn = connect_to_db()

    try:
        nb_lines = len(df_boond)
        insert_df_to_table(df_boond, table_name, 'replace', conn)
        process_monitoring(conn, table_name, nb_lines=nb_lines)
    except Exception as err:
        process_monitoring(conn, table_name, error_message=repr(err))

    disconnect_from_db(conn)


def load_data_from_csv() -> None:
    app_table_name = 'app_table'
    boond_table_name = 'boond_table'

    df = pd.read_excel("./data/Suivi CA licences et maintenance 2023.xlsx",
                       sheet_name='Maintenance SAP BusinessObjects',
                       parse_dates=['Date anniversaire'], date_parser=pd.to_datetime)
    today = datetime.now()
    df['alerte_renouvellement'] = (df['Date anniversaire'] - today).dt.days
    df['alerte_validation_devis'] = (df['Date anniversaire'] - today).dt.days

    # COMPUTE APP TABLE
    logger.info(f"Compute table {app_table_name}")
    conn = connect_to_db()
    try:
        app_columns = ['Code projet Boond', 'Proposition SAP reçue', 'Relance client**', 'Proposition Seenovate créée',
                       'Proposition Seenovate envoyée', 'Proposition signée par le client',
                       'Attente  N° Cde client avant facturation', 'Facture  créée', 'Commande faite SAP',
                       'Facture SAP reçue', 'Remarques', 'Devis', 'Accord de principe', 'Signature client',
                       'Achat éditeur', 'Renouvelé', 'Traitement comptable', 'Paiement SAP', 'Demande de résiliation',
                       'Communication éditeur', 'Résilié', 'Converti ou Extension', 'alerte_renouvellement',
                       'alerte_validation_devis']

        df_app = df[app_columns]
        df_app = df_app.rename(columns={'Code projet Boond': 'code_projet_boond',
                                        'Proposition SAP reçue': 'proposition_sap_recue',
                                        'Relance client**': 'date_relance_client',
                                        'Proposition Seenovate créée': 'proposition_seenovate_creee',
                                        'Proposition Seenovate envoyée': 'date_envoi_proposition',
                                        'Proposition signée par le client': 'date_signature_proposition',
                                        'Attente  N° Cde client avant facturation': 'num_commande',
                                        'Facture  créée': 'date_creation_facture',
                                        'Commande faite SAP': 'commande_faite_sap',
                                        'Facture SAP reçue': 'facture_sap_recue',
                                        'Remarques': 'remarques',
                                        'Devis': 'devis',
                                        'Accord de principe': 'accord_principe',
                                        'Signature client': 'signature_client',
                                        'Achat éditeur': 'achat_editeur',
                                        'Renouvelé': 'renouvele',
                                        'Traitement comptable': 'traitement_comptable',
                                        'Paiement SAP': 'paiement_sap',
                                        'Demande de résiliation': 'demande_resiliation',
                                        'Communication éditeur': 'communication_editeur',
                                        'Résilié': 'resilie',
                                        'Converti ou Extension': 'converti_extension'})
        df_app['prix_achat_n1'] = None
        df_app['prix_vente_n1'] = None
        df_app['marge_n1'] = None

        df_app['check_infos'] = None
        df_app['validation_erronee'] = None
        df_app['envoi_devis'] = None
        df_app['parc_licence'] = None

        nb_lines = len(df_app)
        insert_df_to_table(df_app, app_table_name, 'truncate', conn)
        process_monitoring(conn, app_table_name, nb_lines=nb_lines)
    except Exception as err:
        process_monitoring(conn, app_table_name, error_message=repr(err))
    disconnect_from_db(conn)

    # COMPUTE BOOND TABLE
    logger.info(f"Compute table {app_table_name}")
    conn = connect_to_db()
    try:
        boond_columns = ['Code projet Boond', 'Agence', 'Client', 'ERP_Number_Ref_SAP', 'Date anniversaire',
                         'Achat SAP Maintenance ou GBS ou NEED4VIZ', 'CA maintenance facturé', 'Marge maintenance ',
                         'Type de support SAP', 'Type de contrat', 'Parc/Techno', 'Resp\nCommercial']
        df_boond = df[boond_columns]
        df_boond = df_boond.rename(columns={'Code projet Boond': 'code_projet_boond',
                                            'Agence': 'agence',
                                            'Client': 'client',
                                            'ERP_Number_Ref_SAP': 'num_ref_sap',
                                            'Date anniversaire': 'date_anniversaire',
                                            'Achat SAP Maintenance ou GBS ou NEED4VIZ': 'prix_achat_n',
                                            'CA maintenance facturé': 'prix_vente_n',
                                            'Marge maintenance ': 'marge_n',
                                            'Type de support SAP': 'type_support_sap',
                                            'Type de contrat': 'type_contrat',
                                            'Parc/Techno': 'parc_techno',
                                            'Resp\nCommercial': 'resp_commercial'})

        df_boond['adresse'] = None
        df_boond['ville'] = None
        df_boond['code_postal'] = None

        nb_lines = len(df_boond)
        insert_df_to_table(df_boond, boond_table_name, 'replace', conn)
        process_monitoring(conn, boond_table_name, nb_lines=nb_lines)
    except Exception as err:
        process_monitoring(conn, boond_table_name, error_message=repr(err))
    disconnect_from_db(conn)


load_data_from_csv()
