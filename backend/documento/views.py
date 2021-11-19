import io
from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import parsers, serializers, permissions, generics, status, renderers

from api.views import PaginationAPIView
from .models import Documentos
from rest_framework.authentication import BaseAuthentication, SessionAuthentication, TokenAuthentication
from .serializers import DocumentosSerializer, FacturaSerializer, InfoTributariaSerializer
import base64

#Vistas para los archivos : Sirve para subir y descargar 
class DocumentosViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class =  DocumentosSerializer

    def get_object(self, pk):
        try:
            return Documentos.objects.get(pk=pk)
        except Documentos.DoesNotExist:
            raise ValidationError({'error':'No hay un archivo por para descargar'},status= status.HTTP_204_NO_CONTENT)

    def get(self,request,pk):
        if 'Authorization' in request.headers.keys():
            archivo = self.get_object(pk=pk)
            serializer = self.serializer_class(archivo)
            if serializer:
                return Response(serializer.data)
            else:
                return Response({'error':"Ocurrió un error"},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':"No se ha encontrado su pagina"},status = status.HTTP_401_UNAUTHORIZED)

    def post(self,request):
        if 'Authorization' in request.headers.keys():
            archivo = request.data["file"]
            if archivo != "":
                if request.data["content_type"]=="text/xml":
                    nombre = Documentos.objects.filter(nombreDoc = request.data["nombreDoc"])
                    if not nombre.exists(): # Aqui se cambia el campo
                        read = archivo.file.read()
                        file = io.BytesIO(read)
                        archivo = Documentos.objects.create(_file = base64.encodebytes(file.getvalue()), content_type = request.data["content_type"],nombreDoc = request.data["nombreDoc"],tipoCreacion=request.data["tipoCreacion"])
                        if archivo:
                            return Response({'msg':"Documento guardado",'type':1},status=status.HTTP_201_CREATED)
                        else:
                            return Response({'error':'Ha ocurrido un error al crear el documento','class':'error'},status=status.HTTP_400_BAD_REQUEST)  
                    else:
                        return Response({'error':'El documento ya existe en el sistema '+request.data["nombreDoc"],'class':'existe'},status=status.HTTP_400_BAD_REQUEST)
                return Response({'error':'El tipo de archivo no es compatible','class':'error'},status = status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'error':'No se ha subido archivo','class':'error'},status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':"No se ha encontrado su pagina"},status = status.HTTP_401_UNAUTHORIZED)
        

#Vista lista de archivos : brinda una lista de archivos 
class ListaDocumentosViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class =  DocumentosSerializer

    def get(self,request):
        if 'Authorization' in request.headers.keys():
            if request.user.has_perm("empresa.view_documentos"): 
                serializer = DocumentosSerializer(Documentos.objects.all(), many=True)
                return Response(serializer.data)
            else:
                return Response({'error':'Acceso denegado'},status = status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error':'No se ha encontrado su página'},status=status.HTTP_401_UNAUTHORIZED)




class RecibirDocumentoViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class =  FacturaSerializer


    def validacionInfoFacturaGeneral(self,dictionary):
        if not dictionary =="":
            tipoId = dictionary["tipoIdentificacionComprador"]
            totalSinImpuestos = dictionary["totalSinImpuestos"]
            totalDescuento = dictionary["totalDescuento"]
            if not tipoId:
                return Response({'error':'Falta el campo de tipo identifiacion, por favor coloquelo dentro del esqueema a enviar'},status=status.HTTP_406_NOT_ACCEPTABLE)
            if not tipoId=="04" or not tipoId=="05" or not tipoId=="06" or not tipoId=="07" or not tipoId=="08":
                return Response({'error':'El campo del tipo de identificacion no es correcto, por favor verifíquelo'},status=status.HTTP_406_NOT_ACCEPTABLE)    
            if not totalSinImpuestos:
                return Response({'error':'Falta el campo de totalSinImpuestos, por favor coloquelo dentro del esquema a enviar'},status=status.HTTP_406_NOT_ACCEPTABLE)
            if totalSinImpuestos:
                try:
                    numero = float(totalSinImpuestos)
                    if len(str(numero))>14:
                        return Response({'error':'El campo ingresdo en el totalSinImpuesto supera la cantidad admitida de 14 digitos por el sistema'},status= status.HTTP_406_NOT_ACCEPTABLE)
                except:
                    raise ValidationError({'error':'El campo ingresado en el totalSinImpuestos es erroneo por favor ingresar un dato valido'},status=status.HTTP_406_NOT_ACCEPTABLE)
            if not totalDescuento:
                return Response({'error':'Falta el campo de totalDescuento, por favor coloquelo dentro del esuqema a enviar'},status=status.HTTP_406_NOT_ACCEPTABLE)
            if totalDescuento:
                try:
                    numero = float(totalDescuento)
                    if len(str(numero))>14:
                        return Response({'error':'EL campo ingreaso en el totalDescuento supera la cantidad admitida de 14 digitos por el sistema'},status= status.HTTP_406_NOT_ACCEPTABLE)
                except:
                    raise ValidationError({'error':'El campo ingresado en el totalDescuento es erroneo por favor ingresar un dato valido'},status=status.HTTP_406_NOT_ACCEPTABLE)
            return True

    def post(self,request):
        if request.user.has_perm("documento.view_permiso"):  ## permiso espeficio para emitir
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid(raise_exception=True):
                datos = serializer.validated_data #datos para trabajar
                return Response({'msg':'Documento permitido en el sistema'},status=status.status.HTTP_202_ACCEPTED)
        else:
            return Response({'error':'No se ha encontrado su página'},status=status.HTTP_401_UNAUTHORIZED)
        
class ListaDocumentosPaginados(PaginationAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request,name):
        if request.user.has_perm("empresa.view_documentos"):
            # Buscar por empresa
            query = Documentos.objects.filter(nombreDoc__icontains=name).order_by("-id")
            page = self.paginate_queryset(query)
            if page is not None:
                serializer = self.get_paginated_response(DocumentosSerializer(page,many=True).data)
                return Response(serializer.data)
            
            return Response({"error":"Ocurrió un error con la consulta."},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error':'Acceso denegado'},status=status.HTTP_403_FORBIDDEN)
