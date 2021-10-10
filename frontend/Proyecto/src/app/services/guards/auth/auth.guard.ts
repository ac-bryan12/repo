import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot, UrlTree,Router } from '@angular/router';
import { Observable } from 'rxjs';
import { RequestService } from '../../request/request.service';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private service: RequestService, private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
      const url: string = state.url;
      return this.checkLogin(url);
  }

  async checkLogin(url:string): Promise<true|UrlTree>{
    let autenticated = await this.service.peticionGet(environment.url+"/auth/isLogged/",false).toPromise().then(res => {return res['logged']}).catch(err => {return false})
    if(autenticated) {
      let rol = await this.service.peticionGet(environment.url+"/auth/userPermissions/").toPromise().then( res => {return res}).catch(err => console.log(err))
      if(rol.groups.includes('admin_facturacion') && url.includes('/admin')){
        return true;
      }else if(rol.groups.includes('cliente') && url.includes('/cliente')){
        return true;
      }else if(rol.groups.includes('admin_empresa') && url.includes('/view-company')){
        return true;
      }
    }

    // Store the attempted URL for redirecting
    this.service.redirectUrl = url;
    // Redirect to the login page
    return this.router.parseUrl('/login');
  }

  
  
}
