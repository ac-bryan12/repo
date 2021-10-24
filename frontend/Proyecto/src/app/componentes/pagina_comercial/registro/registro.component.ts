import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, } from '@angular/forms';
import { RequestService } from 'src/app/services/request/request.service';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { ThemePalette } from '@angular/material/core';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';

@Component({
  selector: 'registro',
  templateUrl: './registro.component.html',
  styleUrls: ['./registro.component.css']
})
export class RegistroComponent implements OnInit {
  //Progress bar
  color: ThemePalette = 'primary';
  mode: ProgressSpinnerMode = 'indeterminate';
  loanding = false
  public registroForm: FormGroup;


  constructor(private fb: FormBuilder,private request:RequestService,private router:Router) {
    this.registroForm = this.fb.group({
      razonSocial: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9. ]+$'), Validators.minLength(3)]),
      nombre: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'),Validators.minLength(3)]),
      correo: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._%+\-]+@[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9.\-]+\\.[a-zA-ZñÑáéíóúÁÉÍÓÚ]{2,4}'),Validators.minLength(7)]),
      telefono: this.fb.control('', [Validators.required, Validators.pattern('^[+_0-9]+$'),Validators.minLength(10)]),
      cargo: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ. ]+$'), Validators.minLength(3)],),
      descripcion: this.fb.control('', [Validators.required, Validators.minLength(5)])
    });
  }

  ngOnInit(): void {
  }

  enviarSolicitud(values:any){
    this.loanding = true
    this.request.peticionPost(environment.url+'/auth/register/',values,true).subscribe(res=>{
      this.loanding = false
      this.request.isRegistered = true
      this.request.isCreatedAccount = false
      this.router.navigate(['/env-informacion'])
    },err=>{
      this.loanding = false
      alert(err.error.non_field_errors)
    })
  }

}
