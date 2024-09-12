import pandas as pd
from db import connect_to_db, disconnect_from_db, sql_to_df

# Nom de la table et de la colonne dans la bdd
table_name = 'app_table'
column_name = 'validation_erronee'

# Réinitialisation de la colonne "validation_erronee" à False pour toutes les entrées dans la table
update_query = f"UPDATE {table_name} SET {column_name} = False"

try:
    # Connexion à la base de données
    connection = connect_to_db()

    # Exécution de la mise à jour
    connection.execute(update_query)

    # Déconnexion de la base de données
    disconnect_from_db(connection)
#........................................................................................................................

    print(f"La colonne {column_name} a été réinitialisée à False pour toutes les entrées dans la table {table_name}.")

except Exception as e:
    print(f"Une erreur s'est produite : {e}")
