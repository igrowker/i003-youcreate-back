from allauth.account.views import ConfirmEmailView
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("Usuario.urls")),
    path("auth/", include("dj_rest_auth.urls")),
    re_path(
        "^auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("accounts/", include("allauth.urls")),
    path("_allauth/", include("allauth.headless.urls")),
    path("api/", include("Colaborador.urls")),
    path("api/", include("PagoColaborador.urls")),
    path(
        "api/", include("ObligacionFiscal.urls")
    ),  # Incluye las URLs de ObligacionFiscal
    path("api/", include("ActionLog.urls")),
    path("api/", include("Ingreso.urls")),
]
