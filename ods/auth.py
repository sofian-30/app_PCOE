# Information: This file contains the authentication information for the API.
import psycopg2

# Pour modifier la connexion à la base de données,
# il faut modifier la fonction engine_connection et 
# la fonction db_connection.


# Paramètres de connexion à l'API
def get_auth():
    JWT = 'eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFMyNTYifQ.eyJ1c2VyVG9rZW4iOiIzMzJlNzM2NTY1NmU2Zjc2NjE3NDY1IiwiY2xpZW50VG9rZW4iOiI3MzY1NjU2ZTZmNzY2MTc0NjUiLCJ0aW1lIjoxNjg5ODM3NTkxLCJtb2RlIjoibm9ybWFsIn0.LZHTNajdWn_L98J9xTy1P2NMnoTiNSXsgFMWipDRQYI'
    BASE_API = 'https://ui.boondmanager.com/api'
    return JWT, BASE_API  # retourne le JWT et l'URL de l'API


# Paramètres de connexion à la base de données par SQLAlchemy
def engine_connection():
    # Connection to DB by SQLAlchemy
    engine = 'postgresql://BODS_ODS:324WNm3eq8WFvd@35.195.70.11:5432/postgres'
    return engine


# Fonction pour se connecter à la base de données par psycopg2
def db_connection():
    conn = psycopg2.connect(
        database="postgres", host='35.195.70.11', user='BODS_ODS', password='324WNm3eq8WFvd', port='5432'
    )
    return conn, conn.cursor()


# Fonction pour fermer la connexion à la base de données
def db_close_connection(conn):
    conn.close()  # fermeture de la connexion
