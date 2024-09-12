import psycopg2
import pandas as pd



# Quelques fonctions de base pour se connecter à une base de données PostgreSQL :

# Fonction qui permet d'ouvrir une connection avec la BDD :
def open_connection():
    # Ci-dessous : changer les informations de connexion
    conn = psycopg2.connect(user = "postgres",
                            password = "Seenovate2021$",
                            host = "34.78.54.11",
                            port="5432",
                            database="jmzsd_dev")
    
    return conn


# Fonction qui permet de faire une requête et retourner un DataFrame :
def req2table(requete:str,
              conn = None)-> pd.DataFrame :
    """ Convertit la requete en dataframe """
    if not conn:
        to_close = True
        conn = open_connection()
    else:
        to_close = False
    cursor = conn.cursor()
    try:
        cursor.execute(requete)
    except:
        conn.rollback()
        print(f"Erreur sur: {requete}. L'objet retourné est nul.")
    else:
        col = [x.name for x in cursor.description]
        df = pd.DataFrame(cursor.fetchall(), columns=col)
        return df
    finally:
        if to_close:
            conn.close()
            print("Connexion fermée")

# Fonction qui permet de faire une requête et retourner une valeur :
def req2value(requete:str,
              conn = None)-> pd.DataFrame :
    """ convertit la requete en dataframe """
    if not conn:
        to_close = True
        conn = open_connection()
    else:
        to_close = False
    cursor = conn.cursor()
    try:
        cursor.execute(requete)
    except:
        conn.rollback()
        print(f"Erreur sur: {requete}. L'objet retourné est nul.")
    else:
        val = cursor.fetchall()
        if len(val) == 1:
            if len(val[0]) == 1:
                return val[0][0]
            else:
                print('Nombre de colonnes sélectionnées > 1')
        else:
            if len(val[0]) == 1:
                return [i[0] for i in val]
            else:
                print('Nombre de colonnes sélectionnées > 1')
    finally:
        if to_close:
            conn.close()
            print("Connexion fermée")
            
