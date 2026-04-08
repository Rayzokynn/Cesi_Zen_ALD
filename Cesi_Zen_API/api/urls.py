from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ChangePasswordView, SaveRespirationSessionView, HistoriqueRespirationView, UserProfileView, connecter_utilisateur, create_utilisateur, get_article, get_articles, get_utilisateurs, marquer_article_lu, mes_statistiques, modifier_utilisateur, profil_utilisateur, supprimer_utilisateur, utilisateur_details, vue_securisee_test

urlpatterns = [
    path('utilisateurs/', get_utilisateurs, name='get_utilisateurs'),
    path('utilisateurs/create/', create_utilisateur, name='create_utilisateur'),
    path('utilisateurs/<int:pk>/', utilisateur_details, name='utilisateur_details'),

    path('login/', connecter_utilisateur, name='connecter_utilisateur'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('utilisateurs/me/<int:pk>/', profil_utilisateur, name='profil_utilisateur'),
    path('utilisateurs/me/<int:pk>/modifier/', modifier_utilisateur, name='modifier_profil_utilisateur'),
    path('utilisateurs/me/<int:pk>/supprimer/', supprimer_utilisateur, name='supprimer_utilisateur'),

    path('articles/', get_articles, name='get_articles'),
    path('articles/<int:pk>/', get_article, name='get_article'),
    path('test/', vue_securisee_test, name='vue_securisee_test'),
    path('sessions/respiration/', SaveRespirationSessionView.as_view(), name='save_respiration'),
    path('sessions/respiration/historique/', HistoriqueRespirationView.as_view(), name='historique_respiration'),
    path('profil/stats/', mes_statistiques, name='profil_stats'),
    path('articles/', get_articles, name='articles_list'),
    path('articles/<int:pk>/', get_article, name='article_detail'),
    path('articles/<int:pk>/lu/', marquer_article_lu, name='article_lu'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]