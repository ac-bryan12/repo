import { Component, OnInit } from '@angular/core';
import { ThemePalette } from '@angular/material/core';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';
import { Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'olvido-password',
  templateUrl: './olvido-password.component.html',
  styleUrls: ['./olvido-password.component.css']
})
export class OlvidoPasswordComponent implements OnInit {
  // Progress Bar
  color: ThemePalette = 'primary';
  mode: ProgressSpinnerMode = 'indeterminate';
  loanding = false
  //Other variables
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
<<<<<<< Updated upstream
    this.loanding = true;
=======
>>>>>>> Stashed changes
    this.service.peticionGet(environment.url+"/auth/reset_password_token/"+email+"/", true).subscribe((res)=>{
      this.router.navigate(["/restablecer-password"])
      this.loanding = false;
    }, error=>{
      if(error.hasOwnProperty("error")){
        this.loanding = false;
        this.response_content = "No existe en el sistema"
        
      }
    })
  }
}
