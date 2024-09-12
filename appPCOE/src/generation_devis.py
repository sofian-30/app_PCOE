from docx import Document
import datetime
from dateutil.relativedelta import relativedelta
from python_docx_replace import docx_replace
import numpy as np


def replace_text_in_paragraphs(doc, data):
    for key, value in data.items():
        docx_replace(doc, key = value)

def replace_text_in_tables(doc, data):
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in data.items():
                    cell.text = cell.text.replace(f"[{key}]", value)

def remplir_devis(nom_devis, client, adresse, CP, ville, editeur, type_support, date_anniversaire, code_boond, parc_licence,
                        conditions_facturation, conditions_paiement, prix_vente, prix_vente_tax):
    doc = Document("appPCOE/impressions/template_devis.docx")
    
    date_obj = datetime.datetime.strptime(date_anniversaire, "%Y-%m-%d")
    date_formatee = date_obj.strftime('%d/%m/%Y')
    
    # Ajoutez un jour
    nouvelle_date = date_obj + datetime.timedelta(days=1)
    nouvelle_date_str = nouvelle_date.strftime('%d/%m/%Y')
    date_plus_un_an = date_obj + relativedelta(years=1)
    date_plus_un_an_str = date_plus_un_an.strftime('%d/%m/%Y')
    
    data = {
        'NOM_DU_CLIENT': client,
        'ADRESSE': adresse,
        'CODE_POSTAL_VILLE': f'{ville} {CP}',
        'DATE_DE_GENERATION': datetime.datetime.now().strftime("%d-%m-%Y"),
        'NOM_EDITEUR': editeur,
        'TYPE_DE_SUPPORT': type_support,
        'DATE_ANNIVERSAIRE_UN_J': nouvelle_date_str,
        'DATE_ANNIVERSAIRE_xx_xx_xx': date_plus_un_an_str,
        'CODE_BOOND': code_boond,
        'DATE_ANNIVERSAIRE': date_formatee,
        'CONDITIONS_FACTURATION': conditions_facturation,
        'CONDITIONS_PAIEMENT': conditions_paiement,
        'PRIX_VENTE': str(np.round(prix_vente,2)),
        'PARC_CLIENT': str(parc_licence),
        'PV_20': str(np.round(prix_vente_tax,2))
    }
    docx_replace(doc, **data)
    doc.save('appPCOE/impressions/devis/'+nom_devis+'.docx')
