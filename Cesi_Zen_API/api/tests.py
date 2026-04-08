from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

Utilisateur = get_user_model()

class ProfilTests(APITestCase):
    def setUp(self):
        """
        Cette méthode s'exécute AVANT chaque test. 
        On y prépare notre base de données de test (qui est détruite à la fin).
        """
        self.user = Utilisateur.objects.create_user(
            email='test@cesizen.fr',
            pseudo='TestUser',
            password='Password123!'
        )

        self.other_user = Utilisateur.objects.create_user(
            email='autre@cesizen.fr',
            pseudo='AutreUser',
            password='Password123!'
        )

        self.client.force_authenticate(user=self.user)

        self.update_profile_url = reverse('profile-update') 
        self.change_password_url = '/api/change-password/' 

    def test_update_profile_success(self):
        """
        Test 1: Vérifier qu'un utilisateur PEUT modifier son profil avec des données valides.
        """
        data = {
            'pseudo': 'NouveauPseudo',
            'email': 'nouveau@cesizen.fr'
        }
        response = self.client.put(self.update_profile_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.pseudo, 'NouveauPseudo')
        self.assertEqual(self.user.email, 'nouveau@cesizen.fr')

    def test_update_profile_email_already_taken(self):
        """
        Test 2: Vérifier qu'un utilisateur NE PEUT PAS utiliser l'email d'un autre.
        """
        data = {
            'pseudo': 'MonPseudo',
            'email': 'autre@cesizen.fr'
        }
        response = self.client.put(self.update_profile_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_change_password_success(self):
        """
        Test 3: Vérifier que le changement de mot de passe fonctionne avec le bon ancien mot de passe.
        """
        data = {
            'old_password': 'Password123!',
            'new_password': 'NouveauPassword456!'
        }
        response = self.client.put(self.change_password_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NouveauPassword456!'))

    def test_change_password_wrong_old_password(self):
        """
        Test 4: Vérifier que l'API bloque si l'ancien mot de passe est faux.
        """
        data = {
            'old_password': 'MauvaisPassword!',
            'new_password': 'NouveauPassword456!'
        }
        response = self.client.put(self.change_password_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Password123!'))

    def test_unauthenticated_user_access(self):
        """
        Test 5: Vérifier qu'un visiteur non connecté ne peut pas modifier un profil.
        """
        self.client.force_authenticate(user=None)

        data = {'pseudo': 'Hacker', 'email': 'hacker@cesizen.fr'}
        response = self.client.put(self.update_profile_url, data)

        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])