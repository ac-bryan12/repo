import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { RequestService } from 'src/app/services/request/request.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'header-empresa',
  templateUrl: './header-empresa.component.html',
  styleUrls: ['./header-empresa.component.css']
})
export class HeaderEmpresaComponent implements OnInit {

  constructor(private request:RequestService,private router:Router,private cookie: CookieService ) { }

  ngOnInit(): void {
  }

  logout(){
    
    this.request.peticionPost(environment.url+'/auth/logout/',{}).subscribe(res =>{
      localStorage.setItem('Autenticated',"")
    })
    localStorage.setItem('token','')
    this.cookie.set("return_to","/login",{"path":"/"})
    this.router.navigate(['/login'])
  }

}