import { Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

export const routes: Routes = [
  {
    path: '',
    component: TabsPage,
    children: [
      {
        path: 'tab1',
        loadComponent: () => import('../home/home.page').then((m) => m.HomePage),
      },
      {
        path: 'tab2',
        loadComponent: () => import('../exercice/exercice.page').then((m) => m.ExercicePage),
      },
      {
        path: 'tab3',
        loadComponent: () => import('../profil/profil.page').then((m) => m.ProfilPage),
      },
      {
        path: '',
        redirectTo: 'tab1',
        pathMatch: 'full',
      },
    ],
  }
];