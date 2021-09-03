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
    var cook =this.cookie.get("permissions")
    console.log(cook)
    var coo =JSON.parse(decodeURI(cook.replace(/\\054/g, ',')))
    console.log(JSON.parse(coo)[0]['codename'])
    // this.listGrupos = []
    // this.listPermisos = []
  }

}
