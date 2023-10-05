# Import package
import json
import time
import urllib.request

import pandas as pd

# Import functions
from ods.auth import get_auth

# Identification vers l'API
jwt, BASE_API = get_auth()

table_name = 'boon_tab_projet_achat_fri'
start_time_global = time.time()

# Variables de pagination
FlagInvocationAPI = 1
PageNumber = 1
columns = ["id_projet", "id_achat"]

# Liste des enregistrements
ls_res = []

# Boucle sur les pages de l'API
while FlagInvocationAPI > 0:
    FlagInvocationAPI = 0
    url = BASE_API + '/projects?page=' + str(PageNumber) + '&maxResults=500'
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
        else:
            break

        print('--- invocation API /projects?page=' + str(PageNumber - 1) + '&maxResults=500 : Code retour OK  --')
        print(len(ls_res))
        for item in json_object['data']:
            urlRi = BASE_API + '/projects/' + str(item['id']) + '/rights'
            reqRi = urllib.request.Request(urlRi)

            # Authentification
            reqRi.add_header('X-Jwt-Client-Boondmanager', jwt)

            # Invocation
            responseRi = urllib.request.urlopen(reqRi, data=None)
            if responseRi.getcode() == 200:
                json_objectRi = json.load(responseRi)

                if str(json_objectRi['data']['attributes']['apis']['purchases']['read']) == 'True':

                    urlId = BASE_API + '/projects/' + str(item['id']) + '/purchases'
                    ##
                    # Détail purchase
                    reqId = urllib.request.Request(urlId)
                    # Authentification
                    reqId.add_header('X-Jwt-Client-Boondmanager', jwt)
                    # Invocation
                    responseId = urllib.request.urlopen(reqId, data=None)
                    if responseId.getcode() == 200:
                        json_objectId = json.load(responseId)
                        for itemId in json_objectId['data']:
                            dict_record = dict.fromkeys(columns)
                            try:
                                dict_record['id_projet'] = int(float(item['id']))
                            except (TypeError, KeyError) as e:
                                pass
                            try:
                                dict_record['id_achat'] = int(float(itemId['id']))
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
df.to_csv('./data/projet_achat.csv')
