from allauth.socialaccount.views import signup
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import path, include
from django.views.generic import TemplateView
from .views import UserUpdateView
from .views import GoogleLogin
from .views import TwoFALoginView # 2fa

urlpatterns = [
    # TODO: Add user editing url
    path("signup/", signup, name="account_signup"),
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        TemplateView.as_view(),
        name="password_reset_confirm",
    ),
    path('user/update/', UserUpdateView.as_view(), name='user-update'),  # Ruta para la actualización de usuario
    path('2fa-login/', TwoFALoginView.as_view(), name='2fa-login'), # 2fa
]
