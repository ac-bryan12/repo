import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'alerts',
  templateUrl: './alertas.component.html',
  styleUrls: ['./alertas.component.css']
})
export class AlertasComponent implements OnInit {
  @Input() tipo: string = ''
  @Input() mensaje: string=''
  @Input() shownotify:any[]= []
  @Input() nombreNotify:string = ''
  @Output()
  propagarLista = new EventEmitter<any[]>();    

  constructor() { }

  ngOnInit(): void {
  }

  buscarToast(toast:any){
    let index = 0
    for(let i= 0;i<this.shownotify.length;i++){
      if(toast === this.shownotify[i]){
        index = i
      }
    }
    this.shownotify.splice(index,1)
    this.propagarLista.emit(this.shownotify)
  }

  cerrarToast(toast:HTMLElement) {
    var containerToast = document.getElementById("contenedor")
    containerToast?.getElementsByTagName("alerts")
    toast.classList.add("cerrar")
    toast.classList.remove("cerrar")
    this.buscarToast(toast.id)       
  }
}
