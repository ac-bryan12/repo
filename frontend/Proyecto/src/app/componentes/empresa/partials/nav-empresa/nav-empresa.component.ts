import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
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
    "add_user":false,
    "view_group":false,
    "add_group":false,
    "view_empresatemp":false,
    "view_documentos_emitidos":false,
    "view_documentos_recibidos":false
  }
  
  env = environment.url
  constructor(private request: RequestService,private router: Router,private route:ActivatedRoute) { 
    
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

  documentos(tipo:string){
    this.router.navigate(['./documentos'],{relativeTo:this.route ,queryParams:{tipo:tipo}}).then(()=>{
      window.location.reload()
    })
  }

  submenu(li:HTMLLIElement){
    let icon:any = li.getElementsByClassName('arrow')[0]
    icon.classList.toggle('rotate-45')
    let ul:any = document.querySelector("li:hover + ul")
    ul.classList.toggle('d-block')
  }
}
