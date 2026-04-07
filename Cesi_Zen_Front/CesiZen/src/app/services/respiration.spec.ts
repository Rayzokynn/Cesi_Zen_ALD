import { TestBed } from '@angular/core/testing';

import { RespirationService } from './respiration';

describe('Respiration', () => {
  let service: RespirationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RespirationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
