"""
This module provides functions for working with databases.

The module has functions for connecting to a database, disconnecting from a database, executing a SQL request, inserting
a pandas DataFrame into a database table, and loading a database table into a pandas DataFrame.
"""
from typing import Any, Literal, Optional

import pandas as pd
from config import DB_CONFIG, logger
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import OperationalError


# ================================================= DB UTILS FUNCTIONS =================================================
def connect_to_db(database: str = 'postgresql', host: str = DB_CONFIG['host'], port: int = DB_CONFIG['port'],
                  db_name: str = DB_CONFIG['db_name'], user: str = DB_CONFIG['user'],
                  password: str = DB_CONFIG['password']) -> Optional[Connection]:
    """
    Connect to a database.

    :param database: The type of database to connect to (oracle, postgresql, mysql, sqlserver or hana).
    :param host: The hostname or IP address of the database server.
    :param port: The port number of the database server.
    :param db_name: The name of the database to connect to.
    :param user: The username to use for authentication.
    :param password: The password to use for authentication.
    :return: A connection to the database, or None if the connection failed.
    """
    if database == 'oracle':
        dialect = 'oracle'
        driver = 'cx_oracle'
        connection_url = dialect + '+' + driver + '://' + user + ':' + password + '@' + host + ':' + str(port) + '/' + db_name
    elif database == 'postgresql':
        dialect = 'postgresql'
        driver = 'psycopg2'
        connection_url = dialect + '+' + driver + '://' + user + ':' + password + '@' + host + ':' + str(port) + '/' + db_name
    elif database == 'mysql':
        dialect = 'mysql'
        driver = 'pymysql'
        connection_url = dialect + '+' + driver + '://' + user + ':' + password + '@' + host + ':' + str(port) + '/' + db_name
    elif database == 'sqlserver':
        dialect = 'mssql'
        driver = 'pyodbc'
        connection_url = dialect + '+' + driver + '://' + user + ':' + password + '@' + host + ':' + str(port) + '/' + db_name + '?driver=SQL+SERVER'
    elif database == 'hana':
        dialect = 'hana'
        connection_url = dialect + '://' + user + ':' + password + '@' + host + ':' + str(port)
    else:
        logger.error(f"Unsupported database type: {database}")
        return None

    try:
        engine = create_engine(connection_url, isolation_level="AUTOCOMMIT")
        conn = engine.connect()
        if database == 'hana':
            execute_sql_request(f'SET SCHEMA {db_name}', conn=conn)
        logger.debug(f"Successfully connected to the database {connection_url}")
        return conn
    except OperationalError as err:
        logger.error(f"Failed to connect to the database {connection_url} : {err}")
        return None


def disconnect_from_db(conn: Connection) -> None:
    """
    Disconnect from a database.

    :param conn: The connection to the database to disconnect from.
    :return: None
    """
    try:
        conn.close()
        logger.debug("Successfully disconnected from the database")
    except AttributeError as err:
        logger.warning(f"Failed to disconnect from the database: {err}")


def execute_sql_request(request: str, return_rowcount: bool = False, conn: Connection = None) -> Optional[Any]:
    """
    Execute a SQL request.

    If the `conn` parameter is not provided, the function will create a new connection to the database using
    connect_to_db() function and close it after executing the request.

    :param request: The SQL request to execute.
    :param return_rowcount: Whether to return the number of rows affected by the request (optional). Default False
    :param conn: The connection to the database to use for the request (optional). Default None
    :return: The result of the request (a list of rows for SELECT requests, the number of rows affected for other
    requests if return_rowcount = True or None if return_rowcount = False, or None if the request failed).
    """
    if conn is None:
        conn = connect_to_db()
        need_disconnect = True
    else:
        need_disconnect = False

    if conn:
        try:
            result = conn.execute(text(request))
            logger.debug(f"Successfully executed the SQL request: {request}")
        except Exception as err:
            logger.error(f"Failed to execute the SQL request: {request}\n{err}")
            return None
        finally:
            if need_disconnect:
                disconnect_from_db(conn)
    else:
        logger.error(f"Failed to execute the request: {request}\nInvalidated connection")
        return None

    if request.lower().strip().startswith('select'):
        return result.fetchall()
    else:
        if return_rowcount:
            return result.rowcount
        else:
            return None


