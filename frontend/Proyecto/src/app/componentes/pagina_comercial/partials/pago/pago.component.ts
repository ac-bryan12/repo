import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-pago',
  templateUrl: './pago.component.html',
  styleUrls: ['./pago.component.css']
})
export class PagoComponent implements OnInit {
  
  mostrarFormasPago() {
    let pagos = document.getElementById('botones-tarjetas') as HTMLElement;
    pagos.setAttribute("style","display: none");
    let cont = document.getElementById('metodos-pago') as HTMLElement;
    cont.setAttribute("style","display: inline");
  }

  volverFormaPago(){
    let cont = document.getElementById('metodos-pago') as HTMLElement;
    cont.setAttribute("style","display: inline");
    let cancel = document.getElementById('pay-creditcard') as HTMLElement;
    cancel.setAttribute("style","display: none");
  }

  mostrarPagoTarjeta() {
    let seccion = document.getElementById('metodos-pago') as HTMLElement;
    seccion.setAttribute("style","display: none");
    let cont = document.getElementById('pay-creditcard') as HTMLElement;
    cont.setAttribute("style","display: inline");
  }

  mostrarPagoTransf(){
    let sec = document.getElementById('metodos-pago') as HTMLElement;
    sec.setAttribute("style","display: none");
    let cont = document.getElementById('pay-tranfer') as HTMLElement;
    cont.setAttribute("style","display: inline");
    

  }

  

  constructor() { }

  ngOnInit(): void {
  }

}
