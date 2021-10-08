import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreacionExitosaComponent } from './creacion-exitosa.component';

describe('CreacionExitosaComponent', () => {
  let component: CreacionExitosaComponent;
  let fixture: ComponentFixture<CreacionExitosaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CreacionExitosaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CreacionExitosaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
