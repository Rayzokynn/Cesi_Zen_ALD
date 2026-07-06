from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta
from .models import Utilisateur, SessionRespiration

class ProfilTests(APITestCase):
    def setUp(self):
        """
        Cette méthode s'exécute AVANT chaque test. 
        On y prépare notre base de données de test (qui est détruite à la fin).
        """
        self.user = Utilisateur.objects.create(
            email='test@cesizen.fr',
            pseudo='TestUser',
            password=make_password('Password123!')
        )

        self.other_user = Utilisateur.objects.create(
            email='autre@cesizen.fr',
            pseudo='AutreUser',
            password=make_password('Password123!')
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
        self.assertTrue(check_password('NouveauPassword456!', self.user.password))

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
        self.assertTrue(check_password('Password123!', self.user.password))

    def test_unauthenticated_user_access(self):
        """
        Test 5: Vérifier qu'un visiteur non connecté ne peut pas modifier un profil.
        """
        self.client.force_authenticate(user=None)

        data = {'pseudo': 'Hacker', 'email': 'hacker@cesizen.fr'}
        response = self.client.put(self.update_profile_url, data)

        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])


class RespirationTests(APITestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create(
            email='user@cesizen.fr',
            pseudo='UserRespi',
            password=make_password('Password123!')
        )
        self.client.force_authenticate(user=self.user)
        self.save_session_url = reverse('save_respiration')
        self.historique_url = reverse('historique_respiration')
        self.stats_url = reverse('profil_stats')

    def test_save_respiration_session_success(self):
        """Vérifier qu'un utilisateur authentifié peut enregistrer sa session."""
        data = {
            'technique_name': 'Relaxant',
            'cycles_completed': 4
        }
        response = self.client.post(self.save_session_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SessionRespiration.objects.filter(user=self.user).count(), 1)
        session = SessionRespiration.objects.filter(user=self.user).first()
        self.assertEqual(session.technique_name, 'Relaxant')
        self.assertEqual(session.cycles_completed, 4)

    def test_save_respiration_session_unauthenticated(self):
        """Vérifier qu'un visiteur non connecté est rejeté."""
        self.client.force_authenticate(user=None)
        data = {
            'technique_name': 'Apaisant',
            'cycles_completed': 5
        }
        response = self.client.post(self.save_session_url, data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_historique_respiration_order(self):
        """Vérifier que l'historique est renvoyé chronologiquement décroissant et uniquement pour l'utilisateur."""
        now = timezone.now()
        # Création de sessions pour notre utilisateur avec des dates distinctes en contournant auto_now_add
        s1 = SessionRespiration.objects.create(
            user=self.user,
            technique_name='Apaisant',
            cycles_completed=3
        )
        SessionRespiration.objects.filter(pk=s1.pk).update(created_at=now - timedelta(minutes=5))

        s2 = SessionRespiration.objects.create(
            user=self.user,
            technique_name='Relaxant',
            cycles_completed=2
        )
        SessionRespiration.objects.filter(pk=s2.pk).update(created_at=now)

        # Création d'un autre utilisateur
        other_user = Utilisateur.objects.create(
            email='autre_respi@cesizen.fr',
            pseudo='OtherRespi',
            password=make_password('Password123!')
        )
        # Session pour l'autre utilisateur (ne doit pas apparaître)
        SessionRespiration.objects.create(
            user=other_user,
            technique_name='Équilibrant',
            cycles_completed=10,
            created_at=now
        )

        response = self.client.get(self.historique_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Vérification de l'ordre (chronologique décroissant, donc le 2ème créé en premier)
        self.assertEqual(response.data[0]['technique_name'], 'Relaxant')
        self.assertEqual(response.data[1]['technique_name'], 'Apaisant')

    def test_statistics_exact_calculation(self):
        """Vérifier le calcul précis du temps de relaxation selon la technique."""
        # 1 cycle de Relaxant (19 secondes)
        SessionRespiration.objects.create(user=self.user, technique_name='Relaxant', cycles_completed=1)
        # 3 cycles de Équilibrant (3 * 10 = 30 secondes)
        SessionRespiration.objects.create(user=self.user, technique_name='Équilibrant', cycles_completed=3)
        # Total secondes = 19 + 30 = 49 secondes. Divisé par 60 et arrondi = 1 minute.
        
        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['exercices'], 2)
        self.assertEqual(response.data['minutes'], 1)

