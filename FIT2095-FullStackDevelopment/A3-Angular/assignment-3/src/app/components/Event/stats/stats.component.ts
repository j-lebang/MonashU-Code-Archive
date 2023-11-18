import { Component, OnInit } from '@angular/core';
import { DataBaseService } from 'src/app/services/data-base.service';


@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.css']
})
export class StatsComponent implements OnInit{
  stats: any[] = [];
  constructor( private dbservice:DataBaseService  ) { }
  ngOnInit(): void {
    this.loadStats();
  }
  loadStats() {
      this.dbservice.getstatus().subscribe({
        next: (data: any) => {
          this.stats = Object.entries(data).map(([key, value]) => ({key, value}));
        },
        error: (err) => {}
      });
  }
}