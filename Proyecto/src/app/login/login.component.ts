import { tokenize } from '@angular/compiler/src/ml_parser/lexer';
import { Component, OnInit } from '@angular/core';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  user = {
      email: '',
      password: ''
    }

  msg_content = ''
  msg_d = 'd-none'

  constructor(private request:LoginService) { }

  ngOnInit(): void {
  }


  traerUsuarios(){
    console.log("token: ",this.request.getToken())
    this.request.peticionGet('http://127.0.0.1:8000/api/users/')
    .subscribe(res => {
      console.log(res)
    })
  }

  iniciarSesion(){
    /* Ocultando los mensajes de error */
    this.msg_d = 'd-none'

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
  }

}
