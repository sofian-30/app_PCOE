import pandas as pd

from db import connect_to_db, disconnect_from_db, insert_df_to_table
from config import logger
from utils import process_monitoring


def execute_script(python_script: str) -> None:
    logger.info(f"Start execution of script {python_script}")
    try:
        with open(python_script) as f:
            exec(f.read())
        logger.info(f"Execution of {python_script} terminated")
    except Exception as e:
        logger.error(f"Error executing {python_script}: {str(e)}")


# Créer les fichiers CSV nécessaires avec l'API Boond
script_to_execute = ['load_projet.py', 'load_profil.py', 'load_crmsociete.py', 'load_achat.py', 'load_projet_achat.py',
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
