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
  constructor(private service:RequestService, private cookie:CookieService) { 
    this.listGrupos = []
    this.listPermisos = []
  }

  ngOnInit(): void {
  }

  listar(){
    var cook =this.cookie.get("group")
    console.log(cook)
    var coo =JSON.parse(decodeURIComponent(cook))
    console.log(coo)
    var coo2 = coo.replace("[","").replace("]","").replaceAll("'","").substring(1,coo.length-1)
    console.log(coo2) 
    console.log(JSON.parse(coo2))
    this.listGrupos = []
    this.listPermisos = []
  }

}
