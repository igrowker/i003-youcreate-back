from django.urls import path
from .views import IngresoListCreate, IngresoRetrieveUpdateDestroy

urlpatterns = [
    path("", IngresoListCreate.as_view(), name="ingreso-list-create"),
    path("<int:pk>/", IngresoRetrieveUpdateDestroy.as_view(), name="ingreso-detail"),
]
