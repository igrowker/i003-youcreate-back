from django.urls import path

from .controllers import ObligacionesFiscalesController

urlpatterns = [
    path(
        "obligaciones-fiscales/",
        ObligacionesFiscalesController.as_view(),
        name="obligaciones_fiscales",
    ),
    path(
        "obligaciones-fiscales/<int:id>/",
        ObligacionesFiscalesController.as_view(),
        name="obligacion-fiscal-detail",
    ),
]
