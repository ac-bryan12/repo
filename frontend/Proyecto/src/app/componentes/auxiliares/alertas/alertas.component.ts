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
  propagarLista = new EventEmitter<number>()    
 
  constructor() { }

  ngOnInit(): void {
  }

  cerrarToastAuto(){
    setTimeout(()=>{
      var containerToast = document.getElementById("contenedor")
      var lista = containerToast?.getElementsByTagName("alerts") as HTMLCollectionOf<HTMLElement>
      if(lista.length>0){
        this.shownotify = lista
        for(let i = 0;i<lista.length;i++){
          let parent = lista.item(i)?.parentNode as Node
          setTimeout(()=>{
            this.cerrarToast(lista[i],true)
            containerToast?.removeChild(parent)
          },(i+1)*1100) 
        }
      }  
    },15000)
  }

  cerrarToast(toast:HTMLElement,auto=false) {
    var containerToast = document.getElementById("contenedor")
    var lista = containerToast?.getElementsByTagName("alerts") as HTMLCollectionOf<HTMLElement>
    this.shownotify = lista
    toast.classList.remove("toastC")
    toast.classList.add("hidden")
    if(!auto){
      for(let i = 0;i<lista.length;i++){
        let parent = lista.item(i)?.parentNode as Node
        containerToast?.removeChild(parent)
      }
    }
  }
  
}
