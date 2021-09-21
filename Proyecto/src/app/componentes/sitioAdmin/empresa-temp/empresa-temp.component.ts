import { Component, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';

@Component({
  selector: 'app-empresa-temp',
  templateUrl: './empresa-temp.component.html',
  styleUrls: ['./empresa-temp.component.css']
})
export class EmpresaTempComponent implements OnInit {

  constructor(private request: RequestService) { }

  ngOnInit(): void {
    this.grupos_permisos()
  }


  grupos_permisos() {
    this.request.peticionGet("http://localhost:8000/api/permission").subscribe()
    let contenedor = document.getElementById("tablasEmptmp") as HTMLElement
    this.request.peticionGet('http://localhost:8000/api/empresaTemps/lista-de-empresaTemps').subscribe(res => {
      for (let emp of res) {
        let plantilla =
          `  
          <tr>
            <td>${emp.razonSocial}</td>
            <td>${emp.telefono}</td>
            <td>${emp.correo}</td>
            <td id="botones-acciones">
            <input id="${emp.correo}" type="submit" value="Enviar Correo" class="btn btn-primary btn-block">
            <input type="submit" value="Eliminar" class="btn btn-danger btn-block">
            </td>
          </tr>
          `
          contenedor.innerHTML += plantilla

          let boton = document.getElementsByTagName("input")
          for(let b=0; b<boton.length;b++){
            let opc = boton[0]
            boton[b].addEventListener('click',() =>{ 
              this.request.peticionPost('http://localhost:8000/api/empresaTemps/buscar-empresaTemp/',{"correo" : emp.correo}).subscribe()
            })
          }
      }

       
    })
  }
}
