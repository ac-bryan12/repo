import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import { RequestService } from '../../request/request.service';

@Injectable({
  providedIn: 'root'
})
export class ClienteGuard implements CanActivate {
  constructor(private service: RequestService) { }
  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
      const url: string = state.url;
      let acceso = [["view_profile","/perfil"],["change_profile","/cambiar_contrasenia"],["view_profile","/documentos"]]
      return this.service.check(url,acceso,'cliente');
  }
  
}
