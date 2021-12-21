import io
from django.core.exceptions import ValidationError
from django.http.response import HttpResponse
from django.utils.module_loading import autodiscover_modules
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  permissions, renderers, serializers, status
from django.utils import six, xmlutils
from weasyprint import CSS, HTML
from weasyprint.text.fonts import FontConfiguration
from django.template.loader import render_to_string

from api.parsers import XMLDocRenderer
from documento.soap import recepcionComprobantes
from .models import Documentos, Estado, TipoCreacion, TipoDocumento
from api.views import PaginationAPIView
from rest_framework.authentication import  TokenAuthentication
from .serializers import ComprobanteSerializer, DocumentosSerializer, FacturaSerializer
import base64
from usuario.models import Profile
from rest_framework_xml.renderers import XMLRenderer
import xml.etree.ElementTree as ET


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
        doc = self.get_object(pk=pk)
        if (doc.cliente == request.user and request.user.has_perm("documento.view_documentos_recibidos"))  or (doc.proveedor.profile.empresa.ruc == request.user.profile.empresa.ruc and request.user.has_perm("documento.view_documentos_emitidos") ):
            if request.GET.get("formato") == "xml":
                return Response({"_file":doc._file,"nombreDoc":doc.nombreDoc})
            if request.GET.get("formato") == "pdf":
                return Response({"_file":doc.pdf,"nombreDoc":doc.nombreDoc})    
        else:
            return Response({'error':"Acceso denegado"},status = status.HTTP_401_UNAUTHORIZED)

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
    # renderer_classes = (XMLDocRenderer,)
    
    def getDigitoVerificador(self,codigo):
        mul = [3,2,7,6,5,4,3,2]
        acumulador = 0
        for i in range(len(codigo)):
            acumulador += int(codigo[i])*mul[i]
        acumulador = acumulador % 11
        acumulador =  11 - acumulador 
        return str(acumulador)
        
    def generarClaveAcceso(self,comprobante,doc):
        clave = ""
        clave += str(doc.fechaEmision.date().strftime('%d%m%Y'))
        clave += comprobante['infoTributaria']['codDoc']
        clave += comprobante['infoTributaria']['ruc']
        clave += str(comprobante['infoTributaria']['ambiente'])
        serie  = comprobante['infoTributaria']['codDoc']+str(doc.fechaEmision.date().strftime('%Y'))
        clave += serie
        clave += str(doc.pk).zfill(9)
        clave += str(doc.pk).zfill(8)
        clave += "1"
        clave += self.getDigitoVerificador(str(doc.pk).zfill(8))
        return clave

    def post(self,request):
        
        if request.user.has_perm("documento.add_documentos"):  ## permiso espeficio para emitir
            #self.context['owner'] = request.user
            renderer: XMLDocRenderer = XMLDocRenderer()
            serializer = ComprobanteSerializer(data=request.data,context={"owner":request.user})
            self.charset = "utf-8"
            if serializer.is_valid(raise_exception=True):
                comprobantes = serializer.save()
                #comprobantes.pop('owner')
                items = {}
                for key, value in six.iteritems(comprobantes):
                    renderer.root_tag_name = key
                    new_key = []
                    for comprobante in value:
                        
                        doc = Documentos()
                        doc.save()
                        
                        comprobante['infoTributaria']['secuencial'] = str(doc.pk).zfill(9)
                        comprobante['infoTributaria']['claveAcceso'] = self.generarClaveAcceso(comprobante,doc)
                        comprobante['infoFactura']['fechaEmision'] = str(doc.fechaEmision.date().strftime('%d/%m/%Y'))
                        
                        
                        
                        xml = renderer.render(data=comprobante)
                        xmlByte = xml.encode('utf-8')
                        
                        doc._file = base64.encodebytes(xmlByte) 
                        doc.content_type = "text/xml"
                        doc.nombreDoc = key+"_"+str(doc.pk)
                        doc.estado = Estado.objects.get(pk=1)
                        doc.tipoCreacion = TipoCreacion.objects.get(pk=1)
                        doc.proveedor = request.user
                        doc.tipoDocumento = TipoDocumento.objects.get(pk=comprobante['infoTributaria']['codDoc'])
                        doc.cliente =Profile.objects.get(pk=comprobante['infoFactura']['identificacionComprador']).user
                        
                        iva = 0
                        subtotal12 = 0
                        subtotal0 = 0
                        descuento = 0
                        
                        for impuesto in comprobante["infoFactura"]["totalConImpuestos"]["totalImpuesto"]:
                            if impuesto['codigo'] == 2:
                                iva = impuesto['valor']  
                                subtotal12 = impuesto['baseImponible']
                                if impuesto.get('descuentoAdicional'):
                                    descuento = impuesto['descuentoAdicional']
                            if impuesto['codigo'] == 3:
                                subtotal0 = impuesto['baseImponible']
                        
                        html = render_to_string("comprobantes/factura.html",{"comprobante":comprobante,"iva":iva,"subtotal0":subtotal0,"subtotal12":subtotal12,"descuento":descuento})
                        font_config = FontConfiguration()
                        # css = []
                        # css.append(CSS(filename="factura.css"))
                        pdf = HTML(string=html).write_pdf(font_config=font_config)
                        doc.pdf = base64.encodebytes(pdf)
                        
                        doc.save()
                        recepcionComprobantes(xml.encode("ascii"))
                        new_key.append(xml.encode("ascii"))
                    items[key] = new_key
                        
                return Response(items)
                # return Response(comprobantes)
        else:
            return Response({'error':'No se ha encontrado su página'},status=status.HTTP_401_UNAUTHORIZED)
        
