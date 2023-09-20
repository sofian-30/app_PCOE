from db import connect_to_db, disconnect_from_db, execute_sql_request

conn = connect_to_db()
res = execute_sql_request("SELECT * from monitoring")
print(res)
disconnect_from_db(conn)
