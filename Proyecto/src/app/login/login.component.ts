import { tokenize } from '@angular/compiler/src/ml_parser/lexer';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { LoginService } from '../services/login.service';

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
    private request: LoginService,
    private log: FormBuilder) {
    this.login = this.log.group({
      email: this.log.control('', [Validators.required, Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'), Validators.minLength(7)]),
      password: this.log.control('', [Validators.required, Validators.pattern('^[a-zA-Z0-9_:@.\-]+$'), Validators.minLength(8)])
    })
  }

  ngOnInit(): void {
  }

  iniciarSesion(value : any) {
    let token = "";
    if (this.validacion("email") && this.validacion("password")) {
      const responseT = this.request.peticionPost('http://127.0.0.1:8000/api/auth/', value)
        .toPromise().then(res => {
          if (res['token'] != '0') {
            // alert('Ha iniciado sesión')
            this.request.setToken(res['token'])
            window.location.href = 'http://localhost:8000/api/perfil/';
          } else {
            this.msg_d = 'd-block'
            this.msg_content = "Email o contraseña invalido. El usuario no se encuentra en el sistema."
          }
        });

      // const setToken = async () => {
      //   token = await responseT
      //   alert(token)
      //   this.request.setToken(token)
      //   window.location.href = 'http://localhost:8000/api/perfil/';
      // }
      // setToken()
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

  /*
      let token = "";
      if(this.user.email != '' && this.user.password != ''){
        if(this.user.email.length > 6){
          if(this.user.password.length > 7){
            const responseT = this.request.peticionPost('http://127.0.0.1:8000/api/auth/',this.user)
            .toPromise().then(res => {
              if (res['token'] != '0'){
                alert("Ha iniciado sesión con el correo:"+this.user.email,)
                return res['token']
              }else{
                this.msg_d = 'd-block'
                this.msg_content = "Email o contraseña invalido. El usuario no se encuentra en el sistema."
              }
            });
            const setToken = async() =>{
            token = await responseT
            this.request.setToken(token)
            
            }
            setToken()
          }else{
            this.msg_content = "La contraseña debe tener al menos 8 digitos."
            this.msg_d = 'd-block'
          }
          
        }else{
          this.msg_content = "El email debe tener al menos 7 digitos."
          this.msg_d = 'd-block'
        }
      }else{
        this.msg_d = 'd-block'
        this.msg_content = "Llenar los campos faltantes"
      }
      */
}
