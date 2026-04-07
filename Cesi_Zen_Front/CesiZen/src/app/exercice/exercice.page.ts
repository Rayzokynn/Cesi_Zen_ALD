import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { RespirationService } from '../services/respiration';
import { HeaderComponent } from '../components/header/header.component';


@Component({
  selector: 'app-exercice',
  templateUrl: './exercice.page.html',
  styleUrls: ['./exercice.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, HeaderComponent]
})
export class ExercicePage {

  constructor(public respirationService: RespirationService) {}

  ionViewWillLeave() {
    this.respirationService.resetExercise(); // Arrête l'exercice si on quitte la page
  }
}