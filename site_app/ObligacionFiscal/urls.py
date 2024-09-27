from django.urls import path
from .controllers import ObligacionesFiscalesController

urlpatterns = [
    # Ruta para obtener las obligaciones fiscales
    path(
        "obligaciones-fiscales/",
        ObligacionesFiscalesController.as_view(),
        name="obligaciones_fiscales",
    ),
]
