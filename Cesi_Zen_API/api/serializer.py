from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import ArticleInfo, Utilisateur, SessionRespiration
from django.contrib.auth.models import User

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
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'pseudo', 'email']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['pseudo', 'email']

    def validate_email(self, value):
        if Utilisateur.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def validate_pseudo(self, value):
        if Utilisateur.objects.exclude(pk=self.instance.pk).filter(pseudo=value).exists():
            raise serializers.ValidationError("Ce pseudo est déjà utilisé.")
        return value