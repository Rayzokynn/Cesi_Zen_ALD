from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .models import Utilisateur

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token.get('user_id')
            user = Utilisateur.objects.get(pk=user_id)
            user.is_authenticated = True 
            return user

        except Utilisateur.DoesNotExist:
            raise AuthenticationFailed('Utilisateur introuvable', code='user_not_found')