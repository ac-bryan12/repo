import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { RequestService } from 'src/app/services/request/request.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'nav-admin',
  templateUrl: './nav-admin.component.html',
  styleUrls: ['./nav-admin.component.css']
})
export class NavAdminComponent implements OnInit {
  permissions:string[]

  constructor(private request: RequestService, private cookie: CookieService) {
    this.permissions = []
  }
  ngOnInit(): void {
    this.grupos_permisos()
  }


  async grupos_permisos() {
    let rol = await this.request.peticionGet(environment.url+"/auth/userPermissions/").toPromise().then( res => {return res}).catch(err => console.log(err))
    this.permissions = rol.permissions
  }

}
