import requests
from allauth.account.views import ConfirmEmailView
from django.conf import settings
from django.http import HttpResponseRedirect

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from requests import Response
from rest_framework import generics, status
from rest_framework.views import APIView

from proyecto.settings import BASE_URL_DEV


# class CustomRegisterView(RegisterView):
# permission_classes = [AllowAny]
# authentication_classes = [JWTAuthentication]
# serializer_class = CustomRegisterSerializer
# Retorna el usuario creado como respuesta
# queryset = CustomUser.objects.all()


# class LoginView(TokenObtainPairView):
#     permission_classes = [AllowAny]
#     # Responde con el token generado y el token de refresco
#     serializer_class = CustomTokenObtainPairSerializer

class CustomEmailConfirmView(APIView):
    @staticmethod
    def get(request, key):
        verify_email_url = 'http://localhost:8000/auth/registration/verify-email/'

        # make a POST request to the verify-email endpoint with the key
        response = requests.post(verify_email_url, {'key': key})
        if response.status_code == 200:
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Email verification failed'}, status=status.HTTP_400_BAD_REQUEST)

class EmailConfirmView(generics.UpdateAPIView):
    # Updates the user's verified status - May not be necessary
    # Try the regular ConfirmEmailView first!
    pass


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = BASE_URL_DEV
    client_class = OAuth2Client


def email_confirm_redirect(request, key):
    return HttpResponseRedirect(f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/")


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )
