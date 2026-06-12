import { Component, CUSTOM_ELEMENTS_SCHEMA, inject, OnInit } from '@angular/core';
import { IonHeader, IonToolbar, IonContent, IonCard, AlertController, } from '@ionic/angular/standalone';
import { HeaderComponent } from '../components/header/header.component';
import { FormsModule } from '@angular/forms';
import { Preferences } from '@capacitor/preferences';
import { Router } from '@angular/router';
import { ArticleService } from '../services/article';
import { RespirationService } from '../services/respiration';

interface Article {
  id: number;
  titre: string;
  imageUrl: string; 
}

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [IonHeader, IonToolbar, IonContent, HeaderComponent, FormsModule, IonCard],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})

export class HomePage implements OnInit {
  private respirationService = inject(RespirationService);

  private router: Router = inject(Router);
  private alertController: AlertController = inject(AlertController);
  private articleService: ArticleService = inject(ArticleService);
  private STORAGE_KEY = 'list-images'
  private POPUP_KEY = 'popup-welcome-shown'
  user: string = 'Alexis';
  historique: any[] = [];
  chargement = true;

  tousLesArticles: Article[] = [];
  articles: Article[] = [];

  constructor() {
    console.log('Constructeur  Page');
  }

  lireArticle(id: number) {
    this.router.navigate(['/article-detail', id]);
  }

  async ngOnInit() {
    console.log('ngOnInit');
  }

  ionViewWillEnter() {
    console.log('IonViewWillEnter');
    this.chargerArticles();
    this.chargerHistorique();
  }

  chargerArticles() {
    this.articleService.getArticles().subscribe({
      next: (data) => {
        this.tousLesArticles = data;
        this.articles = [...this.tousLesArticles];
      },
      error: (err) => {
        console.error('Erreur lors de la récupération des articles:', err);
      }
    });
  }
  ionViewDidEnter() {
    console.log('IonViewDidEnter');
    this.showWelcomePopup();
  }

  ionViewWillLeave() {
    console.log('IonViewWillLeave');
  }

  ionViewDidLeave() {
    console.log('IonViewDidLeave');
  } 

  getExercicePage() {
    this.router.navigate(['/tabs/tab2']);
  }

  async showWelcomePopup() {
    const popupShown = await Preferences.get({ key: this.POPUP_KEY });
    
    if (!popupShown.value) {
      const alert = await this.alertController.create({
        header: 'Bienvenue ' + this.user + ' !',
        buttons: ['Merci !'],
      });
      await alert.present();
      
      await Preferences.set({
        key: this.POPUP_KEY,
        value: 'true',
      });
    }
  }

  rechercherArticle(event: any) {
    const texteRecherche = event.target.value.toLowerCase();

    if (!texteRecherche) {
      this.articles = [...this.tousLesArticles];
      return;
    }
    this.articles = this.tousLesArticles.filter(article => 
      article.titre.toLowerCase().includes(texteRecherche)
    );
  }

  chargerHistorique() {
    this.chargement = true;
    this.respirationService.getHistorique().subscribe({
      next: (data) => {
        this.historique = data;
        this.chargement = false;
      },
      error: (err) => {
        console.error('Erreur de récupération:', err);
        this.chargement = false;
      }
    });
  }
}
