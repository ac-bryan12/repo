import { NONE_TYPE } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ThemePalette } from '@angular/material/core';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';
import { RequestService } from 'src/app/services/request/request.service';
import { Validacion } from 'src/assets/Validacion';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.css']
})
export class ChangePasswordComponent implements OnInit {
  // Progress Bar
  color: ThemePalette = 'primary';
  mode: ProgressSpinnerMode = 'indeterminate';
  loanding = false
  //Other variables 
  public changePassword: FormGroup;
  public validate: Validacion = new Validacion();
  btn: any;
  hide:boolean=true
  hideAct:boolean =true
  hideConf:boolean=true
  constructor(
    private fb: FormBuilder,private service: RequestService
  ) {
    this.changePassword = this.fb.group({
      actual_password: this.fb.control('', [Validators.required,Validators.minLength(8)]),
      password: this.fb.control('', [Validators.required, Validators.pattern('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[_.{}=<>;:,\+$@$!%*?&])[A-Za-z\d_.{}=<>;:,\+$@$!%*?&].{7,}')]),
      confpassword: this.fb.control('', [Validators.required, Validators.pattern('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[_.{}=<>;:,\+$@$!%*?&])[A-Za-z\d_.{}=<>;:,\+$@$!%*?&].{7,}')])
    })
  }

  ngOnInit(): void {
    this.btn = document.querySelector('input[type="submit"]') as HTMLInputElement
  }

  validacionPassword() {
    return this.validate.validarConfPassword(this.changePassword.get('password')?.value, this.changePassword.get('confpassword')?.value)
  }

  actualizar(form:any){
    this.loanding = true;
    this.service.peticionPost(environment.url+"/auth/reset_password/",form).subscribe(res=>{
      this.loanding = false;
      alert(res["msg"])
      this.limpiarFormulario()
    },err=>{
      this.loanding = false;
      alert(err.error.error)
    })
  }

  limpiarFormulario(){
    window.location.reload()
  }
}