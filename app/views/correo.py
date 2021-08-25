from app.models.empresaTemp import EmpresaTemp
from facturacion_backend.settings import EMAIL_HOST_USER
from django.shortcuts import redirect 
from django.urls import path 
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import *

@csrf_exempt
def send_mail(mail, razonsocial):  
    context = {'mail':mail,'razonSocial':razonsocial}
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
    context ={'mail':mail,'nombre':razonsocial,'telefono':telefono}
    template =get_template('envioCorreoAdmin.html')
    content =template.render(context)
    email = EmailMultiAlternatives( 
        'Correo de confirmacion de registro',
        'Facturación eléctronica',
        EMAIL_HOST_USER,
        [EMAIL_HOST_USER]
    )
    EmpresaTemp.objects.create(razonSocial=razonsocial,direccion="",telefono=telefono,correo=mail)
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
    
urlpatterns = [
    path('registro/',registro)
]

