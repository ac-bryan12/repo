import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, } from '@angular/forms';
import { RequestService } from 'src/app/services/request/request.service';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'registro',
  templateUrl: './registro.component.html',
  styleUrls: ['./registro.component.css']
})
export class RegistroComponent implements OnInit {
  public registroForm: FormGroup;
  constructor(private fb: FormBuilder,private request:RequestService,private router:Router) {
    this.registroForm = this.fb.group({
      razonSocial: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9. ]+$'), Validators.minLength(5), Validators.maxLength(150)]),
      nombre: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'), Validators.maxLength(150)]),
      correo: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._%+\-]+@[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9.\-]+\\.[a-zA-ZñÑáéíóúÁÉÍÓÚ]{2,4}'), Validators.minLength(7),Validators.maxLength(150)]),
      telefono: this.fb.control('', [Validators.required, Validators.pattern('^[+_0-9]+$'), Validators.minLength(10)]),
      cargo: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ. ]+$'), Validators.minLength(3), Validators.maxLength(30)],),
      descripcion: this.fb.control('', [Validators.required, Validators.minLength(10), Validators.maxLength(250)])
    });
  }

  ngOnInit(): void {
  }

  enviarSolicitud(values:any){
    this.request.peticionPost(environment.url+'/auth/register/',values,true).subscribe(res=>{
      this.request.isRegistered = true
      this.request.isCreatedAccount = false
      this.router.navigate(['/env-informacion'])
    },err=>{
      console.log(err.error); 
    })
  }

}
