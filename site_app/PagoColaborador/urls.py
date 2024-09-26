from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PagoColaboradorViewSet

router = DefaultRouter()
router.register(r'pagos-colaboradores', PagoColaboradorViewSet, basename='pagocolaborador')

urlpatterns = [
    path('api/', include(router.urls)),
]
