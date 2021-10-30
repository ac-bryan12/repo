import { Component, Injectable, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';
import { saveAs } from 'file-saver';
import { environment } from 'src/environments/environment';
import { HttpEventType, HttpResponse } from '@angular/common/http';
import { AlertasComponent } from '../../auxiliares/alertas/alertas.component';


@Component({
  selector: 'documentos-company',
  templateUrl: './documentos-company.component.html',
  styleUrls: ['./documentos-company.component.css']
})
export class DocumentosCompanyComponent implements OnInit {
  previsualizacion:any
  listaDocumentos: Array<any> = [];
  totalDocsSubir:any
  progressInfo:any = []
  notificaciones:any = []
  progreso:any
  message = '';
  fileName = "";

  constructor(private envio:RequestService,) { 
  }

  ngOnInit(): void {
    this.cargarDocumentos()
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

  subirArchivos(doc:HTMLInputElement){
    var file:any = doc.files
    this.totalDocsSubir = file.length
    for(let i = 0; i<file?.length;i++){
      this.enviodoc(i,file.item(i),file.length)
    }
    
  }
  enviodoc(index:any,file:any,totalDocs:any){
    let forms  = new FormData()
    forms.append("file",file)
    forms.append("content_type",file.type)
    forms.append("nombreDoc",file.name)
    this.progressInfo[index] = { value: 0, fileName: file.name };
    this.envio.peticionPost(environment.url+'/api/empresa/documentos/guardar-documentos/',forms).subscribe((res)=>{
      console.log(res)
        if (res.type === HttpEventType.UploadProgress) {
          this.progressInfo[index].value = Math.round(100 * (index+1) / totalDocs)
          this.progreso = Math.round(100 * (index+1) / totalDocs)
          this.notificaciones.push(file.name)
        }
      },err => {
        this.progressInfo[index].value = 0;
        this.message = 'No se puede subir el archivo ' + file.name;
      })
    
  }
  descargardoc(id:any){
    this.envio.peticionGet(environment.url+'/api/empresa/documentos/descargar-documento/'+id+'/').subscribe((res)=>{
      const Filepath = 'data:text/xml;base64,'+res._file
      saveAs(Filepath,res.nombreDoc)
    })
  }
  cargarDocumentos(){
    this.envio.peticionGet(environment.url+'/api/empresa/documentos/lista-documentos-empresa/').subscribe((res)=>{
      this.listaDocumentos = res
      console.log(this.listaDocumentos)
    })
  }

}
