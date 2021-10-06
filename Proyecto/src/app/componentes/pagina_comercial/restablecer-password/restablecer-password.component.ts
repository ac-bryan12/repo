import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';
import { Validacion } from 'src/assets/Validacion';

@Component({
  selector: 'restablecer-password',
  templateUrl: './restablecer-password.component.html',
  styleUrls: ['./restablecer-password.component.css']
})
export class RestablecerPasswordComponent implements OnInit {
  public restablecerPassword: FormGroup;
  public codeVerificacion: FormGroup;
  response_d = ''
  response_button:boolean
  response_content = ''
  public validate:Validacion = new Validacion();
  
  constructor(
    private router:Router,
    private service: RequestService,
    private fb: FormBuilder,
    private fb2: FormBuilder
  ) {
    this.restablecerPassword = this.fb.group({
        password: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z0-9_:@.\-]+$'),Validators.minLength(8)]),
        confpassword: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9_:@.\-]+$')]),
    });
    this.codeVerificacion = this.fb2.group({
        code : this.fb2.control('', [Validators.required])
    }); 
    this.response_button = true
  };
  ngOnInit(): void {
  }

  validacionPassword(){
    return this.validate.validarConfPassword(this.restablecerPassword.get(["password"])?.value,this.restablecerPassword.get(["confpassword"])?.value)    
  }
  enviarCode(code:string){
    this.response_d ="d-block"
    this.response_content ="Verificando su codigo"
    this.service.peticionGet("http://localhost:8000/auth/reset_password_verification/"+code, true).subscribe((res) =>{
      console.log(res)
      this.response_content = res.msg
      this.response_button = !res.validated
    },error => {
      if(error.hasOwnProperty("error")){
        this.response_content = error.error.error
        this.response_button = !error.validated
      }
    })
  }
}
