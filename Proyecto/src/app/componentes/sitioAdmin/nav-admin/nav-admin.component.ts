import { Component, OnInit } from '@angular/core';
import { RequestService } from 'src/app/services/request/request.service';

@Component({
  selector: 'nav-admin',
  templateUrl: './nav-admin.component.html',
  styleUrls: ['./nav-admin.component.css']
})
export class NavAdminComponent implements OnInit {
  private listGrupos:string[]
  constructor(private service:RequestService) { 
    this.listGrupos = []
  }
  ngOnInit(): void {
  }


}
