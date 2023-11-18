import { Component } from '@angular/core';
import { DataBaseService } from 'src/app/services/data-base.service';

@Component({
  selector: 'app-list-category',
  templateUrl: './list-category.component.html',
  styleUrls: ['./list-category.component.css']
})
export class ListCategoryComponent {
  categories: any[] = [];

  constructor(private dbService: DataBaseService) { this.getAll(); }

  getAll() {
    this.dbService.getCategories().subscribe({
      next: (data: any) => {
        this.categories = data;
      }
    });
  }
}
