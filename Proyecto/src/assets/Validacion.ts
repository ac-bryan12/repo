import { Injectable, OnInit } from "@angular/core";
import { FormGroup } from "@angular/forms";

@Injectable()
export class Validacion implements OnInit{
    constructor(){
    }

    ngOnInit(): void {
    }

  validarConfPassword(password:string,confpassword:string): boolean{
    if(password != confpassword){
      return true;
    }
    return false;
  }

  validarPN(subcadena:String,subcadena2:String){
    var arreglo = subcadena.split("")
    var coeficientes = [2,1,2,1,2,1,2,1,2]
    var result = []
    var acum = 0
    console.log("dentro")
    for(let i = 0; i<coeficientes.length;i++){
        var num = Number(arreglo[i])*coeficientes[i]
        if(num<=9) result[i]=num
        else result[i]=num-9
    }
    for(let j = 0;j<result.length;j++)
       acum+=result[j]
    acum = (acum%10)
    if(acum !=0)
      acum = 10 - acum
    if(acum === Number(subcadena2))
      return true
    return false
  }
  validarPJ(subcadena:String,subcadena2:String){
    var arreglo = subcadena.split("")
    var coeficientes = [4,3,2,7,6,5,4,3,2]
    var result = []
    var acum = 0
    for(let i = 0; i<coeficientes.length;i++){
        var num = Number(arreglo[i])*coeficientes[i]
        result[i]=num
    }
    for(let j = 0;j<result.length;j++)
       acum+=result[j]
    acum = (acum%11)
    if(acum != 0) 
      acum = 11-acum
    if(acum === Number(subcadena2))
      return true
    return false
  }
  validarIP(subcadena:String,subcadena2:String){
    var arreglo = subcadena.split("")
    var coeficientes = [3,2,7,6,5,4,3,2]
    var result = []
    var acum = 0
    for(let i = 0; i<coeficientes.length;i++){
        var num = Number(arreglo[i])*coeficientes[i]
        result[i]=num
    }
    for(let j = 0;j<result.length;j++)
       acum+=result[j]
    acum =(acum%11)
    if(acum != 0) 
      acum = 11-acum
    if(acum === Number(subcadena2))
      return true
    return false
  }
  validarRuc(ruc:string){
    if (ruc.length === 13) {
      console.log("Valida 13 digitos")
      const ultimoDigito = ruc.substring(9, 10);
      const digitoRegion = ruc.substring(0, 2)
      if (digitoRegion >= String("01") && digitoRegion <= String("24") || digitoRegion == String(30) && ultimoDigito>=String("1")) {
          const tercerDigito = ruc.substring(2,3);
          if(tercerDigito >= String(0) && tercerDigito <= String(5)){
            //Persona natural
            var valDecimoDigito = this.validarPN(ruc.substring(0,9),ruc.substring(9,10)) 
            if(valDecimoDigito){
              console.log('Persona natural')
              return true;
            }
            else{
              console.log('Formato incorrecto')
              return false
            }  
          }
          else if(tercerDigito==String(9)){
            //Persona juridica falta validar residuo cero
            var valDecimoDigito = this.validarPJ(ruc.substring(0,9),ruc.substring(9,10)) 
            if(valDecimoDigito){
              console.log('Persona juridica')
              return true;
            }
            else{
              console.log('Formato incorrecto')
              return false
            }  
          }
          else if(tercerDigito==String(6)){
            //Entidad publica solo falta valida residuo cero
            var valDecimoDigito = this.validarIP(ruc.substring(0,8),ruc.substring(8,9)) 
            if(valDecimoDigito){
              console.log('Entidad publica')
              return true;
            }
            else{
              console.log('Formato incorrecto')
              return false
            }  
          }
          else{
            return false
          }
      } else {
        return false
      }
    } else {
      return false
    }
  
  }

  validarCampNum(tlf:any,numMaximo: number) {
    if(!isNaN(tlf.value) && !tlf.value.includes(" ") && tlf.value != ''){
      if(tlf.value.length > numMaximo) tlf.value = tlf.value.substring(0,tlf.value.length-1)
    }
    else{
      tlf.value = tlf.value.substring(0,tlf.value.length-1)
    }
  }
}