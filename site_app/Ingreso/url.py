from django.urls import path
from .views import IngresosView, IngresosTotalesView, IngresosPorFechaView

urlpatterns = [
    path('ingresos/<int:usuario_id>/', IngresosView.as_view()),
    path('ingresos-totales/<int:usuario_id>/', IngresosTotalesView.as_view()),
    path('ingresos-por-fecha/<int:usuario_id>/', IngresosPorFechaView.as_view()),
]
