import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthSrv } from '../../services/auth';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthSrv);
  const router = inject(Router);

  if (authService.isAuthenticated) {
    return true;
  } else {
    router.navigate(['/connexion']);
    return false;
  }
};