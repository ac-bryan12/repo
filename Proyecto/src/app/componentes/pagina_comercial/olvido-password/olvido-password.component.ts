import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';

@Component({
  selector: 'olvido-password',
  templateUrl: './olvido-password.component.html',
  styleUrls: ['./olvido-password.component.css']
})
export class OlvidoPasswordComponent implements OnInit {
  msg  =""
  response_d = ''
  response_content = ''
  constructor(private service:RequestService, private router:Router) { }
  
  ngOnInit(): void {
  }

  restablecer(email:any){
    //Verificar que si el correo existe en el sistema, verificar que no sea un cliente
    this.response_content = "Espere unos segundos, revise su correo por favor"
    this.response_d = "d-block"
    this.service.peticionGet("http://localhost:8000/auth/reset_password_token/"+email, true).subscribe((res)=>{
      this.router.navigate(["/restablecer-password"])
    }, error=>{
      if(error.hasOwnProperty("error")){
        this.response_content = "No existe en el sistema"
      }
    })
  }
}
