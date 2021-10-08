from django.shortcuts import render

def front_end(request):
    return render(request,"index.html")