import { Component } from '@angular/core';
import { SocketService } from 'src/app/services/socket.service';

@Component({
  selector: 'app-text-to-speech',
  templateUrl: './text-to-speech.component.html',
  styleUrls: ['./text-to-speech.component.css']
})
export class TextToSpeechComponent {
  text: string = "";
  
  constructor(private socket: SocketService) {}

  sendText() {
    this.socket.textToSpeech(this.text);
  }
}
