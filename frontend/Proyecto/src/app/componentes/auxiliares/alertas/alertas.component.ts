import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Observable } from 'rxjs';

@Component({
  selector: 'alerts',
  templateUrl: './alertas.component.html',
  styleUrls: ['./alertas.component.css']
})
export class AlertasComponent implements OnInit {
  shownotify:any
  @Input() listaTotal:any[] = [] 
  @Input() tipo: string = ''
  @Input() mensaje: string=''
  @Output()
  propagarLista = new EventEmitter<any[]>()    
 
  constructor() { }

  ngOnInit(): void {
  }

  buscarToast(toast:any,indice:any){
    if(indice!=0){
      this.listaTotal.splice(indice,1)
    }else{
      for(let i = 0;i <this.shownotify.length;i++){
        this.listaTotal.splice(indice,1)
      }
    }
    this.propagarLista.emit(this.listaTotal)

  }

  cerrarToastAuto(){
    var containerToast = document.getElementById("contenedor")
    var lista = containerToast?.getElementsByTagName("alerts") as HTMLCollectionOf<HTMLElement>
    this.shownotify = lista
    for(let i = 0;i<lista.length;i++){
      let toast = lista.item(i) as HTMLElement
      setTimeout(()=>{
        this.cerrarToast(toast,i)
      },(i+1)*5000)
    }
  }

  cerrarToast(toast:HTMLElement,indice:any = 0) {
      toast.classList.remove("toastC")
      toast.classList.add("hidden")
      this.buscarToast(toast,indice)     
  }
}
