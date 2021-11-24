from rest_framework import exceptions
from django.core.exceptions import ValidationError

    
def validarTipoPersona(subcadena:str,subcadena2:str,coeficientes,modulo: int):
    # coeficientes = [2,1,2,1,2,1,2,1,2]
    result = []
    acum = 0
    
    for  i in  range(len(coeficientes)):
        num = int(subcadena[i])*coeficientes[i]
        if num<=9 and modulo ==10 or modulo == 11:
            result.append(num)
        else :
            result.append(num-9)
            
    # for  j  in result:
    #     acum += j
    
    acum = sum(result)
       
    acum = acum % modulo
    
    if acum != 0 :
        acum = modulo-acum
        
    if acum == int(subcadena2):
      return True
  
    return False


def validar_identificacion(value:str):
    print(value)
    ultimoDigito = value[9]
    digitoRegion = value[0:2]
    print(ultimoDigito)
    print(digitoRegion)
    if digitoRegion >= "01" and digitoRegion <= "24" or digitoRegion == "30" and ultimoDigito >= "1" :
        tercerDigito = value[2]
        print(tercerDigito)
        if tercerDigito >= "0" and tercerDigito <= "5":
            #Persona natural
            valDecimoDigito = validarTipoPersona(value[0:9],value[9],[2,1,2,1,2,1,2,1,2],10)
            if valDecimoDigito :
                return value;    
            else:
                raise ValidationError({"error":"Número de identificación incorrecto."})
            
        elif tercerDigito == "9":
            # Persona juridica falta validar residuo cero
            valDecimoDigito = validarTipoPersona(value[0:9],value[9],[4,3,2,7,6,5,4,3,2],11) 
            if valDecimoDigito:
                return value
            else:
                raise ValidationError({"error":"Número de identificación incorrecto."})
            
        elif tercerDigito == "6":
            # Entidad publica solo falta valida residuo cero
            valDecimoDigito = validarTipoPersona(value[0:8],value[8],[3,2,7,6,5,4,3,2],11) 
            if valDecimoDigito:
                return value
            else:
                raise ValidationError({"error":"Número de identificación incorrecto."})
    
        else:
            raise ValidationError({"error":"Número de identificación incorrecto."})
            
    else:
        raise ValidationError({"error":"Número de identificación incorrecto."})
      
  

  

# def validarPJ(subcadena:str,subcadena2:str):
#     coeficientes = [4,3,2,7,6,5,4,3,2]
#     result = []
#     acum = 0
#     for i in range(coeficientes.length):
#         num = int(subcadena[i])*coeficientes[i]
#         result[i]=num
    
#     for j in result:
#         acum += j
        
#     acum = acum%11
#     if acum != 0:
#         acum = 11-acum
        
#     if acum == int(subcadena2):
#         return True
#     return False
    
# def validarIP(subcadena:str,subcadena2:str):
#     coeficientes = [3,2,7,6,5,4,3,2]
#     result = []
#     acum = 0
#     for i in range(coeficientes.length):
#         num = int(subcadena[i])*coeficientes[i]
#         result[i]=num
    
#     for j in result:
#         acum += j
        
#     acum = acum%11 
#     if acum != 0:
#         acum = 11-acum
        
#     if acum == int(subcadena2):
#         return True
#     return False
    
  