import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MentionsLegalesPage } from './mentions-legales.page';

describe('MentionsLegalesPage', () => {
  let component: MentionsLegalesPage;
  let fixture: ComponentFixture<MentionsLegalesPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(MentionsLegalesPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
