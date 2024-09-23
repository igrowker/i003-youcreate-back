
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
   # Juntar todas rutas api/ en un path
    path("auth/", include("Usuario.urls")),
    path('api/', include('PagoColaborador.urls')),
    path('api/', include('Colaborador.urls')),
    path('api/obligaciones-fiscales/', include('ObligacionFiscal.urls')),
    path('api/ingresos/', include('Ingreso.urls')),
]
