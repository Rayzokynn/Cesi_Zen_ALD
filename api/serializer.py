from rest_framework import serializers
from .models import ArticleInfo, FavoriActivite, Utilisateur

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleInfo
        fields = '__all__'

class FavoriActiviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriActivite
        fields = '__all__'