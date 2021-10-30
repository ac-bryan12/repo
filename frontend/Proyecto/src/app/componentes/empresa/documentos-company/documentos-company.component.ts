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
    console.log(file.item(0).name)
    if(this.listaDocumentos.length==0 && this.listaDocumentosAux.length==0){ 
      for(let i = 0; i<file?.length;i++){ //Comprueba la lista servidor
        console.log(file[i])
        this.listaDocumentosAux.push(file.item(i).name)
        this.enviodoc(i,file.item(i),file.length)
      }
    }
    for(let i = 0;i<file.length;i++){
      if(this.listaDocumentosAux.length!=0){ //Se comprueba la lista auxiliar
        for(let j = 0;j<this.listaDocumentosAux.length;j++){ 
          if(this.listaDocumentosAux[j] == file.item(i).name){
            this.notificaciones.push({value:"recargar",name:file.item(i).name}) //Aqui se repite, aqui puede que encuentre alguno si se subio sin recargar
          }
        }
      }
      if(this.listaDocumentosAux.length==0 && this.listaDocumentos.length!=0){ //No hay lista auxiliar
        for(let j = 0;j<this.listaDocumentos.length;j++){ 
          console.log("Lista aux" + this.listaDocumentos[j].nombreDoc)
          if(this.listaDocumentos[j].nombreDoc == file.item(i).name){ 
            this.notificaciones.push({value:"existe",name:file.item(i).name})
          }else{ //Aqui se agregar a files 
            this.listaDocumentosAux.push(file.item(i).name) //Aqui esta el error, debe verse que solo agregue una vez el i y no varias 
            files.push(file.item(i))                        // Controlalo con alguna variable, recuerda que arriba tambien se ve si se repite
          }
        }
      }  
    }
    //A partir de aqui hace todo 
    for(let i = 0; i<files.length;i++){
      console.log(files[i])
      this.enviodoc(i,files[i],files.length)
    }
    this.enviar = true
  }
  enviodoc(index:any,file:any,totalDocs:any){
    let forms  = new FormData()
    forms.append("file",file)
    forms.append("content_type",file.type)
    forms.append("nombreDoc",file.name)
    this.progressInfo[index] = { value: "existe", fileName: file.name };
    this.envio.peticionPost(environment.url+'/api/empresa/documentos/guardar-documentos/',forms).subscribe((res)=>{
      console.log(res)
        if (res.type === HttpEventType.UploadProgress) {
          this.progressInfo[index].value = Math.round(100 * (index+1) / totalDocs)
          this.progreso = Math.round(100 * (index+1) / totalDocs)
          this.notificaciones.push({value:"creado",name:file.name})
        }
      },err => {
        this.progressInfo[index].value = 0;
        this.notificaciones.push({value:"error",name:file.name})
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
