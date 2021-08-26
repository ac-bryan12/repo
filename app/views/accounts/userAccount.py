from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.urls import path


@csrf_exempt
def perfil(request):
    return render(request,'dashboard.html')


urlpatterns = [
    path('perfil/',perfil,name='perfil')
]