import { Component, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'nav-empresa',
  templateUrl: './nav-empresa.component.html',
  styleUrls: ['./nav-empresa.component.css']
})
export class NavEmpresaComponent implements OnInit {
  permissions: any = {
    "view_profile": false,
    "change_profile":false,
    "view_empresa":false,
    "view_user":false,
    "view_group":false,
    "view_empresatemp":false,
    "view_documentos":false,
  }
  

  constructor(private request: RequestService) { 
    
  }

  ngOnInit(): void {
    this.habilitarMenus()
  }

  habilitarMenus(){
    this.request.peticionGet(environment.url+"/auth/userPermissions/").subscribe( res => {
      for(let permiso of res.permissions){
        if (permiso.codename in this.permissions){
          this.permissions[permiso.codename] = true
        }
      }
    }
    ,err => {
      console.log("Error al cargar permisos")
    })

  }
}
