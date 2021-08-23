import { Component, OnInit } from '@angular/core';
import { LoginService } from 'src/app/services/login.service';
import { FormBuilder, FormGroup, Validators} from '@angular/forms';


@Component({
  selector: 'app-create-cuenta',
  templateUrl: './create-cuenta.component.html',
  styleUrls: ['./create-cuenta.component.css']
})

export class CreateCuentaComponent implements OnInit {
  public createAccount: FormGroup;
  
  objeto = {
    Organizacion: { ruc: '', correoorg: '', razon: '', telefono: '', direccion: '' },
    Usuario: { nombre: '', apellido: '', cargo: '', contrasena: '', correouser: '', valcontrasena: '' }
  }
  constructor(
    private envio: LoginService,
    private fb: FormBuilder
  ) {
    this.createAccount = this.fb.group({
      ruc: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$'),Validators.maxLength(13),Validators.minLength(13)]),
      mail: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9_.]+@[a-zA-Z].+[a-zA-Z0-9]$'),Validators.minLength(7)]),
      razonsocial: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z_ ]+$'),Validators.minLength(5), Validators.maxLength(20)]),
      telefono: this.fb.control('', [Validators.required,Validators.pattern('^[+_0-9]+$'),Validators.minLength(13),Validators.maxLength(20)]),
      direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9._ ]+$')]),

      firstName: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z_ ]+$'),Validators.minLength(3),Validators.maxLength(15)]),
      lastName: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z_ ]+$'),Validators.minLength(3),Validators.maxLength(15)]),
      cargo: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z_ ]+$'),Validators.minLength(4),Validators.maxLength(35)],),
      password: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z0-9]+$'),Validators.minLength(6),Validators.maxLength(20)]),
      confpassword: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9]+$'),Validators.minLength(6),Validators.maxLength(20)]),
    });
  };

  ngOnInit(): void {
  }

}
