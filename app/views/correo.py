from django.shortcuts import redirect, render 
from django.urls import path 
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from facturacion_backend import settings
from django.views.decorators.csrf import *
from django.http import HttpResponse

@csrf_exempt
def send_mail(mail,nombre,razonsocial):

    context = {'mail':mail,'nombre':nombre,'razonsocial':razonsocial}
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
        razonsocial = request.POST.get('razonsocial')
        send_mail(mail,nombre,razonsocial)
     return redirect("http://localhost:4200/env-informacion")
    
urlpatterns = [
    path('registro/',registro)
]

