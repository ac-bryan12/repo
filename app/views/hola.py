from django.conf import urls
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from app.models.plan import Plan
from app.models.roles import Rol

@csrf_exempt
def saludo(request):
    return render(request,'hola.html')

def population_Planes(request):
        list = [
                ["Económico",20.0,"Ideal para baja cantidad de documentos","20 Comprobantes electrónicos",5,"Soporte ilimitado","Uso de firma electronica","1 usuario","10 clientes"],
                ["Avanzado",35.0,"Ideal para empresas pequeñas","35 Comprobantes electrónicos",7,"Soporte ilimitado","Uso de firma electronica","1 usuarios","20 clientes"],
                ["Profesional",60.0,"Ideal para empresas medianas","65 Comprobantes electrónicos",10,"Soporte ilimitado","Uso de firma electronica","2 usuario","40clientes"],
                ["Business",95.0,"Ideal para grandes empresas","100 Comprobantes electrónicos",15,"Soporte ilimitado","Uso de firma electronica","3 usuario","60 clientes"]
            ]
            
        for i in range(len(list)):
            Plan.objects.create(nombre=list[i][0],precio=list[i][1],description=list[i][2],documentos=list[i][3],reportes=list[i][4],soporte=list[i][5],firma=list[i][6],usuarios=list[i][7],clientes=list[i][8])
        return render(request,"hola.html")


def population_Roles(request):
        list = [
            ["1","Admin"],["2","Analista"],["3","Cliente"]
        ]
        for i in range(len(list)):
            Rol.objects.create(codigo=list[i][0],nombre=list[i][1])
        return HttpResponse("creacion de roles")

urlpatterns = [
    path('',population_Planes),
    path('Roles/',population_Roles)
]