import { Component, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';
import { environment } from 'src/environments/environment';

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
    let contenedor = document.getElementById("tablasEmptmp") as HTMLElement
    this.request.peticionGet(environment.url+'/api/empresa/empresaTemps/lista-de-empresaTemps/').subscribe(res => {
      for (let emp of res) {
        let plantilla =
          `  
          <tr class="text-center">
            <td>${emp.razonSocial}</td>
            <td>${emp.nombre}</td>
            <td>${emp.cargo}</td>
            <td>${emp.telefono}</td>
            <td>${emp.correo}</td>
            <td><textarea disabled rows="4" class="w-100">${emp.descripcion}</textarea></td>
            <td id="botones-acciones">
            <input id="${emp.correo}" type="submit" value="Aceptar" class="btn btn-primary btn-block">       
            </td>
          </tr>
          `
          //<input type="submit" value="Eliminar" class="btn btn-danger btn-block">
          contenedor.innerHTML += plantilla

          let boton = document.getElementsByTagName("input")
          for(let b=0; b<boton.length;b++){
            boton[b].addEventListener('click',() =>{ 
              let correo = boton[b].getAttribute("id")
              alert("Se le enviará un correo al usuario.")
              this.request.peticionPost(environment.url+'/api/empresa/empresaTemps/buscar-empresaTemp/',{"correo" : correo}).subscribe()
            })
          }
      }

       
    })
  }
}
