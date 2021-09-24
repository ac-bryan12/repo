import { TestBed } from '@angular/core/testing';

import { UtilGuard } from './util.guard';

describe('UtilGuard', () => {
  let guard: UtilGuard;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    guard = TestBed.inject(UtilGuard);
  });

  it('should be created', () => {
    expect(guard).toBeTruthy();
  });
});
