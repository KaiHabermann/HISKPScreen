from django.shortcuts import render, HttpResponse

__CALLS__ = 0
__pages__ = ["SPS_page1.html","LHC_page1.html"]

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
    return render(request,f) 

def main(request):
    return render(request,"main.html")