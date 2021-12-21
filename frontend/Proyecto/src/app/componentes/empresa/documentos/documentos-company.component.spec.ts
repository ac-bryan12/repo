import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DocumentosCompanyComponent } from './documentos-company.component';

describe('DocumentosCompanyComponent', () => {
  let component: DocumentosCompanyComponent;
  let fixture: ComponentFixture<DocumentosCompanyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DocumentosCompanyComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DocumentosCompanyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
