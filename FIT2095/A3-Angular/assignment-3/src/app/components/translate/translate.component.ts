import { Component } from '@angular/core';
import { SocketService } from 'src/app/services/socket.service';

interface Translation {
  text: string;
  language: string;
  translation: string;
}

const LANGUAGE_MAP: { [key: string]: string } = {
  'zh': 'Chinese',
  'ko': 'Korean',
  'fr': 'French',
};

@Component({
  selector: 'app-translate',
  templateUrl: './translate.component.html',
  styleUrls: ['./translate.component.css']
})
export class TranslateComponent {

  public text = '';
  public language = 'zh'; 
  public translations: Translation[] = [];

  constructor(private socketService: SocketService) { 
    this.socketService.getTranslatedText().subscribe((message: string) => {
      this.translations.push({
        text: this.text, 
        language: `${LANGUAGE_MAP[this.language]}(${this.language})`, 
        translation: message
      });
    });
  }

  sendText() {
    this.socketService.sendText({text: this.text, language: this.language});
  }
}