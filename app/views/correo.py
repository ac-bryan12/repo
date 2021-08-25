from app.models.empresa import Empresa
from app.models.profile import Profile
from django.contrib.auth.models import User
from app.models.empresaTemp import EmpresaTemp
from facturacion_backend.settings import EMAIL_HOST_USER
from django.shortcuts import redirect 
from django.urls import path 
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import *
from rest_framework.authtoken.models import Token

@csrf_exempt
def send_mail(mail, razonsocial,token):
    context = {'mail':mail,'razonSocial':razonsocial,'token':token}
    template  = get_template('envioCorreo.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Correo de confirmacion de su registro',
        'FACTURACION ELECTRÓNICA',
        EMAIL_HOST_USER,
        [mail], 
    )
    email.attach_alternative(content,'text/html')
    print("Correo enviado ")
    print(mail)
    email.send()

@csrf_exempt
def send_mail_admin(razonsocial,telefono,mail):

    context ={'mail':mail,'nombre':razonsocial,'telefono':telefono,}
    template =get_template('envioCorreoAdmin.html')
    content =template.render(context)
    email = EmailMultiAlternatives( 
        'Correo de confirmacion de registro',
        'Facturación eléctronica',
        EMAIL_HOST_USER,
        [EMAIL_HOST_USER]
    )
    empresa:EmpresaTemp = EmpresaTemp.objects.create(razonSocial=razonsocial,direccion="",telefono=telefono,correo=mail)
    # crearToken(empresa)

    email.attach_alternative(content,'text/html')
    email.send()

@csrf_exempt
def registro(request):
     if request.method == 'POST':
        mail = request.POST.get('email')
        razonsocial = request.POST.get('razonsocial')
        telefono = request.POST.get('telefono')
        send_mail_admin(razonsocial,telefono,mail)
     return redirect("http://localhost:4200/env-informacion")
    
# @csrf_exempt
# def crearToken(empresa:EmpresaTemp):
#     print('entra... crear token')
#     user:User = User()
#     user.first_name = empresa.razonSocial
#     user.email = empresa.correo
#     user.save()

#     profile:Profile = user.profile
#     profile.telefono = empresa.id
#     token = Token.objects.get_or_create(user=user)
#     print('salir... crear token')


urlpatterns = [
    path('registro/',registro)
]

