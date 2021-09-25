import { Component, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-grupos-permisos',
  templateUrl: './grupos-permisos.component.html',
  styleUrls: ['./grupos-permisos.component.css']
})
export class GruposPermisosComponent implements OnInit {
  listUsuarios :any[]
  constructor(private service:RequestService, private cookie:CookieService, private router:Router) { 

    this.listUsuarios = []
  }

  ngOnInit(): void {
    this.listaUsuarios()
  }

  listaUsuarios(){
    
    this.service.peticionGet("http://localhost:8000/api/lista-de-users").subscribe((res)=>{
      var campos = document.getElementById("usuarios") as HTMLElement
      this.listUsuarios = res
    })
  }
  envioId(id:any){
    console.log(id)
    let id2 = id as HTMLElement
    this.router.navigate(["/editarUser"],{queryParams:{id:id2.innerText}})
  }
}
