# Import package
import json
import time
import urllib.request

import pandas as pd

# Import functions
from ods.auth import get_auth

# Identification vers l'API
jwt, BASE_API = get_auth()

table_name = 'boon_tab_bondecommande_fri'
start_time_global = time.time()

# Variables de pagination
FlagInvocationAPI = 1
PageNumber = 1
columns = ["id_bondecommande", "bdc_date", "bdc_refclient", "bdc_ref", "bdc_accordclient",
           "bdc_turnoverinvoicedexcludtax", "bdc_turnoverorderedexcludtax", "bdc_deltainvoicedexcludtax",
           "bdc_etat", "id_respuser", "id_projet", "bdc_typreglement", "bdc_condreglement", "bdc_typepayment"]

# Liste des enregistrements
ls_res = []

# Boucle sur les pages de l'API
while FlagInvocationAPI > 0:
    FlagInvocationAPI = 0
    url = BASE_API + '/orders?maxResults=500&page=' + str(PageNumber)
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

        print('--- invocation API orders?page=' + str(PageNumber - 1) + ' : Code retour OK  --')

        for item in json_object['data']:
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            dict_record = dict.fromkeys(columns)

            try:
                dict_record['id_bondecommande'] = str(item['id'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['bdc_date'] = str(item[u'attributes'][u'date'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['bdc_refclient'] = str(item[u'attributes'][u'number'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['bdc_ref'] = str(item[u'attributes'][u'reference'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['bdc_accordclient'] = (item[u'attributes'][u'customerAgreement'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['bdc_turnoverinvoicedexcludtax'] = str(item[u'attributes'][u'turnoverInvoicedExcludingTax'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['bdc_turnoverorderedexcludtax'] = str(item[u'attributes'][u'turnoverOrderedExcludingTax'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['bdc_deltainvoicedexcludtax'] = str(item[u'attributes'][u'deltaInvoicedExcludingTax'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['bdc_etat'] = (item[u'attributes'][u'state'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['id_respuser'] = str(item[u'relationships'][u'mainManager'][u'data'][u'id'])
            except (TypeError, KeyError) as e:
                pass
            try:
                dict_record['id_projet'] = str(item[u'relationships'][u'project'][u'data'][u'id'])
            except (TypeError, KeyError) as e:
                pass

            urlId = BASE_API + '/orders/' + str(item[u'id']) + '/information'
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
                    dict_record['bdc_typreglement'] = str(item_id[u'attributes'][u'typeOf'])
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['bdc_condreglement'] = str(item_id[u'attributes'][u'paymentTerm'])
                except (TypeError, KeyError) as e:
                    pass
                try:
                    dict_record['bdc_typepayment'] = str(item_id[u'attributes'][u'paymentMethod'])
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
df.bdc_accordclient = df.bdc_accordclient.astype(int)
df.bdc_turnoverinvoicedexcludtax = pd.to_numeric(df.bdc_turnoverinvoicedexcludtax, errors='coerce')
df.bdc_turnoverorderedexcludtax = pd.to_numeric(df.bdc_turnoverorderedexcludtax, errors='coerce')
df.bdc_deltainvoicedexcludtax = pd.to_numeric(df.bdc_deltainvoicedexcludtax, errors='coerce')
df.bdc_etat = df.bdc_etat.astype(int)
df.bdc_condreglement = df.bdc_condreglement.astype(int)
df.bdc_typepayment = df.bdc_typepayment.astype(int)

df.to_csv('./data/bondecommande.csv')
