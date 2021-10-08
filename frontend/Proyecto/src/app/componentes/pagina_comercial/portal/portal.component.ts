import { Component, OnInit } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-portal',
  templateUrl: './portal.component.html',
  styleUrls: ['./portal.component.css']
})
export class PortalComponent implements OnInit {
  
  constructor(private request:RequestService,private router:Router) { }
  
  ngOnInit(): void {
  }

  logout(){
    
    this.request.peticionPost(environment.url+'/auth/logout/',{}).subscribe(res =>{
      console.log(res['estado'])
      localStorage.setItem('Autenticated',"")
      this.router.navigate(['/home'])
    })
  }

}
