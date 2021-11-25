import { Component, Input, OnInit, Output, EventEmitter, OnChanges, DoCheck, SimpleChange, SimpleChanges} from '@angular/core';
import { environment } from 'src/environments/environment';
import { Router } from '@angular/router';
import { RequestService } from 'src/app/services/request/request.service';

@Component({
  selector: 'list-pagination',
  templateUrl: './paginacion.component.html',
  styleUrls: ['./paginacion.component.css']
})
export class PaginacionComponent implements OnChanges {
    @Input() urlRequest: string = ""
    @Output() listObjects =  new EventEmitter<any[]>()

    // Paginación
    count: number 
    page_size: number
    next: string
    previous: string
    n_pag: number[]
    pag_actual: number
    previousControl: string
    nextControl: string
    listObjectslength: number
    oldUrl : string


  constructor(private service:RequestService,private router:Router) {
      // Entrada y salida

      // Paginación
      this.count = 0
      this.page_size = 10
      this.previous = ""
      this.next = ""
      this.n_pag = [0]
      this.pag_actual = 0
      this.previousControl = "disabled"
      this.nextControl = "disabled"

      this.listObjectslength = 0

      this.oldUrl = " "
   }

  ngOnChanges(changes:SimpleChanges): void {
    if(changes.urlRequest){
      this.oldUrl = this.urlRequest
      this.next = environment.url+this.urlRequest
      this.obtenerObjetos()
    } 
  }

  cambiarPagina(pag:number){
    let urlPeticion = ""
    if (pag == this.pag_actual+1){
      urlPeticion = this.next
    }else if(pag == this.pag_actual-1){
      urlPeticion = this.previous
    }else{
      if(this.urlRequest.substr(this.urlRequest.length-1,this.urlRequest.length) == '/'){
        urlPeticion = environment.url+this.urlRequest+"?page="+pag
      }
      else{
        urlPeticion = environment.url+this.urlRequest+"&page="+pag
      }
      
    }
    this.obtenerObjetos(urlPeticion,pag)
  }

  obtenerObjetos(url: string = this.next, pag : number = 1){

    this.service.peticionGet(url).subscribe((res)=>{
      // Change active pag
      let pagActualControl = document.getElementById('pag_'+pag)
      pagActualControl?.classList.add("active")
      let pagAnteriorControl = document.getElementById('pag_'+this.pag_actual)
      pagAnteriorControl?.classList.remove("active")

      // 
      this.pag_actual = pag
      this.listObjects.emit(res.results)
      this.listObjectslength = res.results.length
      this.count = res.count
      this.next = res.next
      this.previous = res.previous
      this.n_pag =  Array.from(Array(Math.ceil(this.count/this.page_size)).keys())
      if (this.next){
        this.nextControl = ""
      }else{
        this.nextControl = "disabled"
      }
      if (this.previous){
        this.previousControl = ""
      }else{
        this.previousControl = "disabled"
      }
    })
  }
}
