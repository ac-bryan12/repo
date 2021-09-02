from app.serializers.serializer_empresa import EmpresaSerializer
from django.http.response import HttpResponse
from rest_framework import serializers
from app.models.empresa import Empresa
from app.views.forms import EmpresaForms
from django.urls import path
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect


def listarEmpresa(request):
    empresas = Empresa.objects.all()
    return render(request,"listaEmpresas.html",{"empresas":empresas})
        

def crearEmpresa(request):
    if request.method == 'POST':
        empresa_form = EmpresaForms(data= request.POST)
        if empresa_form.is_valid():
            empresa_form.save()
            return redirect("http://localhost:4200/home")
    else:
        empresa_form = EmpresaForms()
    return render(request,"crearEmpresa.html",{'empresa_form':empresa_form})


def editarEmpresa(request,ruc):
    if request.method == "POST":
        empresa= Empresa.objects.get(ruc = ruc)
        empresa_form = EmpresaForms(request.POST,instance=empresa)
        if empresa_form.is_valid():
            empresa_form.save()
        redirect("http://localhost:4200/home")
    return render(request,"crearEmpresa.html",{"empresa_form":empresa_form})
    
# def eliminarEmpresa(request, ruc):
#      empresa = Empresa.objects.get(ruc=ruc)
#      empresa.delete()
#      return redirect
#      if request.method == "POST":


urlpatterns = [
    path('crearEmpresa/', crearEmpresa),
    path('editarEmpresa/<int:ruc>',editarEmpresa),
    path('listaEmpresas',listarEmpresa)
]