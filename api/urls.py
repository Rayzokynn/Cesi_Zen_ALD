from django.urls import path
from .views import connecter_utilisateur, create_utilisateur, get_article, get_articles, get_utilisateurs, modifier_utilisateur, profil_utilisateur, supprimer_utilisateur, utilisateur_details

urlpatterns = [
    path('utilisateurs/', get_utilisateurs, name='get_utilisateurs'),
    path('utilisateurs/create/', create_utilisateur, name='create_utilisateur'),
    path('utilisateurs/<int:pk>/', utilisateur_details, name='utilisateur_details'),

    path('login/', connecter_utilisateur, name='connecter_utilisateur'),
    path('utilisateurs/me/<int:pk>/', profil_utilisateur, name='profil_utilisateur'),
    path('utilisateurs/me/<int:pk>/modifier/', modifier_utilisateur, name='modifier_profil_utilisateur'),
    path('utilisateurs/me/<int:pk>/supprimer/', supprimer_utilisateur, name='supprimer_utilisateur'),

    path('articles/', get_articles, name='get_articles'),
    path('articles/<int:pk>/', get_article, name='get_article'),

]