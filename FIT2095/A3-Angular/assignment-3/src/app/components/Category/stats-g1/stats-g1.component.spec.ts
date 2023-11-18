import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StatsG1Component } from './stats-g1.component';

describe('StatsG1Component', () => {
  let component: StatsG1Component;
  let fixture: ComponentFixture<StatsG1Component>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [StatsG1Component]
    });
    fixture = TestBed.createComponent(StatsG1Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
