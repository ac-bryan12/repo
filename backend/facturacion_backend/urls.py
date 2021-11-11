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
from correo.views import RegisterView
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls.static import static
from django.conf import settings
from usuario.views import LoginView,LogoutView, PasswordResetTokenView, PasswordResetView,UserPermissionView
from empresa.views import CreateView
from .views import front_end

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
    path('auth/login/',LoginView.as_view()),
    path('auth/logout/',LogoutView.as_view()),
    path('auth/register/',RegisterView.as_view()),
    path('auth/create/',CreateView.as_view()),
    path('auth/userPermissions/',UserPermissionView.as_view()),
    path('auth/reset_password_token/<str:email>',PasswordResetTokenView.as_view()),
    path('auth/reset_password_verification/<str:token>',PasswordResetView.as_view()),
    path('auth/reset_password/',PasswordResetView.as_view()),
    path('',front_end),
    path('home/',front_end),
    path('login/',front_end),
    path('create-cuenta/',front_end),
    path('registro/',front_end),
    path('planes/',front_end),
    path('confirmacion/',front_end),
    path('env-informacion/',front_end),
    path('empresas/',front_end),
    path('empresasTemp/',front_end),
    path('creacion-exitosa/',front_end),
    path('grupos-permisos/',front_end),



    # path('',include('app.views.hola'),name="hola"),
    # path('api/',include('app.views.accounts.login')),
    # path('api/',include('app.views.accounts.createEmpresa')),
    # # path('login/',include('app.views.accounts.login')),
    # path('', include('app.views.correo')),
    # path('', include('app.serializers.serializers')),
    # path('portal/',include('app.views.accounts.userAccount')),
    # path('api/', include('app.views.accounts.profile')),
    # path('api/',include('app.views.accounts.users')),
    # path('api/',include('app.views.empresaTemp')),
    # path('api/',include('app.views.groups')),
    

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
