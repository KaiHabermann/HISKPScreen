from django.shortcuts import render, HttpResponse

__CALLS__ = 0

def SPS(request):
    return render(request,"SPS_page1.html")

def read_html(html_file):
    with open(html_file,"r") as f:
        data = f.read() 
    return data

def rotation(request):
    global __CALLS__
    pages = ["SPS_page1.html","LHC_page1.html"]
    f = pages[__CALLS__]
    __CALLS__ = (__CALLS__ + 1) % len(pages)
    return render(request,f) 

def main(request):
    return render(request,"main.html")