import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators,} from '@angular/forms';

@Component({
  selector: 'registro',
  templateUrl: './registro.component.html',
  styleUrls: ['./registro.component.css']
})
export class RegistroComponent implements OnInit {
  public registroForm: FormGroup;
  constructor(private fb: FormBuilder) { 
    this.registroForm = this.fb.group({
      registro: this.fb.group({
        razonSocial: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9_ ]+$'),Validators.minLength(5), Validators.maxLength(20)]),
        nombres: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(3),Validators.maxLength(17)]),
        email: this.fb.control('', [Validators.required,Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'),Validators.minLength(7)]),
        telefono: this.fb.control('', [Validators.required,Validators.pattern('^[+_0-9]+$'),Validators.minLength(13),Validators.maxLength(20)]),
        direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9._ ]+$')]),
        cargo: this.fb.control('',[Validators.required,Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(13),Validators.maxLength(20)]),
        descripcion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z ]+$'),Validators.minLength(13),Validators.maxLength(20)])
      
      })
});
  }
  
  ngOnInit(): void {
  }

}
