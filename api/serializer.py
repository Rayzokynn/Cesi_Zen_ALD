from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import ArticleInfo, FavoriActivite, Utilisateur

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

class FavoriActiviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriActivite
        fields = '__all__'