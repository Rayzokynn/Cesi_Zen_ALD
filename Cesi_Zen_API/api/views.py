from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ArticleInfo, ArticleLu, Utilisateur
from .serializer import ArticleSerializer, ChangePasswordSerializer, UserSerializer, UtilisateurSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from .models import SessionRespiration
from .serializer import SessionRespirationSerializer


@api_view(['GET'])
def get_utilisateurs(request):
    users = Utilisateur.objects.all()
    serializer = UtilisateurSerializer(users, many=True)   
    return Response(serializer.data)


@api_view(['POST'])
def create_utilisateur(request):
    serializer = UtilisateurSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)  
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def utilisateur_details(request, pk):
    try:
        user = Utilisateur.objects.get(pk=pk)
    except Utilisateur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UtilisateurSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UtilisateurSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vue_securisee_test(request):
    return Response({'message': f"felicitation {request.user.pseudo} Vous êtes authentifié et pouvez accéder à cette vue sécurisée."})

@api_view(['POST'])
def connecter_utilisateur(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = Utilisateur.objects.get(email=email)
    except Utilisateur.DoesNotExist:
        return Response({'error': 'Email introuvable'}, status=status.HTTP_404_NOT_FOUND)
    if not check_password(password, user.password):
        return Response({'error': 'Mot de passe incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
    user.date_connexion = timezone.now()
    user.save()
    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'message': f'Bienvenue {user.pseudo} !'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def profil_utilisateur(request, pk):
    try:
        user = Utilisateur.objects.get(pk=pk)
        serializer = UtilisateurSerializer(user)
        return Response(serializer.data)
    except Utilisateur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modifier_utilisateur(request, pk):
    if request.user.id != pk:
        return Response({'error': 'Accès refusé. Vous ne pouvez modifier que votre propre profil.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = Utilisateur.objects.get(pk=pk)
    except Utilisateur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UtilisateurSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def supprimer_utilisateur(request, pk):
    if request.user.id != pk:
        return Response({'error': 'Accès refusé. Vous ne pouvez supprimer que votre propre profil.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = Utilisateur.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Utilisateur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Gestion articles 


@api_view(['GET'])
def get_articles(request):
    articles = ArticleInfo.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_article(request, pk):
    try:
        article = ArticleInfo.objects.get(pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    except ArticleInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

class SaveRespirationSessionView(generics.CreateAPIView):
    queryset = SessionRespiration.objects.all()
    serializer_class = SessionRespirationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HistoriqueRespirationView(generics.ListAPIView):
    serializer_class = SessionRespirationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SessionRespiration.objects.filter(user=self.request.user).order_by('-created_at')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def marquer_article_lu(request, pk):
    try:
        article = ArticleInfo.objects.get(pk=pk)
        ArticleLu.objects.get_or_create(utilisateur=request.user, article=article)
        return Response({'message': 'Lecture enregistrée'}, status=201)
    except ArticleInfo.DoesNotExist:
        return Response({'error': 'Article introuvable'}, status=404)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mes_statistiques(request):
    sessions = SessionRespiration.objects.filter(user=request.user)
    nb_exercices = sessions.count()
    nb_articles = ArticleLu.objects.filter(utilisateur=request.user).count()
    
    total_cycles = sum(session.cycles_completed for session in sessions)
    minutes_relax = round((total_cycles * 10) / 60)

    return Response({
        'exercices': nb_exercices,
        'minutes': minutes_relax,
        'articles': nb_articles
    })

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# Changer le mot de passe
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        
        if not user.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Ancien mot de passe incorrect."]}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response({"message": "Mot de passe mis à jour !"}, status=status.HTTP_200_OK)
    

# Dans views.py
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    return Response({
        'username': request.user.username, # Doit correspondre au HTML
        'email': request.user.email
    })