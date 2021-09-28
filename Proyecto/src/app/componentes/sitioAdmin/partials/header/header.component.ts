import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';

@Component({
  selector: 'header-admin',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  constructor(private request:RequestService,private router:Router) { }

  ngOnInit(): void {
  }

  logout(){
    
    this.request.peticionPost('http://localhost:8000/auth/logout/',{}).subscribe(res =>{
      localStorage.setItem('Autenticated',"")
      this.router.navigate(['/login'])
    })
  }

}
