import datetime

from config import logger
from db import execute_sql_request
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


def update_boond_table(code_projet_boond: int,
                       agence: str,
                       client: str,
                       num_ref_sap: str,
                       date_anniversaire: datetime.date,
                       prix_achat_n: float,
                       prix_vente_n: float,
                       marge_n: float,
                       type_support_sap: str,
                       type_contrat: str,
                       parc_techno: str,
                       resp_commercial: str,
                       adresse: str,
                       ville: str,
                       cope_postal: str) -> None:
    update_request = f"""UPDATE boond_table
                     SET agence = '{agence}',
                         client = '{client}',
                         num_ref_sap = '{num_ref_sap}',
                         date_anniversaire = '{date_anniversaire}',
                         prix_achat_n = {prix_achat_n},
                         prix_vente_n = {prix_vente_n},
                         marge_n = {marge_n},
                         type_support_sap = '{type_support_sap}',
                         type_contrat = '{type_contrat}',
                         parc_techno = '{parc_techno}',
                         resp_commercial = '{resp_commercial}',
                         adresse = '{adresse}',
                         ville = '{ville}',
                         cope_postal = '{cope_postal}',    
                     WHERE code_projet_boond = {code_projet_boond}"""

    execute_sql_request(update_request)
