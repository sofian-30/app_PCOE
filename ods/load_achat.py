# Import package
import datetime
import json
import time
import urllib.request

import pandas as pd

# Import functions
from ods.auth import get_auth

# Identification vers l'API
jwt, BASE_API = get_auth()

# ------------------------------------------------------------------
table_name = 'boon_tab_achat_fri'  # NOM TABLE A CHANGER
# ------------------------------------------------------------------

start_time_global = time.time()

# Variables de pagination
FlagInvocationAPI = 1
PageRecNumber = 0
PageNumber = 1
columns = ["id_achat", "achat_datecrea", "achat_dateupdate", "achat_date",
           "achat_etat", "achat_montantht", "achat_quantité", "achat_titre",
           "achat_ref", "achat_type", "achat_commentaire"]

# Variables de filtre date en entrée au format AAAA-MM

# Variable de filtre date en entrée au format AAAA-MM
startMonth = '2020-01'
# endmonth est le mois actuel + 1 mois
endMonth = str(datetime.datetime.now().year) + '-' + str(datetime.datetime.now().month + 1)

# Liste des enregistrements
ls_res = []

# Boucle sur les pages de l'API
while FlagInvocationAPI > 0:
    url = BASE_API + '/purchases?startMonth=' + startMonth + '&endMonth=' + endMonth + '&page=' + str(
        PageNumber - 1) + '&maxResults=500&perimeterAgencies=1'
    FlagInvocationAPI = 0

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
        print('--- invocation API /purchases?startMonth=' + startMonth + '&endMonth=' + endMonth + '&page=' + str(
            PageNumber) + '&maxResults=30&perimeterAgencies=1 : Code retour OK  --')
        print(len(ls_res))
        for item in json_object['data']:

            urlId = BASE_API + '/purchases/' + str(item[u'id']) + '/information'
            reqId = urllib.request.Request(urlId)
            # Authentification
            reqId.add_header('X-Jwt-Client-Boondmanager', jwt)
            # Invocation
            responseId = urllib.request.urlopen(reqId, data=None)
            if responseId.getcode() == 200:
                # ___________________
                json_objectId = json.load(responseId)
                item_id_i = json_objectId['data']
                dict_record = dict.fromkeys(columns)
                # ___________________
                try:
                    dict_record['id_achat'] = str(item[u'id'])
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['achat_datecrea'] = str(item_id_i[u'attributes'][u'creationDate'])
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['achat_dateupdate'] = str(item_id_i[u'attributes'][u'updateDate'])
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['achat_date'] = str(item_id_i[u'attributes'][u'date'])
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['achat_etat'] = str(item_id_i[u'attributes'][u'state'])
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['achat_montantht'] = str(item_id_i[u'attributes'][u'amountExcludingTax'])
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['achat_quantité'] = str(item_id_i[u'attributes'][u'quantity'])
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['achat_titre'] = str(item_id_i[u'attributes'][u'title'])
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['achat_ref'] = str(item_id_i[u'attributes'][u'reference'])
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['achat_type'] = str(item_id_i[u'attributes'][u'subscription'])
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['achat_commentaire'] = str(item_id_i[u'attributes'][u'informationComments'])
                except (TypeError, KeyError) as e:
                    pass

                ls_res.append(dict_record.copy())
                PageRecNumber += 1

        # fin lecture si aucun enregistrement  
        if PageRecNumber == 0:
            FlagInvocationAPI = 0
            # ___________________________________________________________
        # Page suivante    

    # _+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+
else:
    print('--- Fin invocation API -----')

# Conversion en dataframe
df = pd.json_normalize(ls_res)

# Conversion des champs en numérique
df.achat_etat = df.achat_etat.astype(int)
df.achat_montantht = df.achat_montantht.astype('float64')
df = df.rename(columns={'achat_quantité': 'achat_quantite'})
df['achat_quantite'] = df['achat_quantite'].astype('float64')
df.achat_type = df.achat_type.astype(int)

df.to_csv('./data/achat.csv')
