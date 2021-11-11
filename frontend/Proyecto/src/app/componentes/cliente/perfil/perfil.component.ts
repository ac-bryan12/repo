import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ThemePalette } from '@angular/material/core';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';
import { Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';
import { Validacion } from 'src/assets/Validacion';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'perfil',
  templateUrl: './perfil.component.html',
  styleUrls: ['./perfil.component.css']
})
export class PerfilComponent implements OnInit {
  // Progress Bar
  color: ThemePalette = 'primary';
  mode: ProgressSpinnerMode = 'indeterminate';
  loanding = false
  //Other variables
  public profile: FormGroup;
  public validate: Validacion = new Validacion;
  tipo = ''
  permissions: any = []

  constructor(
    private fb: FormBuilder,
    private service: RequestService,
    private router: Router,
  ) {
    this.profile = this.fb.group({
      user: this.fb.group({
        id:"",
        first_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'), Validators.minLength(3)]),
        last_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'), Validators.minLength(3)]),
        email: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._%+\-]+@[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9.\-]+\\.[a-zA-ZñÑáéíóúÁÉÍÓÚ]{2,4}'), Validators.minLength(7)]),
      }),
      n_identificacion: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$')]),
      tipo_identificacion:"",
      direccion: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._ ]+$'),Validators.minLength(4)]),
      telefono: this.fb.control('', [Validators.required, Validators.pattern('^[0-9]+$'), Validators.minLength(10)]),
    })
    this.tipo = 'RUC'
  }

  async ngOnInit(){
    this.obtenerPermisos()
  }

  changeTipo(value: any) {
    this.tipo = value
    let input = document.getElementById("n_identificacion") as HTMLElement
    input.innerText = this.tipo
  }

  validarRucCedula(){
    let dni = this.profile.get('n_identificacion')?.value
    let identificadores = document.querySelector('input[name="tipo"]:checked') as HTMLInputElement
    if(identificadores.value == 'CEDULA'){
      return !this.validate.validarRuc(dni,10)
    }
    return !this.validate.validarRuc(dni)
  }

  actualizarInfo(value: any){
    this.loanding = true;
    this.service.peticionPost(environment.url+"/api/user/PerfilInfo/",value).subscribe(res =>{
      this.loanding = false;
      alert(res.msg)
    },err =>{
      this.loanding = false;
      alert(err.error.error);
    })
  }

  obtenerInfo(){
    this.service.peticionGet(environment.url+"/api/user/PerfilInfo/").subscribe(res =>{
      let profile = res.profile
      this.profile.get(["user","first_name"])?.setValue(profile.user.first_name)
      this.profile.get(["user","last_name"])?.setValue(profile.user.last_name)
      this.profile.get(["user","email"])?.setValue(profile.user.email)
      this.profile.get(["user","id"])?.setValue(profile.user.id)
      this.profile.get(["n_identificacion"])?.setValue(profile.n_identificacion)
      this.profile.get(["tipo_identificacion"])?.setValue(profile.tipo_identificacion)
      this.profile.get(["direccion"])?.setValue(profile.direccion)
      this.profile.get(["telefono"])?.setValue(profile.telefono)
      this.changeTipo(profile.tipo_identificacion)
      let dni:HTMLInputElement = document.getElementById(profile.tipo_identificacion) as HTMLInputElement
      dni.checked = true
      this.desabilitarForm()
    },err =>{
      if(err.error.error == undefined){
        alert("Ha ocurrido un error al cargar los datos.")
      }else{
        alert(err.error.error);
      }
    })
  }

  async obtenerPermisos(){
    this.service.peticionGet(environment.url+"/auth/userPermissions/").subscribe(res =>{
      this.permissions = res.permissions
      let form:any = document.getElementById('perfil_form')
      form.disabled = true
      let continuar = true
      for (let permiso of this.permissions){
        if(permiso.codename == 'change_profile'){
          form.disabled = false
        }

        if(permiso.codename == 'view_empresatemp'){
          this.router.navigate(['/portal/empresasTemp'])
          continuar = false          
        }
      }

      if(continuar){
        this.obtenerInfo()
      }
      
    },err =>{
      alert('Ocurrió un error al cargar los permisos, por favor recargue la página.')
    })
  }

  desabilitarForm(){
    let form:any = document.getElementById('perfil_form')
    form.disabled = true
    for (let permiso of this.permissions){
      if(permiso.codename == 'change_profile'){
        form.disabled = false
        break
      }
    }
    
  }
}
