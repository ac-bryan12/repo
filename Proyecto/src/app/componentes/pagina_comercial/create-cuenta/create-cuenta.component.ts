import { Component, OnInit } from '@angular/core';
import { LoginService } from 'src/app/services/login.service';
import { FormBuilder, FormGroup, Validators,} from '@angular/forms';


@Component({
  selector: 'app-create-cuenta',
  templateUrl: './create-cuenta.component.html',
  styleUrls: ['./create-cuenta.component.css']
})

export class CreateCuentaComponent implements OnInit {
  public createAccount: FormGroup;
  token = ''
  msg_content = ''
  msg_d = 'd-none'
  
  constructor(
    private envio: LoginService,
    private fb: FormBuilder
  ) {
    this.createAccount = this.fb.group({
      empresa: this.fb.group({
        ruc: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$'),Validators.maxLength(13),Validators.minLength(13)]),
        email: this.fb.control('', [Validators.required,Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'),Validators.minLength(7)]),
        razonSocial: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9. ]+$'),Validators.minLength(5), Validators.maxLength(20)]),
        telefono: this.fb.control('', [Validators.required,Validators.pattern('^[+_0-9]+$'),Validators.minLength(13),Validators.maxLength(20)]),
        direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9._ ]+$')]),
      }),
      usuario: this.fb.group({
        firstName: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(3),Validators.maxLength(15)]),
        lastName: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(3),Validators.maxLength(15)]),
        cargo: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(4),Validators.maxLength(35)],),
        password: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z0-9_:@.\-]+$'),Validators.minLength(8)]),
        confpassword: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9_:@.\-]+$')]),
        email: this.fb.control('', [Validators.required,Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'),Validators.minLength(7)]),
        telefono: this.fb.control('', [Validators.required,Validators.pattern('^[+_0-9]+$'),Validators.minLength(13),Validators.maxLength(20)]),
        direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9._ ]+$')]),
        token: this.fb.control('', [Validators.required,Validators.minLength(4)]),
      })
    });
  };

  ngOnInit(): void {
  }

  enviar(values:any){
    this.envio.setToken(values.usuario.token)
    this.envio.peticionPost("http://localhost:8000/api/create/",values).toPromise().then(res=>{
      console.log(res.json())
    })
  }

  validarConfPassword(): boolean{
    this.msg_d = 'd-none'
    let pass = this.createAccount.get(['usuario','password'])?.value
    let valpass = this.createAccount.get(['usuario','confpassword'])?.value
    if(this.createAccount.get(['usuario','password'])?.hasError('required') || pass != valpass){
      this.msg_d = 'd-block'
      this.msg_content = "Contraseña no coincide"
      return false;
    }
    return true;
  }

}
