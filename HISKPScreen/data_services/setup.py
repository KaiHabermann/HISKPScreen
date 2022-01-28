from HISKPScreen.data_services.database_connections import get_conn_and_cur

def database_setup():
    conn, cur = get_conn_and_cur("")
    conn.autocommit = True # no transaction
    try:
        cur.execute("CREATE DATABASE main_db;")
        print("Sucess")
    except:
        print("Databse already exists!")
    conn.close()