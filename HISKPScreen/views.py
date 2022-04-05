from django.shortcuts import render, HttpResponse
from datetime import datetime
import random

from HISKPScreen.data_services.database_connections import get_conn_and_cur
from HISKPScreen.indico_service import get_week_plan, get_indico_screengrab
__CALLS__ = 0
__pages__ = ["SPS_page1.html","LHC_page1.html","HISKP_LOGO.html",get_week_plan().split("/")[-1]]
__particle_time__ = None
__particle_of_the_day__ = None

def SPS(request):
    return render(request,"SPS_page1.html")

def read_html(html_file):
    with open(html_file,"r") as f:
        data = f.read() 
    return data

def rotation(request):
    global __CALLS__, __pages__
    
    f = __pages__[__CALLS__]
    __CALLS__ = (__CALLS__ + 1) % len(__pages__)
    pod = get_pod()
    get_week_plan()
    get_indico_screengrab()
    return render(request,f,{'location':pod['data_path'].split("/static")[-1]}) 

def check_and_update_time():
    global __particle_time__
    if __particle_time__ is None:
        __particle_time__ = datetime.now()
        return True
    if datetime.today().date() > __particle_time__.date():
        __particle_time__ = datetime.now()
        return True
    return False  

def update_particle_of_the_day():
    global __particle_of_the_day__
    if check_and_update_time():
        conn,cur = get_conn_and_cur("particle_db")
        cur.execute("""SELECT * FROM public.particles""")
        particles = list(cur.fetchall())
        __particle_of_the_day__ = random.choice(particles)

def get_pod():
    update_particle_of_the_day()
    print(__particle_of_the_day__['data_path'])
    return __particle_of_the_day__


def particle_of_the_day(request):
    global __particle_of_the_day__
    update_particle_of_the_day()
    print(__particle_of_the_day__['data_path'])
    return render(request,"particle_of_the_day.html",{'location':__particle_of_the_day__['data_path'].split("/static")[-1]})

def main(request):
    return render(request,"main.html")