import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { RequestService } from 'src/app/services/request/request.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'list-grupos',
  templateUrl: './list-grupos.component.html',
  styleUrls: ['./list-grupos.component.css']
})
export class ListGruposComponent implements OnInit {
  listGrupos :any[]
  constructor(private service:RequestService, private cookie:CookieService, private router:Router,private route:ActivatedRoute){
    this.listGrupos = []
  }

  ngOnInit(): void {
  }

  listaGrupos(){
    this.service.peticionGet(environment.url+"/api/user/grupos/").subscribe((res)=>{
      this.listGrupos = res.profile
    })
  }

  crearGrupo(){
    this.router.navigate(["../editarGrupos"],{relativeTo:this.route})
  }
}
