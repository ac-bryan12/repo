import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

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
    // 'Content-type':'application/x-www-form-urlencoded; charset=UTF-8',
  }
  
  constructor(private http:HttpClient) { 
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

  peticionGet(url:string):Observable<any>{
    this.setToken()
    return this.http.get(url,{headers:this.headers,withCredentials: true})
  }


  setToken(){
    this.headers.Authorization= `Token ${localStorage.getItem("token")}`
  }
}
