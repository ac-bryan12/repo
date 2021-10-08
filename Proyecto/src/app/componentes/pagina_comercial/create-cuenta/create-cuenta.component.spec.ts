import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateCuentaComponent } from './create-cuenta.component';

describe('CreateCuentaComponent', () => {
  let component: CreateCuentaComponent;
  let fixture: ComponentFixture<CreateCuentaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CreateCuentaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateCuentaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
