from django.urls import path
from .views import CrearIngresoView, IngresosView, IngresosTotalesView, IngresosPorAnioView, IngresosPorMesView

urlpatterns = [
    path('ingresos/<int:usuario_id>/', IngresosView.as_view(), name='ingresos-usuario'),
    path('ingresos-totales/<int:usuario_id>/', IngresosTotalesView.as_view(), name='ingresos-totales'),
    path('ingresos-por-mes/<int:usuario_id>/<int:mes>/<int:anio>/', IngresosPorMesView.as_view(), name='ingresos-por-mes'),
    path('ingresos-por-anio/<int:usuario_id>/<int:anio>/', IngresosPorAnioView.as_view(), name='ingresos-por-anio'),
    path('ingresos/', CrearIngresoView.as_view(), name='crear-ingreso'),  

]
