from django.urls import path
from .views import PagoColaboradorListCreate, PagoColaboradorRetrieveUpdateDestroy

urlpatterns = [
    path('', PagoColaboradorListCreate.as_view(), name='pagocolaborador-list-create'),
    path('<int:pk>/', PagoColaboradorRetrieveUpdateDestroy.as_view(), name='pagocolaborador-detail'),
]