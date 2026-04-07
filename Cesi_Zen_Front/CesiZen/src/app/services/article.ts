import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ArticleService {
  private http = inject(HttpClient);
  
  getArticles() {
    return this.http.get<any[]>(`${environment.apiUrl}/articles/`);
  }

  getArticleById(id: string | number) {
    return this.http.get<any>(`${environment.apiUrl}/articles/${id}/`);
  }
}