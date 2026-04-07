import { Injectable, OnDestroy } from '@angular/core';

export interface Phase {
  name: string;
  time: number;
  targetBottom: number;
}

export interface Technique {
  name: string;
  description: string;
  inspire: number;
  apnee: number;
  expire: number;
}

@Injectable({
  providedIn: 'root'
})
export class RespirationService implements OnDestroy {
  techniques: Technique[] = [
    { name: 'Relaxant', description: '7s inspiration, 4s apnée, 8s expiration', inspire: 7, apnee: 4, expire: 8 },
    { name: 'Équilibrant', description: '5s inspiration, 5s expiration', inspire: 5, apnee: 0, expire: 5 },
    { name: 'Apaisant', description: '4s inspiration, 6s expiration', inspire: 4, apnee: 0, expire: 6 }
  ];

  activeTechnique: Technique = this.techniques[0];
  phases: Phase[] = [];
  currentPhaseIndex = 0;
  timeLeft = 0;
  cycleCount = 0;
  isPlaying = false;
  instruction = '';
  
  balloonBottom = 0;
  balloonTransition = 'bottom 0.5s ease-out';

  private timer: any;

  constructor() {
    this.setTechnique(this.activeTechnique);
  }

  ngOnDestroy() {
    this.clearTimer();
  }

  // 3. La logique métier
  setTechnique(technique: Technique) {
    this.activeTechnique = technique;
    
    this.phases = [{ name: 'Inspirez', time: technique.inspire, targetBottom: 90 }];
    if (technique.apnee > 0) {
      this.phases.push({ name: 'Maintenez', time: technique.apnee, targetBottom: 90 });
    }
    this.phases.push({ name: 'Expirez', time: technique.expire, targetBottom: 0 });

    this.resetExercise();
  }

  togglePlay() {
    if (this.isPlaying) {
      this.clearTimer();
      this.balloonTransition = 'none'; 
    } else {
      this.animationBallon();
      this.timer = setInterval(() => this.tick(), 1000);
    }
    this.isPlaying = !this.isPlaying;
  }

  tick() {
    if (this.timeLeft > 1) {
      this.timeLeft--;
    } else {
      this.currentPhaseIndex++;
      if (this.currentPhaseIndex >= this.phases.length) {
        this.currentPhaseIndex = 0;
        this.cycleCount++;
      }
      this.timeLeft = this.phases[this.currentPhaseIndex].time;
      this.instruction = this.phases[this.currentPhaseIndex].name;
      this.animationBallon();
    }
  }

  animationBallon() {
    this.balloonTransition = `bottom ${this.timeLeft}s linear`;
    this.balloonBottom = this.phases[this.currentPhaseIndex].targetBottom;
  }

  resetExercise() {
    this.clearTimer();
    this.isPlaying = false;
    this.currentPhaseIndex = 0;
    this.cycleCount = 0;
    this.timeLeft = this.phases[0].time;
    this.instruction = this.phases[0].name;
    this.balloonTransition = 'bottom 0.5s ease-out';
    this.balloonBottom = 0;
  }

  private clearTimer() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }
}