import { TestBed } from '@angular/core/testing';

import { UserSrv } from './user';

describe('UserSrv', () => {
  let service: UserSrv;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UserSrv);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
