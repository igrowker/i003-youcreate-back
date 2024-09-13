from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ObligacionFiscalViewSet

router = DefaultRouter()
router.register(r'obligaciones-fiscales', ObligacionFiscalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]