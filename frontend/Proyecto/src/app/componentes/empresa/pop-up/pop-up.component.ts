import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder,Validators} from '@angular/forms';
import { Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';
import { Validacion } from 'src/assets/Validacion';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'pop-up',
  templateUrl: './pop-up.component.html',
  styleUrls: ['./pop-up.component.css']
})
export class PopUpComponent implements OnInit {
  public addEmp: FormGroup;
  public validate:Validacion = new Validacion();
  id:string = ""
  response_d = ''
  response_content = ''
  usuario:any = {}
  listGrupos:any[]
  listPermisos :any[]
  listGruposSeleccionados :any []
  listPermisosSeleccionados :any[]
  listPermisosEmpresa:any[]
  msg:string =""
  constructor(
    private service: RequestService,
    private router:Router,
    private fb: FormBuilder) {
    this.addEmp = this.fb.group({
      user: this.fb.group({
        first_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(3),Validators.maxLength(50)]),
        last_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(3),Validators.maxLength(50)]),
        password: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z0-9_:@.\-]+$'),Validators.minLength(8)]),
        confpassword: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9_:@.\-]+$')]),
        email: this.fb.control('', [Validators.required,Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'),Validators.minLength(7)]),
        groups:this.fb.control(''),
        permissions: this.fb.control('')
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
  }

  ngOnInit(): void {
    this.enviar()
    }
  validacionPassword(){
      return this.validate.validarConfPassword(this.addEmp.get(["user.password"])?.value,this.addEmp.get(["user.confpassword"])?.value)    
  }

  enviarInfo(values:any){
    console.log(values)
    let list:any = []
    for(let group of this.listGruposSeleccionados){
      list.push({name:group})
    }
    values.user.groups = list
    list = []
    for(let permiso of this.listPermisosSeleccionados){
      list.push({codename:permiso})
    }
    values.user.permissions = list
    if(this.id!="")
      values.user.id =this.id
    // localStorage.setItem('token',values.usuario.token)
    this.service.peticionPost(environment.url+"/api/user/asignarPermisosRoles/",values).subscribe((res)=>{
      if(res['msg']!= ''){
        this.service.isCreatedAccount= true
        this.service.isRegistered = false
        alert("Proceso exitoso")
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

  enviar(){
    this.id = this.router.parseUrl(this.router.url).queryParams["id"]
    this.usuario = this.router.parseUrl(this.router.url).queryParams["usuario"] 
    if(this.usuario){
      this.usuario = JSON.parse(this.usuario)
      this.addEmp.get(["user","first_name"])?.setValue(this.usuario.user.first_name)
      this.addEmp.get(["user","last_name"])?.setValue(this.usuario.user.last_name)   
      this.addEmp.get(["user","password"])?.setValue("") 
      this.addEmp.get(["user","email"])?.setValue(this.usuario.user.email)
      this.addEmp.get("telefono")?.setValue(0+this.usuario.telefono) 
      this.addEmp.get("direccion")?.setValue(this.usuario.direccion) 
      this.addEmp.get("cargoEmpres")?.setValue(this.usuario.cargoEmpres)  
    }
    if(this.id != ""){
        this.service.peticionGet(environment.url+`/api/user/getPermisosRoles/${this.id}`).subscribe((res)=>{
        for(let grupo of res.groups){
          this.listGruposSeleccionados.push(grupo)
        } 
        for(let permiso of res.permissions){
          this.listPermisosSeleccionados.push(permiso)
        }
        this.permisosGrupos2()
      }, error =>{
        this.msg = "Ocurrió un error al cargar los datos"
        this.listGruposSeleccionados.push(this.msg)
        this.listPermisosSeleccionados.push(this.msg)
      })
    }
    else{
      this.permisosGrupos2()
    }
  }
  permisosGrupos2(){
    this.service.peticionGet(environment.url+"/api/user/grupos/").subscribe((res)=>{
            for(let grupo of res){
              if(this.listGruposSeleccionados.indexOf(grupo)==-1){
                this.listGrupos.push(grupo)
              }
            }
          }, error =>{
            this.msg = "Ocurrió un error al cargar los datos"
            this.listGrupos.push(this.msg)
          })
    this.service.peticionGet(environment.url+"/api/user/permisos").subscribe((res) =>{
            for(let permisosEmpresa of res.permissions){
              if(this.listPermisosSeleccionados.indexOf(permisosEmpresa)==-1){
                this.listPermisos.push(permisosEmpresa)
              }  
            }
          }, error =>{
            this.msg = "Ocurrió un erro al cargar los datos"
            this.listPermisos.push(this.msg)
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
