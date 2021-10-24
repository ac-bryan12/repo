import { Component, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';
import { HttpErrorResponse } from '@angular/common/http';
import { FormBuilder,FormGroup, ValidatorFn,Validators} from '@angular/forms';
import { Validacion } from 'src/assets/Validacion';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { ThemePalette } from '@angular/material/core';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-create-cuenta',
  templateUrl: './create-cuenta.component.html',
  styleUrls: ['./create-cuenta.component.css']
})

export class CreateCuentaComponent implements OnInit {
  // Progress Bar
  color: ThemePalette = 'primary';
  mode: ProgressSpinnerMode = 'indeterminate';
  loanding = false
  //Other variables
  public createAccount: FormGroup;
  response_d = ''
  response_content = ''
  public validate:Validacion = new Validacion();
  btn:any;
  constructor(
    private router:Router,
    private envio: RequestService,
    private fb: FormBuilder
  ) {
    this.createAccount = this.fb.group({
      empresa: this.fb.group({
        ruc: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$'),Validators.minLength(13),]),
        correo: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._%+\-]+@[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9.\-]+\\.[a-zA-ZñÑáéíóúÁÉÍÓÚ]{2,4}'),Validators.minLength(7)]),
        razonSocial: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9. ]+$'),Validators.minLength(3)]),
        telefono: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$'),Validators.minLength(10)]),
        direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._ ]+$'),Validators.minLength(4)])
      }),
      user: this.fb.group({
        first_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'),Validators.minLength(3)]),
        last_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'),Validators.minLength(3)]),
        password: this.fb.control('', [Validators.required, Validators.pattern('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[_.{}=<>;:,\+$@$!%*?&])[A-Za-z\d_.{}=<>;:,\+$@$!%*?&].{7,}')]),
        confpassword: this.fb.control('', [Validators.required,Validators.pattern('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[_.{}=<>;:,\+$@$!%*?&])[A-Za-z\d_.{}=<>;:,\+$@$!%*?&].{7,}')]),
        email: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._%+\-]+@[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9.\-]+\\.[a-zA-ZñÑáéíóúÁÉÍÓÚ]{2,4}'),Validators.minLength(7)]),
        groups:''
      }),
      n_identificacion: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$'),Validators.minLength(10),]),
      tipo_identificacion: "CEDULA" ,
      telefono: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$'),Validators.minLength(10)]),
      direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._ ]+$'),Validators.minLength(4)]),
      cargoEmpres: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'),Validators.minLength(4)],),
      token: this.fb.control('', [Validators.required,Validators.minLength(4)]),

    });
    this.btn = null;
  };

  ngOnInit(): void {
    this.btn = document.getElementById("submit_create_cuenta")
  }

  enviar(values:any){
    this.loanding = true;
    values.user.groups = [
      {name:'admin_empresa'}
    ]
    // localStorage.setItem('token',values.usuario.token)
    this.envio.peticionPost(environment.url+"/auth/create/",values,true).subscribe((res)=>{
      if(res['msg']!= ''){
        this.loanding = false;
        this.envio.isCreatedAccount= true
        this.envio.isRegistered = false
        this.router.navigate(['/creacion-exitosa'])
      }
    },(err:HttpErrorResponse)=>{
      this.loanding = false;
      if(err.error.hasOwnProperty('usuario')){
        if(err.error.usuario.hasOwnProperty('non_field_errors')){
          alert("Contacto: "+err.error.usuario.non_field_errors[0])
        }
      }else if(err.error.hasOwnProperty('empresa')){
        if(err.error.empresa.hasOwnProperty('non_field_errors')){
          alert("Organización: "+err.error.empresa.non_field_errors[0])
        }
      }else{
        alert("Contacto: "+err.error.error)
      }
    
    })
  }

  validacionPassword(){
    return this.validate.validarConfPassword(this.createAccount.get(["user","password"])?.value,this.createAccount.get(["user","confpassword"])?.value)
  }
  validarRuc(){
    let ruc = this.createAccount.get(['empresa','ruc'])?.value
    return !this.validate.validarRuc(ruc)
  }

}
