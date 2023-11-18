import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeleteEventComponent } from './delete-event.component';

describe('DeletetEventComponent', () => {
  let component: DeleteEventComponent;
  let fixture: ComponentFixture<DeleteEventComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DeleteEventComponent]
    });
    fixture = TestBed.createComponent(DeleteEventComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
