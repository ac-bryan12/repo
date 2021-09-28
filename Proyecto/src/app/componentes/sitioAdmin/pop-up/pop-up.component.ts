import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder,Validators} from '@angular/forms';
import { Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';

@Component({
  selector: 'pop-up',
  templateUrl: './pop-up.component.html',
  styleUrls: ['./pop-up.component.css']
})
export class PopUpComponent implements OnInit {
  public addEmp: FormGroup;
  id:string = ""
  listGrupos:any[]
  listPermisos :any[]
  listGruposSeleccionados :any []
  listPermisosSeleccionados :any[]
  constructor(
    private service: RequestService,
    private router:Router,
    private fb: FormBuilder) {
    this.addEmp = this.fb.group({
      user: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$'),Validators.maxLength(13),Validators.minLength(13),]),
        permisos: this.fb.control('', [Validators.required,Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'),Validators.minLength(7)]),
        razonSocial: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9. ]+$'),Validators.minLength(5), Validators.maxLength(50)]),
        telefono: this.fb.control('', [Validators.required,Validators.minLength(10),Validators.maxLength(11)]),
        direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9._ ]+$')])
    })
    this.listGrupos = []
    this.listGruposSeleccionados =[]
    this.listPermisosSeleccionados = []
    this.listPermisos = []
  }

  ngOnInit(): void {
    this.enviar()
    }

  enviar(){
    let info = {
      ruc:this.addEmp.get('ruc'),
      razonSocial: this.addEmp.get('razonSocial'),
      telefono: this.addEmp.get('telefono'),
      direccion: this.addEmp.get('direccion')
    }
    this.id = this.router.parseUrl(this.router.url).queryParams["id"]
    if(this.id != ""){
        this.service.peticionGet(`http://localhost:8000/api/user/getPermisosRoles/${this.id}`).subscribe((res)=>{
        console.log(res)
        for(let grupo of res.groups)
          this.listGruposSeleccionados.push(grupo.name)
        for(let permiso of res.permissions)
          this.listPermisosSeleccionados.push(permiso.codename)
      })
    }
    this.service.peticionGet("http://localhost:8000/api/user/grupos/").subscribe((res)=>{
      for(let grupo of res){
        if(this.listGruposSeleccionados.indexOf(grupo.name)==-1)
          this.listGrupos.push(grupo.name)
      }
    })
    }

    asignarSelect(name:string){
      let input = document.getElementById(name) as HTMLSelectElement
      if(name ==="grupos"){     
        if(input.value != "" && input.value !==null && this.listGrupos.indexOf(input.value)!=-1){
            this.listGruposSeleccionados.push(input.value)
            this.listGrupos.splice(this.listGrupos.indexOf(input.value),1)
        }
      }else{
        if(input.value != "" && input.value !==null && this.listPermisos.indexOf(input.value)!=-1){
          this.listPermisosSeleccionados.push(input.value)
          this.listPermisos.splice(this.listPermisos.indexOf(input.value),1)
        }
      }
    }
    removerSelect(name:string){
      let input = document.getElementById(name) as HTMLSelectElement
      if(name == "gruposSelect"){
        if(input.value != "" && input.value !==null && this.listGruposSeleccionados.indexOf(input.value)!=-1){
          this.listGrupos.push(input.value)
          this.listGruposSeleccionados.splice(this.listGruposSeleccionados.indexOf(input.value),1)
        }
      }else{
        if(input.value != "" && input.value !==null && this.listPermisosSeleccionados.indexOf(input.value)!=-1){
          this.listPermisos.push(input.value)
          this.listPermisosSeleccionados.splice(this.listPermisosSeleccionados.indexOf(input.value),1)
        }  
      } 
    }
    removeAll(nameLista:string){
      if(nameLista === "Grupos"){
        let lista = this.listGruposSeleccionados.splice(0,this.listGruposSeleccionados.length) 
        this.listGrupos = this.listGrupos.concat(lista)
      }else{
        let lista = this.listPermisosSeleccionados.splice(0,this.listPermisosSeleccionados.length) 
        this.listPermisos = this.listPermisos.concat(lista)
      }

    }

}
