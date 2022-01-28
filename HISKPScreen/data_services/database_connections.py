import psycopg2 as pg


def get_conn_and_cur(database="main_db"):
    conn = pg.connect("dbname='%s' user='postgres' host='database' password='postgres'"%database)

    return  conn, conn.cursor()

