import { HttpErrorResponse } from '@angular/common/http';
import { NONE_TYPE } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { ThemePalette } from '@angular/material/core';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';
import { ActivatedRoute, Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';
import { Validacion } from 'src/assets/Validacion';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'pop-up',
  templateUrl: './pop-up.component.html',
  styleUrls: ['./pop-up.component.css']
})
export class PopUpComponent implements OnInit {
  // Progress Bar
  color: ThemePalette = 'primary';
  mode: ProgressSpinnerMode = 'indeterminate';
  loanding = false
  //Other variables
  tipo = ''
  public addEmp: FormGroup;
  public validate: Validacion = new Validacion();
  id: string = ""
  response_d = ''
  response_content = ''
  usuario: any = {}
  listGrupos: any[]
//  listPermisos: any[]
//  listGruposSeleccionados: any[]
  listPermisosSeleccionados: any[]
//  listPermisosEmpresa: any[]
  msg: string = ""
  constructor(
    private route: ActivatedRoute,
    private service: RequestService,
    private router: Router,
    private fb: FormBuilder) {
    this.addEmp = this.fb.group({
      user: this.fb.group({
        first_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'), Validators.minLength(3)]),
        last_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'), Validators.minLength(3)]),
        // password: this.fb.control('', [Validators.required, Validators.pattern('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[_.{}=<>;:,\+$@$!%*?&])[A-Za-z\d_.{}=<>;:,\+$@$!%*?&].{7,}')]),
        // confpassword: this.fb.control('', [Validators.required]),
        email: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._%+\-]+@[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9.\-]+\\.[a-zA-ZñÑáéíóúÁÉÍÓÚ]{2,4}'), Validators.minLength(7)]),
        groups: this.fb.control(''),
        permissions: this.fb.control('')
      }),
      telefono: this.fb.control('', [Validators.required, Validators.pattern('^[0-9]+$'), Validators.minLength(10)]),
      direccion: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._ ]+$'), Validators.minLength(4)]),
      cargoEmpres: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'), Validators.minLength(4)],),
      n_identificacion: this.fb.control('', [Validators.required, Validators.pattern('^[0-9]+$')]),
      tipo_identificacion: ""
    })
    this.listGrupos = []
    this.listPermisosSeleccionados = []
