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
  constructor(
    private envio: RequestService,
    private fb: FormBuilder) {
    this.addEmp = this.fb.group({
      ruc: this.fb.control('', [Validators.required,Validators.pattern('^[0-9]+$'),Validators.maxLength(13),Validators.minLength(13),]),
        email: this.fb.control('', [Validators.required,Validators.pattern('^[a-z0-9._%+\-]+@[a-z0-9.\-]+\\.[a-z]{2,4}'),Validators.minLength(7)]),
        razonSocial: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9. ]+$'),Validators.minLength(5), Validators.maxLength(50)]),
        telefono: this.fb.control('', [Validators.required,Validators.minLength(10),Validators.maxLength(11)]),
        direccion: this.fb.control('', [Validators.required,Validators.pattern('^[a-zA-Z0-9._ ]+$')])
    })
  }

  ngOnInit(): void {
    }

  enviar(){
    let info = {
      ruc:this.addEmp.get('ruc'),
      razonSocial: this.addEmp.get('razonSocial'),
      telefono: this.addEmp.get('telefono'),
      direccion: this.addEmp.get('direccion')
    }
    /*
    this.envio.peticionPost('http://localhost:8000/api/create/',info).subscribe((res)=>{

    })
    */
    }
}
