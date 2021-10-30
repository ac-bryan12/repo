import { Component, Injectable, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';
import { saveAs } from 'file-saver';
import { environment } from 'src/environments/environment';
import { HttpEventType, HttpResponse } from '@angular/common/http';



@Component({
  selector: 'documentos-company',
  templateUrl: './documentos-company.component.html',
  styleUrls: ['./documentos-company.component.css']
})
export class DocumentosCompanyComponent implements OnInit {
  previsualizacion:any
  listaDocumentos: Array<any> = [];
  listaDocumentosAux: Array<any> = [];
  progressInfo:any = []
  notificaciones:any = [] 
  progreso:any
  message = '';
  fileName = "";
  enviar = false

  constructor(private envio:RequestService,) { 
  }

  ngOnInit(): void {
    this.cargarDocumentos()
  }
  procesaPropagar(lista:any){
    console.log(lista)
  }

  capturarFile(firma:HTMLInputElement){
    var  file = firma.files?.item(0)
    if(file!=null){
      this.previsualizacion = file.name
      this.enviar = true
    }
    else{
      this.previsualizacion =""
      this.enviar=false
    }
  }

  subirArchivos(doc:HTMLInputElement){
    this.enviar = false
    var file:any = doc.files 
    let files:any = new Array
    for(let i = 0; i<file?.length;i++){
      var control = 0 
      if(this.listaDocumentos.length<this.listaDocumentosAux.length){ //Recargue
        for(let j = 0;j<this.listaDocumentosAux.length;j++){ 
          if(this.listaDocumentosAux[i] == file[i].name){
            this.notificaciones.push({value:2,name:file[i].name})
            control+=1
          }
        }
      }
      if(this.listaDocumentos.length>0 && this.listaDocumentosAux.length==0){  //condicion
        for(let j = 0;j<this.listaDocumentos.length;j++){ 
          if(this.listaDocumentos[j].nombreDoc == file[i].name){ 
            this.notificaciones.push({value:0,name:file[i].name})
            control+=1
          }
        }
      }
      if(control==0){
        console.log(control)
        console.log(this.listaDocumentosAux)
        this.listaDocumentosAux.push(file[i].name)
        files.push(file[i])
      }
      if(this.listaDocumentos.length==0 && this.listaDocumentosAux.length==0){ //Primera vez 
        this.listaDocumentosAux.push(file[i].name)
        this.enviodoc(i,file[i],file.length)
      }
    }
    for(let i = 0; i<files.length;i++){
      this.enviodoc(i,files[i],files.length)
    }
    this.notificaciones.push({value:2,name:''})
    this.enviar = true
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
          this.notificaciones.push({value:1,name:file.name})
        }
      },err => {
        this.progressInfo[index].value = 0;
        this.message = 'No se puede subir el archivo ' + file.name;
        this.notificaciones.push({value:-1,name:file.name})
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
