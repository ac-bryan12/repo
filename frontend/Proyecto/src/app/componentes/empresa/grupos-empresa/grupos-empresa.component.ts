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
  usuario: any = {}

  listGrupos: any[];
  listPermisos: any[];
  listGruposSeleccionados: any[];
  listPermisosSeleccionados: any[];
  listPermisosEmpresa: any[];
  msg: string = ""
  public addEmp: FormGroup;
  public validate: Validacion = new Validacion();


  constructor(private route: ActivatedRoute,
    private service: RequestService,
    private router: Router,
    private fb: FormBuilder) {
    this.addEmp = this.fb.group({
      user: this.fb.group({
        first_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'), Validators.minLength(3)]),
      })

    }
    )
    this.listGrupos = []
    this.listGruposSeleccionados = []
    this.listPermisosSeleccionados = []
    this.listPermisos = []
    this.listPermisosEmpresa = []
  }

  ngOnInit(): void {
    this.enviar()
  }

  enviarInfo(values: any) {
    console.log(values)
    let list: any = []
    for (let permiso of this.listPermisosSeleccionados) {
      list.push({ codename: permiso })
      values.user.permissions = list
    }

  }

  enviar() {
    this.id = this.router.parseUrl(this.router.url).queryParams["id"]
    this.usuario = this.router.parseUrl(this.router.url).queryParams["usuario"]
    if (this.usuario) {
      this.usuario = JSON.parse(this.usuario)
      this.addEmp.get(["user", "first_name"])?.setValue(this.usuario.user.first_name)
    }
    if (this.id) {
      this.service.peticionGet(environment.url + `/api/user/getPermisosRoles/${this.id}/`).subscribe((res) => {
        for (let permiso of res.permissions) {
          this.listPermisosSeleccionados.push(permiso)
        }
        this.permisosGrupos2()
      }, error => {
        this.msg = "Ocurrió un error al cargar los datos"
        this.listPermisosSeleccionados.push(this.msg)
      })
    }
    else {
      this.permisosGrupos2()
    }

  }

  permisosGrupos2() {
    this.service.peticionGet(environment.url + "/api/user/permisos/").subscribe((res) => {
      for (let permisosEmpresa of res.permissions) {
        if (this.listPermisosSeleccionados.indexOf(permisosEmpresa) == -1) {
          this.listPermisos.push(permisosEmpresa)
        }
      }
    }, error => {
      this.msg = "Ocurrió un erro al cargar los datos"
      this.listPermisos.push(this.msg)
    })

  }

  removeAll(nameLista: string) {
    let lista = this.listPermisosSeleccionados.splice(0, this.listPermisosSeleccionados.length)
    this.listPermisos = this.listPermisos.concat(lista)
  }

  asignarSelect(name: string, inputButton: any = null) {
    let input = document.getElementById(name) as HTMLSelectElement
    if (input.value != "" && input.value !== null && this.listPermisos.indexOf(input.value) != -1) {
      this.listPermisosSeleccionados.push(input.value)
      this.listPermisos.splice(this.listPermisos.indexOf(input.value), 1)
    }
  }


  removerSelect(name: string, inputButton: any = null) {
    let input = document.getElementById(name) as HTMLSelectElement

    if (input.value != "" && input.value !== null && this.listPermisosSeleccionados.indexOf(input.value) != -1) {
      this.listPermisos.push(input.value)
      this.listPermisosSeleccionados.splice(this.listPermisosSeleccionados.indexOf(input.value), 1)
    }
  }



}
