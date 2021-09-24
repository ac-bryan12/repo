import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder,Validators} from '@angular/forms';
import { RequestService } from 'src/app/services/request/request.service';

@Component({
  selector: 'pop-up',
  templateUrl: './pop-up.component.html',
  styleUrls: ['./pop-up.component.css']
})
export class PopUpComponent implements OnInit {
  public addEmp: FormGroup;
  listGrupos:string[]
  listPermisos :string[]
  constructor(
    private service: RequestService,
    private fb: FormBuilder) {
    this.addEmp = this.fb.group({
      user: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$'),Validators.maxLength(13),Validators.minLength(13),]),
        permisos: this.fb.control('', [Validators.required,Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'),Validators.minLength(7)]),
        razonSocial: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9. ]+$'),Validators.minLength(5), Validators.maxLength(50)]),
        telefono: this.fb.control('', [Validators.required,Validators.minLength(10),Validators.maxLength(11)]),
        direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9._ ]+$')])
    })
    this.listGrupos = []
    this.listPermisos = []
  }

  ngOnInit(): void {
    this.enviar()
    }

  enviar(){
    let info = {
      ruc:this.addEmp.get('ruc'),
      razonSocial: this.addEmp.get('razonSocial'),
      telefono: this.addEmp.get('telefono'),
      direccion: this.addEmp.get('direccion')
    }
    this.service.peticionGet("http://localhost:8000/api/grupos").subscribe((res)=>{
      for(let grupo of res){
        this.listGrupos.push(grupo.name)
      }
    })
   
    this.service.peticionGet("http://localhost:8000/api/permisos").subscribe((res)=>{
      for(let grupo of res){
        this.listPermisos.push(grupo.name)
      }
    })
    }

    asignarGrupo(){
      let input = document.getElementById("grupos") as HTMLInputElement
      let selectAsignado = document.getElementById("gruposSelect") as HTMLElement
      selectAsignado.innerHTML+= `<option [value] = "${input.value}">${input.value}</option>`
    }
    removerGrupo(){
  
    }
    asignarPermiso(){
      let input = document.getElementById("permisos") as HTMLInputElement
      let selectAsignado = document.getElementById("permisosSelect") as HTMLElement
      console.log(input.value)
      selectAsignado.innerHTML+= `<option [value] = "${input.value}">${input.value}</option>`
    }
}
