import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NavEmpresaComponent } from './nav-empresa.component';

describe('NavEmpresaComponent', () => {
  let component: NavEmpresaComponent;
  let fixture: ComponentFixture<NavEmpresaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NavEmpresaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NavEmpresaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
