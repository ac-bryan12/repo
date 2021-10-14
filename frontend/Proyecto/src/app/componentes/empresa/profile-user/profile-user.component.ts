import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Validacion } from 'src/assets/Validacion';

@Component({
  selector: 'profile-user',
  templateUrl: './profile-user.component.html',
  styleUrls: ['./profile-user.component.css']
})
export class ProfileUserComponent implements OnInit {
  public profile: FormGroup;
  public validate: Validacion = new Validacion;
  constructor(
    private fb: FormBuilder
  ) { 
    this.profile = this.fb.group({
      direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._ ]+$')]),
      email: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._%+\-]+@[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9.\-]+\\.[a-zA-ZñÑáéíóúÁÉÍÓÚ]{2,4}'),Validators.minLength(7)]),
      telefono: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$'),Validators.minLength(10)]),
    })
  }

  ngOnInit(): void {
  }

}
