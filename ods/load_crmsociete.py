# Import package
import json
import time
import urllib.request

import pandas as pd

# Import functions
from ods.auth import get_auth

# Identification vers l'API
jwt, BASE_API = get_auth()

table_name = 'boon_tab_crmsociete_fri'
start_time_global = time.time()

# Variables de pagination
FlagInvocationAPI = 1
PageNumber = 1
columns = ["id_crmsociete", "csoc_societe", "csoc_intervention", "csoc_type", "csoc_metiers", "csoc_web", "csoc_tel",
           "csoc_ville", "csoc_pays", "csoc_date", "id_profil", "id_societe", "id_pole", "id_action_previous",
           "id_action_next", 'id_provenance', "csoc_cp"]

# Liste des enregistrements
ls_res = []

# Boucle sur les pages de l'API
while FlagInvocationAPI > 0:
    FlagInvocationAPI = 0
    url = BASE_API + '/companies?maxResults=500&page=' + str(PageNumber)
    print(url)
    req = urllib.request.Request(url)

    # Authentification
    req.add_header('X-Jwt-Client-Boondmanager', jwt)

    # Invocation
    response = urllib.request.urlopen(req, data=None)

    # Parsing
    if response.getcode() == 200:
        json_object = json.load(response)
        # Parsing
        if len(json_object['data']) > 0:
            PageNumber = PageNumber + 1
            FlagInvocationAPI = 1

        print('--- invocation API /companies?maxResults=500&page=' + str(PageNumber - 1) + ' : Code retour OK  --')

        for item in json_object['data']:
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            dict_record = dict.fromkeys(columns)

            try:
                dict_record['id_crmsociete'] = str(item['id'])
            except (TypeError, KeyError) as e:
                pass

            try:
                dict_record['csoc_societe'] = str(item[u'attributes'][u'name'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['csoc_intervention'] = str(item[u'attributes'][u'expertiseArea'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['csoc_type'] = int(item[u'attributes'][u'state'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['csoc_metiers'] = str(item[u'attributes'][u'informationComments'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['csoc_web'] = str(item[u'attributes'][u'website'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['csoc_tel'] = str(item[u'attributes'][u'phone1'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['csoc_ville'] = str(item[u'attributes'][u'town'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['csoc_pays'] = str(item[u'attributes'][u'country'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['csoc_date'] = str(item[u'attributes'][u'creationDate'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['id_profil'] = str(item[u'relationships'][u'mainManager'][u'data'][u'id'])
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
                dict_record['id_action_previous'] = str(item[u'relationships'][u'previousAction'][u'data'][u'id'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['id_action_next'] = str(item[u'relationships'][u'nextAction'][u'data'][u'id'])
            except (TypeError, KeyError) as e:
                pass

            urlId = BASE_API + f'/companies/{str(item["id"])}/information'
            print(urlId)
            reqId = urllib.request.Request(urlId)

            # Authentification
            reqId.add_header('X-Jwt-Client-Boondmanager', jwt)

            # Invocation
            responseId = urllib.request.urlopen(reqId, data=None)
            if responseId.getcode() == 200:
                json_objectId = json.load(responseId)

            try:
                dict_record[u'id_provenance'] = str(
                    json_objectId['data'][u'attributes'][u'origin'][u'typeOf'])  # rajouté xavier
            except (TypeError, KeyError) as e:
                pass

            if 'origin' in item['attributes'] and 'typeOf' in item['attributes']['origin']:  # pour remédier aux null
                dict_record['id_provenance'] = str(item['attributes']['origin']['typeOf'])

            urlId = BASE_API + '/companies/' + str(item[u'id']) + '/information'
            reqId = urllib.request.Request(urlId)
            # Authentification
            reqId.add_header('X-Jwt-Client-Boondmanager', jwt)
            # Invocation
            responseId = urllib.request.urlopen(reqId, data=None)

            if responseId.getcode() == 200:
                # print ('-- invocation API times-reports/{id} for id_listetemps {'+str(item[u'id'])+'} : Code retour OK  --')
                # ___________________
                json_objectId = json.load(responseId)

                item_id = json_objectId['data']

                # ___________________
                try:
                    dict_record['csoc_cp'] = str(item_id[u'attributes'][u'postcode'])
                except (TypeError, KeyError) as e:
                    pass

            ls_res.append(dict_record.copy())

        # ___________________________________________________________
        # Page suivante    
    # _+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+
    else:
        print('--- Fin invocation API -----')

# Conversion en dataframe
df = pd.json_normalize(ls_res)

# Conversion des champs en numérique
# df.id_provenance = df.id_provenance.astype(int)
# df["id_provenance"] = df["id_provenance"].astype(pd.Int64Dtype())
df["id_provenance"] = df["id_provenance"].astype(pd.Int8Dtype())

# Affichage des valeurs uniques de la colonne "id_provenance"
print(df["id_provenance"].unique())
# print(df["id_pole"].unique())

df.to_csv('./data/crmsociete.csv')
