import { Component, OnInit } from '@angular/core';
import { LoginService } from 'src/app/services/login.service';
import { FormBuilder, FormControl, FormGroup, Validators,ValidationErrors,ValidatorFn, AbstractControl, AsyncValidator, AsyncValidatorFn} from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';



@Component({
  selector: 'app-create-cuenta',
  templateUrl: './create-cuenta.component.html',
  styleUrls: ['./create-cuenta.component.css']
})

export class CreateCuentaComponent implements OnInit {
  public createAccount: FormGroup;
  response_d = ''
  response_content = ''
  token = ''
  msg_content = ''
  msg_d = 'd-none'
  ruc_d = ''
  ruc_content = ''
  
  constructor(
    private envio: LoginService,
    private fb: FormBuilder
  ) {
    this.createAccount = this.fb.group({
      empresa: this.fb.group({
        ruc: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$'),Validators.maxLength(13),Validators.minLength(13),]),
        email: this.fb.control('', [Validators.required,Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'),Validators.minLength(7)]),
        razonSocial: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9. ]+$'),Validators.minLength(5), Validators.maxLength(50)]),
        telefono: this.fb.control('', [Validators.required,Validators.pattern('^[+_0-9]+$'),Validators.minLength(13),Validators.maxLength(13)]),
        direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9._ ]+$')]),
      }),
      usuario: this.fb.group({
        firstName: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(3),Validators.maxLength(50)]),
        lastName: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(3),Validators.maxLength(50)]),
        cargo: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(4),Validators.maxLength(50)],),
        password: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z0-9_:@.\-]+$'),Validators.minLength(8)]),
        confpassword: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9_:@.\-]+$')]),
        email: this.fb.control('', [Validators.required,Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'),Validators.minLength(7)]),
        telefono: this.fb.control('', [Validators.required,Validators.pattern('^[+_0-9]+$'),Validators.minLength(13),Validators.maxLength(20)]),
        direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9._ ]+$')]),
        token: this.fb.control('', [Validators.required,Validators.minLength(4)]),
      })
    });
  };

  ngOnInit(): void {
  }

  enviar(values:any){
    this.envio.setToken(values.usuario.token)
    this.envio.peticionPost("http://localhost:8000/api/create/",values).subscribe((res)=>{
      if(res['msg']!= ''){
        window.location.href = 'http://localhost:4200/creacion-exitosa';
      }
    },(err:HttpErrorResponse)=>{
      if(err.error.hasOwnProperty('usuario')){
        if(err.error.usuario.hasOwnProperty('non_field_errors')){
          this.response_d = 'd-block'
          this.response_content = err.error.usuario.non_field_errors[0]
        }
      }else if(err.error.hasOwnProperty('empresa')){
        if(err.error.usuario.hasOwnProperty('non_field_errors')){
          this.response_d = 'd-block'
          this.response_content = err.error.empresa.non_field_errors[0]
        }
      }else{
        this.response_d = 'd-block'
        this.response_content = err.error[0]
      }
    
    })
  }

  validarConfPassword(): boolean{
    this.msg_d = 'd-none'
    let pass = this.createAccount.get(['usuario','password'])?.value
    let valpass = this.createAccount.get(['usuario','confpassword'])?.value
    if(this.createAccount.get(['usuario','password'])?.hasError('required') || pass != valpass){
      this.msg_d = 'd-block'
      this.msg_content = "Contraseña no coincide"
      return false;
    }
    return true;
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
    acum = 10 - (acum%10)
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
  validarRuc(){
    this.ruc_d = 'd-none'
    var ruc = this.createAccount.get(['empresa','ruc'])?.value
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
              this.ruc_d = 'd-block'
              this.ruc_content = "Ingrese ruc válido"
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
              this.ruc_d = 'd-block'
              this.ruc_content = "Ingrese ruc válido"
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
              this.ruc_d = 'd-block'
              this.ruc_content = "Ingrese Ruc válido"
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

}
