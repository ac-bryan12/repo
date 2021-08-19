from django.shortcuts import render 
from django.urls import path 
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from facturacion_backend import settings
from django.views.decorators.csrf import *
from django.http import HttpResponse

@csrf_exempt
def send_mail(mail,nombre,apellido):

    context = {'mail':mail,'nombre':nombre,'apellido':apellido}
    template  = get_template('envioCorreo.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Correo de confirmacion de su registro',
        'FACTURACION ELECTRÓNICA',
        settings.EMAIL_HOST_USER,
        [mail], 
    )
    email.attach_alternative(content,'text/html')
    print("Correo enviado ")
    print(mail)
    email.send()

@csrf_exempt
def registro(request):
     if request.method == 'POST':

        mail = request.POST.get('email')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        send_mail(mail,nombre,apellido)
     return HttpResponse("Usuario enviado")
    
urlpatterns = [
    path('registro/',registro)
]

