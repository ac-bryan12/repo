from django.shortcuts import render

def front_end(request,exception=None, *args, **argv):
    return render(request,"index.html")