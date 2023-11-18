import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UtilService {
  calculateEndTime(startDateTime: Date, durationInMinutes: number): string {
    const startDate = new Date(startDateTime);
    const endTime = new Date(startDate.getTime() + durationInMinutes * 60000); // Convert minutes to milliseconds
    return endTime.toLocaleString();
  }
  getCategoryIds(categoryList: any[]): string {
    return categoryList.map(category => category.id).join(', ');
  }
  eventToAdd: number = 0;

  setEventToAdd(value: number) {
    this.eventToAdd = value;
  }

  getEventToAdd() {
    return this.eventToAdd;
  }
}