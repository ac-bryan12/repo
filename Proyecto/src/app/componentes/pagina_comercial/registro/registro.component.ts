import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, } from '@angular/forms';
import { RequestService } from 'src/app/services/request/request.service';
import { Router } from '@angular/router';

@Component({
  selector: 'registro',
  templateUrl: './registro.component.html',
  styleUrls: ['./registro.component.css']
})
export class RegistroComponent implements OnInit {
  public registroForm: FormGroup;
  constructor(private fb: FormBuilder,private request:RequestService,private router:Router) {
    this.registroForm = this.fb.group({
      razonSocial: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z0-9. ]+$'), Validators.minLength(5), Validators.maxLength(20)]),
      nombre: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'), Validators.maxLength(15)]),
      correo: this.fb.control('', [Validators.required, Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'), Validators.minLength(7)]),
      telefono: this.fb.control('', [Validators.required, Validators.pattern('^[+_0-9]+$'), Validators.minLength(13), Validators.maxLength(20)]),
      cargo: this.fb.control('', [Validators.required, Validators.pattern('^[a-zA-Z ]+$'), Validators.minLength(4), Validators.maxLength(35)],),
      descripcion: this.fb.control('', [Validators.required, Validators.minLength(10), Validators.maxLength(250)])
    });
  }

  ngOnInit(): void {
  }

  enviarSolicitud(values:any){
    this.request.peticionPost('http://localhost:8000/auth/register/',values,true).subscribe(res=>{
      this.request.isRegistered = true
      this.request.isCreatedAccount = false
      this.router.navigate(['/env-informacion'])
    },err=>{
      console.log(err.error); 
    })
  }

}
