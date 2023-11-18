import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DataBaseService } from 'src/app/services/data-base.service';
import { UtilService } from 'src/app/services/util.service';

@Component({
  selector: 'app-category-details',
  templateUrl: './category-details.component.html',
  styleUrls: ['./category-details.component.css']
})
export class CategoryDetailsComponent implements OnInit {
  category: any = {
    id: "",
    name: "",
    desc: "",
    image: "",
    createdAt: "",
  }

  events: any[] = [];

  constructor(
    private dbService: DataBaseService, 
    private route: ActivatedRoute,
    private util: UtilService) {}

  ngOnInit() {
    this.category.id = this.route.snapshot.paramMap.get("id");
    this.dbService.getCategories(this.category.id).subscribe({
      next: (data) => {
        this.category = data;
        this.category = this.category[0];
        this.events = this.category.eventList;
        for (let i = 0; i < this.events.length; i++) {
          let start = new Date(this.events[i].startDateTime);
          this.events[i].endDateTime = new Date(start.getTime() + this.events[i].durationInMinutes * 60000);
          console.log(this.events[i]);
        }
      },
    });
  }

}
