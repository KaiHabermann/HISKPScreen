from datetime import datetime
import os
import time
from data_services.database_connections import get_conn_and_cur


__data_folder__ = "/code/static/particle_images/"

def update_particles():
    conn,cur = get_conn_and_cur("particle_db")
    import glob, os
    os.chdir("static/particle_images/")
    cur.execute("TRUNCATE public.particles;")
    for file in glob.glob("*.png"):
        print(file)
        cur.execute("""INSERT INTO public.particles (name,link, data_path,date) values (%s,%s,%s,%s) ON CONFLICT DO NOTHING""",("","","particle_images/"+file,datetime.now()))
    conn.commit()
    print("Update done!")
    
def update_loop():
    t = 24*3600 # a day
    while True:
        try:
            create_folders()
            update_particles()
            time.sleep(t)
        except Exception as e:
            print(e)
            time.sleep(t)

def get_current_particles():
    conn,cur = get_conn_and_cur("particle_db")
    cur.execute("""SELECT * from public.particles""")
    data = cur.fetchall()
    for d in data:
        print(d)
    return data

def create_folders():
    if not os.path.exists(__data_folder__):
        os.makedirs(__data_folder__)

def startup():
    conn,cur = get_conn_and_cur("particle_db")
    query = """
        CREATE TABLE IF NOT EXISTS particle_db.public.particles (
        name text,
        link text , 
        data_path text,
        date TIMESTAMP
        );
    """
    cur.execute(query)
    conn.commit()

if __name__=="__main__":
    # particle_database_from_pdg_live()
    startup()
    update_loop()
