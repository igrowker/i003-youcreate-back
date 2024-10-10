from allauth.account.signals import email_confirmed
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.dispatch import receiver
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login
from rest_framework.permissions import AllowAny, IsAuthenticated

from .utils import send_otp_via_email, verify_otp
from .models import CustomUser
from .serializers import CustomTokenObtainPairSerializer, UserUpdateSerializer
from .serializers import TwoFALoginSerializer


from proyecto.settings import BASE_URL_DEV
from .serializers import UserUpdateSerializer


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
        serializer = UserUpdateSerializer(
            user, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TwoFALoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TwoFALoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if serializer.validated_data.get('mfa_required'):
            # Almacenar el email en la sesión para que el endpoint de verificación de 2FA pueda accederlo
            request.session['email'] = user.email

            # Responder que se necesita la verificación 2FA
            send_otp_via_email(user)
            return Response({
                "detail": "2FA requerido. Se ha enviado un código a tu correo."
            }, status=status.HTTP_200_OK)

        # Si no se requiere 2FA, generar el token directamente
        login(request, user)
        # Aquí es donde generamos el token JWT o sesión
        token = CustomTokenObtainPairSerializer.get_token(user)
        return Response({
            "token": str(token.access_token),
            "refresh": str(token)
        }, status=status.HTTP_200_OK)


# vista para generar la verificacion 2FA
class TwoFAVerifyView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        otp_code = request.data.get('otp_code')

        # Obtener el email de la sesión
        email = request.session.get('email')

        # Verificar si hay un email en la sesión
        if not email:
            return Response({"detail": "Sesión no válida o ha expirado."}, status=status.HTTP_401_UNAUTHORIZED)

        # Obtener al usuario usando el email
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)


        if not verify_otp(user, otp_code):
            return Response({"detail": "Código OTP inválido."}, status=status.HTTP_400_BAD_REQUEST)

        # Generar el token una vez verificado el OTP
        token = CustomTokenObtainPairSerializer.get_token(user)
        return Response({
            "token": str(token.access_token),
            "refresh": str(token)
        }, status=status.HTTP_200_OK)
