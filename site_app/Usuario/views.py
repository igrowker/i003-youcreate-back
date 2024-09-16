from django.urls import path

# from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.views import TokenVerifyView

# TODO: Add login required decorator to the relevant views

urlpatterns = [
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
