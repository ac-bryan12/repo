from django.conf import urls
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.urls import path

@csrf_exempt
def saludo(request):
    return render(request,'hola.html')

urlpatterns = [
    path('',saludo,name="saludo")
]