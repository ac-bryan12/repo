import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import { RequestService } from '../../request/request.service';

@Injectable({
  providedIn: 'root'
})
export class EmpresaGuard implements CanActivate {
  constructor(private service: RequestService) { }

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
      const url: string = state.url;
      let acceso = [["view_user","/grupos-permisos"],["change_user","/editarUser"],["view_profile","/perfil"],["view_profile","/documentos-company"],["view_empresa","/vista-empresa"],["change_user","/cambiar-contrasenia"]]
      return this.service.check(url,acceso,'admin_empresa');
  }
  
}
