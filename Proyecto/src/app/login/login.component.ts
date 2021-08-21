import { tokenize } from '@angular/compiler/src/ml_parser/lexer';
import { Component, OnInit } from '@angular/core';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  user:any;
  constructor(private login:LoginService) { }

  ngOnInit(): void {
    this.user = {
      email: '',
      password: ''
    }
  }

  traerUsuarios(){
    console.log("token: ",this.login.getToken())
    this.login.peticionGet('http://127.0.0.1:8000/api/users/')
    .subscribe(res => {
      console.log(res)
    })
  }

  iniciarSesion(){
    let token = "";
    if(this.user.email.length > 3 && this.user.password.length > 7){
      const responseT = this.login.login('http://127.0.0.1:8000/api/auth/',this.user)
      .toPromise().then(res => {
        if (res['token'] != '0'){
          return res['token']
        }else{
          alert("El usuario no está registrado")
        }
      });
    

    const setToken = async() =>{
      token = await responseT
      this.login.setToken(token)
      this.traerUsuarios()
    }

    setToken()
    }else{
      alert('No cumple con el minimo de caracteres')
    }
  }

}
