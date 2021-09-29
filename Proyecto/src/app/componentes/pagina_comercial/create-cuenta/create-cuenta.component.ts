import { Component, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';
import { HttpErrorResponse } from '@angular/common/http';
import { FormBuilder,FormGroup, Validators} from '@angular/forms';
import { Validacion } from 'src/assets/Validacion';
import { Router } from '@angular/router';


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
    private router:Router,
    private envio: RequestService,
    private fb: FormBuilder
  ) {
    this.createAccount = this.fb.group({
      empresa: this.fb.group({
        ruc: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$'),Validators.maxLength(13),Validators.minLength(13),]),
        email: this.fb.control('', [Validators.required,Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'),Validators.minLength(7)]),
        razonSocial: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9. ]+$'),Validators.minLength(5), Validators.maxLength(50)]),
        telefono: this.fb.control('', [Validators.required,Validators.minLength(10),Validators.maxLength(11)]),
        direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9._ ]+$')])
      }),
      user: this.fb.group({
        first_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(3),Validators.maxLength(50)]),
        last_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(3),Validators.maxLength(50)]),
        password: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z0-9_:@.\-]+$'),Validators.minLength(8)]),
        confpassword: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9_:@.\-]+$')]),
        email: this.fb.control('', [Validators.required,Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'),Validators.minLength(7)]),
        token: this.fb.control('', [Validators.required,Validators.minLength(4)]),
        groups:''
      }),
      telefono: this.fb.control('', [Validators.required,Validators.minLength(10),Validators.maxLength(11)]),
      direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9._ ]+$')]),
      cargoEmpres: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(4),Validators.maxLength(50)],),

    });
  };

  ngOnInit(): void {
  }

  enviar(values:any){
    values.user.groups = [
      {name:'admin_empresa'}
    ]
    console.log(values)
    // localStorage.setItem('token',values.usuario.token)
    this.envio.peticionPost("http://localhost:8000/auth/create/",values,true).subscribe((res)=>{
      if(res['msg']!= ''){
        this.envio.isCreatedAccount= true
        this.envio.isRegistered = false
        this.router.navigate(['/creacion-exitosa'])
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
    return this.validate.validarConfPassword(this.createAccount.get(["user","password"])?.value,this.createAccount.get(["user","confpassword"])?.value)    
  }
  validarRuc(){
    let ruc = this.createAccount.get(['empresa','ruc'])?.value
    return !this.validate.validarRuc(ruc)
  }

}
