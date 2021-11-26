import io
from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  permissions, renderers, status
from .models import Documentos, TipoCreacion
from api.views import PaginationAPIView
from rest_framework.authentication import  TokenAuthentication
from .serializers import ComprobanteSerializer, DocumentosSerializer, FacturaSerializer
import base64
from rest_framework_xml.renderers import XMLRenderer

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
        if request.user.has_perm("documento.view_documentos"):
            archivo = self.get_object(pk=pk)
            serializer = self.serializer_class(archivo)
            if serializer:
                return Response(serializer.data)
            else:
                return Response({'error':"Ocurrió un error"},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':"No se ha encontrado su pagina"},status = status.HTTP_401_UNAUTHORIZED)

    def post(self,request):
        if request.user.has_perm("documento.add_documentos"):
            archivo = request.data["file"]
            if archivo != "":
                if request.data["content_type"]=="text/xml":
                    nombre = Documentos.objects.filter(nombreDoc = request.data["nombreDoc"])
                    if not nombre.exists(): # Aqui se cambia el campo
                        read = archivo.file.read()
                        file = io.BytesIO(read)
                        
                        archivo = Documentos.objects.create(_file = base64.encodebytes(file.getvalue()), content_type = request.data["content_type"],nombreDoc = request.data["nombreDoc"])
                        archivo.tipoCreacion = TipoCreacion.objects.get(pk=2)
                        archivo.proveedor = request.user
                        archivo.fechaEmision = None
                        archivo.save()
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
    renderer_classes = (XMLRenderer,)
    # serializer_class =  ComprobanteSerializer
        
    # def crear_facturas(self,attrs):
    #     serializer = FacturaSerializer(data=attrs)
    #     try:
    #         if serializer.is_valid(raise_exception=True):
    #             factura = serializer.save() 
    #             print(factura)
    #             return None
    #     except:
    #         return "Factura no valida"

    def post(self,request):
        if request.user.has_perm("documento.add_documentos"):  ## permiso espeficio para emitir
            #msgError = []
            # if request.data.get("facturas"):
            #     msg = self.crear_facturas(request.data.get("facturas"))
            #     if msg:
            #         msgError.append(msg)
            serializer = ComprobanteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                comprobantes = serializer.save(owner=request.user)
                comprobantes.pop('owner')
                return Response(comprobantes)
        else:
            return Response({'error':'No se ha encontrado su página'},status=status.HTTP_401_UNAUTHORIZED)
        
class ListaDocumentosPaginados(PaginationAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        if request.user.has_perm("documento.view_documentos"):
            # Buscar por empresa
            if request.GET.get("name"):
                print("si entra")
                query = Documentos.objects.filter(nombreDoc__icontains=request.GET.get("name")).order_by("-id")
            else:
                query = Documentos.objects.all().order_by("-id")
            page = self.paginate_queryset(query)
            if page is not None:
                serializer = self.get_paginated_response(DocumentosSerializer(page,many=True).data)
                return Response(serializer.data)
            
            return Response({"error":"Ocurrió un error con la consulta."},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error':'Acceso denegado'},status=status.HTTP_403_FORBIDDEN)
