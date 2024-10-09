from allauth.account.signals import email_confirmed
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.dispatch import receiver
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserUpdateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login # 2fa
from .serializers import TwoFALoginSerializer # 2fa


from proyecto.settings import BASE_URL_DEV


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = BASE_URL_DEV
    client_class = OAuth2Client
    success_url = "/"


@receiver(email_confirmed)
def email_confirmed(request, email_address, **kwargs):
    user = email_address.user
    user.email_verified = True

    user.save()

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 2fa
class TwoFALoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = TwoFALoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)
        return Response({"detail": "Inicio de sesión exitoso"}, status=status.HTTP_200_OK)
 # 2fa
 