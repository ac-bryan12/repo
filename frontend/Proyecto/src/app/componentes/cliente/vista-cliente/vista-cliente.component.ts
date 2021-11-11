import { Component, OnInit } from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';

@Component({
  selector: 'cliente',
  templateUrl: './vista-cliente.component.html',
  styleUrls: ['./vista-cliente.component.css']
})
export class VistaClienteComponent implements OnInit {

  constructor(private router:Router,private route:ActivatedRoute) { }

  ngOnInit(): void {
  }

}
