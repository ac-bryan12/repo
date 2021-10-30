import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GruposEmpresaComponent } from './grupos-empresa.component';

describe('GruposEmpresaComponent', () => {
  let component: GruposEmpresaComponent;
  let fixture: ComponentFixture<GruposEmpresaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GruposEmpresaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GruposEmpresaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
