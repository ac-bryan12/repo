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
  previsualizacion: any
  listaDocumentos: Array<any> = [];
  listaDocumentosAux: Array<any> = [];
  notificaciones: any = []
  fileName = "";
  enviar = false
  namesFilesAux = new Set()
  totalDocs: number = 0

  constructor(private envio: RequestService,) {
  }

  ngOnInit(): void {
    this.cargarDocumentos()
  }
  procesaPropagar(lista: any) {
    console.log(lista)
  }

  capturarFile(firma: HTMLInputElement) {
    var file = firma.files?.item(0)
    if (file != null) {
      this.previsualizacion = file.name
      this.enviar = true
    }
    else {
      this.previsualizacion = ""
      this.enviar = false
    }
  }

  subirArchivos(doc: HTMLInputElement) {
    this.enviar = false
    var file: any = doc.files
    for(let docs of this.listaDocumentos){
      this.namesFilesAux.add(docs.nombreDoc)
    }
    if (this.listaDocumentos.length != 0) {
      for (let i = 0; i < file.length; i++) {
        if (this.listaDocumentosAux.length != 0) {
          for (let datos of this.namesFilesAux) {
            if (datos == file.item(i).name) {
              this.notificaciones.push({ value: "existe", name: file.item(i).name })
            }
          }
        }
      }
    }
    for (let i = 0; i < file.length; i++) {
      if (!(this.namesFilesAux.has(file.item(i).name))) {
        this.totalDocs++
        this.enviodoc(file[i])
        this.listaDocumentosAux.push(file.item(i).name)
        this.namesFilesAux.add(file.item(i).name)
      }
      else {
        this.notificaciones.push({ value: "existe", name: file.item(i).name })
      }
    }
    this.enviar = true
  }


  enviodoc(file: any,) {
    let forms = new FormData()
    forms.append("file", file)
    forms.append("content_type", file.type)
    forms.append("nombreDoc", file.name)
    this.envio.peticionPost(environment.url + '/api/empresa/documentos/guardar-documentos/', forms).subscribe((res) => {
      if (res.type === HttpEventType.UploadProgress) {
        this.notificaciones.push({ value: "creado", name: file.name })
      }
    }, err => {
      this.notificaciones.push({ value: "error", name: file.name })
    })
  }
  descargardoc(id: any) {
    this.envio.peticionGet(environment.url + '/api/empresa/documentos/descargar-documento/' + id + '/').subscribe((res) => {
      const Filepath = 'data:text/xml;base64,' + res._file
      saveAs(Filepath, res.nombreDoc)
    })
  }
  cargarDocumentos() {
    this.envio.peticionGet(environment.url + '/api/empresa/documentos/lista-documentos-empresa/').subscribe((res) => {
      this.listaDocumentos = res
    })
  }

}
