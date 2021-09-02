import { tokenize } from '@angular/compiler/src/ml_parser/lexer';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { RequestService } from '../services/request/request.service';
import { HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  public login: FormGroup;
  /*
  user = {
      email: '',
      password: ''
    }
*/
  msg_content = ''
  msg_d = 'd-none'

  constructor(
    private route:Router,
    private request: RequestService,
    private log: FormBuilder) {
    this.login = this.log.group({
      email: this.log.control('', [Validators.required, Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'), Validators.minLength(7)]),
      password: this.log.control('', [Validators.required, Validators.pattern('^[a-zA-Z0-9_:@.\-]+$'), Validators.minLength(8)])
    })
  }

  ngOnInit(): void {
  }


  iniciarSesion(value : any) {
    if (this.validacion("email") && this.validacion("password")) {
      this.request.peticionPost('http://localhost:8000/api/auth/', value,true)
        .subscribe(res => {
          this.request.isLoggedIn = true
          localStorage.setItem('token',res['token']);
          localStorage.setItem('Autenticated',"true");
          this.route.navigate(["/admin"])
        },(err:HttpErrorResponse)=>{
          this.msg_d = 'd-block'
          this.msg_content = err.error.error;
          [0]
        });
    }
  }

  validacion(v: string): boolean {
    this.msg_d = 'd-none'
    if (this.login.get(v)?.hasError('required')) {
      this.msg_d = 'd-block'
      this.msg_content = "Rellena la información requerida"
      return false;
    }
    else if (this.login.get(v)?.hasError('minlength') || this.login.get(v)?.hasError('pattern')) {
      this.msg_d = 'd-block'
      this.msg_content = `Ingresa ${v} válido`
      return false;
    }
    else {
      return true;
    }
  }

}
