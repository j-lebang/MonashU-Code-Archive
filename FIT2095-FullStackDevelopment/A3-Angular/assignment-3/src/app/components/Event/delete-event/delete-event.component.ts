import { Component } from '@angular/core';
import { DataBaseService } from 'src/app/services/data-base.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-delete-event',
  templateUrl: './delete-event.component.html',
  styleUrls: ['./delete-event.component.css']
})
export class DeleteEventComponent {
  
  calculateEndTime(startDateTime: Date, durationInMinutes: number) {
    const startDate = new Date(startDateTime);
    const endTime = new Date(startDate.getTime() + durationInMinutes * 60000); // Convert minutes to milliseconds
    return endTime.toLocaleString();
  }
  getLocalDateString(dateString: string): string {
    return new Date(dateString).toLocaleString();
  }
  getCategoryIds(categoryList: any[]): string {
    return categoryList.map(category => category.id).join(', ');
  }
  records: any[] = [];
    
  constructor(private dbservice:DataBaseService, private router: Router){
    this.getRecords();
  }
  deleteRecord(eventId: string) {
    this.dbservice.deleteEvent(eventId).subscribe({
      next: () => {
        const index = this.records.findIndex(event => event.id === eventId);
        if (index !== -1) {
          this.records.splice(index, 1);
        }
      },
      error: (error) => {
        if (error.status === 400) {
          this.router.navigate(['/invalid-data-error']);
        } else {
          console.error('Error deleting record');
        }
      }
    });
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
