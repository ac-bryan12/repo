import { Component, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';
import { Validacion } from 'src/assets/Validacion';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'vista-empresa',
  templateUrl: './vista-empresa.component.html',
  styleUrls: ['./vista-empresa.component.css']
})
export class VistaEmpresaComponent implements OnInit {
  public validate: Validacion = new Validacion();

  constructor(
    private envio: RequestService,
  ) { }

  ngOnInit(): void {
    this.valores()

  }

  valores() {
    let ruc = document.getElementById("inputRUC")
    let correo = document.getElementById("inputEmail")
    let razonSocial = document.getElementById("inputRazonSocial")
    let telefono = document.getElementById("inputNumphone")
    let direccion = document.getElementById("inputDireccion")
    
    this.envio.peticionGet(environment.url+'/api/empresa/buscar-empresa/').subscribe(res => {
      
      ruc?.setAttribute("value", res.ruc);
      correo?.setAttribute("value", res.correo)
      razonSocial?.setAttribute("value", res.razonSocial)
      telefono?.setAttribute("value", res.telefono)
      direccion?.setAttribute("value", res.direccion)
      
    })
    
  }


}
