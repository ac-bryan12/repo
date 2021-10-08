import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';

@Component({
  selector: 'header-client',
  templateUrl: './header-client.component.html',
  styleUrls: ['./header-client.component.css']
})
export class HeaderClientComponent implements OnInit {

  constructor(private request:RequestService,private router:Router) { }

  ngOnInit(): void {
  }

  logout(){
    
    this.request.peticionPost('http://localhost:8000/api/logout/',{}).subscribe(res =>{
      localStorage.setItem('Autenticated',"")
      this.router.navigate(['/login'])
    })
  }
}
