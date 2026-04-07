from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import ArticleInfo, Utilisateur, SessionRespiration

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = '__all__'
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleInfo
        fields = '__all__'

class SessionRespirationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionRespiration
        fields = ['id', 'technique_name', 'cycles_completed', 'created_at']

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleInfo
        fields = '__all__' # Si c'est comme ça, c'est parfait !
        # OU fields = ['id', 'titre', 'contenu', 'date_publi', 'imageUrl', ...]