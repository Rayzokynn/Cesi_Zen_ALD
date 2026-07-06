from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    ChangePasswordView,
    SaveRespirationSessionView,
    HistoriqueRespirationView,
    UserProfileView,
    connecter_utilisateur,
    create_utilisateur,
    get_article,
    get_articles,
    marquer_article_lu,
    mes_statistiques,
    vue_securisee_test,
)
from . import views

urlpatterns = [
    # Inscription et connexion publiques
    path('utilisateurs/create/', create_utilisateur, name='create_utilisateur'),
    path('login/', connecter_utilisateur, name='connecter_utilisateur'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Articles
    path('articles/', get_articles, name='articles_list'),
    path('articles/<int:pk>/', get_article, name='article_detail'),
    path('articles/<int:pk>/lu/', marquer_article_lu, name='article_lu'),

    # Exercices et statistiques (sécurisés)
    path('sessions/respiration/', SaveRespirationSessionView.as_view(), name='save_respiration'),
    path('sessions/respiration/historique/', HistoriqueRespirationView.as_view(), name='historique_respiration'),
    path('profil/stats/', mes_statistiques, name='profil_stats'),

    # Profil utilisateur (sécurisé)
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='profile-update'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    # Utilitaires de test
    path('test/', vue_securisee_test, name='vue_securisee_test'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)