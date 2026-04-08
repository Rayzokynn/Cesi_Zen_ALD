import { Component, inject, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { IonHeader, IonToolbar, IonContent, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonAvatar, IonList, IonItem, IonLabel, IonButton, IonIcon, IonGrid, IonRow, IonCol, IonText, IonInput, AlertController } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HeaderComponent } from '../components/header/header.component';
import { AuthSrv } from '../services/auth';
import { personOutline, statsChartOutline, settingsOutline, pencilOutline, lockClosedOutline, logOutOutline } from 'ionicons/icons';

@Component({
  selector: 'app-profil',
  templateUrl: 'profil.page.html',
  styleUrls: ['profil.page.scss'],
  standalone: true,
  imports: [CommonModule, FormsModule, IonHeader, IonToolbar, IonContent, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonAvatar, IonList, IonItem, IonLabel, IonButton, IonIcon, IonGrid, IonRow, IonCol, IonText, IonInput, HeaderComponent],
})
export class ProfilPage implements OnInit {
  private http = inject(HttpClient);
  private authService = inject(AuthSrv);
  private alertCtrl = inject(AlertController);
  
  user: any = { username: '', email: '' };
  userBackup: any = {};
  isEditing: boolean = false;
  userInitials: string = 'U';
  stats = { exercices: 0, articles: 0, minutes: 0 };

  personOutline = personOutline;
  statsChartOutline = statsChartOutline;
  settingsOutline = settingsOutline;
  pencilOutline = pencilOutline;
  lockClosedOutline = lockClosedOutline;
  logOutOutline = logOutOutline;

  ngOnInit() {
    this.loadProfile();
  }

  ionViewWillEnter() {
    this.chargerStatistiques();
  }

  loadProfile() {
    this.authService.getProfile().subscribe({
      next: (res: any) => {
        this.user = res;
        this.userBackup = { ...res };
        this.userInitials = this.getInitials(res.pseudo);
      },
      error: (err: any) => console.error('Erreur profil:', err)
    });
  }

  toggleEdit() {
    this.isEditing = true;
  }

  cancelEdit() {
    this.isEditing = false;
    this.user = { ...this.userBackup };
  }

  onUpdateProfile() {
    this.authService.updateProfile(this.user).subscribe({
      next: () => {
        this.isEditing = false;
        this.userBackup = { ...this.user };
        this.userInitials = this.getInitials(this.user.username);
        window.alert('Profil mis à jour !');
      },
      error: () => window.alert('Erreur lors de la mise à jour.')
    });
  }

  async openChangePassword() {
    const alertPopup = await this.alertCtrl.create({
      header: 'Sécurité',
      subHeader: 'Changer le mot de passe',
      inputs: [
        { name: 'old_password', type: 'password', placeholder: 'Ancien mot de passe' },
        { name: 'new_password', type: 'password', placeholder: 'Nouveau mot de passe' }
      ],
      buttons: [
        { text: 'Annuler', role: 'cancel' },
        {
          text: 'Confirmer',
          handler: (data) => {
            this.authService.changePassword(data).subscribe({
              next: () => window.alert('Mot de passe modifié !'),
              error: (err: any) => window.alert('Erreur: ' + (err.error?.detail || 'Échec'))
            });
          }
        }
      ]
    });
    await alertPopup.present();
  }

  chargerStatistiques() {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    const headers = new HttpHeaders({ 'Authorization': `Bearer ${token}` });
    this.http.get<any>(`${environment.apiUrl}/profil/stats/`, { headers }).subscribe({
      next: (data) => this.stats = data,
      error: (err) => console.error('Erreur stats:', err)
    });
  }

  seDeconnecter() { this.authService.logout(); }

  private getInitials(name: string): string {
    if (!name) return 'U';
    const parts = name.trim().split(' ');
    return parts.length > 1 ? (parts[0][0] + parts[1][0]).toUpperCase() : parts[0][0].toUpperCase();
  }
}