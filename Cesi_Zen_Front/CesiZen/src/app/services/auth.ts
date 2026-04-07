import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AuthSrv {
  private http = inject(HttpClient);
  public isAuthenticated = false;

  constructor() {
    this.isAuthenticated = !!localStorage.getItem('access_token');
  }

  login(credentials: { email: string; password: string }) {
    return this.http.post<any>(`${environment.apiUrl}/login/`, credentials).pipe(
      tap(response => {
        if (response && response.access) {
          localStorage.setItem('access_token', response.access);
          if (response.refresh) {
            localStorage.setItem('refresh_token', response.refresh);
          }
          this.isAuthenticated = true;
        }
      })
    );
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.isAuthenticated = false;
  }

  register(userData: { pseudo: string; email: string; password: string }) {
    return this.http.post(`${environment.apiUrl}/utilisateurs/create/`, userData);
  }
}