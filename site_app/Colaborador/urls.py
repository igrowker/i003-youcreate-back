from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ColaboradorViewSet

router = DefaultRouter()
router.register(r"colaboradores", ColaboradorViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
