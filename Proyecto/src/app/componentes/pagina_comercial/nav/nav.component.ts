import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'nav_bar',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.css']
})
export class NavComponent implements OnInit {
  urlLogin = 'http://localhost:8000/login'
  constructor() { }

  ngOnInit(): void {
  }
  colornb(evento:Event){
    var elemento : HTMLElement = evento.target as HTMLElement;
    elemento.classList.add("active2");
    let vari = function(elemento : HTMLElement){
      let lista = document.getElementsByClassName("nb_element");
      for(let i = 0 ;i<lista.length;i++){
          let list = lista[i] as HTMLElement
          if(list.classList.contains("active2") && list!=elemento)
            list.classList.remove("active2");
      }
    };
    vari(elemento);
  }

}
