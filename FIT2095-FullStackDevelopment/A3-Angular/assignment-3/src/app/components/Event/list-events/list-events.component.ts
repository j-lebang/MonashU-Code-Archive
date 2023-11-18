import { Component } from '@angular/core';
import { DataBaseService } from 'src/app/services/data-base.service';
import { UtilService } from 'src/app/services/util.service';

@Component({
  selector: 'app-list-events',
  templateUrl: './list-events.component.html',
  styleUrls: ['./list-events.component.css']
})
export class ListEventsComponent {
  calculateEndTime(startDateTime: Date, durationInMinutes: number) {
    return this.utilService.calculateEndTime(startDateTime, durationInMinutes);
  }
  getCategoryIds(categoryList: any[]): string {
    return this.utilService.getCategoryIds(categoryList);
  }
  getLocalDateString(dateString: string): string {
    return new Date(dateString).toLocaleString();
  }
  
  records: any[] = [];
    
  constructor(private dbservice:DataBaseService, private utilService: UtilService){
    this.getRecords();
  }

  getRecords(){
    this.dbservice.getEvents().subscribe({
      next:(data:any)=>{
        this.records=data;
      },
      error:(err)=>{}
    })
  }
}
