from django.shortcuts import render, HttpResponse
from datetime import datetime
import random

from HISKPScreen.data_services.database_connections import get_conn_and_cur
from HISKPScreen.indico_service import get_week_plan, get_indico_screengrab
__CONNECTIONS__ = {}
# __pages__ = ["SPS_page1.html","LHC_page1.html","HISKP_LOGO.html",get_week_plan().split("/")[-1],"particle_of_the_day.html","QRCode.html"]
__pages__ = ["SPS_page1.html","LHC_page1.html","HISKP_LOGO.html","particle_of_the_day.html","QRCode.html"]

__particle_time__ = None
__particle_of_the_day__ = None


class connection:
    def __init__(self,ip,timeout = 30):
        self.__ip = ip
        self.last_call = datetime.now()
        self.__calls = 0
        self.timeout = timeout

    def check(self):
        t = datetime.now()
        diff = (t-self.last_call).seconds
        if diff > self.timeout:
            return False
        return True    
        
    @property
    def calls(self):
        global __CALLS__, __pages__
        c = self.__calls
        self.__calls = (self.__calls + 1) % len(__pages__)
        self.last_call = datetime.now()
        return c


def update_connections():
    global __CONNECTIONS__
    timeouted_ips = []
    for ip,conn in __CONNECTIONS__.items():
        print("%s is %s"%(ip,{True:"active",False:"inactive"}[conn.check()]))
        if not conn.check():
            timeouted_ips.append(ip)
    for ip in timeouted_ips:
        del __CONNECTIONS__[ip]
    

def get_connection(adress):
    global __CONNECTIONS__
    update_connections()
    if __CONNECTIONS__.get(adress,None) is None:
        __CONNECTIONS__[adress] = connection(adress)
    return __CONNECTIONS__[adress]


def SPS(request):
    return render(request,"SPS_page1.html")

def read_html(html_file):
    with open(html_file,"r") as f:
        data = f.read() 
    return data

def rotation(request):
    global __pages__
    adress = request.META.get("REMOTE_ADDR")
    conn = get_connection(adress)
    f = __pages__[conn.calls]
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