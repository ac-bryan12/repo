import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'empresa',
  templateUrl: './empresa.component.html',
  styleUrls: ['./empresa.component.css']
})
export class EmpresaComponent implements OnInit {
  constructor(
  ) { }

  ngOnInit(): void {
  }

  mostrar(){
    let boton = document.getElementById("btnEmp") as HTMLElement
    let contenedor = document.getElementById("formulario") as HTMLElement
    contenedor.innerHTML = ""
    boton.addEventListener('click', ()=>{
      contenedor.innerHTML = `<div id="title"><span>Agregar Empresa</span></div>
      <div class="card-body">
          <form>
              <div>
                  <div id="container-form">
                      <div id="container"class="text-center">
                          <div class="mb-3">
                              <div class="form-floating mb-3 mb-md-0">
                                  <input class="form-control" id="inputRUC" name="ruc" type="text"
                                      placeholder="Ingrese el RUC de su empresa">
                                  <label for="inputRUC">RUC</label>
                              </div>
                          </div>
      
                          <div class="mb-3">
                              <div class="form-floating mb-3 mb-md-0">
                                  <input class="form-control" id="inputEmail" name="mailorganizacion" type="email"
                                      placeholder="name@example.com">
                                  <label for="inputEmail">Correo Electrónico</label>
                              </div>
                          </div>
      
                          <div class="mb-3">
                              <div class="form-floating mb-3 mb-md-0">
                                  <input class="form-control" id="inputRazonSocial" name="razonsocial" type="text"
                                      placeholder="Ingrese la Razon social de su empresa">
                                  <label for="inputRazonSocial">Razón Social</label>
                              </div>
                          </div>
      
                          <div class="mb-3">
                              <div class="form-floating">
                                  <input #telf class="form-control" id="inputNumphone" name="telefono" type="text"
                                      placeholder="Ingrese su numero de telefono">
                                  <label for="inputNumphone">Teléfono</label>
                              </div>
                          </div>
      
                          <div class="mb-3">
                              <div class="form-floating">
                                  <input class="form-control" id="inputDireccion" name="direccion" type="text"
                                      placeholder="Ingrese su dirección">
                                  <label for="inputDireccion">Dirección</label>
                              </div>
                          </div>
                          <div id="buttons" class="mt-4 mb-0">
                              <input type="submit" value="Close" class="btn btn-primary btn-block">
                              <input type="submit" value="Guardar" class="btn btn-primary btn-block">
                          </div>
                      </div>
                      
                  </div>
              </div>
          </form>
      </div>`
    })
  }
}
