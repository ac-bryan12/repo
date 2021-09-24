import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot, UrlTree } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { Observable } from 'rxjs';
import { RequestService } from '../../request/request.service';

@Injectable({
  providedIn: 'root'
})
export class AdminGuard implements CanActivate {
  constructor(private service: RequestService, private router: Router, private cookie: CookieService) { }

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    const url: string = state.url;
    return this.checkPermission(url);
  }

  checkPermission(url: string): true | UrlTree {
    let response: any = this.router.parseUrl('/login');
    if (localStorage.getItem('Autenticated')=='true') {
      let permissions = this.cookie.get('permissions')
      let permissionsFormated = JSON.parse(decodeURI(permissions.replace(/\\054/g, ',')))
      let permissionsName = JSON.parse(permissionsFormated)

      permissionsName.forEach((permission: any) => {
        permission = permission['codename']
        if (permission == 'view_empresatemp' && url.endsWith('/empresasTemp')) {
          response = null
          response = true
        } else if (permission == 'view_empresa' && url.endsWith('/empresas')) {
          response = null
          response = true
        }/*else if (permission == 'view_user' && url.endsWith('/')) {
        return true
      }*/


      }
      );
    }
    this.service.redirectUrl = url;
    // Redirect to the login page
    return response

  }

}
