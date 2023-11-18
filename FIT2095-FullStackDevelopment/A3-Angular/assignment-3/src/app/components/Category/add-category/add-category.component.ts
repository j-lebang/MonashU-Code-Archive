import { Component } from '@angular/core';
import { RouterModule, Router } from '@angular/router';
import { DataBaseService } from 'src/app/services/data-base.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-add-category',
  templateUrl: './add-category.component.html',
  styleUrls: ['./add-category.component.css']
})
export class AddCategoryComponent {
  category: any = {
    name: "",
    desc: "",
    image: ""
  }

  constructor(private dbService: DataBaseService, private router: Router) {}

  saveCategory() {
    let category = {
      "name": this.category.name,
      "desc": this.category.desc,
      "image": this.category.image
    }
    this.dbService.addCategory(category).subscribe({
      next: () => { this.router.navigate(["/33279500/event-categories"]); },
      error: () => { this.router.navigate(["/invalid-data-error"]); }
    });
  }
}
