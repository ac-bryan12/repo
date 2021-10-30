from django.urls import path,include,re_path
from .views import  DocumentosViewSet, ListaDocumentosViewSet, planViewSet,empresaViewSet,listEmpresaViewSet,EmpresaTempViewSet,listEmpresaTempViewSet

urlpatterns = [
    path('planes.format.json/',planViewSet.as_view()),
    path('buscar-empresa/',empresaViewSet.as_view(), name = "Empresa"),
    path('lista-de-empresas/', listEmpresaViewSet.as_view()),
    path('empresaTemps/buscar-empresaTemp/', EmpresaTempViewSet.as_view(), name = " EmpresaTemp"),
    path('empresaTemps/lista-de-empresaTemps/', listEmpresaTempViewSet.as_view()),
    path('documentos/guardar-documentos/',DocumentosViewSet.as_view()),
    path('documentos/descargar-documento/<int:pk>/',DocumentosViewSet.as_view()),
    path('documentos/lista-documentos-empresa/',ListaDocumentosViewSet.as_view())
]
