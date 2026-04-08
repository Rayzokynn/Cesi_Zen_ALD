import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // TEST 1 : Est-ce que l'intercepteur est bien branché ?
  console.log('🌍 REQUÊTE INTERCEPTÉE :', req.url); 

  const router = inject(Router);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      // TEST 2 : Quel est le code d'erreur exact renvoyé par Django ?
      console.error('🚨 ERREUR API REÇUE :', error.status, error.message); 

      // On vérifie 401 (Non autorisé) et 403 (Interdit)
      if (error.status === 401 || error.status === 403) {
        console.warn('🔄 Redirection vers la page de connexion déclenchée.');
        localStorage.removeItem('access_token');
        
        // ATTENTION : Vérifie que le chemin de ta page de connexion est bien '/login'
        router.navigate(['/connexion']); 
      }
      return throwError(() => error);
    })
  );
};