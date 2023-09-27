import pandas as pd
import urllib.request
import json


# Paramètres de connexion à l'API
def get_auth():
    JWT = 'eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFMyNTYifQ.eyJ1c2VyVG9rZW4iOiIzMzJlNzM2NTY1NmU2Zjc2NjE3NDY1IiwiY2xpZW50VG9rZW4iOiI3MzY1NjU2ZTZmNzY2MTc0NjUiLCJ0aW1lIjoxNjg5ODM3NTkxLCJtb2RlIjoibm9ybWFsIn0.LZHTNajdWn_L98J9xTy1P2NMnoTiNSXsgFMWipDRQYI'
    BASE_API = 'https://ui.boondmanager.com/api'
    return JWT, BASE_API  # retourne le JWT et l'URL de l'API


# Identification vers l'API
jwt, BASE_API = get_auth()

# Paramètres de la requête
PageNumber = 1
params = {
    'page': PageNumber,
    'maxResults': 500
}

# URL complète de la requête
url = BASE_API + '/projects?page=' + str(PageNumber) + '&maxResults=500'
req = urllib.request.Request(url)

# Authentification
req.add_header('X-Jwt-Client-Boondmanager', jwt)

# Invocation
response = urllib.request.urlopen(req, data=None)

# Lecture de la réponse JSON
if response.getcode() == 200:
    print(response.getcode())
    json_data = json.load(response)
    with open("donnees.json", "w") as json_file:

        json.dump(json_data, json_file)

    for item in json_data['data']:
        # ++++++++++++++++++++++++++++++
        # ++++++++++++++++++++++++++++++
        dict_record = dict.fromkeys(item)

        try:
            dict_record['id_projet'] = str(item[u'id'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['prj_change'] = float(item[u'attributes'][u'exchangeRate'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['prj_changeagence'] = float(item[u'attributes'][u'exchangeRateAgency'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['prj_debut'] = str(item[u'attributes'][u'startDate'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['prj_devise'] = float(item[u'attributes'][u'currency'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['prj_turnover_excludingtax'] = float(item[u'attributes'][u'turnoverSimulatedExcludingTax'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['prj_margin_excludingtax'] = float(item[u'attributes'][u'marginSimulatedExcludingTax'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['prj_profitability'] = float(item[u'attributes'][u'profitabilitySimulated'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['prj_deviseagence'] = float(item[u'attributes'][u'currencyAgency'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['prj_fin'] = str(item[u'attributes'][u'endDate'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['prj_reference'] = str(item[u'attributes'][u'reference'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['prj_type'] = int(float(item[u'attributes'][u'mode']))
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['prj_typeref'] = int(float(item[u'attributes'][u'typeOf']))
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['id_profil'] = str(item[u'relationships'][u'mainManager'][u'data'][u'id'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['id_ao'] = str(item[u'relationships'][u'opportunity'][u'data'][u'id'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['id_crmcontact'] = str(item[u'relationships'][u'contact'][u'data'][u'id'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['id_crmsociete'] = str(item[u'relationships'][u'company'][u'data'][u'id'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['id_societe'] = str(item[u'relationships'][u'agency'][u'data'][u'id'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['id_pole'] = str(item[u'relationships'][u'pole'][u'data'][u'id'])
        except (TypeError, KeyError) as e:
            pass
        try:
            dict_record['id_profilcdp'] = str(item['relationships']['mainManager']['data']['id'])
        except (TypeError, KeyError) as e:
            pass

    # Convertir la réponse JSON en un DataFrame Pandas
    df_projects = pd.DataFrame(json_data['data'])

    # print (df.attributes[0])
    print(dict_record)

    # Configure Pandas to display all columns and rows
    pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)

    # Maintenant, vous avez vos données dans le DataFrame 'df'
    print(df_projects)
else:
    print(f'Erreur lors de la requête à l\'API : {response.getcode()}')
