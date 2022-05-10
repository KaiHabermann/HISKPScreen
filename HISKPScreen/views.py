from django.shortcuts import render, HttpResponse
from datetime import datetime
import random
import os

from HISKPScreen.data_services.database_connections import get_conn_and_cur
from HISKPScreen.indico_service import get_week_plan, get_indico_screengrab
__CONNECTIONS__ = {}
# __pages__ = ["SPS_page1.html","LHC_page1.html","HISKP_LOGO.html",get_week_plan().split("/")[-1],"particle_of_the_day.html","QRCode.html"]
__pages__ = ["SPS_page1.html","LHC_page1.html","HISKP_LOGO.html","particle_of_the_day.html","QRCode.html"]
__rotation_time__ = 16000

def ping(url):
    response = os.system("ping -c 1 " + url + " > /dev/null")
    return bool(response == 0)

class page:
    def __init__(self,location,name="",dependencies = None):
        self.location = location # where is the file? just the name is enough if it is in static
        self.name = name # what should this site be called? 
        self.dependecies = dependencies  # what links are loaded on the site? We ping them before display to avoid errors
        # please allso let the site call rotation, if any load fails or display a proper backup image/site

    def check(self):
        if self.dependecies is None:
            return True
        for dependency in self.dependecies:
            try:
                if not ping(dependency):
                    print("Dependency %s for page %s at location %s was not reachable. Skipping!"%(dependency,self.name,self.location))
                    return False
                return True
            except:
                print("Dependency %s for page %s at location %s was not reachable. Skipping!"%(dependency,self.name,self.location))
                return False

__pages__ = [page("SPS_page1.html","SPS page 1",["vistar-capture.web.cern.ch"]),
            page("LHC_page1.html","LHC page 1",["vistar-capture.web.cern.ch"]),
            page("HISKP_LOGO.html","HISKP Logo"),
            page("particle_of_the_day.html","Particle of the Day"),
            page("QRCode.html","Group Neubert")]


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
    while not f.check():
        f = __pages__[conn.calls]
    f = f.location
    pod = get_pod()
    get_week_plan()
    get_indico_screengrab()
    return render(request,f,{'location':pod['data_path'].split("/static")[-1]}) 

def get_pod_from_db():
    try:
        conn,cur = get_conn_and_cur("particle_db")
        cur.execute("SELECT * FROM public.pod")
        pod = cur.fetchone()
        return pod
    except:
        return None

def save_pod(pod_dict):
    conn,cur = get_conn_and_cur("particle_db")
    cur.execute("CREATE TABLE IF NOT EXISTS public.pod (name text, link text, data_path text, date TIMESTAMP);")
    cur.execute("TRUNCATE TABLE public.pod")
    dtc = pod_dict.copy()
    dtc["date"] = datetime.now()
    cur.execute("INSERT INTO public.pod(name, link, data_path, date) values(%(name)s,%(link)s,%(data_path)s,%(date)s)",dtc)
    conn.commit()
    conn.close()

def check_and_update_time():
    pod = get_pod_from_db()
    if pod is None:
        return True
    t = pod["date"]
    if datetime.today().date() > t.date():
        return True
    return False 

def update_particle_of_the_day():
    if check_and_update_time():
        conn,cur = get_conn_and_cur("particle_db")
        cur.execute("""SELECT * FROM public.particles""")
        particles = list(cur.fetchall())
        pod = random.choice(particles)
        save_pod(pod)

def get_pod():
    update_particle_of_the_day()
    return get_pod_from_db()


def particle_of_the_day(request):

    update_particle_of_the_day()
    return render(request,"particle_of_the_day.html",{'location':get_pod()['data_path'].split("/static")[-1]})

def main(request):
    return render(request,"main.html",{'rotation_time':__rotation_time__})