from django.urls import path

from .views import (
    IngresoTotalPorMes,
    IngresoTotalPorAnio,
    CrearIngresoView,
    IngresosView,
    IngresosTotalesView,
    IngresosPorAnioView,
    IngresosPorMesView,
)

urlpatterns = [
    path("ingresos/<int:usuario_id>/", IngresosView.as_view(), name="ingresos-usuario"),
    path(
        "ingresos-totales/<int:usuario_id>/",
        IngresosTotalesView.as_view(),
        name="ingresos-totales",
    ),
    path(
        "ingresos-de-un-mes/<int:usuario_id>/<int:mes>/<int:anio>/",
        IngresosPorMesView.as_view(),
        name="ingresos-por-mes",
    ),
    path(
        "ingresos-de-un-anio/<int:usuario_id>/<int:anio>/",
        IngresosPorAnioView.as_view(),
        name="ingresos-por-anio",
    ),
    path(
        "ingreso-total-en-un-mes/<int:usuario_id>/<int:mes>/<int:anio>/",
        IngresoTotalPorMes.as_view(),
        name="ingreso-total-mes",
    ),
    path(
        "ingreso-total-en-un-mes/<int:usuario_id>/<int:anio>/",
        IngresoTotalPorAnio.as_view(),
        name="ingreso-total-anio",
    ),
    path("ingresos/", CrearIngresoView.as_view(), name="crear-ingreso"),
]
