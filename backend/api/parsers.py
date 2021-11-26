
from io import StringIO
from django.utils import six
from django.utils.encoding import smart_text
from rest_framework_xml.renderers import XMLRenderer
from django.utils.xmlutils import SimplerXMLGenerator

class XMLDocRenderer(XMLRenderer):
    root_tag_name = 'prueba-root'
    item_tag_name = 'prueba-list'
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized XML.
        """
        if data is None:
            return ''

        stream = StringIO()

        xml:SimplerXMLGenerator = SimplerXMLGenerator(stream, self.charset)
        xml.startDocument()
        xml.startElement(self.root_tag_name, {"id":"comprobante","version":"1.1.0"})

        self._to_xml(xml, data)

        xml.endElement(self.root_tag_name)
        xml.endDocument()
        return stream.getvalue()
    
    def get_properties(self,data):
        properties = {}
        val = ''
        if isinstance(data, dict):
            for key, value in six.iteritems(data):
                if key.startswith('_'):
                    properties[key[1:]] = value
                elif key.startswith('#'):
                    val=value
        return properties, val     
    
    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                properties, val = self.get_properties(item)
                xml.startElement(self.item_tag_name,properties)
                if val :
                    item = val
                self._to_xml(xml, item)
                xml.endElement(self.item_tag_name)

        elif isinstance(data, dict):
            for key, value in six.iteritems(data):
                if not key.startswith('_') and not key.startswith('#'):
                    if isinstance(value, (list, tuple)):
                        self.item_tag_name = key
                        self._to_xml(xml, value)
                        continue
                    
                    properties, val = self.get_properties(value)
                    xml.startElement(key,properties)
                    if val :
                        value = val
                    self._to_xml(xml, value)
                    xml.endElement(key)
        elif data is None:
            # Don't output any value
            pass

        else:
            xml.characters(smart_text(data))