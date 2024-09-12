# Import package
import json
import time
import urllib.request

import pandas as pd

# Import functions
from ods.auth import get_auth

# Identification vers l'API
jwt, BASE_API = get_auth()

table_name = 'boon_tab_projet_fri'
start_time_global = time.time()

# Variables de pagination
FlagInvocationAPI = 1
PageNumber = 1
columns = ["id_projet",
           "prj_etat",
           "prj_date",
           "prj_dateupdate",
           "prj_debut",
           "prj_fin",
           "prj_typeref",
           "prj_type",
           "prj_reference",
           "prj_devise",
           "prj_change",
           "prj_deviseagence",
           "prj_changeagence",
           "prj_adr",
           "prj_cp",
           "prj_ville",
           "prj_pays",
           "prj_lotstab",
           "prj_commentaires",
           "prj_turnover_excludingtax",
           "prj_margin_excludingtax",
           "prj_profitability",
           "id_profil",
           "id_ao",
           "id_crmcontact",
           "id_crmsociete",
           "id_societe",
           "id_pole",
           "id_profilcdp"]

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

        print('--- invocation API /projects?page=' + str(PageNumber) + ' : Code retour OK  --')
        print(len(ls_res))
        for item in json_object['data']:
            # ++++++++++++++++++++++++++++++++++++++++++
            # ++++++++++++++++++++++++++++++
            dict_record = dict.fromkeys(columns)

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

            urlInfo = BASE_API + '/projects/' + str(item['id']) + '/information'
            reqInfo = urllib.request.Request(urlInfo)
            # Authentification
            reqInfo.add_header('X-Jwt-Client-Boondmanager', jwt)
            # Invocation
            responseInfo = urllib.request.urlopen(reqInfo, data=None)
            if responseInfo.getcode() == 200:
                json_objectId = json.load(responseInfo)

                try:
                    dict_record['prj_date'] = json_objectId[u'data'][u'attributes'][u'creationDate']
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['prj_dateupdate'] = json_objectId[u'data'][u'attributes'][u'updateDate']
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['prj_adr'] = json_objectId[u'data'][u'attributes'][u'address']
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['prj_cp'] = json_objectId[u'data'][u'attributes'][u'postcode']
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['prj_ville'] = json_objectId[u'data'][u'attributes'][u'town']
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['prj_pays'] = json_objectId[u'data'][u'attributes'][u'country']
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['prj_etat'] = str(json_objectId[u'data'][u'attributes'][u'state'])
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['prj_commentaires'] = json_objectId[u'data'][u'attributes'][u'informationComments']
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
df.to_csv('./data/projet.csv')
