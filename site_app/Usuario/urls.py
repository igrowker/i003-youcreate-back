from allauth.socialaccount.views import signup
from dj_rest_auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    LoginView,
    LogoutView,
    UserDetailsView,
    PasswordChangeView,
)
from django.urls import path
from django.views.generic import TemplateView

from proyecto import settings
from .views import GoogleLogin, AccountDataView, UserUpdateView

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
    # Ruta para la actualización de usuario
    path("user/update/", UserUpdateView.as_view(), name="user-update"),
    path("user/account-data/", AccountDataView.as_view(), name="account_data"),
    # URLs that do not require a session or valid token
    path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
    path("login/", LoginView.as_view(), name="rest_login"),
    # URLs that require a user to be logged in with a valid session / token.
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("password/change/", PasswordChangeView.as_view(), name="rest_password_change"),
]

if settings.REST_AUTH["USE_JWT"]:
    from rest_framework_simplejwt.views import TokenVerifyView

    from dj_rest_auth.jwt_auth import get_refresh_view

    urlpatterns += [
        path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
        path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    ]
