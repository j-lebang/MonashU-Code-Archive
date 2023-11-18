import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { DataBaseService } from 'src/app/services/data-base.service';

@Component({
  selector: 'app-delete-category',
  templateUrl: './delete-category.component.html',
  styleUrls: ['./delete-category.component.css']
})
export class DeleteCategoryComponent {
  categories: any[] = [];

  constructor(private dbService: DataBaseService, private router: Router) {
    this.getAll()
  }

  getAll() {
    this.dbService.getCategories().subscribe({
      next: (data: any) => {
        this.categories = data;
      }
    });
  }

  deleteCategory(id: string) {
    this.dbService.deleteCategory(id).subscribe({
      next: () => {
        this.router.navigate(['/33279500/event-categories']);
      }
    });
  }
}
