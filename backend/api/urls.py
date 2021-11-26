from django.urls import path,include,re_path
from .views import XMLParserView

urlpatterns = [
    path('user/',include('usuario.urls')),
    path('empresa/',include('empresa.urls')),
    path('correo/',include('correo.urls')),
    path('documentos/',include('documento.urls')),
    path('pruebaXml/',XMLParserView.as_view())
]