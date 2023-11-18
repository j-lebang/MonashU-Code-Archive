import { Component } from '@angular/core';
import { DataBaseService } from 'src/app/services/data-base.service';
import { Router } from '@angular/router';

import { FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-add-events',
  templateUrl: './add-events.component.html',
  styleUrls: ['./add-events.component.css']
})
export class AddEventsComponent {
  eventForm = new FormGroup({
    name: new FormControl('', Validators.required),
    description: new FormControl(''),
    image: new FormControl('', Validators.required),
    startDateTime: new FormControl('', Validators.required),
    durationInMinutes: new FormControl(0, Validators.required),
    isActive: new FormControl(''),
    capacity: new FormControl(0),
    ticketsAvailable: new FormControl(0),
    categoryList: new FormControl('', Validators.required),
  });

  constructor(private dbService: DataBaseService, private router: Router) {}

  saveEvent() {
    if (this.eventForm.valid) {
      let eventobj = this.eventForm.value;
      this.dbService.addEvent(eventobj).subscribe({
        next: (result) => {
          console.log(result);
          this.router.navigate(['/YantaoHe/list-events']);
        },
        error: (error) => {
          if (error.status === 400) {
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
}
