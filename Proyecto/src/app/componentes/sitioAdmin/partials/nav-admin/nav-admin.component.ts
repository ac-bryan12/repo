import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { RequestService } from 'src/app/services/request/request.service';

@Component({
  selector: 'nav-admin',
  templateUrl: './nav-admin.component.html',
  styleUrls: ['./nav-admin.component.css']
})
export class NavAdminComponent implements OnInit {
  viewEmpresaTemp:boolean
  viewEmpresa:boolean
  viewUser:boolean
  isUser:boolean
  private listGrupos: string[]

  constructor(private request: RequestService, private cookie: CookieService) {
    this.isUser = false
    this.viewEmpresaTemp = false
    this.viewEmpresa = false
    this.viewUser = false
    this.listGrupos = []
  }
  ngOnInit(): void {
    
    this.grupos_permisos()

    
  }


  async grupos_permisos() {
    return await this.request.peticionGet("http://localhost:8000/auth/userPermissions/").subscribe(res=>{
      // setTimeout('', 500);
      let group = this.cookie.get('group')
      let groupFormated = JSON.parse(decodeURI(group.replace(/\\054/g, ',')))
      let groupName = JSON.parse(groupFormated)[0]['name']
      if(groupName == 'admin_empresa'){
        this.isUser = true
      }else if(groupName == 'admin_facturacion'){
        console.log("Si entra")
        this.mostrarMenus(this.cookie.get('permissions'))
      }
    })
  }

  mostrarMenus(permissions: string) {

    let permissionsFormated = JSON.parse(decodeURI(permissions.replace(/\\054/g, ',')))
    let permissionsName = JSON.parse(permissionsFormated)
    permissionsName.forEach((permission: any) => {
      permission = permission['codename']
      if (permission == 'view_empresatemp') {
        this.viewEmpresaTemp = true
      }
      if (permission == 'view_empresa') {
        this.viewEmpresa = true
      }
      if (permission == 'view_user') {
        this.viewUser = true
      }

    }
    );

  }
}
