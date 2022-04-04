from datetime import datetime
from bs4 import BeautifulSoup
import requests
import urllib
import time
from data_services.database_connections import get_conn_and_cur
from spellchecker import SpellChecker
from pdf2image import convert_from_bytes


__exclusions__ = ["Searches","mixture","Mixing","Decay","Number","Properties","States","and"]
__data_folder__ = "/code/static/particle_images/"

def has_normal_text(string):
    try:
        return False
        s = SpellChecker()
        word_list = [word.lower() for word in s.split_words(string)]
        unknowns = s.unknown(word_list)
        unknowns = {u.lower() for u in unknowns if len(u) > 1}
        unknowns.union( {word for word in ["tau","muon","neutrino","electron","boson","quark","lepton"] if word in word_list} )
        print(word_list,unknowns)
        return len(set(word_list)) > len(unknowns)
    except Exception as e:
        print(e)
    return False

def wanted(f):
    try:
        return not any(e.lower() in f.lower() for e in __exclusions__) and not has_normal_text(f)
    except Exception as e:
        print(e,f)
    return False

def wanted_category(string):
    try:
        return not any(e.lower() in string.lower() for e in __exclusions__)
    except Exception as e:
        print(e,string)
    return False

def download_file(download_url, filename):
    response = urllib. request. urlopen(download_url).read()
    pages = convert_from_bytes(response,single_file=True)
    page = pages[0]
    path = filename.replace("pdf","jpeg")
    page.save(path , 'JPEG')
    return path

def update_needed(particles_new:dict):
    try:
        conn,cur = get_conn_and_cur("particle_db")
        cur.execute("""SELECT * FROM public.particles""")
        particles = list(cur.fetchall())
        conn.close()
        names = [p['name'] for p in particles]
        return any(p not in names for p in particles_new.keys()) or any((p["date"] - datetime.now()).total_seconds() > (24 * 14 * 3600) for p in particles)
    except:
        return True

def update_particles(    main_page = "https://pdg.lbl.gov/2021/"):
    link = main_page + "listings/contents_listings.html"
    url = requests.get(link)
    htmltext = url.text
    DOMdocument = BeautifulSoup(htmltext, 'html.parser')
    # print(DOMdocument)
    Ptypes = DOMdocument.find_all(class_="panel panel-default")
    # print(Ptypes)
    particles = {}

    for Ptype in Ptypes:
        title = Ptype.find(class_="panel-section-title")
        if wanted_category(title.text):
            print("Scanning" ,title.text)
            particles.update({particle.find(class_="iframe").text: 
            main_page + particle.find("a",href=True)["href"].split("file=../")[-1] 
            for particle in Ptype.find_all(class_="list-group-item") 
            if wanted(particle.find(class_="iframe").text)})

    if update_needed(particles):
        conn, cur = get_conn_and_cur("particle_db")
        query = """DROP TABLE IF EXISTS public.particles"""
        cur.execute(query)
        query = """CREATE TABLE IF NOT EXISTS public.particles (name text, link text, data_path text, date TIMESTAMP);"""
        cur.execute(query)
        for name,link in particles.items():
            print(name)
        for name,link in particles.items():
            path = __data_folder__ + link.split("/")[-1]
            new_path = download_file(link,path)
            cur.execute("""INSERT INTO public.particles (name,link, data_path,date) values (%s,%s,%s,%s)""",(name,link,new_path,datetime.now()))
            print(name,new_path)
        conn.commit()
    print("Particles up to date")        

def update_loop():
    t = 24*3600 # a day
    while True:
        try:
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

if __name__=="__main__":
    update_loop()
