from django.urls import path

from .controllers import ObligacionesFiscalesController

urlpatterns = [
    path(
        "obligaciones-fiscales/",
        ObligacionesFiscalesController.as_view(),
        name="obligaciones_fiscales",
    ),  # obligaciones fiscales del mes
    path(
        "actualizacion-estados/<int:id>/",
        ObligacionesFiscalesController.as_view(),
        name="actualizacion-estados",
    ),  # cambio de estados de emeil_automatico y estado_pago
]
