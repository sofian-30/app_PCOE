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
