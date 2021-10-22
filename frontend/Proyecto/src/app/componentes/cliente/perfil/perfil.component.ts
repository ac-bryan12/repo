import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { RequestService } from 'src/app/services/request/request.service';
import { Validacion } from 'src/assets/Validacion';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'perfil',
  templateUrl: './perfil.component.html',
  styleUrls: ['./perfil.component.css']
})
export class PerfilComponent implements OnInit {
  public profile: FormGroup;
  public validate: Validacion = new Validacion;
  tipo = ''
  constructor(
    private fb: FormBuilder,
    private service: RequestService
  ) {
    this.profile = this.fb.group({
      user: this.fb.group({
        id:"",
        first_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'), Validators.minLength(3), Validators.maxLength(50)]),
        last_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'), Validators.minLength(3), Validators.maxLength(50)]),
        email: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._%+\-]+@[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9.\-]+\\.[a-zA-ZñÑáéíóúÁÉÍÓÚ]{2,4}'), Validators.minLength(7)]),
      }),
      n_identificacion: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$')]),
      tipo_identificacion:"",
      direccion: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._ ]+$')]),
      telefono: this.fb.control('', [Validators.required, Validators.pattern('^[0-9]+$'), Validators.minLength(10)]),
    })
    this.tipo = 'RUC'
  }

  ngOnInit(): void {
    this.obtenerInfo()
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
    this.service.peticionPost(environment.url+"/api/user/PerfilInfo/",value).subscribe(res =>{
      alert(res.msg)
    },err =>{
      alert(err.error);
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

    },err =>{
      alert("Ha ocurrido un error al cargar los datos.")
    })
  }
}
