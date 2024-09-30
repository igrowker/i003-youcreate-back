from allauth.socialaccount.views import signup
from django.urls import path
from .views import GoogleLogin

urlpatterns = [
    # TODO: Add user editing url
    path("signup/", signup, name="socialaccount_signup"),
    path("google/", GoogleLogin.as_view(), name="google_login"),
]
