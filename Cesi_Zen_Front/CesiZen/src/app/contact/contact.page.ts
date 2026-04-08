import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonContent, IonHeader, IonTitle, IonToolbar, IonCardContent, IonCard, IonBackButton, IonButton, IonButtons, IonIcon, IonTextarea, IonText, IonLabel, IonItem, IonInput, IonList} from '@ionic/angular/standalone';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.page.html',
  styleUrls: ['./contact.page.scss'],
  standalone: true,
  imports: [IonContent, IonHeader, IonTitle, IonToolbar, CommonModule, FormsModule, IonCardContent, IonCard, IonBackButton, IonButton, IonButtons, IonIcon, IonTextarea, IonText, IonLabel, IonItem, IonInput, IonList]
})
export class ContactPage implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
