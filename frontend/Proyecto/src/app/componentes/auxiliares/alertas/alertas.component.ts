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
  @Input() cantidad:number = 0
  @Output()
  propagarLista = new EventEmitter<any[]>()    
  @Output()
  propagarCierre = new EventEmitter<any[]>()

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

  OnPropagarCierre(){
    if(this.shownotify.length>0)
      this.cerrarToastAuto()
      this.propagarCierre.emit(this.shownotify)
  }

  cerrarToastAuto(){
    let var1 = this
    setTimeout(function(){
      var containerToast = document.getElementById("contenedor")
      var lista = containerToast?.getElementsByTagName("alerts") as HTMLCollectionOf<HTMLElement>
      for(let i = 0; i<lista.length;i++){
          let toast = lista.item(i) as HTMLElement
          toast?.classList.add("cerrar")
          toast?.classList.remove("cerrar")
          var1.buscarToast(toast.id)
      } 
    },3000,var1)
  }

  cerrarToast(toast:HTMLElement) {
    var containerToast = document.getElementById("contenedor")
    containerToast?.getElementsByTagName("alerts")
    toast.classList.add("cerrar")
    toast.classList.remove("cerrar")
    this.buscarToast(toast.id)       
  }
}
