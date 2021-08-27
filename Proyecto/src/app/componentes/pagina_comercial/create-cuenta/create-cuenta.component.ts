import { Component, OnInit } from '@angular/core';
import { LoginService } from 'src/app/services/login.service';
import { HttpErrorResponse } from '@angular/common/http';
import { FormBuilder,FormGroup, Validators} from '@angular/forms';
import { Validacion } from 'src/assets/Validacion';


@Component({
  selector: 'app-create-cuenta',
  templateUrl: './create-cuenta.component.html',
  styleUrls: ['./create-cuenta.component.css']
})

export class CreateCuentaComponent implements OnInit {
  public createAccount: FormGroup;
  response_d = ''
  response_content = ''
  public validate:Validacion = new Validacion();
  
  constructor(
    private envio: LoginService,
    private fb: FormBuilder
  ) {
    this.createAccount = this.fb.group({
      empresa: this.fb.group({
        ruc: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$'),Validators.maxLength(13),Validators.minLength(13),]),
        email: this.fb.control('', [Validators.required,Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'),Validators.minLength(7)]),
        razonSocial: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9. ]+$'),Validators.minLength(5), Validators.maxLength(50)]),
        telefono: this.fb.control('', [Validators.required,Validators.minLength(10),Validators.maxLength(11)]),
        direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9._ ]+$')]),
      }),
      usuario: this.fb.group({
        firstName: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(3),Validators.maxLength(50)]),
        lastName: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(3),Validators.maxLength(50)]),
        cargo: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(4),Validators.maxLength(50)],),
        password: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z0-9_:@.\-]+$'),Validators.minLength(8)]),
        confpassword: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9_:@.\-]+$')]),
        email: this.fb.control('', [Validators.required,Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'),Validators.minLength(7)]),
        telefono: this.fb.control('', [Validators.required,Validators.minLength(10),Validators.maxLength(11)]),
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

  validacionPassword(){
    return this.validate.validarConfPassword(this.createAccount.get(["usuario","password"])?.value,this.createAccount.get(["usuario","confpassword"])?.value)    
  }
  validarRuc(){
    let ruc = this.createAccount.get(['empresa','ruc'])?.value
    return !this.validate.validarRuc(ruc)
  }

}
