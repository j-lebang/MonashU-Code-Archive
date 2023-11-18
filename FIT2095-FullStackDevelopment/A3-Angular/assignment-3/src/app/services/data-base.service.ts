import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { catchError } from 'rxjs';

const httpoption = {
  headers: new HttpHeaders({"Content-Type":"application/json"})
}

@Injectable({
  providedIn: 'root'
})
export class DataBaseService {

  constructor(private http: HttpClient) { }

  addCategory(aCategory: any) {
    return this.http.post("/33279500/api/v1/add-category", aCategory);
  }

  getCategories(id: any = "") {
    return this.http.get("/33279500/api/v1/event-categories" + (id ? `/?id=${id}` : ""));
  }

  deleteCategory(categoryId: string) {
    return this.http.delete("/33279500/api/v1/delete-category", { body: { id: categoryId } });
  }

  updateCategory(aCategory: any) {
    return this.http.put("/33279500/api/v1/update-category", aCategory);
  }

  getCounts() {
    return this.http.get("/33279500/api/v1/get-status");
  }

  getEvents(eventId?: string){
      let url = '/YantaoHe/api/v1/list-events';
      if (eventId) {
        url += `?eventId=${eventId}`;
      }
      return this.http.get(url);
  }
  addEvent(newEvent:any){
    return this.http.post("/YantaoHe/api/v1/add-event",newEvent,httpoption);
  }
  deleteEvent(eventId: string) {
    return this.http.delete('/YantaoHe/api/v1/delete-event', { body: { eventId: eventId } });
  }
  
  getstatus(){
    return this.http.get("/YantaoHe/api/v1/get-status");
  }
  updateEvent(eventId: string, formData: any) {
    const requestBody = { ...formData, eventId: eventId };
    return this.http.put('/YantaoHe/api/v1/update-event', requestBody);
  }
}



