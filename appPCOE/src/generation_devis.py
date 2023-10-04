from docx import Document
import datetime
from dateutil.relativedelta import relativedelta


def remplir_devis(acces_devis, client, adresse, CP, ville, editeur, type_support, date_anniversaire, code_boond,
                  conditions_facturation,
                  conditions_paiement, condition_parc, prix_vente):
    # doc = Document("template_devis.docx")
    doc = Document("appPCOE/impressions/template_devis.docx")

    paragraphs_from_docx = doc.paragraphs

    # Gestion des paragraphes :

    # Nom du client 
    paragraphs_from_docx[3].text = client
    # Adresse
    paragraphs_from_docx[4].text = adresse
    # CP / Ville
    paragraphs_from_docx[5].text = CP + ' ' + ville

    # Obtenez la date actuelle
    date_actuelle = datetime.datetime.now()
    # Formatez la date en tant que chaîne de caractères
    date_actuelle_formatee = date_actuelle.strftime("%d-%m-%Y")

    # Date génération : 'Le [DATE de génération], à Paris'
    paragraphs_from_docx[7].text = 'Le ' + date_actuelle_formatee + ', à Paris'

    # Contrat :'Contrat\xa0: Support éditeur [NOM EDITEUR] - [TYPE DE SUPPORT]'
    paragraphs_from_docx[9].runs[5].text = editeur
    paragraphs_from_docx[9].runs[7].text = type_support

    date_obj = datetime.datetime.strptime(date_anniversaire, "%Y-%m-%dT%H:%M:%S")

    date_formatee = date_obj.strftime('%d/%m/%Y')

    # Ajoutez un jour
    nouvelle_date = date_obj + datetime.timedelta(days=1)
    nouvelle_date_str = nouvelle_date.strftime('%d/%m/%Y')

    date_plus_un_an = date_obj + relativedelta(years=1)
    date_plus_un_an_str = date_plus_un_an.strftime('%d/%m/%Y')

    # Date du contrat :Date du contrat\xa0: du [DATE ANNIVERSAIRE+1j] au [DATE ANNIVERSAIRE (xx/xx/xx)]' -laisser l'espace devant la date anniversaire.
    paragraphs_from_docx[10].runs[4].text = nouvelle_date_str
    paragraphs_from_docx[10].runs[5].text = ''
    paragraphs_from_docx[10].runs[7].text = ' ' + date_plus_un_an_str
    paragraphs_from_docx[10].runs[8].text = ''
    paragraphs_from_docx[10].runs[9].text = ''

    # Référence contrat : 'Référence contrat\xa0: [CODE BOOND]'
    paragraphs_from_docx[11].runs[3].text = code_boond

    # Validité : 'Validité\xa0: [DATE ANNIVERSAIRE]' - laisser l'espace devant
    paragraphs_from_docx[19].runs[1].text = ' ' + date_formatee

    # Conditions de factuation : 'Condition de facturation\xa0: [Conditions]'
    paragraphs_from_docx[20].runs[3].text = conditions_facturation

    # Conditions de paiement : 'Condition de paiement\xa0: [Conditions]'
    paragraphs_from_docx[21].runs[2].text = conditions_paiement

    # Gestion des tables :
    tables = doc.tables

    # Parc Client
    tables[0].rows[1].cells[0].text = condition_parc
    # Prix Vente
    tables[0].rows[1].cells[1].text = str(round(prix_vente, 2)) + ' €'

    # Montant HT :
    tables[1].rows[1].cells[0].text = str(round(prix_vente, 2)) + ' €'

    # Montant TTC
    tables[1].rows[1].cells[2].text = str(round(prix_vente * 1.2, 2)) + ' €'

    doc.save('appPCOE/impressions/devis/devis_finalise.docx')
