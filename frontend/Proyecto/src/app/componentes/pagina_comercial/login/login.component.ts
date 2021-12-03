import { tokenize } from '@angular/compiler/src/ml_parser/lexer';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { RequestService } from '../../../services/request/request.service';
import { HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { environment } from 'src/environments/environment';
import { ThemePalette } from '@angular/material/core';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  public login: FormGroup;
  //Progress bar
  color: ThemePalette = 'primary';
  mode: ProgressSpinnerMode = 'indeterminate';
  loanding = false
  hide:boolean =true
  msg_content = 'contenido'
  msg_d = 'invisible'

  constructor(
    private cookie:CookieService,
    private route: Router,
    private request: RequestService,
    private log: FormBuilder) {
    this.login = this.log.group({
      email: this.log.control('', [Validators.required, Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'), Validators.minLength(7)]),
      password: this.log.control('', [Validators.required, Validators.minLength(8)])
    })
  }

  ngOnInit(): void {
    let return_to = this.cookie.get("return_to")
    if(return_to){
      this.route.navigate([return_to])
    }
  }

  // cambiarVistas(groups:string[]){
  //   if(groups.includes('admin_facturacion')){
  //     this.route.navigate(["/admin"])
  //   }else if(groups.includes('cliente')){
  //     this.route.navigate(["/cliente"])
  //   }else if(groups.includes('admin_empresa')){
  //     this.route.navigate(["/view-company"])
  //   }else{
  //     this.route.navigate(["/login"])
  //   }
  // }


  iniciarSesion(value: any) {
    this.loanding = true
    if (this.validacion("email") && this.validacion("password")) {
      this.request.peticionPost(environment.url+'/auth/login/', value, true)
        .subscribe(res => {
          this.loanding = false
          this.request.isLoggedIn = true
          localStorage.setItem('token', res['token']);
          localStorage.setItem('Autenticated', "true");
          // this.grupos_permisos()   
          this.route.navigate(["/portal/perfil"])
        }, (err: HttpErrorResponse) => {
          this.loanding = false
          // this.msg_d = 'd-block'
          alert(err.error.error);
        });
    }
  }
  // grupos_permisos() {
  //   this.request.peticionGet(environment.url+"/auth/userPermissions/").subscribe(res =>{
  //     console.log(res)
  //     this.cambiarVistas(res['groups'])
  //   })
  // }
  validacion(v: string): boolean {
    this.msg_d = 'invisible'
    if (this.login.get(v)?.hasError('required')) {
      this.msg_d = 'visible'
      this.msg_content = "Rellena la información requerida"
      return false;
    }
    else if (this.login.get(v)?.hasError('minlength') || this.login.get(v)?.hasError('pattern')) {
      this.msg_d = 'visible'
      this.msg_content = `Ingresa ${v} válido`
      return false;
    }
    else {
      return true;
    }
  }

}
