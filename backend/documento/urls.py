from django.urls import path,include,re_path
from .views import  DocumentosViewSet, ListaDocumentosPaginados, ListaDocumentosViewSet

urlpatterns = [
    path('guardar-documentos/',DocumentosViewSet.as_view()),
    path('descargar-documento/<int:pk>/',DocumentosViewSet.as_view()),
    path('lista-documentos-empresa/',ListaDocumentosViewSet.as_view()),
    path('buscar_por_empresa/<str:name>',ListaDocumentosPaginados.as_view())
]