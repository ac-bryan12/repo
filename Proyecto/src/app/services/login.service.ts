import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  // private token = "";
    
  private token;
  constructor(private http:HttpClient) { 
    this.token=""
  }

  peticionPost(url:string,user:any):Observable<any>{
    const headers = { 
      // 'Content-type':'application/x-www-form-urlencoded; charset=UTF-8',
      // 'Access-Control-Allow-Headers':'Content-Type',
      // 'Access-Control-Allow-Methods': 'POST',
      // 'Access-Control-Allow-Origin': '*',
      // 'Access-Control-Allow-Credentials':"true"
    }  
    // const body=JSON.stringify(user);
    return this.http.post(url,user,{'headers':{'Authorization':this.getToken()}})
  }

  peticionGet(url:string):Observable<any>{
    return this.http.get(url,{headers:{'Authorization':this.getToken()}})
  }

  setToken(token:string):void{
    this.token = "Token "+token
  }

  getToken():string{
    return this.token
  }

}
