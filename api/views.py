from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Activite, ArticleInfo, Utilisateur
from .serializer import ArticleSerializer, UtilisateurSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

# Gestion utilisateurs


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
def modifier_utilisateur(request, pk):
    try:
        user = Utilisateur.objects.get(pk=pk)
    except Utilisateur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UtilisateurSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def supprimer_utilisateur(request, pk):
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

