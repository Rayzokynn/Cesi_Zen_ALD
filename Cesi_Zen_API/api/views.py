"""
Module de vues pour l'API Cesi Zen.

Ce module contient toutes les vues et endpoints pour la gestion des utilisateurs,
articles et sessions de respiration.
"""

from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ArticleInfo, ArticleLu, SessionRespiration, Utilisateur
from .serializer import (
    ArticleSerializer,
    ChangePasswordSerializer,
    SessionRespirationSerializer,
    UpdateProfileSerializer,
    UserSerializer,
    UtilisateurSerializer,
)



@api_view(['POST'])
def create_utilisateur(request):
    """Crée un nouvel utilisateur.

    Args:
        request: La requête HTTP contenant les données de l'utilisateur.

    Returns:
        Response: Les données du nouvel utilisateur ou les erreurs de validation.
    """
    serializer = UtilisateurSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vue_securisee_test(request):
    """Vue de test sécurisée pour vérifier l'authentification.

    Args:
        request: La requête HTTP de l'utilisateur authentifié.

    Returns:
        Response: Un message de félicitation personnalisé.
    """
    message = (
        f"félicitation {request.user.pseudo} "
        "Vous êtes authentifié et pouvez accéder à cette vue sécurisée."
    )
    return Response({'message': message})

@api_view(['POST'])
def connecter_utilisateur(request):
    """Authentifie un utilisateur et retourne les tokens JWT.

    Args:
        request: La requête HTTP contenant email et password.

    Returns:
        Response: Les tokens JWT et un message de bienvenue.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = Utilisateur.objects.get(email=email)
    except Utilisateur.DoesNotExist:
        return Response(
            {'error': 'Email introuvable'},
            status=status.HTTP_404_NOT_FOUND
        )

    if not check_password(password, user.password):
        return Response(
            {'error': 'Mot de passe incorrect'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    user.date_connexion = timezone.now()
    user.save()
    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'message': f'Bienvenue {user.pseudo} !'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_articles(request):
    """Récupère la liste de tous les articles.

    Args:
        request: La requête HTTP.

    Returns:
        Response: Liste de tous les articles.
    """
    articles = ArticleInfo.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_article(request, pk):
    """Récupère un article spécifique par son identifiant.

    Args:
        request: La requête HTTP.
        pk: L'identifiant primaire de l'article.

    Returns:
        Response: Les données de l'article.
    """
    try:
        article = ArticleInfo.objects.get(pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    except ArticleInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

class SaveRespirationSessionView(generics.CreateAPIView):
    """Vue pour créer une nouvelle session de respiration."""

    queryset = SessionRespiration.objects.all()
    serializer_class = SessionRespirationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Sauvegarde la session de respiration avec l'utilisateur courant.

        Args:
            serializer: Le sérialiseur de la session de respiration.
        """
        serializer.save(user=self.request.user)


class HistoriqueRespirationView(generics.ListAPIView):
    """Vue pour récupérer l'historique des sessions de respiration."""

    serializer_class = SessionRespirationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retourne les sessions de respiration de l'utilisateur courant.

        Returns:
            QuerySet: Sessions triées par date décroissante.
        """
        return SessionRespiration.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def marquer_article_lu(request, pk):
    """Marque un article comme lu pour l'utilisateur courant.

    Args:
        request: La requête HTTP de l'utilisateur authentifié.
        pk: L'identifiant primaire de l'article.

    Returns:
        Response: Un message de confirmation ou une erreur.
    """
    try:
        article = ArticleInfo.objects.get(pk=pk)
        ArticleLu.objects.get_or_create(
            utilisateur=request.user, article=article
        )
        return Response(
            {'message': 'Lecture enregistrée'}, status=status.HTTP_201_CREATED
        )
    except ArticleInfo.DoesNotExist:
        return Response(
            {'error': 'Article introuvable'},
            status=status.HTTP_404_NOT_FOUND
        )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mes_statistiques(request):
    """Retourne les statistiques de l'utilisateur courant en calculant précisément
    les minutes de relaxation selon les techniques pratiquées.

    Args:
        request: La requête HTTP de l'utilisateur authentifié.

    Returns:
        Response: Dictionnaire contenant exercices, minutes et articles lus.
    """
    sessions = SessionRespiration.objects.filter(user=request.user)
    nb_exercices = sessions.count()
    nb_articles = ArticleLu.objects.filter(
        utilisateur=request.user
    ).count()

    # Dictionnaire des durées de cycle par technique (en secondes)
    durees_cycles = {
        'Relaxant': 19,
        'Équilibrant': 10,
        'Apaisant': 10
    }

    total_secondes = 0
    for session in sessions:
        # Récupère la durée du cycle correspondante (10 secondes par défaut)
        duree_cycle = durees_cycles.get(session.technique_name, 10)
        total_secondes += session.cycles_completed * duree_cycle

    minutes_relax = round(total_secondes / 60)

    return Response({
        'exercices': nb_exercices,
        'minutes': minutes_relax,
        'articles': nb_articles
    })

class UserProfileView(generics.RetrieveUpdateAPIView):
    """Vue pour récupérer ou mettre à jour le profil utilisateur."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retourne l'utilisateur courant.

        Returns:
            Utilisateur: L'utilisateur authentifié.
        """
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """Vue pour changer le mot de passe de l'utilisateur."""

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """Change le mot de passe de l'utilisateur courant.

        Args:
            request: La requête HTTP contenant ancien et nouveau mot de passe.
            *args: Arguments positionnels additionnels.
            **kwargs: Arguments nommés additionnels.

        Returns:
            Response: Un message de confirmation ou une erreur.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        old_password = serializer.validated_data.get("old_password")
        if not check_password(old_password, user.password):
            return Response(
                {"old_password": ["Ancien mot de passe incorrect."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_password = serializer.validated_data.get("new_password")
        user.password = make_password(new_password)
        user.save()

        return Response(
            {"message": "Mot de passe mis à jour !"},
            status=status.HTTP_200_OK
        )


class UpdateProfileView(generics.UpdateAPIView):
    """Vue pour mettre à jour le profil utilisateur."""

    queryset = Utilisateur.objects.all()
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retourne l'utilisateur courant.

        Returns:
            Utilisateur: L'utilisateur authentifié.
        """
        return self.request.user
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """Récupère le profil de l'utilisateur courant.

    Args:
        request: La requête HTTP de l'utilisateur authentifié.

    Returns:
        Response: Dictionnaire avec username et email.
    """
    return Response({
        'username': request.user.username,
        'email': request.user.email
    })
