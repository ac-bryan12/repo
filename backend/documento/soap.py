from zeep import Client

def recepcionComprobantes(xml):
    client = Client("https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl")
    result = client.service.validarComprobante(xml)
    print(result)
    # file = open("prueba.txt","w")
    # file.write(result)
    # file.close()
    