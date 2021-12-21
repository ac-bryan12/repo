import { Component, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';
import { CookieService } from 'ngx-cookie-service';
import { ActivatedRoute, Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { reference } from '@popperjs/core';

@Component({
  selector: 'app-grupos-permisos',
  templateUrl: './list-users.component.html',
  styleUrls: ['./list-users.component.css']
})
export class ListUsersComponent implements OnInit {
  listUsuarios :any[]
  agregarUsuario = "disabled"
  editarUsuario = "disabled"
  eliminarUsuario = "disabled"
  nombreDocumento = ""
  constructor(private service:RequestService, private cookie:CookieService, private router:Router,private route:ActivatedRoute) { 

    this.listUsuarios = []
  }

  ngOnInit(): void {
    //this.listaUsuarios()
    this.habilitarControles()
  }

  habilitarControles(){
    this.service.peticionGet(environment.url+"/auth/userPermissions/").subscribe(res => {
      for(let permiso of res.permissions){
        if(permiso.codename == 'add_user'){
          this.agregarUsuario = ""
        }
        if(permiso.codename == 'change_user'){
          this.editarUsuario = ""
        }
        if(permiso.codename == 'delete_user'){
          this.eliminarUsuario = ""
        }
      }
    })
  }

  /*listaUsuarios(){
    this.service.peticionGet(environment.url+"/api/user/lista-de-profiles/").subscribe((res)=>{
      this.listUsuarios = res.results
    })
  }
  */
  
  envioId(id:any){
    let usuario = {}
    for(let user of this.listUsuarios){
      if(user.user.id === id.innerText){
        usuario = user
      }    
    }
    let id2 = id as HTMLElement
    this.router.navigate(["../editarUser"],{relativeTo:this.route,queryParams:{id:id2.innerText,usuario:JSON.stringify(usuario)}})
  }
  crearUser(){
    this.router.navigate(["../editarUser"],{relativeTo:this.route})
  }

  borrarUser(id:any){
    let continuar = confirm("¿Seguro que desea eliminar este usuario?")
    if(continuar){
      this.service.peticionDelete(environment.url+"/api/user/asignarPermisosRoles/"+id.innerText+"/").subscribe(res=>{
        alert(res.msg)
        window.location.reload()
      },err =>{
        alert(err.error.error)
      })
    }
    
  }

  obtenerObjetos(listUser:any){
    this.listUsuarios = listUser
  }

  buscador(nombre:any){
    if(nombre == ""){
      this.nombreDocumento = ""
    }
    else{
      this.nombreDocumento = "?name="+nombre.value
    }
  }
}