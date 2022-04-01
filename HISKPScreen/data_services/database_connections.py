import psycopg2 as pg


def get_conn_and_cur(database="main_db"):
    query = "dbname='%s' user='postgres' host='db' password='postgres'"%database
    # print(query)
    conn = pg.connect(query)

    return  conn, conn.cursor()

