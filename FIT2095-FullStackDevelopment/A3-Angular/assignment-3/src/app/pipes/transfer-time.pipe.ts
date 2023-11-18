import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'transferTime'
})
export class TransferTimePipe implements PipeTransform {

  transform(durationInMinutes: number): string {
    const hours = Math.floor(durationInMinutes / 60);
    const minutes = durationInMinutes % 60;
    return `${hours} hour(s) ${minutes} minute(s)`;
  }

}
