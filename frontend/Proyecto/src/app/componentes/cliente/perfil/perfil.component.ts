import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Validacion } from 'src/assets/Validacion';

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
    private fb: FormBuilder
  ) {
    this.profile = this.fb.group({
      first_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'), Validators.minLength(3), Validators.maxLength(50)]),
      last_name: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'), Validators.minLength(3), Validators.maxLength(50)]),
      tipo: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$')]),
      direccion: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._ ]+$')]),
      email: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._%+\-]+@[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9.\-]+\\.[a-zA-ZñÑáéíóúÁÉÍÓÚ]{2,4}'), Validators.minLength(7)]),
      telefono: this.fb.control('', [Validators.required, Validators.pattern('^[0-9]+$'), Validators.minLength(10)]),

    })
    this.tipo = 'RUC'
  }

  ngOnInit(): void {
  }

  prueba(text: any) {
    this.tipo = text.value
    let input = document.getElementById("tipo") as HTMLElement
    input.innerText = this.tipo
  }

  validarRucCedula(){
    let tipo = this.profile.get('tipo')?.value
    let identificadores = document.querySelector('input[name="tipo"]:checked') as HTMLInputElement
    if(identificadores.value == 'CEDULA'){
      return !this.validate.validarRuc(tipo,10)
    }
    return !this.validate.validarRuc(tipo)
  }

}
