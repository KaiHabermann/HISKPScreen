from HISKPScreen.data_services.database_connections import get_conn_and_cur

def database_setup():
    return
    conn, cur = get_conn_and_cur("")
    conn.autocommit = True # no transaction
    try:
        print("Sucess")
    except:
        print("Databse already exists!")
    conn.close()