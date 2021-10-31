import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ThemePalette } from '@angular/material/core';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';
import { ActivatedRoute, Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';
import { Validacion } from 'src/assets/Validacion';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'editar-grupo',
  templateUrl: './grupos-empresa.component.html',
  styleUrls: ['./grupos-empresa.component.css']
})
export class GruposEmpresaComponent implements OnInit {
  response_d = ''
  response_content = ''
  // Progress Bar
  color: ThemePalette = 'primary';
  mode: ProgressSpinnerMode = 'indeterminate';
  loanding = false;

  id: string = ""
  name: any = ""

  listGrupos: any[];
  listPermisos: any[];
  listPermisosAsignados: any[];
  msg: string = ""
  public addGroup: FormGroup;
  public validate: Validacion = new Validacion();


  constructor(private route: ActivatedRoute,
    private service: RequestService,
    private router: Router,
    private fb: FormBuilder) {
    this.addGroup = this.fb.group({
      groups: this.fb.group({
        name: this.fb.control('', [Validators.required, Validators.pattern('^[0-9a-zA-ZñÑáéíóúÁÉÍÓÚ_.\-]+$'), Validators.minLength(3)]),
      })
    })
    this.listGrupos = []
    this.listPermisosAsignados = []
    this.listPermisos = []
  }

  ngOnInit(): void {
    this.inicializarValores()
  }

  enviarInfo(values: any) {
    let list: any = []
    for (let permiso of this.listPermisosAsignados) {
      list.push({ name: permiso })
      values.permissions = list
    }
    if(!this.id){
      
      this.service.peticionPost(environment.url+"/auth/userPermissions/",values).subscribe(res =>{
        alert(res.msg)
      },err =>{
        alert(err.error.error)
      })
    }else{
      values.id = this.id
      console.log(values)
      this.service.peticionPut(environment.url+"/auth/userPermissions/",values).subscribe(res =>{
        alert(res.msg)
      },err =>{
        alert(err.error.error)
      })
    }


  }

  inicializarValores() {
    this.id = this.router.parseUrl(this.router.url).queryParams["id"]
    this.name = this.router.parseUrl(this.router.url).queryParams["name"]
    
    if(this.id == '2' || this.id == '3' ){
      let formGroup : any = document.getElementById('group-form')
      formGroup.disabled = true
    }

    if (this.name && this.id) {
      this.addGroup.get(["groups","name"])?.setValue(this.name)
      this.service.peticionGet(environment.url + `/api/user/permisos/${this.id}/`).subscribe((res) => {
        for (let permiso of res.permissions) {
          this.listPermisosAsignados.push(permiso.name)
        }
        this.permisosGrupos2()
      }, error => {
        this.msg = "Ocurrió un error al cargar los datos"
        alert(this.msg)
      })
    }
    else {
      this.permisosGrupos2()
    }

  }

  permisosGrupos2() {
    this.service.peticionGet(environment.url + "/api/user/permisos/2/").subscribe((res) => {
      for (let permisos of res.permissions) {
        if (this.listPermisosAsignados.indexOf(permisos.name) == -1) {
          this.listPermisos.push(permisos.name)
        }
      }
    }, error => {
      this.msg = "Ocurrió un erro al cargar los datos"
      alert(this.msg)
    })

  }

  removeAll(nameLista: string) {
    let lista = this.listPermisosAsignados.splice(0, this.listPermisosAsignados.length)
    this.listPermisos = this.listPermisos.concat(lista)
  }

  asignarSelect(name: string, inputButton: any = null) {
    let input = document.getElementById(name) as HTMLSelectElement
    if (input.value != "" && input.value !== null && this.listPermisos.indexOf(input.value) != -1) {
      this.listPermisosAsignados.push(input.value)
      this.listPermisos.splice(this.listPermisos.indexOf(input.value), 1)
    }
  }


  removerSelect(name: string, inputButton: any = null) {
    let input = document.getElementById(name) as HTMLSelectElement

    if (input.value != "" && input.value !== null && this.listPermisosAsignados.indexOf(input.value) != -1) {
      this.listPermisos.push(input.value)
      this.listPermisosAsignados.splice(this.listPermisosAsignados.indexOf(input.value), 1)
    }
  }



}
