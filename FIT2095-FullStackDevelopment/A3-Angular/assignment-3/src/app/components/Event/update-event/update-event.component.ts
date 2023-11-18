import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { DataBaseService } from 'src/app/services/data-base.service';
import { UtilService } from 'src/app/services/util.service';

@Component({
  selector: 'app-update-event',
  templateUrl: './update-event.component.html',
  styleUrls: ['./update-event.component.css']
})
export class UpdateEventComponent {
  eventForm = new FormGroup({
    name: new FormControl('', Validators.required),
    capacity: new FormControl(0),
  });
  transferTime(durationInMinutes: number): string {
    const hours = Math.floor(durationInMinutes / 60);
    const minutes = durationInMinutes % 60;
    return `${hours} hour(s) ${minutes} minute(s)`;
  }
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
  selectedEvent: any;
  constructor(private dbservice:DataBaseService, private utilService: UtilService,private router: Router){
    this.getRecords();
  }
  selectEvent(event: any) {
    this.selectedEvent = event;
  }
  

  saveEvent() {
    if (this.eventForm.valid) {
      this.dbservice.updateEvent(this.selectedEvent.id, this.eventForm.value).subscribe({
        next: (result) => {
          console.log(result);
          this.router.navigate(['/YantaoHe/list-events']);
        },
        error: (error) => {
          if (error.status === 404) {
            this.router.navigate(['/invalid-data-error']);
          } else {
            console.log(error);
          }
        }
      });
    } else {
      console.log('Form is invalid');
    }
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


