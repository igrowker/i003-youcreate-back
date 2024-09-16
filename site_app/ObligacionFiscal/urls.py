from django.urls import path, include
from .views import ObligacionesFiscalesController

urlpatterns = [
    path('api/obligaciones-fiscales/', ObligacionesFiscalesController.as_view(), name='obligaciones_fiscales'),
]
