import { TestBed } from '@angular/core/testing';

import { ApiSrv } from './api-srv';

describe('ApiSrv', () => {
  let service: ApiSrv;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ApiSrv);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