/*
    this.listPermisos = []
    this.listPermisosEmpresa = []
    */
  }

  ngOnInit(): void {
    this.tipo = "RUC"
    this.addEmp.get('tipo_identificacion')?.setValue("RUC")
    this.inicializarValores()
  }
  // validacionPassword(){
  //     return this.validate.validarConfPassword(this.addEmp.get(["user","password"])?.value,this.addEmp.get(["user","confpassword"])?.value)    
  // }

  validarGrupo(inputGrupo:any){
    if(inputGrupo.value != "" || inputGrupo.value != null){
      return true;
    }
    return false;
  }

  enviarInfo(values: any) {
    let list: any = []
/*
    for (let group of this.listGruposSeleccionados) {
      list.push({ name: group })
    }
*/
    values.user.groups = list
    
    if (this.id != "") {
      values.user.id = this.id
    }
    this.loanding = true;
    this.service.peticionPost(environment.url + "/api/user/asignarPermisosRoles/", values).subscribe((res) => {
      this.loanding = false;
      if (res['msg'] != '') {
        this.service.isCreatedAccount = true
        this.service.isRegistered = false
        alert("Proceso exitoso")
        this.router.navigate(["../grupos-permisos"], { relativeTo: this.route })
      }
    }, (err: HttpErrorResponse) => {
      this.loanding = false;
      if (err.error.hasOwnProperty('user')) {
        if (err.error.user.hasOwnProperty('non_field_errors')) {
          alert(err.error.user.non_field_errors[0])
        }
        if (err.error.user.hasOwnProperty('error')) {
          alert(err.error.user.error[0])
        }
      } else {
        alert(err.error.error[0])
      }
    })
  }

  inicializarValores() {
    this.id = this.router.parseUrl(this.router.url).queryParams["id"]
    this.usuario = this.router.parseUrl(this.router.url).queryParams["usuario"]
    if (this.usuario) {
      this.usuario = JSON.parse(this.usuario)
      this.addEmp.get(["user", "first_name"])?.setValue(this.usuario.user.first_name)
      this.addEmp.get(["user", "last_name"])?.setValue(this.usuario.user.last_name)
      // this.addEmp.get(["user","password"])?.setValue("") 
      this.addEmp.get(["user", "email"])?.setValue(this.usuario.user.email)
      this.addEmp.get("telefono")?.setValue(this.usuario.telefono)
      this.addEmp.get("direccion")?.setValue(this.usuario.direccion)
      this.addEmp.get("cargoEmpres")?.setValue(this.usuario.cargoEmpres)
      this.addEmp.get("n_identificacion")?.setValue(this.usuario.n_identificacion)
      let inputDNI: HTMLInputElement = document.getElementById(this.usuario.tipo_identificacion) as HTMLInputElement
      inputDNI.checked = true
      this.changeValue(this.usuario.tipo_identificacion)
    }

    this.service.peticionGet(environment.url + "/api/user/grupos/").subscribe((res) => {
      for (let grupo of res) {
          this.listGrupos.push(grupo)
      }
    }, error => {
      this.msg = "Ocurrió un error al cargar los datos"
      alert(this.msg)
    })

    if (this.id) {
      this.service.peticionGet(environment.url + `/api/user/getPermisosRoles/${this.id}/`).subscribe((res) => {
        
        for (let permiso of res.permissions) {
          this.listPermisosSeleccionados.push(permiso)
        }
        let inputGrupos : any = document.getElementById("grupos")
        inputGrupos.value = res.groups

      }, error => {
        this.msg = "Ocurrió un error al cargar los datos"
        //this.listGruposSeleccionados.push(this.msg)
        alert(this.msg)
      })
    }
    
  }
  buscarPermisos(grupoId:any) {
    console.log(grupoId)
/*
    this.service.peticionGet(environment.url + "/api/user/permisos/"+ grupoId+"/").subscribe((res) => {
      
      this.listPermisosSeleccionados = []
      
      for (let permisosEmpresa of res.permissions) {
        this.listPermisosSeleccionados.push(permisosEmpresa)
      }
    }, error => {
      this.msg = "Ocurrió un erro al cargar los datos"
      alert(this.msg)
    })
    */

  }

  // asignarSelect(name: string, inputButton: any = null) {
  //   let 
  //   let input = document.getElementById(name) as HTMLSelectElement
  //   if (name === "grupos") {
  //     if (input.value != "" && input.value !== null && this.listGrupos.indexOf(input.value) != -1) {
  //       this.listGruposSeleccionados.push(input.value)
  //       this.listGrupos.splice(this.listGrupos.indexOf(input.value), 1)
  //     }
  //   } else {
  //     if (input.value != "" && input.value !== null && this.listPermisos.indexOf(input.value) != -1) {
  //       this.listPermisosSeleccionados.push(input.value)
  //       this.listPermisos.splice(this.listPermisos.indexOf(input.value), 1)
  //     }
  //   }
  // }
  
  

  changeValue(text: any) {
    this.tipo = text
    let input = document.getElementById("n_identificacion") as HTMLElement
    input.innerText = this.tipo
  }

  validarRucCedula() {
    let tipo = this.addEmp.get('n_identificacion')?.value
    let identificadores = document.querySelector('input[name="tipo"]:checked') as HTMLInputElement
    this.addEmp.get("tipo_identificacion")?.setValue(identificadores.value)
    if (identificadores.value == 'CEDULA') {
      return !this.validate.validarRuc(tipo, 10)
    }
    return !this.validate.validarRuc(tipo)
  }
}
