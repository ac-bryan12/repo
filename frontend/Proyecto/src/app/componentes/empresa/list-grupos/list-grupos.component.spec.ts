import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListGruposComponent } from './list-grupos.component';

describe('ListGruposComponent', () => {
  let component: ListGruposComponent;
  let fixture: ComponentFixture<ListGruposComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ListGruposComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ListGruposComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
