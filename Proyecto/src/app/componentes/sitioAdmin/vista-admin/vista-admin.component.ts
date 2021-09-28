import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';

@Component({
  selector: 'vista-admin',
  templateUrl: './vista-admin.component.html',
  styleUrls: ['./vista-admin.component.css']
})
export class VistaAdminComponent implements OnInit {

  constructor(private request:RequestService) { }

  ngOnInit(): void {
    this.grupos_permisos()
  }

  grupos_permisos() {
    this.request.peticionGet("http://localhost:8000/auth/userPermissions").subscribe(res =>{
      
    })
  }

}
