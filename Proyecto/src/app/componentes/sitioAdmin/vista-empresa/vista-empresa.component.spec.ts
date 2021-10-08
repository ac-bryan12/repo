import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VistaEmpresaComponent } from './vista-empresa.component';

describe('VistaEmpresaComponent', () => {
  let component: VistaEmpresaComponent;
  let fixture: ComponentFixture<VistaEmpresaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ VistaEmpresaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(VistaEmpresaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
