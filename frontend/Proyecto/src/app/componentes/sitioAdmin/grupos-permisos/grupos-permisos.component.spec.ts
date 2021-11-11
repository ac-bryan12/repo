import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GruposPermisosComponent } from './grupos-permisos.component';

describe('GruposPermisosComponent', () => {
  let component: GruposPermisosComponent;
  let fixture: ComponentFixture<GruposPermisosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GruposPermisosComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GruposPermisosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
