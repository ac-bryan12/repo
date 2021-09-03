"""facturacion_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from facturacion_backend.settings import STATIC_URL
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.views.hola'),name="hola"),
    path('api/',include('app.views.accounts.login')),
    path('api/',include('app.views.accounts.createEmpresa')),
    # path('login/',include('app.views.accounts.login')),
    path('', include('app.views.correo')),
    path('', include('app.serializers.serializers')),
    path('portal/',include('app.views.accounts.userAccount')),
    path('api/', include('app.views.accounts.profile')),
    path('api/',include('app.views.accounts.users')),
    path('api/',include('app.views.empresaTemp')),
    path('api/',include('app.views.groups')),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
