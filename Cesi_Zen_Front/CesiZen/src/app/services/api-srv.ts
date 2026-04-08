import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ApiSrv {
  private http: HttpClient = inject(HttpClient);
  baseApiUrl: string = 'https://cataas.com/cat';

  getCat() {
    return this.http.get(this.baseApiUrl + '?json=true');
  }
}
