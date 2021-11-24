from django.urls import path,include,re_path

urlpatterns = [
    path('user/',include('usuario.urls')),
    path('empresa/',include('empresa.urls')),
    path('correo/',include('correo.urls')),
    path('documentos/',include('documento.urls'))
]