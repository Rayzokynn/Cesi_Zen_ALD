import { HttpClient, HttpHeaders } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AuthSrv {
  private http = inject(HttpClient);
  private router = inject(Router);
  public isAuthenticated = !!localStorage.getItem('access_token');

  private getHeaders() {
    return {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      })
    };
  }

  // --- AUTHENTIFICATION ---
  login(credentials: { email: string; password: string }) {
    return this.http.post<any>(`${environment.apiUrl}/login/`, credentials).pipe(
      tap(response => {
        if (response && response.access) {
          localStorage.setItem('access_token', response.access);
          if (response.refresh) localStorage.setItem('refresh_token', response.refresh);
          this.isAuthenticated = true;
        }
      })
    );
  }

  register(userData: any) {
    return this.http.post(`${environment.apiUrl}/utilisateurs/create/`, userData);
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.isAuthenticated = false;
    this.router.navigate(['/connexion']);
  }

  // --- PROFIL ---
  getProfile(): Observable<any> {
    return this.http.get(`${environment.apiUrl}/profile/`, this.getHeaders());
  }

  updateProfile(data: any): Observable<any> {
    return this.http.put(`${environment.apiUrl}/profile/update/`, data, this.getHeaders());
  }

  changePassword(data: any): Observable<any> {
    return this.http.post(`${environment.apiUrl}/change-password/`, data, this.getHeaders());
  }
}