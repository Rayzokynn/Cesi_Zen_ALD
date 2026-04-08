import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonContent, IonHeader, IonTitle, IonToolbar, IonCardContent, IonCard, IonCardTitle, IonCardHeader, IonBackButton, IonButtons} from '@ionic/angular/standalone';

@Component({
  selector: 'app-mentions-legales',
  templateUrl: './mentions-legales.page.html',
  styleUrls: ['./mentions-legales.page.scss'],
  standalone: true,
  imports: [IonContent, IonHeader, IonTitle, IonToolbar, CommonModule, FormsModule, IonCardContent, IonCard, IonCardTitle, IonCardHeader, IonBackButton, IonButtons]
})
export class MentionsLegalesPage implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
