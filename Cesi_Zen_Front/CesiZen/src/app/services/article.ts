import { Injectable } from '@angular/core';

export interface Article {
  id: number;
  title: string;
  imageUrl: string;
}

@Injectable({
  providedIn: 'root'
})
export class ArticleService {

  private articles: Article[] = [
    { id: 1, title: 'Article 1', imageUrl: 'assets/placeholder-image.png' },
    { id: 2, title: 'Article 2', imageUrl: 'assets/placeholder-image.png' },
    { id: 3, title: 'Article 3', imageUrl: 'assets/placeholder-image.png' }
  ];

  constructor() { }

  getArticles(): Article[] {
    return this.articles;
  }

  getArticleById(id: number): Article | undefined {
    return this.articles.find(article => article.id === id);
  }
}