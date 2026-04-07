import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExercicePage } from './exercice.page';

describe('ExercicePage', () => {
  let component: ExercicePage;
  let fixture: ComponentFixture<ExercicePage>;

  beforeEach(async () => {
    fixture = TestBed.createComponent(ExercicePage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
