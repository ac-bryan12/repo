import { Component, OnInit } from '@angular/core';
import { LoginService } from 'src/app/services/login.service';
import { FormBuilder, FormGroup, Validators,FormControlName,FormArrayName} from '@angular/forms';


@Component({
  selector: 'app-create-cuenta',
  templateUrl: './create-cuenta.component.html',
  styleUrls: ['./create-cuenta.component.css']
})

export class CreateCuentaComponent implements OnInit {
  public createAccount: FormGroup;
  
  constructor(
    private envio: LoginService,
    private fb: FormBuilder
  ) {
    this.createAccount = this.fb.group({
      empresa: this.fb.group({
        ruc: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$'),Validators.maxLength(13),Validators.minLength(13)]),
        email: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9_.]+@[a-zA-Z].+[a-zA-Z0-9]$'),Validators.minLength(7)]),
        razonSocial: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z_ ]+$'),Validators.minLength(5), Validators.maxLength(20)]),
        telefono: this.fb.control('', [Validators.required,Validators.pattern('^[+_0-9]+$'),Validators.minLength(13),Validators.maxLength(20)]),
        direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9._ ]+$')]),

      }),
      usuario: this.fb.group({
        firstName: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z_ ]+$'),Validators.minLength(3),Validators.maxLength(15)]),
        lastName: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z_ ]+$'),Validators.minLength(3),Validators.maxLength(15)]),
        cargo: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z_ ]+$'),Validators.minLength(4),Validators.maxLength(35)],),
        password: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z0-9]+$'),Validators.minLength(6),Validators.maxLength(20)]),
        confpassword: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9]+$'),Validators.minLength(6),Validators.maxLength(20)]),
        email: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9_.]+@[a-zA-Z].+[a-zA-Z0-9]$'),Validators.minLength(7)]),
        telefono: this.fb.control('', [Validators.required,Validators.pattern('^[+_0-9]+$'),Validators.minLength(13),Validators.maxLength(20)]),
        direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9._ ]+$')]),
      })
    });
  };

  ngOnInit(): void {
  }

  enviar(values:any){
    console.log(values)
    this.envio.peticionPost("http://localhost:8000/api/create/",values).toPromise().then(res=>{
      console.log(res.json())
    })
  }

}
