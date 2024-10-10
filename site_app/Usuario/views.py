from allauth.account.models import EmailConfirmationHMAC, EmailConfirmation
from allauth.account.signals import email_confirmed
from allauth.account.views import ConfirmEmailView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from proyecto import settings
from proyecto.settings import BASE_URL_DEV
from .serializers import UserUpdateSerializer, UserDataSerializer


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = BASE_URL_DEV
    client_class = OAuth2Client
    success_url = "/"


class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, request, *args, **kwargs):
        try:
            # Use the provided key to confirm the email
            key = kwargs.get("key")
            confirmation = EmailConfirmationHMAC.from_key(key)
            confirmation.confirm(request)
            # Redirect to the Angular login page with a success message
            return HttpResponseRedirect(f"{settings.FRONTEND_URL}?email_confirmed=true")
        except EmailConfirmation.DoesNotExist:
            # Handle error and redirect to an error page or frontend login with error message
            return HttpResponseRedirect(
                f"{settings.FRONTEND_URL}?email_confirmed=false"
            )


class AccountDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserDataSerializer(
            user, context={"request": request}, data=request.data
        ).get_user_data()
        return Response(serializer, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(
            user, data=request.data, partial=True, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@receiver(email_confirmed)
def email_confirmed(request, email_address, **kwargs):
    user = email_address.user
    user.email_verified = True

    user.save()
