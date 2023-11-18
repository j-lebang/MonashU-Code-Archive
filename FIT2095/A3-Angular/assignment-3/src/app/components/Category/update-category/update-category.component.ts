import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { DataBaseService } from 'src/app/services/data-base.service';

@Component({
  selector: 'app-update-category',
  templateUrl: './update-category.component.html',
  styleUrls: ['./update-category.component.css']
})
export class UpdateCategoryComponent {
  category = {
    id: "",
    name: "",
    desc: ""
  }

  constructor(private dbService: DataBaseService, private router: Router) {}

  updateCategory() {
    this.dbService.updateCategory(this.category).subscribe({
      next: () => {
        this.router.navigate(["/33279500/event-categories"]);
      }
    });
  }
}
