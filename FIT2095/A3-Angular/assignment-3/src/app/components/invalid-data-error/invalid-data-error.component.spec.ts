import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InvalidDataErrorComponent } from './invalid-data-error.component';

describe('InvalidDataErrorComponent', () => {
  let component: InvalidDataErrorComponent;
  let fixture: ComponentFixture<InvalidDataErrorComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [InvalidDataErrorComponent]
    });
    fixture = TestBed.createComponent(InvalidDataErrorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