class ListaDocumentosPaginados(PaginationAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        if request.user.has_perm("documento.view_documentos_emitidos") and request.GET.get("tipo") == "emitidos":
            # Buscar por empresa
            if request.GET.get("name"):
                query = Documentos.objects.filter(nombreDoc__icontains=request.GET.get("name"),proveedor__profile__empresa=request.user.profile.empresa).order_by("-id")
            else:
                query = Documentos.objects.filter(proveedor__profile__empresa=request.user.profile.empresa).order_by("-id")
            page = self.paginate_queryset(query)
            if page is not None:
                serializer = self.get_paginated_response(DocumentosSerializer(page,many=True).data)
                return Response(serializer.data)
            
            return Response({"error":"Ocurrió un error con la consulta."},status=status.HTTP_400_BAD_REQUEST)
        
        elif request.user.has_perm("documento.view_documentos_recibidos") and request.GET.get("tipo") == "recibidos":
            if request.GET.get("name"):
                print("si entra")
                query = Documentos.objects.filter(nombreDoc__icontains=request.GET.get("name"),cliente=request.user).order_by("-id")
            else:
                query = Documentos.objects.filter(cliente=request.user).order_by("-id")
            page = self.paginate_queryset(query)
            if page is not None:
                serializer = self.get_paginated_response(DocumentosSerializer(page,many=True).data)
                return Response(serializer.data)
            
            return Response({"error":"Ocurrió un error con la consulta."},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error':'Acceso denegado'},status=status.HTTP_403_FORBIDDEN)

class ObtenerDocumentos(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):        
        if request.GET.get("id"):
            doc = Documentos.objects.filter(id=request.GET.get("id"))
            if doc.exists():
                doc = doc.get()
                if (doc.cliente == request.user and request.user.has_perm("documento.view_documentos_recibidos"))  or (doc.proveedor.profile.empresa.ruc == request.user.profile.empresa.ruc and request.user.has_perm("documento.view_documentos_emitidos") ):
                    context = {}
                    html = render_to_string("comprobantes/factura.html", context)

                    #response = Response(content_type="application/pdf")
                    #response["Content-Disposition"] = "inline; report.pdf"

                    #font_config = FontConfiguration()
                    #pdf = HTML(string=html).write_pdf(font_config=font_config)

                    return Response("Si puede ver")
                else:
                    return Response({'error':"Acceso denegado"},status=status.HTTP_403_FORBIDEN)    
            else:
                return Response({'error':"No existe el comprobante"},status=status.HTTP_404_NOT_FOUND)
