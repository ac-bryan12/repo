import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';
import { Validacion } from 'src/assets/Validacion';


@Component({
  selector: 'profile-form',
  templateUrl: './profile-form.component.html',
  styleUrls: ['./profile-form.component.css']
})
export class ProfileFormComponent implements OnInit {
  public createAccount: FormGroup;
  response_d = ''
  response_content = ''
  id:string = ""
  msg:string =""
  usuario:any = {}
  listGrupos:any[]
  listPermisos :any[]
  listGruposSeleccionados :any []
  listPermisosSeleccionados :any[]
  listPermisosEmpresa:any[]
  public validate:Validacion = new Validacion();
  
  
  constructor(
    private router:Router,
    private service: RequestService,
    private fb: FormBuilder,
  ) {
    this.createAccount = this.fb.group({
      user: this.fb.group({
        first_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(3),Validators.maxLength(50)]),
        last_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(3),Validators.maxLength(50)]),
        password: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z0-9_:@.\-]+$'),Validators.minLength(8)]),
        confpassword: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9_:@.\-]+$')]),
        email: this.fb.control('', [Validators.required,Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'),Validators.minLength(7)]),
        token: this.fb.control('', [Validators.required,Validators.minLength(4)]),
        groups:''
      }),
      telefono: this.fb.control('', [Validators.required,Validators.minLength(10),Validators.maxLength(11)]),
      direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9._ ]+$')]),
      cargoEmpres: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(4),Validators.maxLength(50)],),

    })
    this.listGrupos = []
    this.listGruposSeleccionados =[]
    this.listPermisosSeleccionados = []
    this.listPermisos = []
    this.listPermisosEmpresa = []
  };

  ngOnInit(): void {
    this.enviar()
  }
  validacionPassword(){
    return this.validate.validarConfPassword(this.createAccount.get(["user","password"])?.value,this.createAccount.get(["user","confpassword"])?.value)    
  }
  enviar(){
    this.id = this.router.parseUrl(this.router.url).queryParams["id"]
    this.usuario = this.router.parseUrl(this.router.url).queryParams["usuario"]
    console.log(this.usuario.username)
    if(this.id != ""){
        this.service.peticionGet(`http://localhost:8000/api/user/getPermisosRoles/${this.id}`).subscribe((res)=>{
        console.log(res)
        for(let grupo of res.groups)
          this.listGruposSeleccionados.push(grupo.name)
        for(let permiso of res.permissions)
          this.listPermisosSeleccionados.push(permiso.codename)
      }, error =>{
        this.msg = "Ocurrió un error al cargar los datos"
        this.listGruposSeleccionados.push(this.msg)
        this.listPermisosSeleccionados.push(this.msg)
      })
    }
    this.service.peticionGet("http://localhost:8000/api/user/grupos/").subscribe((res)=>{
      for(let grupo of res){
        if(this.listGruposSeleccionados.indexOf(grupo.name)==-1)
          this.listGrupos.push(grupo.name)
      }
    }, error =>{
      this.msg = "Ocurrió un error al cargar los datos"
      this.listGrupos.push(this.msg)
    })
    this.service.peticionGet("http://localhost:8000/api/user/permisos").subscribe((res) =>{
      for(let permisosEmpresa of res){
        if(this.listPermisosSeleccionados.indexOf(permisosEmpresa.name)==-1)
          this.listPermisosEmpresa.push(permisosEmpresa)
      }
    }, error =>{
      this.msg = "Ocurrió un erro al cargar loas datos"
      this.listPermisosEmpresa.push(this.msg)
    })
    }

  enviarForm(values:any){
    values.user.groups = [
      {name:'admin_empresa'}
    ]
    console.log(values)
    // localStorage.setItem('token',values.usuario.token)
    this.service.peticionPost("http://localhost:8000/auth/create/",values,true).subscribe((res)=>{
      if(res['msg']!= ''){
        this.service.isCreatedAccount= true
        this.service.isRegistered = false
        this.router.navigate(['/creacion-exitosa'])
      }
    },(err:HttpErrorResponse)=>{
      if(err.error.hasOwnProperty('usuario')){
        if(err.error.usuario.hasOwnProperty('non_field_errors')){
          this.response_d = 'd-block'
          this.response_content = err.error.usuario.non_field_errors[0]
        }
      }else if(err.error.hasOwnProperty('empresa')){
        if(err.error.usuario.hasOwnProperty('non_field_errors')){
          this.response_d = 'd-block'
          this.response_content = err.error.empresa.non_field_errors[0]
        }
      }else{
        this.response_d = 'd-block'
        this.response_content = err.error[0]
      }
    
    })
  }
}
