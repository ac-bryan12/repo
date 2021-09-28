from empresa.serializers import EmpresaTempSerializer
from facturacion_backend.settings import EMAIL_HOST_USER
from django.urls import path 
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import *
from rest_framework import parsers, renderers
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView

class RegisterView(APIView):
    # throttle_classes = ()
    permission_classes = [permissions.AllowAny]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class= EmpresaTempSerializer
    # @csrf_exempt
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

    # @csrf_exempt
    def send_mail_admin(self,empresa):

        context ={'mail':empresa.correo,'nombre':empresa.razonSocial,'telefono':empresa.telefono,}
        template =get_template('envioCorreoAdmin.html')
        content =template.render(context)
        email = EmailMultiAlternatives( 
            'Correo de confirmacion de registro',
            'Facturación eléctronica',
            EMAIL_HOST_USER,
            [EMAIL_HOST_USER]
        )
        # EmpresaTemp.objects.create(razonSocial=razonsocial,direccion="",telefono=telefono,correo=mail)
        # crearToken(empresa)

        email.attach_alternative(content,'text/html')
        email.send()

    # @csrf_exempt
    def post(self,request):
        # if request.method == 'POST':
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            print("Es valido")
            empresa = serializer.save()
            # mail = request.POST.get('email')
            # razonsocial = request.POST.get('razonsocial')
            # telefono = request.POST.get('telefono')
            self.send_mail_admin(empresa)
            return Response({"msg":"Creación de cuenta exitosa"})
            
        
    
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

