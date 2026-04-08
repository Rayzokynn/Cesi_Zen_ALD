import { Routes } from '@angular/router';
import { authGuard } from './src/app/guard-guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'tabs/tab1',
    pathMatch: 'full',
  },
  {
    path: 'connexion',
    loadComponent: () => import('./connexion/connexion.page').then( m => m.ConnexionPage)
  },
  {
    path: 'tabs',
    loadChildren: () => import('./tabs/tabs.routes').then(m => m.routes),
    canActivate: [authGuard]
  },
  {
    path: 'article-detail/:id',
    loadComponent: () => import('./article-detail/article-detail.page').then( m => m.ArticleDetailPage)
  },
  {
    path: 'cgu',
    loadComponent: () => import('./cgu/cgu.page').then( m => m.CguPage)
  },
  {
    path: 'mentions-legales',
    loadComponent: () => import('./mentions-legales/mentions-legales.page').then( m => m.MentionsLegalesPage)
  },
  {
    path: 'contact',
    loadComponent: () => import('./contact/contact.page').then( m => m.ContactPage)
  },
];