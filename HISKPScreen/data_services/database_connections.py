import psycopg2 as pg
import psycopg2.extras

def get_conn_and_cur(database="main_db"):
    query = "dbname='%s' user='postgres' host='db' password='postgres'"%database
    # print(query)
    conn = pg.connect(query)

    return  conn, conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

