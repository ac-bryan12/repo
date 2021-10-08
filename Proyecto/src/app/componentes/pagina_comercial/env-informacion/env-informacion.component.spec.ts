import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EnvInformacionComponent } from './env-informacion.component';

describe('EnvInformacionComponent', () => {
  let component: EnvInformacionComponent;
  let fixture: ComponentFixture<EnvInformacionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EnvInformacionComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EnvInformacionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
