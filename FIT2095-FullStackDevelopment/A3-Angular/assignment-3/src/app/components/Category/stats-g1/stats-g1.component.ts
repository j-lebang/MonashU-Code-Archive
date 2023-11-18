import { Component, OnInit } from '@angular/core';
import { DataBaseService } from 'src/app/services/data-base.service';

@Component({
  selector: 'app-stats-g1',
  templateUrl: './stats-g1.component.html',
  styleUrls: ['./stats-g1.component.css']
})
export class StatsG1Component implements OnInit {
  categoryCount: number = 0;
  eventCount: number = 0;

  constructor(private dbService: DataBaseService) {}

  ngOnInit() {
    this.dbService.getCounts().subscribe({
      next: (data: any) => {
        this.categoryCount = data.categoryCount;
        this.eventCount = data.eventCount;
      }
    });
  }
}
