"""
Module de sérialisation pour l'API Cesi Zen.

Ce module contient tous les sérialiseurs pour la validation et la transformation
des données de l'application Cesi Zen.
"""

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import ArticleInfo, SessionRespiration, Utilisateur


class UtilisateurSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la gestion des utilisateurs."""

    class Meta:
        """Configuration du sérialiseur Utilisateur."""

        model = Utilisateur
        fields = '__all__'

    def validate_password(self, value):
        """Valide la force du mot de passe.

        Args:
            value: Le mot de passe à valider.

        Returns:
            str: Le mot de passe validé.

        Raises:
            serializers.ValidationError: Si le mot de passe est trop court.
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                "Le mot de passe doit contenir au moins 8 caractères."
            )
        return value

    def create(self, validated_data):
        """Crée un nouvel utilisateur avec mot de passe hashé.

        Args:
            validated_data: Les données validées de l'utilisateur.

        Returns:
            Utilisateur: L'utilisateur créé.
        """
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class SessionRespirationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les sessions de respiration."""

    class Meta:
        """Configuration du sérialiseur SessionRespiration."""

        model = SessionRespiration
        fields = ['id', 'technique_name', 'cycles_completed', 'created_at']


class ArticleSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les articles."""

    class Meta:
        """Configuration du sérialiseur Article."""

        model = ArticleInfo
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour afficher les informations limitées de l'utilisateur."""

    class Meta:
        """Configuration du sérialiseur User."""

        model = Utilisateur
        fields = ['id', 'pseudo', 'email']


class ChangePasswordSerializer(serializers.Serializer):
    """Sérialiseur pour le changement de mot de passe."""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UpdateProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la mise à jour du profil utilisateur."""

    class Meta:
        """Configuration du sérialiseur UpdateProfile."""

        model = Utilisateur
        fields = ['pseudo', 'email']

    def validate_email(self, value):
        """Valide l'unicité de l'email.

        Args:
            value: L'email à valider.

        Returns:
            str: L'email validé.

        Raises:
            serializers.ValidationError: Si l'email est déjà utilisé.
        """
        if Utilisateur.objects.exclude(
            pk=self.instance.pk
        ).filter(email=value).exists():
            raise serializers.ValidationError(
                "Cet email est déjà utilisé."
            )
        return value

    def validate_pseudo(self, value):
        """Valide l'unicité du pseudo.

        Args:
            value: Le pseudo à valider.

        Returns:
            str: Le pseudo validé.

        Raises:
            serializers.ValidationError: Si le pseudo est déjà utilisé.
        """
        if Utilisateur.objects.exclude(
            pk=self.instance.pk
        ).filter(pseudo=value).exists():
            raise serializers.ValidationError(
                "Ce pseudo est déjà utilisé."
            )
        return value
