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
  listPermissions :any[]
  constructor(private service:RequestService, private cookie:CookieService, private router:Router,private route:ActivatedRoute){
    this.listGrupos = []
    this.listPermissions = []
  }

  ngOnInit(): void {
    this.listaGrupos()
    this.obtenerPermisos()
  }

  obtenerPermisos(){
    this.service.peticionGet(environment.url+"/auth/userPermissions/").subscribe(res =>{
      for(let permiso of res.permissions){
        this.listPermissions.push(permiso.codename)
      }
      console.log(this.listPermissions)
    },err =>{
      alert(err.error.error);
    })
  }

  listaGrupos(){
    this.service.peticionGet(environment.url+"/api/user/grupos/").subscribe((res)=>{
      this.listGrupos = res
    })
  }

  crearGrupo(){
    this.router.navigate(["../editarGrupos"],{relativeTo:this.route})
  }

  envioId(id:any){
    let grupoEnviar = null
    for(let grupo of this.listGrupos){
      if(grupo.id === id.innerText){
        grupoEnviar = grupo
      }    
    }
    id = id.innerText
    this.router.navigate(["../editarGrupos"],{relativeTo:this.route,queryParams:{id:id,name:grupoEnviar.name}})
  }

}
