import { Component, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';

@Component({
  selector: 'app-empresa-temp',
  templateUrl: './empresa-temp.component.html',
  styleUrls: ['./empresa-temp.component.css']
})
export class EmpresaTempComponent implements OnInit {

  constructor(private request:RequestService) { }

  ngOnInit(): void {
    this.grupos_permisos()
  }


  grupos_permisos() {
    this.request.peticionGet("http://localhost:8000/api/permission").subscribe()
  }
}
