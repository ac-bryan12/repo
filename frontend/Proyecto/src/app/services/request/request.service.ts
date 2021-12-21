import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Router, UrlTree } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';

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
  private headerFiles = {
    "Authorization":`Token ${localStorage.getItem("token")}`,
  }
  
  constructor(private http:HttpClient,private router:Router,private cookies:CookieService) { 
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

  peticionPut(url:string,user:any,isLogin:boolean=false):Observable<any>{
    if(!isLogin){
      this.setToken()
      return this.http.put(url,user,{headers:this.headers,withCredentials:true})
    }else{
      return this.http.put(url,user)
    }
  }

  peticionDelete(url:string):Observable<any>{
      this.setToken()
      return this.http.delete(url,{headers:this.headers,withCredentials:true})
  }

  peticionPostFiles(url:string,firma:any,isLogin:boolean=false):Observable<any>{
    if(!isLogin){
      this.setToken()
      return this.http.post(url,firma,{headers:this.headers,withCredentials:true})
    }else{
      return this.http.post(url,firma)
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

  checkPermissions(acceso:any,url:string,permissions:any):boolean{
    for(let [permiso,ruta]of acceso){
      for (let permission of permissions){
        if (permission.codename.includes(permiso)  && url.includes(ruta)) {
          this.cookies.set("return_to",url,{"path":"/"})
          return true
        }
      }
    }
    this.cookies.set("return_to",'/login')
    return false
  }

  async check(url: string,acceso:any): Promise<true | UrlTree>{
    let authenticated:boolean = await this.peticionGet(environment.url+"/auth/isLogged/",false).toPromise()
    .then(res=> {
        return res['logged']
    })
    .catch(err => {return false})
    if(authenticated){
      let rol = await this.peticionGet(environment.url+"/auth/userPermissions/").toPromise().then( res => {return res}).catch(err => console.log(err))
      if(this.checkPermissions(acceso,url,rol.permissions)){
        return true
      }

    }

    this.redirectUrl = url;
    return this.router.parseUrl('/login');

  }
}