def sql_to_df(sql_request: str, conn: Connection = None) -> pd.DataFrame:
    """Execute a SQL SELECT request and return the result as a pandas DataFrame.

    If the `conn` parameter is not provided, the function will create a new connection to the database using
    connect_to_db() function and close it after loading the data from the table.

    :param sql_request: The SQL SELECT request to be executed.
    :param conn: The database connection object (optional). Default None.
    :return A pandas DataFrame containing the result of the SQL request. If an error occurs, the function returns None.
    """
    if conn is None:
        conn = connect_to_db()
        need_disconnect = True
    else:
        need_disconnect = False

    if conn:
        try:
            df = pd.read_sql(sql_request, conn)
            logger.debug(f"Data successfully loaded from request: {sql_request}")
            return df
        except Exception as err:
            logger.error(f"Failed to load data from request: {sql_request}\n{err}")
        finally:
            if need_disconnect:
                disconnect_from_db(conn)

    else:
        logger.error("Failed to load table: Invalidated connection")


def table_to_df(table_name: str, conn: Connection = None) -> pd.DataFrame:
    """
    Load the data from a database table into a Pandas DataFrame.

    If the `conn` parameter is not provided, the function will create a new connection to the database using
    connect_to_db() function and close it after loading the data from the table.

    :param table_name: The name of the table to load data from.
    :param conn: The connection to the database containing the table (optional). Default None.
    :return: The data from the table as a Pandas DataFrame.
    """

    if conn is None:
        conn = connect_to_db()
        need_disconnect = True
    else:
        need_disconnect = False

    if conn:
        try:
            df = pd.read_sql_table(table_name, conn)
            logger.info(f"Data successfully loaded from table {table_name}")
            return df
        except Exception as err:
            logger.error(f"Failed to load data from table {table_name}\n{err}")
        finally:
            if need_disconnect:
                disconnect_from_db(conn)

    else:
        logger.error("Failed to load table: Invalidated connection")


def insert_df_to_table(df: pd.DataFrame, table_name: str, if_exists: Literal["fail", "replace", "append"] = "append",
                       conn: Connection = None) -> bool:
    """
    Insert the data from a Pandas DataFrame into a database table.

    If the `conn` parameter is not provided, the function will create a new connection to the database using
    connect_to_db() function and close it after inserting the data into the table.

    :param df: The DataFrame containing the data to insert (pandas.DataFrame).
    :param table_name: The name of the table to insert data into.
    :param if_exists: What to do if the table already exists (optional). Default "append"
                      Possible values are "fail", "replace", and "append".
    :param conn: The connection to the database containing the table (optional). Default None.
    :return: A boolean indicating whether the insertion was successful (True) or not (False).
    """
    if conn is None:
        conn = connect_to_db()
        need_disconnect = True
    else:
        need_disconnect = False

    if conn:
        try:
            df.to_sql(table_name, con=conn, if_exists=if_exists, index=False)
            logger.info(f"Data successfully saved in table {table_name}")
            success_flag = True
        except Exception as err:
            logger.error(f"Failed to insert DataFrame to table {table_name}\n{err}")
            success_flag = False
        finally:
            if need_disconnect:
                disconnect_from_db(conn)

    else:
        logger.error(f"Failed to insert DataFrame to table {table_name}: Invalidated connection")
        return False

    return success_flag


def execute_many_sql_request(request_body: str, values: list, conn: Connection = None) -> bool:
    """
    Execute several request SQL request using executemany method.

    If the `db_conn` parameter is not provided, the function will create a new connection to the database using
    connect_to_db() function and close it after executing the request.

    :param request_body: The SQL request body to execute
    :param values: The list of values to use in the request
    :param conn: The connection to the database to use for the request (optional). Default None
    :return: True if the execution is successfully, False otherwise
    """
    if conn is None:
        conn = connect_to_db()
        need_disconnect = True
    else:
        need_disconnect = False

    if conn:
        try:
            cursor = conn.cursor()
            cursor.executemany(request_body, values)
            logger.debug(f"Successfully executed the SQL requests with body: {request_body}")
            return True
        except Exception as err:
            logger.error(f"Failed to execute the SQL request with body: {request_body}\n{err}")
            return False
        finally:
            if need_disconnect:
                disconnect_from_db(conn)
    else:
        logger.error(f"Failed to execute the requests with body: {request_body}\nInvalidated connection")
        return False
