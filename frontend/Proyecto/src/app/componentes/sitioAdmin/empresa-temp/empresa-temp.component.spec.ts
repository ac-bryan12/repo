import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmpresaTempComponent } from './empresa-temp.component';

describe('EmpresaTempComponent', () => {
  let component: EmpresaTempComponent;
  let fixture: ComponentFixture<EmpresaTempComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EmpresaTempComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EmpresaTempComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
