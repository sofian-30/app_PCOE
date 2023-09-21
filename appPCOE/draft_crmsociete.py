import pandas as pd
import requests
import urllib.request
import json

# Paramètres de connexion à l'API
def get_auth():
    JWT = 'eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFMyNTYifQ.eyJ1c2VyVG9rZW4iOiIzMzJlNzM2NTY1NmU2Zjc2NjE3NDY1IiwiY2xpZW50VG9rZW4iOiI3MzY1NjU2ZTZmNzY2MTc0NjUiLCJ0aW1lIjoxNjg5ODM3NTkxLCJtb2RlIjoibm9ybWFsIn0.LZHTNajdWn_L98J9xTy1P2NMnoTiNSXsgFMWipDRQYI'
    BASE_API = 'https://ui.boondmanager.com/api'
    return JWT, BASE_API # retourne le JWT et l'URL de l'API



# Identification vers l'API
jwt, BASE_API = get_auth()

# Paramètres de la requête
PageNumber = 1
params = {
    'page': PageNumber,
    'maxResults': 500
}

# URL complète de la requête
url = BASE_API + '/companies?maxResults=500&page='+str(PageNumber)
req = urllib.request.Request(url)

 ## Authentification
req.add_header('X-Jwt-Client-Boondmanager', jwt)

## Invocation 
response = urllib.request.urlopen(req, data=None)

# Lecture de la réponse JSON
if response.getcode() == 200:
    print(response.getcode())
    json_data = json.load(response)
    with open("donnees_crmsociete.json", "w") as json_file:

        json.dump(json_data, json_file)

    # Convertir les données JSON en un DataFrame Pandas
    df_crmsociete = pd.DataFrame(json_data)
    print(df_crmsociete)

    # Maintenant, vous avez vos données dans le DataFrame 'df' et vous pouvez les utiliser dans votre application Dash
else:
    print(f'Erreur lors de la requête à l\'API : {response.getcode()} - {response.text}')