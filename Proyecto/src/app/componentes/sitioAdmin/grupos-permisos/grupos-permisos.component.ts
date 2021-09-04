import { Component, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';
import { CookieService } from 'ngx-cookie-service';
@Component({
  selector: 'app-grupos-permisos',
  templateUrl: './grupos-permisos.component.html',
  styleUrls: ['./grupos-permisos.component.css']
})
export class GruposPermisosComponent implements OnInit {
  listGrupos:string[]
  listPermisos :string[]
  listUsuarios :string[]
  constructor(private service:RequestService, private cookie:CookieService) { 
    this.listGrupos = []
    this.listPermisos = []
    this.listUsuarios = []
  }

  ngOnInit(): void {
    this.listaUsuarios()
  }

  listaUsuarios(){
    
    this.service.peticionGet("http://localhost:8000/api/lista-de-users").subscribe((res)=>{
      this.listUsuarios = res
      var campos = document.getElementById("usuarios") as HTMLElement
      for(let user of res){
        campos.innerHTML += `<tr>
                                <td>${user.id}</td>
                                <td>${user.is_superuser}</td>
                                <td>${user.username}</td>
                                <td>${user.email}</td>
                                <td id="botones-acciones">
                                    <input id="btn" value="Agregar grupo" type="submit" value="Agregar accion" class="btn btn-primary btn-block">
                                    <input value ="${user.id}"type="submit" value="Agregar grupo" class="d-none">
                                </td>
                            </tr>`
      }
          
    
    })
    this.service.peticionGet("http://localhost:8000/api/grupos").subscribe((res)=>{
      for(let grupo of res){
        this.listGrupos.push(grupo.name)
      }
    })
   
    this.service.peticionGet("http://localhost:8000/api/permisos").subscribe((res)=>{
      for(let grupo of res){
        this.listPermisos.push(grupo.name)
      }
    })
    var btn = document.getElementById("btn")
    
  }

  
}
