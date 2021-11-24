from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  permissions, status
from .models import Documentos
from rest_framework.authentication import  TokenAuthentication
from .serializers import DocumentosSerializer, FacturaSerializer
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
                        archivo = Documentos.objects.create(_file = base64.encodebytes(file.getvalue()), content_type = request.data["content_type"],nombreDoc = request.data["nombreDoc"])
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


    def post(self,request):
        if request.user.has_perm("documento.view_permiso"):  ## permiso espeficio para emitir
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid(raise_exception=True):
                datos = serializer.validated_data #datos para trabajar
                return Response({'msg':'Documento permitido en el sistema'},status=status.status.HTTP_202_ACCEPTED)
        else:
            return Response({'error':'No se ha encontrado su página'},status=status.HTTP_401_UNAUTHORIZED)
