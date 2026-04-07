import { Component, inject } from '@angular/core';
import { IonHeader, IonToolbar, IonContent, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonAvatar, IonList, IonItem, IonLabel, IonButton, IonIcon, IonGrid, IonRow, IonCol, IonText } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../components/header/header.component';
import { UserSrv } from '../services/user';
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
  imports: [CommonModule, IonHeader, IonToolbar, IonContent, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonAvatar, IonList, IonItem, IonLabel, IonButton, IonIcon, IonGrid, IonRow, IonCol, IonText, HeaderComponent],
})

export class ProfilPage {
  private userService: UserSrv = inject(UserSrv);
  
  userProfil : User = this.userService.getUsers()[0];
  userInitials: string = 'U';

  // Icons
  personOutline = personOutline;
  statsChartOutline = statsChartOutline;
  settingsOutline = settingsOutline;
  pencilOutline = pencilOutline;
  lockClosedOutline = lockClosedOutline;
  logOutOutline = logOutOutline;

  constructor() {
    this.userInitials = this.getInitials(this.userProfil?.name);
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
