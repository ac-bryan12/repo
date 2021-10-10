import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Router, UrlTree } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class RequestService {
  isLoggedIn = false;
  isCreatedAccount = false
  isRegistered = false

  redirectUrl: string | null = null;
  private headers = { 
    "Authorization":`Token ${localStorage.getItem("token")}`,
  }
  
  constructor(private http:HttpClient,private router:Router) { 
    this.redirectUrl = ""
  }

  peticionPost(url:string,user:any,isLogin:boolean=false):Observable<any>{
    if(!isLogin){
      this.setToken()
      return this.http.post(url,user,{headers:this.headers,withCredentials:true})
    }else{
      return this.http.post(url,user)
    }
  }

  peticionGet(url:string,isLogin:boolean=false):Observable<any>{
    if(!isLogin){
      this.setToken()
      return this.http.get(url,{headers:this.headers,withCredentials: true})
    }else{
      return this.http.get(url)
    }
    
  }

  setToken(){
    this.headers.Authorization= `Token ${localStorage.getItem("token")}`
  }

  checkPermissions(acceso:any,url:string,permissions:string[]):boolean{
    console.log(url)
    for(let [permiso,ruta]of acceso){
      if (permissions.includes(permiso)  && url.endsWith(ruta)) {
        return true
      }
    }
    return false
  }

  async check(url: string,acceso:any,grupo:string): Promise<true | UrlTree>{
    let authenticated:boolean = await this.peticionGet(environment.url+"/auth/isLogged/",false).toPromise()
    .then(res=> {
        return res['logged']
    })
    .catch(err => {return false})

    console.log(authenticated)
    if(authenticated){
      let rol = await this.peticionGet(environment.url+"/auth/userPermissions/").toPromise().then( res => {return res}).catch(err => console.log(err))
      if(rol.groups.includes(grupo)){
        if(this.checkPermissions(acceso,url,rol.permissions)){
          return true
        }
      }
    }

    this.redirectUrl = url;
    return this.router.parseUrl('/login');

  }
}
