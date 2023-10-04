import datetime

from config import logger
from db import execute_sql_request, connect_to_db, disconnect_from_db
from sqlalchemy.engine import Connection


def process_monitoring(conn: Connection, table_name: str, success_flag: int = 1, nb_lines: int = 0,
                       error_message: str = None) -> None:
    if error_message:
        error_message_for_db = error_message.replace("'", "''")
        execute_sql_request(f"INSERT INTO monitoring "
                            f"VALUES (NOW(), '{table_name}', 'ERROR', '{error_message_for_db}', 0)",
                            conn=conn)
        logger.error(f"An error occur while loading table {table_name} : {error_message}")
    elif success_flag:
        execute_sql_request(f"INSERT INTO monitoring VALUES (NOW(), '{table_name}', 'SUCCESS', NULL, {nb_lines})",
                            conn=conn)
        logger.debug(f"{nb_lines} lines loaded into table {table_name}")
    else:
        execute_sql_request(f"INSERT INTO monitoring VALUES (NOW(), '{table_name}', 'ERROR', "
                            f"'insert_df_to_table failed', 0)",
                            conn=conn)


def update_app_table(code_projet_boond: int,
                     prix_achat_n1: float,
                     prix_vente_n1: float,
                     marge_n1: float,
                     parc_licence: str,
                     check_infos: bool,
                     validation_erronee: bool,
                     envoi_devis: bool,
                     accord_principe: bool,
                     signature_client: bool,
                     achat_editeur: bool,
                     traitement_comptable: bool,
                     paiement_sap: bool) -> None:
    if not prix_vente_n1:
        prix_vente_n1 = 'NULL'
    if not prix_achat_n1:
        prix_achat_n1 = 'NULL'
    if not marge_n1:
        marge_n1 = 'NULL'
    update_request = f"""UPDATE app_table
                     SET prix_achat_n1 = {prix_achat_n1},
                         prix_vente_n1 = {prix_vente_n1},
                         marge_n1 = {marge_n1},
                         parc_licence = '{parc_licence}',
                         check_infos = {check_infos},
                         validation_erronee = {validation_erronee},
                         envoi_devis = {envoi_devis},
                         accord_principe = {accord_principe},
                         signature_client = {signature_client},
                         achat_editeur = {achat_editeur},
                         traitement_comptable = {traitement_comptable},
                         paiement_sap = {paiement_sap}
                     WHERE code_projet_boond = {code_projet_boond}"""
    conn = connect_to_db()
    execute_sql_request(update_request, conn=conn)
    disconnect_from_db(conn)


def update_app_table_resiliation(code_projet_boond: str) -> None:
    resiliation_request = f"""UPDATE app_table
                     SET resilie = True
                     WHERE code_projet_boond = {code_projet_boond}"""
    conn = connect_to_db()
    execute_sql_request(resiliation_request, conn=conn)
    disconnect_from_db(conn)
