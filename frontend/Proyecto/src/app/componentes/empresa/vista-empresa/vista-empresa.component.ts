import { Component, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';
import { Validacion } from 'src/assets/Validacion';
import { environment } from 'src/environments/environment';
import { FormGroup, FormBuilder,Validators} from '@angular/forms';
<<<<<<< Updated upstream
import { ThemePalette } from '@angular/material/core';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';
=======
>>>>>>> Stashed changes
import { saveAs } from 'file-saver';

@Component({
  selector: 'vista-empresa',
  templateUrl: './vista-empresa.component.html',
  styleUrls: ['./vista-empresa.component.css']
})
export class VistaEmpresaComponent implements OnInit {
  // Progress Bar
  color: ThemePalette = 'primary';
  mode: ProgressSpinnerMode = 'indeterminate';
  loanding = false
  //Other variables
  public validate: Validacion = new Validacion();
  public formulario: FormGroup;
  previsualizacion:any;

  constructor(private envio: RequestService,private fb: FormBuilder ) {
    this.formulario = this.fb.group({
      ruc : this.fb.control('',[Validators.required]),
      razonSocial :  this.fb.control('',[Validators.required]),
      direccion : this.fb.control('',[Validators.required,Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._ ]+$'),Validators.minLength(4)]),
      telefono : this.fb.control('',[Validators.required,Validators.pattern('^[0-9]+$'),Validators.minLength(10)]),
      correo : this.fb.control('',[Validators.required,Validators.pattern('^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._%+\-]+@[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9.\-]+\\.[a-zA-ZñÑáéíóúÁÉÍÓÚ]{2,4}'),Validators.minLength(7)])
    })
   }

  ngOnInit(): void {
    this.valores()

  }

  valores() {    
    this.envio.peticionGet(environment.url+'/api/empresa/buscar-empresa/').subscribe(res => {
      if (res.ruc.length < 13){
        res.ruc = "0"+res.ruc
      }
      if (res.telefono.length < 10){
        res.telefono = "0"+res.telefono
      }
      this.formulario.get('ruc')?.setValue(res.ruc)
      this.formulario.get('correo')?.setValue(res.correo)
      this.formulario.get('razonSocial')?.setValue(res.razonSocial)
      this.formulario.get('telefono')?.setValue(res.telefono)
      this.formulario.get('direccion')?.setValue(res.direccion)      
    })
    
  }
  capturarFile(firma:HTMLInputElement){
    var  file = firma.files?.item(0)
    if(file!=null){
      this.previsualizacion = file.name
    }
    else{
      this.previsualizacion =""
    }
  }
  envioFirma(firma:HTMLInputElement, form:any){
    let forms  = new FormData()
    var file:any = firma.files?.item(0)
    console.log(file)
    forms.append("file",file)
    forms.append("content_type",file.type)
    this.envio.peticionPost(environment.url+'/api/empresa/firma/',forms).subscribe((res)=>{
      console.log(res)
    })
    
  }
  descargarFirma(){
    this.envio.peticionGet(environment.url+'/api/empresa/firma/23/').subscribe((res)=>{
      const downloadLink = document.createElement("a");
      const fileName = "sample.pdf";
      const Filepath = 'data:application/pdf;base64,'+res._file

      saveAs(Filepath,fileName)
    })
  }

  enviarInfo(values:any){
    this.loanding = true;
    this.envio.peticionPost(environment.url+"/api/empresa/buscar-empresa/",values).subscribe(res =>{
      this.loanding = false;
      alert(res["msg"])
    },err =>{
      this.loanding = false;
      alert(err.error.error)
    })
  }


}
