import { NgModule, isDevMode } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';
import { AppComponent } from './app.component';
import { AddEventsComponent } from './components/Event/add-events/add-events.component';
import { ListCategoryComponent } from './components/Category/list-category/list-category.component';
import { ListEventsComponent } from './components/Event/list-events/list-events.component';
import { DeleteEventComponent } from './components/Event/delete-event/delete-event.component';
import { UpdateEventComponent } from './components/Event/update-event/update-event.component';
import { InvalidDataErrorComponent } from './components/invalid-data-error/invalid-data-error.component';
import { PageNotFoundComponent } from './components/page-not-found/page-not-found.component';
import { StatsComponent } from './components/Event/stats/stats.component';
import { Route, RouterModule, Routes } from '@angular/router';
import { DataBaseService } from './services/data-base.service';
import { UtilService } from './services/util.service';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { EventDetailsComponent } from './components/Event/event-details/event-details.component';
import { TransferTimePipe } from './pipes/transfer-time.pipe';
import { ServiceWorkerModule } from '@angular/service-worker';
import { TranslateComponent } from './components/translate/translate.component';
import { IndexComponent } from './index/index.component';
import { AddCategoryComponent } from './components/Category/add-category/add-category.component';
import { DeleteCategoryComponent } from './components/Category/delete-category/delete-category.component';
import { UpdateCategoryComponent } from './components/Category/update-category/update-category.component';
import { CategoryDetailsComponent } from './components/Category/category-details/category-details.component';
import { StatsG1Component } from './components/Category/stats-g1/stats-g1.component';
import { TextToSpeechComponent } from './components/text-to-speech/text-to-speech.component';



const routes: Routes =[
  { path: "33279500/add-category", component: AddCategoryComponent },
  { path: "33279500/event-categories", component: ListCategoryComponent },
  { path: "33279500/delete-category", component: DeleteCategoryComponent },
  { path: "33279500/update-category", component: UpdateCategoryComponent },
  { path: "33279500/category/:id", component: CategoryDetailsComponent },
  { path: "33279500/stats-g1", component: StatsG1Component },
  { path: "33279500/text-to-speech", component: TextToSpeechComponent },
  {path:'YantaoHe/add-event',component: AddEventsComponent},
  {path:'YantaoHe/list-events',component: ListEventsComponent},
  {path:'YantaoHe/delete-event',component: DeleteEventComponent},
  {path:'YantaoHe/update-events',component: UpdateEventComponent},
  {path:'YantaoHe/stats-events',component: StatsComponent},
  {path: 'YantaoHe/event-details/:eventId', component: EventDetailsComponent},
  {path: 'invalid-data-error', component: InvalidDataErrorComponent },
  {path: 'YantaoHe/translate', component: TranslateComponent},
  {path: 'index', component: IndexComponent},
  {path: '', redirectTo: 'index', pathMatch: 'full'},
  {path:'',pathMatch:'full',redirectTo:'add-event'},
  {path:'**',component: PageNotFoundComponent}]




@NgModule({
  declarations: [
    AppComponent,
    AddEventsComponent,
    AddCategoryComponent,
    ListEventsComponent,
    DeleteEventComponent,
    UpdateEventComponent,
    InvalidDataErrorComponent,
    PageNotFoundComponent,
    StatsComponent,
    EventDetailsComponent,
    TransferTimePipe,
    TranslateComponent,
    IndexComponent,
    ListCategoryComponent,
    DeleteCategoryComponent,
    UpdateCategoryComponent,
    CategoryDetailsComponent,
    StatsG1Component,
    TextToSpeechComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes,{useHash: true}),
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule, 
    ServiceWorkerModule.register('ngsw-worker.js', {
      enabled: !isDevMode(),
      // Register the ServiceWorker as soon as the application is stable
      // or after 30 seconds (whichever comes first).
      registrationStrategy: 'registerWhenStable:30000'
    })
  ],
  providers: [DataBaseService, UtilService],
  bootstrap: [AppComponent]
})
export class AppModule { }
