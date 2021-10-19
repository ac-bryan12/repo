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
from django.views.generic.base import TemplateView
from correo.views import RegisterView
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls.static import static
from django.conf import settings
from usuario.views import LoginView,LogoutView, PasswordResetTokenView, PasswordResetView,UserPermissionView, isLogged
from empresa.views import CreateView
from .views import front_end

urlpatterns = [
    path('auth/admin/', admin.site.urls),
    path('api/',include('api.urls')),
    path('auth/login/',LoginView.as_view()),
    path('auth/logout/',LogoutView.as_view()),
    path('auth/register/',RegisterView.as_view()),
    path('auth/create/',CreateView.as_view()),
    path('auth/userPermissions/',UserPermissionView.as_view()),
    path('auth/reset_password_token/<str:email>',PasswordResetTokenView.as_view()),
    path('auth/reset_password_verification/<str:token>',PasswordResetView.as_view()),
    path('auth/reset_password/',PasswordResetView.as_view()),
    path('auth/isLogged/',isLogged.as_view()),
    re_path(r'^.*', TemplateView.as_view(template_name="index.html"), name="home")
    # path('',front_end),
    # path('home/',front_end),
    # path('login/',front_end),
    # path('create-cuenta/',front_end),
    # path('registro/',front_end),
    # path('planes/',front_end),
    # path('confirmacion/',front_end),
    # path('env-informacion/',front_end),
    # path('empresas/',front_end),
    # path('empresasTemp/',front_end),
    # path('creacion-exitosa/',front_end),
    # path('grupos-permisos/',front_end),
    # path('admin/',front_end),
    # path('view-company/',front_end),
    # path('cliente',front_end)

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)