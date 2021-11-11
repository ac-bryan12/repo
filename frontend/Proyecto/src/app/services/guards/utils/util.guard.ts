import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import { RequestService } from '../../request/request.service';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class UtilGuard implements CanActivate {

  constructor(private service: RequestService, private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
      const url: string = state.url;

      return this.checkState(url);
  }

  checkState(url:string):true|UrlTree{
    console.log(url)
    if(this.service.isRegistered && url.endsWith('/env-informacion') ) { 
      return true; 
    }else if(this.service.isCreatedAccount && url.endsWith('/creacion-exitosa')){
      return true; 
    }
    // Store the attempted URL for redirecting
    this.service.redirectUrl = url;
    // Redirect to the login page
    return this.router.parseUrl('/home');
  }
  

}
