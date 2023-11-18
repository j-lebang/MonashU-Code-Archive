// socket.service.ts
import { Injectable } from '@angular/core';
import { io } from 'socket.io-client';
import { Observable, Observer } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SocketService {
  private socket;

  constructor() { 
    this.socket = io();
  }
  
  public sendText(data: {text: string, language: string}) {
    this.socket.emit('sendText', data);
  }
  
  public getTranslatedText = () => {
    return new Observable((observer: Observer<string>) => {
      this.socket.on('translatedText', (message: string) => {
        observer.next(message);
      });
    });
  }

  public textToSpeech(text: string) {
    this.socket.emit("text-present", text);
  }

}