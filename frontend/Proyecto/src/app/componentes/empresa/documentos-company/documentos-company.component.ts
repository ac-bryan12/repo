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
  loanding = false
  listaDocumentos: Array<any> = [];
  listaDocumentosAux: Array<any> = [];
  notificaciones: any = []
  fileName = "";
  enviar = true
  enviarDocumentos = false
  namesFilesAux = new Set()
  totalDocs: number = 0
  existDocs: number = 0
  errorDocs: number = 0

  constructor(private envio: RequestService,) {
  }

  ngOnInit(): void {
    this.cargarDocumentos()
    this.habilitarControles()
  }

  habilitarControles() {
    this.envio.peticionGet(environment.url + "/auth/userPermissions/").subscribe(res => {
      for (let permiso of res.permissions) {
        if (permiso.codename == 'add_documentos') {
          this.enviarDocumentos = true
        }
      }
    }, err => {
      alert(err.error.error);
    })
  }

  procesaPropagar(lista: any) {
    this.notificaciones = lista
  }
  procesarCierre() {
  }

  capturarFile(firma: HTMLInputElement) {
    var file = firma.files?.item(0)
    if (file != null) {
      this.previsualizacion = firma.files?.length
      this.enviar = false
    }
    else {
      this.previsualizacion = ""
      this.enviar = true
    }
  }

  subirArchivos(docs: HTMLInputElement) {
    this.enviar = true
    var file: any = docs.files
    for (let docs of this.listaDocumentos) {
      this.namesFilesAux.add(docs.nombreDoc)
    }
    for (let i = 0; i < file.length; i++) {
      if (!(this.namesFilesAux.has(file.item(i).name))) {
        this.enviodoc(file[i])
        this.listaDocumentosAux.push(file.item(i).name)
        this.namesFilesAux.add(file.item(i).name)
      }
      else {
        this.notificaciones.push({ value: "existe", name: file.item(i).name })
        this.existDocs++
      }
    }
    let var1 = this
    setTimeout(function () {
      if (var1.totalDocs > 0) {
        var1.notificaciones.push({ value: "creados", name: "" })
        var1.notificaciones.push({ value: "recargar", name: "" })
      }
      var1.enviar = false
      var1.loanding = false
    }, 4000, var1)
  }


  enviodoc(file: any) {
    let forms = new FormData()
    forms.append("file", file)
    forms.append("content_type", file.type)
    forms.append("nombreDoc", file.name)
    this.loanding = true
    this.envio.peticionPost(environment.url + '/api/empresa/documentos/guardar-documentos/', forms).subscribe((res) => {
      if (res.type === HttpEventType.UploadProgress) {
        this.totalDocs++
      }
    }, err => {
      this.notificaciones.push({ value: "error", name: file.name })
      this.errorDocs++
    })
    this.procesarCierre()
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

  buscador() {
    let search = document.getElementById("buscador") as HTMLElement
    let inputsearch = document.getElementById("inputbuscador") as HTMLDataElement
    let nameDoc = document.getElementsByClassName("nameDocs")
    let filas = document.getElementsByClassName("fila");
    inputsearch.addEventListener("change",()=>{
      if(inputsearch.value == ''){
        for (let i = 0; i < nameDoc.length; i++) {
          filas[i].classList.remove("class","d-none")
        }
      }
    })

    search.addEventListener("click", () => {
      this.evento(search,nameDoc,filas, inputsearch)
    })
  }

  evento(tag: HTMLElement, nameDoc: HTMLCollectionOf<Element>, filas: HTMLCollectionOf<Element>, inputsearch:HTMLDataElement){
    tag.addEventListener("click", () => {
      for (let i = 0; i < nameDoc.length; i++) {
        if (!nameDoc[i].textContent?.toLocaleLowerCase().includes(inputsearch.value.toLocaleLowerCase())) {
          filas[i].classList.add("class", "d-none")
        }
        else {
          filas[i].classList.remove("class","d-none")
        }
      }
    })

  }
}
