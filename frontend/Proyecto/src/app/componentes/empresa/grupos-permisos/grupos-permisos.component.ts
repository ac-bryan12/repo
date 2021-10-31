import { Component, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';
import { CookieService } from 'ngx-cookie-service';
import { ActivatedRoute, Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { reference } from '@popperjs/core';

@Component({
  selector: 'app-grupos-permisos',
  templateUrl: './grupos-permisos.component.html',
  styleUrls: ['./grupos-permisos.component.css']
})
export class GruposPermisosComponent implements OnInit {
  listUsuarios :any[]
  constructor(private service:RequestService, private cookie:CookieService, private router:Router,private route:ActivatedRoute) { 

    this.listUsuarios = []
  }

  ngOnInit(): void {
    this.listaUsuarios()
  }

  listaUsuarios(){
    this.service.peticionGet(environment.url+"/api/user/lista-de-profiles/").subscribe((res)=>{
      this.listUsuarios = res.profile
    })
  }
  
  envioId(id:any){
    let usuario = {}
    for(let user of this.listUsuarios){
      if(user.user.id === id.innerText){
        user.empresa = null
        usuario = user
      }    
    }
    let id2 = id as HTMLElement
    this.router.navigate(["../editarUser"],{relativeTo:this.route,queryParams:{id:id2.innerText,usuario:JSON.stringify(usuario)}})
  }
  crearUser(){
    this.router.navigate(["../editarUser"],{relativeTo:this.route})
  }

}
