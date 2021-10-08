import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot, UrlTree,Router } from '@angular/router';
import { Observable } from 'rxjs';
import { RequestService } from '../../request/request.service';

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

  checkLogin(url:string): true|UrlTree{
    if(localStorage.getItem("Autenticated")=='true') { return true; }

    // Store the attempted URL for redirecting
    this.service.redirectUrl = url;
    // Redirect to the login page
    return this.router.parseUrl('/login');
  }
  
}
