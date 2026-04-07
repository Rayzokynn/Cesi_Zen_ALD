import { Component, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { IonHeader, IonToolbar, IonContent, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonAvatar, IonList, IonItem, IonLabel, IonButton, IonIcon, IonGrid, IonRow, IonCol, IonText } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../components/header/header.component';
import { UserSrv } from '../services/user';
import { AuthSrv } from '../services/auth';
import { personOutline, statsChartOutline, settingsOutline, pencilOutline, lockClosedOutline, logOutOutline } from 'ionicons/icons';

interface User {
  id: number;
  name: string;
  email: string;
  age: number;
}

@Component({
  selector: 'app-profil',
  templateUrl: 'profil.page.html',
  styleUrls: ['profil.page.scss'],
  standalone: true,
  imports: [CommonModule, IonHeader, IonToolbar, IonContent, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonAvatar, IonList, IonItem, IonLabel, IonButton, IonIcon, IonGrid, IonRow, IonCol, IonText, HeaderComponent],
})

export class ProfilPage {
  private userService: UserSrv = inject(UserSrv);
  private http = inject(HttpClient);
  
  userProfil : User = this.userService.getUsers()[0];
  userInitials: string = 'U';

  stats = {
    exercices: 0,
    articles: 0,
    minutes: 0
  };

  // Icons
  personOutline = personOutline;
  statsChartOutline = statsChartOutline;
  settingsOutline = settingsOutline;
  pencilOutline = pencilOutline;
  lockClosedOutline = lockClosedOutline;
  logOutOutline = logOutOutline;

  constructor(private authService: AuthSrv) {}
  
  ionViewWillEnter() {
    this.chargerStatistiques();
  }
  
  chargerStatistiques() {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });

    this.http.get<any>(`${environment.apiUrl}/profil/stats/`, { headers }).subscribe({
      next: (data) => {
        this.stats = data; // Met à jour l'interface avec les vrais chiffres
      },
      error: (err) => console.error('Erreur stats:', err)
    });
  }
  seDeconnecter(){
    this.authService.logout();
  }

  private getInitials(name: string | undefined): string {
    if (!name || name.trim() === '') {
      return 'U';
    }

    const words = name.trim().split(' ');
    if (words.length === 1) {
      return words[0].charAt(0).toUpperCase();
    } else {
      return (words[0].charAt(0) + words[1].charAt(0)).toUpperCase();
    }
  }
}
