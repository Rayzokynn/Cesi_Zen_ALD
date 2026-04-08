import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class Profile {
  private http = inject(HttpClient);


  getProfile(): Observable<any> {
    return this.http.get(`${environment.apiUrl}/profile/`);
  }

  updateProfile(data: any): Observable<any> {
    return this.http.put(`${environment.apiUrl}/profile/`, data);
  }

  changePassword(data: any): Observable<any> {
    return this.http.put(`${environment.apiUrl}/change-password/`, data);
  }
}
