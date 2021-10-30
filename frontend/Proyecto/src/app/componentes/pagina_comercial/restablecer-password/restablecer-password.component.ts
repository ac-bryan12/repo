import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ThemePalette } from '@angular/material/core';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';
import { Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';
import { Validacion } from 'src/assets/Validacion';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'restablecer-password',
  templateUrl: './restablecer-password.component.html',
  styleUrls: ['./restablecer-password.component.css']
})
export class RestablecerPasswordComponent implements OnInit {
  // Progress Bar
  color: ThemePalette = 'primary';
  mode: ProgressSpinnerMode = 'indeterminate';
  loanding = false
  //Other variables
  public restablecerPassword: FormGroup;
  public codeVerificacion: FormGroup;
  response_d = ''
  response_button:boolean
  response_content = ''
  hide:boolean = true
  hideConf:boolean = true 
  public validate:Validacion = new Validacion();
  
  constructor(
    private router:Router,
    private service: RequestService,
    private fb: FormBuilder,
    private fb2: FormBuilder
  ) {
    this.restablecerPassword = this.fb.group({
        password: this.fb.control('', [Validators.required, Validators.pattern('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[_.{}=<>;:,\+$@$!%*?&])[A-Za-z\d_.{}=<>;:,\+$@$!%*?&].{7,}')]),
        confpassword: this.fb.control('', [Validators.required, Validators.pattern('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[_.{}=<>;:,\+$@$!%*?&])[A-Za-z\d_.{}=<>;:,\+$@$!%*?&].{7,}')]),
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
    this.service.peticionGet(environment.url+"/auth/reset_password_verification/"+code+"/", true).subscribe((res) =>{
      // this.response_content = res.msg
      this.response_button = !res.validated
      alert(res.msg)
      localStorage.setItem('token', code);
    },error => {
      if(error.hasOwnProperty("error")){
        alert(error.error.error)
        this.response_button = !error.validated
      }
    })
  }

  enviar(value:any){
    this.loanding = true;
    this.service.peticionPost(environment.url+"/auth/reset_password/",{"password":value}).subscribe(res =>{
      this.loanding = false;
      alert(res["msg"])
      this.router.navigate(["/login"])
    },err =>{
      this.loanding = false;
      alert(err.error.error)
    })
  }
}
