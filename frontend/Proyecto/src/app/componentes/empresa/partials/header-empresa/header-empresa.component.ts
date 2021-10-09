import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'header-empresa',
  templateUrl: './header-empresa.component.html',
  styleUrls: ['./header-empresa.component.css']
})
export class HeaderEmpresaComponent implements OnInit {

  constructor(private request:RequestService,private router:Router) { }

  ngOnInit(): void {
  }

  logout(){
    
    this.request.peticionPost(environment.url+'/auth/logout/',{}).subscribe(res =>{
      localStorage.setItem('Autenticated',"")
      this.router.navigate(['/login'])
    })
  }

}
