
from django.urls import path
from .controllers import ObligacionesFiscalesController

urlpatterns = [
    # Ruta para obtener las obligaciones fiscales
    path('', ObligacionesFiscalesController.as_view(), name='obligaciones_fiscales'),  # Cambiado a vacío para coincidir con la ruta completa
]
