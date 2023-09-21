import pandas as pd

from db import connect_to_db, disconnect_from_db, execute_sql_request
from config import logger


def execute_script(python_script: str) -> None:
    logger.info(f"Start execution of script {python_script}")
    try:
        with open(python_script) as f:
            exec(f.read())
        logger.info(f"Execution of {python_script} terminated")
    except Exception as e:
        logger.error(f"Error executing {python_script}: {str(e)}")


# # Créer les fichiers CSV nécessaires avec l'API Boond
# script_to_execute = ['load_projet.py', 'load_profil.py', 'load_crmsociete.py', 'load_achat.py', 'load_projet_achat.py',
#                      'load_bondecommande.py']
# for script in script_to_execute:
#     execute_script('ods/' + script)

# Charger les fichiers CSV
projet = pd.read_csv("data/projet.csv", sep=",", quotechar='"', index_col=0)
profil = pd.read_csv("data/profil.csv", sep=",", quotechar='"', index_col=0)
crmsociete = pd.read_csv("data/crmsociete.csv", sep=",", quotechar='"', index_col=0)
achat = pd.read_csv("data/data_rfo/achat.csv", sep=";", quotechar='"')
print(achat)
projet_achat = pd.read_csv("data/projet_achat.csv", sep=",", quotechar='"', index_col=0)
bdc = pd.read_csv("data/bondecommande.csv", sep=",", quotechar='"', index_col=0)

# Garder uniquement l'id et le trigramme dans le profil
profil['profil_trigramme'] = profil['profil_prenom'].str[0] + profil['profil_nom'].str[:2]
profil = profil[['id_profil', 'profil_trigramme']]

# Garder les enregistrements uniques dans achat, projet_achat et bdc
achat = achat.drop_duplicates()
print(achat)
print(achat.columns)
print(len(achat))
projet_achat = projet_achat.drop_duplicates()
df_achat = pd.merge(achat, projet_achat, on='id_projet', how='left')
print(df_achat)
print(df_achat.columns)
print(len(df_achat))

bdc = bdc.drop_duplicates()

# Trier bdc par ordre décroissant de id_bondecommande et garder les premiers enregistrements pour chaque id_projet
bdc = bdc.sort_values(by='id_bondecommande', ascending=False)
derniers_bdc = bdc.groupby('id_projet').first().reset_index()

# Filtrer les lignes dans projet où prj_etat est égal à 1 et prj_typeref est dans [6, 12]
projet = projet[(projet['prj_etat'] == 1) & (projet['prj_typeref'].isin([6, 12]))]

# Fusionner projet avec crmsociete sur la colonne 'id_crmsociete' (équivalent d'un LEFT JOIN en SQL)
projet_update = pd.merge(projet, crmsociete, on='id_crmsociete', how='left')

# Fusionner projet_update avec profil sur la colonne 'id_profilcdp' et 'id_profil' (équivalent d'un LEFT JOIN en SQL)
projet_update = pd.merge(projet_update, profil, left_on='id_profilcdp', right_on='id_profil', how='left')

# Convertir la colonne 'achat_date' en date et filtrer les enregistrements où la date est supérieure à '2022-09-01'
achat['achat_date'] = pd.to_datetime(achat['achat_date'])
achat_update = achat[achat['achat_date'] > '2022-09-01']

# Fusionner projet_update avec achat_update sur la colonne 'id_projet' (équivalent d'un LEFT JOIN en SQL)
projet_achat = pd.merge(projet_update, achat_update, on='id_projet', how='left')

# Fusionner projet_achat avec derniers_bdc sur la colonne 'id_projet' (équivalent d'un LEFT JOIN en SQL)
projet_achat_bdc = pd.merge(projet_achat, derniers_bdc, on='id_projet', how='left')

# Écrire le résultat dans un fichier CSV
projet_achat_bdc.to_csv('./data/pcoe.csv', index=False, sep=';')

conn = connect_to_db()
res = execute_sql_request("SELECT * from monitoring")
disconnect_from_db(conn)
