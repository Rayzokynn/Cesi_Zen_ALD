import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { ActivatedRoute } from '@angular/router';
import { ArticleService } from '../services/article';
import { environment } from '../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-article-detail',
  templateUrl: './article-detail.page.html',
  styleUrls: ['./article-detail.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule]
})
export class ArticleDetailPage implements OnInit {
  article: any = null;
  chargement = true;
  
  private route = inject(ActivatedRoute);
  private articleService = inject(ArticleService);
  private http = inject(HttpClient);

  ngOnInit() {
    const idParam = this.route.snapshot.paramMap.get('id');
    
    if (idParam) {
      this.articleService.getArticleById(idParam).subscribe({
        next: (data) => {
          this.article = data;
          this.chargement = false;
          this.enregistrerLecture(idParam);
        },
        error: (err) => {
          console.error('Erreur lors du chargement de l\'article', err);
          this.chargement = false;
        }
      });
    } else {
      this.chargement = false;
    }
  }

  enregistrerLecture(id: string) {
    const token = localStorage.getItem('access_token');
    const headers = new HttpHeaders({ 'Authorization': `Bearer ${token}` });
    
    this.http.post(`${environment.apiUrl}/articles/${id}/lu/`, {}, { headers }).subscribe({
      next: () => console.log('Statistique de lecture mise à jour'),
      error: (err: any) => console.error('Erreur stat lecture:', err)
    });
  }
}