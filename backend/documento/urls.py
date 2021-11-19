from django.urls import path,include,re_path
from .views import  DocumentosViewSet, ListaDocumentosViewSet, planViewSet,empresaViewSet,listEmpresaViewSet,EmpresaTempViewSet,listEmpresaTempViewSet

urlpatterns = [
    path('documentos/guardar-documentos/',DocumentosViewSet.as_view()),
    path('documentos/descargar-documento/<int:pk>/',DocumentosViewSet.as_view()),
    path('documentos/lista-documentos-empresa/',ListaDocumentosViewSet.as_view())
]