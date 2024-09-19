from django.urls import path
from .views import ColaboradorListCreate, ColaboradorRetrieveUpdateDestroy

urlpatterns = [
    path('', ColaboradorListCreate.as_view(), name='colaborador-list-create'),
    path('<int:pk>/', ColaboradorRetrieveUpdateDestroy.as_view(), name='colaborador-detail'),
]