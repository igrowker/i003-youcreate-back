from allauth.account.views import confirm_email
from allauth.socialaccount.views import signup
from dj_rest_auth.registration.views import (
    VerifyEmailView,
    ResendEmailVerificationView,
    RegisterView,
)
from dj_rest_auth.views import (
    LogoutView,
    UserDetailsView, LoginView,
)
from django.urls import path
from django.views.generic import TemplateView

from .views import (
    GoogleLogin,
)

urlpatterns = [
    # path("login/", LoginView.as_view(), name="login_url"),
    # path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # dj-rest-auth urls
    path("register/", RegisterView.as_view(), name="rest_register"),
    path("registration/account-confirm-email/<key>/", confirm_email, name="account_confirm_email"),
    # re_path("registration/" + r"^account-confirm-email/(?P<key>[-:\w]+)/$", CustomEmailConfirmView.as_view(), name="account_confirm_email"),
    path("registration/account-email-verification-sent/", TemplateView.as_view(), name="account_email_verification_sent"),
    path("registration/verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path("registration/resend-email/", ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),

    path("signup/", signup, name="socialaccount_signup"),
    path("google/", GoogleLogin.as_view(), name="google_login"),
]
