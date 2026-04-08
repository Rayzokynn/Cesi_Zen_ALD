import { addIcons } from 'ionicons';
import { eye, eyeOff } from 'ionicons/icons';
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthSrv } from '../services/auth';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import {IonContent, IonCard, IonCardContent, IonInput, IonButton, IonIcon, IonItem, IonLabel, IonNote, IonSpinner} from '@ionic/angular/standalone';
import { lockClosedOutline, mailOutline, personOutline } from 'ionicons/icons';

@Component({
  selector: 'app-connexion',
  templateUrl: './connexion.page.html',
  styleUrls: ['./connexion.page.scss'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, IonContent, IonCard, IonCardContent, IonInput, IonButton, IonIcon, IonItem, IonLabel, IonNote, IonSpinner],
})
export class ConnexionPage implements OnInit {
  loginForm!: FormGroup;
  registerForm!: FormGroup;
  isLoading = false;
  showPassword = false;
  isLoginMode = true;

  lockClosedOutline = lockClosedOutline;
  mailOutline = mailOutline;
  personOutline = personOutline;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthSrv,
    private router: Router
  ) {
    addIcons({ eye, 'eye-off': eyeOff });
  }

  private initializeForm() {
    this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]], 
    });
    this.registerForm = this.formBuilder.group({
      pseudo: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
    });
  }

  ngOnInit() {
    this.initializeForm();
  }

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  toggleMode() {
    this.isLoginMode = !this.isLoginMode;
    this.loginForm.reset();
    this.registerForm.reset();
  }

  onSubmit() {
    if (this.isLoginMode && this.loginForm.valid) {
      this.isLoading = true;
      const credentials = this.loginForm.value;

      this.authService.login(credentials).subscribe({
        next: (res) => {
          this.isLoading = false;
          this.router.navigate(['/tabs']);
        },
        error: (err) => {
          this.isLoading = false;
          alert('Email ou mot de passe incorrect.');
        }
      });

    } else if (!this.isLoginMode && this.registerForm.valid) {
      this.isLoading = true;
      const userData = this.registerForm.value;

      this.authService.register(userData).subscribe({
        next: (res) => {
          this.isLoading = false;
          alert('Compte créé avec succès ! Vous pouvez maintenant vous connecter.');
          this.toggleMode();
        },
        error: (err) => {
          this.isLoading = false;
          alert('Erreur lors de la création du compte. Cet email ou pseudo est peut-être déjà pris.');
          console.error(err);
        }
      });
    }
  }
  
  getEmailError(): string {
    const emailControl = this.loginForm.get('email');
    if (emailControl?.hasError('required')) {
      return 'Email requis';
    }
    if (emailControl?.hasError('email')) {
      return 'Email invalide';
    }
    return '';
  }

  getPasswordError(): string {
    const passwordControl = this.loginForm.get('password');
    if (passwordControl?.hasError('required')) {
      return 'Mot de passe requis';
    }
    if (passwordControl?.hasError('minlength')) {
      return 'Minimum 6 caractères';
    }
    return '';
  }
}
