from datetime import datetime
import os

from bs4 import BeautifulSoup
import requests
import urllib
import time
from data_services.database_connections import get_conn_and_cur
from spellchecker import SpellChecker
from pdf2image import convert_from_bytes


__exclusions__ = ["Searches","mixture","Mixing","Decay","Number","Properties","States","and"]
__data_folder__ = "/code/static/particle_images/"
__pdg_live__ = "https://pdglive.lbl.gov/Viewer.action"

def wanted(f):
    try:
        return not any(e.lower() in f.lower() for e in __exclusions__) 
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

def update_particles_pdg(main_page = "https://pdg.lbl.gov/2021/"):
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
