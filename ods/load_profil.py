# Import package
import json
import time
import urllib.request

import pandas as pd

# Import functions
from ods.auth import get_auth

# Identification vers l'API
jwt, BASE_API = get_auth()

table_name = 'boon_tab_profil_fri'
start_time_global = time.time()

# Variables de pagination
FlagInvocationAPI = 1
PageNumber = 1
columns = ["id_profil",
           "profil_date",
           "profil_dateupdate",
           "profil_civilite",
           "profil_prenom",
           "profil_nom",
           "profil_reference",
           "profil_type",
           "profil_statut",
           "profil_etat",
           "profil_visibilite",
           "param_mobilite",
           "comp_competence",
           "dt_titre",
           "profil_datenaissance",
           "id_respmanager",
           "id_resprh",
           "id_societe",
           "id_pole",
           "profil_email"]

# Liste des enregistrements
ls_res = []

# Boucle sur les pages de l'API
while FlagInvocationAPI > 0:
    FlagInvocationAPI = 0
    url = BASE_API + '/resources?maxResults=500&page=' + str(PageNumber)
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

        print('--- invocation API /resources?maxResults=500&page=' + str(PageNumber - 1) + ' : Code retour OK  --')
        print(len(ls_res))
        for item in json_object['data']:
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            dict_record = dict.fromkeys(columns)

            try:
                dict_record['id_profil'] = str(item['id'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['profil_date'] = str(item[u'attributes'][u'creationDate'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['profil_civilite'] = int(float(item[u'attributes'][u'civility']))
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['profil_prenom'] = str(item[u'attributes'][u'firstName'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['profil_nom'] = str(item[u'attributes'][u'lastName'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['profil_reference'] = str(item[u'attributes'][u'reference'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['profil_type'] = int(float(item[u'attributes'][u'typeOf']))
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['profil_etat'] = int(float(item[u'attributes'][u'state']))
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['profil_visibilite'] = int(float(item[u'attributes'][u'isVisible']))
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['comp_competence'] = str(item[u'attributes'][u'skills'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['param_mobilite'] = str(item[u'attributes'][u'mobilityAreas'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['dt_titre'] = str(item[u'attributes'][u'title'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['id_respmanager'] = str(item[u'relationships'][u'mainManager'][u'data'][u'id'])
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
                dict_record['profil_email'] = str(item[u'attributes'][u'email1'])
            except (TypeError, KeyError) as e:
                pass

            urlId = BASE_API + '/resources/' + str(item[u'id'])
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
                    dict_record['profil_dateupdate'] = str(item_id[u'attributes'][u'updateDate'])
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['profil_datenaissance'] = str(item_id[u'attributes'][u'dateOfBirth'])
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['id_resprh'] = str(item_id[u'relationships'][u'hrManager'][u'data'][u'id'])
                except (TypeError, KeyError) as e:
                    pass

            url_id_i = BASE_API + '/resources/' + str(item[u'id']) + '/information'
            req_id_i = urllib.request.Request(url_id_i)
            # Authentification
            req_id_i.add_header('X-Jwt-Client-Boondmanager', jwt)
            # Invocation
            response_id_i = urllib.request.urlopen(req_id_i, data=None)

            if response_id_i.getcode() == 200:
                json_object_id_i = json.load(response_id_i)

                item_id_i = json_object_id_i['data']
                try:
                    dict_record['profil_statut'] = str(item_id_i[u'attributes'][u'function'])
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
df.to_csv('./data/profil.csv')
