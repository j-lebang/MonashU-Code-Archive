import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DataBaseService } from 'src/app/services/data-base.service';
import { UtilService } from 'src/app/services/util.service';

@Component({
  selector: 'app-event-details',
  templateUrl: './event-details.component.html',
  styleUrls: ['./event-details.component.css']
})
export class EventDetailsComponent implements OnInit {
  eventId: string = '';
  records: any[] = [];
  calculateEndTime(startDateTime: Date, durationInMinutes: number) {
    return this.utilService.calculateEndTime(startDateTime, durationInMinutes);
  }
  getCategoryIds(categoryList: any[]): string {
    return this.utilService.getCategoryIds(categoryList);
  }
  constructor(private dbservice:DataBaseService, private utilService: UtilService, private route: ActivatedRoute) {}

  ngOnInit() {
    this.eventId = this.route.snapshot.paramMap.get('eventId') ?? '';
    this.getRecords();
  }

  getRecords() {
    this.dbservice.getEvents(this.eventId).subscribe({
      next: (data: any) => {
        this.records = data;
      },
      error: (err) => {}
    });
  }
}
