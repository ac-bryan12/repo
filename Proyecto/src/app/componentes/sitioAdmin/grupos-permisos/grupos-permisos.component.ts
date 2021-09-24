import { Component, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';
import { CookieService } from 'ngx-cookie-service';
@Component({
  selector: 'app-grupos-permisos',
  templateUrl: './grupos-permisos.component.html',
  styleUrls: ['./grupos-permisos.component.css']
})
export class GruposPermisosComponent implements OnInit {
  listUsuarios :string[]
  constructor(private service:RequestService, private cookie:CookieService) { 

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
        console.log(user)
        campos.innerHTML += `<tr>
                                <td>${user.id}</td>
                                <td>${user.is_superuser}</td>
                                <td>${user.username}</td>
                                <td>${user.email}</td>
                                <td id="botones-acciones">
                                    <a  value="Editar" href="/editarUser" class="btn btn-primary btn-block">
                                    <a  value ="${user.id}"type="submit" value="Agregar grupo" class="d-none">
                                </td>
                            </tr>`
        
      }
          
    
    })
  }
}
