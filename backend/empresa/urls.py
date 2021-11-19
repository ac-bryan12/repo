from django.urls import path,include,re_path
from .views import   planViewSet,empresaViewSet,listEmpresaViewSet,EmpresaTempViewSet,listEmpresaTempViewSet

urlpatterns = [
    path('planes.format.json/',planViewSet.as_view()),
    path('buscar-empresa/',empresaViewSet.as_view(), name = "Empresa"),
    path('lista-de-empresas/', listEmpresaViewSet.as_view()),
    path('empresaTemps/buscar-empresaTemp/', EmpresaTempViewSet.as_view(), name = " EmpresaTemp"),
    path('empresaTemps/lista-de-empresaTemps/', listEmpresaTempViewSet.as_view()),
]
