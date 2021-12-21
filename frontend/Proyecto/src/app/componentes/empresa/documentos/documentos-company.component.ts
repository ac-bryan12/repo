import { Component, Injectable, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';
import { saveAs } from 'file-saver';
import { environment } from 'src/environments/environment';
import { HttpEventType, HttpResponse } from '@angular/common/http';
import { AlertasComponent } from '../../auxiliares/alertas/alertas.component';
import { Router } from '@angular/router';



@Component({
  selector: 'documentos-company',
  templateUrl: './documentos-company.component.html',
  styleUrls: ['./documentos-company.component.css']
})
export class DocumentosCompanyComponent implements OnInit {
  id:Number = 0
  tipo = null
  previsualizacion: any
  loanding = false
  listaDocumentos: Array<any> = [];
  documentSearch: Array<any> = [];
  notificaciones: any[] = []
  enviar = true
  enviarDocumentos = false
  totalDocs: number = 0
  errorDocs: number = 0
  nombreDocumento = ""
  env = environment.url

  constructor(private envio: RequestService,private router: Router) {
  }

  ngOnInit(): void {
    // this.cargarDocumentos()
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.tipo =  this.router.parseUrl(this.router.url).queryParams["tipo"]  
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

  procesaPropagar($event: any) {
    console.log($event)
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
    for (let i = 0; i < file.length; i++) {
      this.enviodoc(file[i])
    }
    setTimeout(() => {
      if (this.totalDocs > 0) {
        this.notificaciones.push({ value: "creados", mensaje: "Se ha cargado con éxito", time: this.totalDocs })
        this.notificaciones.push({ value: "recargar", mensaje: "Recargue para ver los últimos cambios ", cantidad: this.totalDocs, time: this.totalDocs })
      }
      this.enviar = false
      this.loanding = false
      AlertasComponent.prototype.cerrarToastAuto()
    }, 4000)
  }


  enviodoc(file: any) {
    let forms = new FormData()
    forms.append("file", file)
    forms.append("content_type", file.type)
    forms.append("nombreDoc", file.name)
    forms.append("tipoCreacion", "SUBIDO")
    this.loanding = true
    this.envio.peticionPost(environment.url + '/api/documentos/guardar-documentos/', forms).subscribe((res) => {
      if (res.type === HttpEventType.UploadProgress) {
        this.totalDocs++
      }
    }, err => {
      this.errorDocs++
      this.notificaciones.push({ value: err.error.class, mensaje: err.error.error, cantidad: 1, time: this.errorDocs })
    })
  }
  descargardoc(format:any) {
    this.envio.peticionGet(environment.url + '/api/documentos/descargar-documento/' + this.id + '/?formato='+format).subscribe((res) => {
      let Filepath = null
      if (format == "pdf"){
        Filepath = 'data:application/pdf;base64,' + res._file
      }else{
        Filepath = 'data:text/xml;base64,' + res._file
      }
      saveAs(Filepath, res.nombreDoc)
    })
  }
  // cargarDocumentos() {
  //   this.envio.peticionGet(environment.url + '/api/documentos/lista-documentos-empresa/').subscribe((res) => {
  //     this.listaDocumentos = res
  //   })
  // }

  visualizardoc(id: any) {
    this.envio.peticionGet(environment.url + "/api/documentos/descargar-documento/" + id + "/?formato=pdf").subscribe(res => {
      let blob2 = this.b64toBlob(res._file, "application/pdf")
      let url = URL.createObjectURL(blob2)
      window.open(url, res.nombreDoc)
    }, err => {
      console.log(err)
    })
  }

  b64toBlob(b64Data: any, contentType: any) {
    var byteCharacters = atob(b64Data);

    var byteArrays = [];

    for (let offset = 0; offset < byteCharacters.length; offset += 512) {
      var slice = byteCharacters.slice(offset, offset + 512),
        byteNumbers = new Array(slice.length);
      for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }
      var byteArray = new Uint8Array(byteNumbers);

      byteArrays.push(byteArray);
    }
    var blob = new Blob(byteArrays, { type: contentType });
    return blob;
  }

  obtenerObjetos(listDoc: any) {
    this.listaDocumentos = listDoc
  }

  buscador(nombre: any) {
    if (nombre == "") {
      this.nombreDocumento = ""
    }
    else {
      this.nombreDocumento = "?name=" + nombre.value
    }
  }

  cerrarConfirmacion() {
    let select = document.getElementById("select") as HTMLSelectElement
    this.descargardoc(select.value)
    let div = document.getElementById("emergente") as HTMLElement
    div.classList.toggle('visually-hidden')
    div.classList.remove("show")
    div?.classList.add("hide")
    
  }
  validarOpcion(id:any) {
    this.id = id
    let div = document.getElementById("emergente") as HTMLElement
    div.classList.toggle('visually-hidden')
    div?.classList.remove("hide")
    div.classList.add("show")
  }
}

