from django.urls import path
from .views import UsuarioListCreate, UsuarioRetrieveUpdateDestroy

urlpatterns = [
    path('', UsuarioListCreate.as_view(), name='usuario-list-create'),
    path('<int:pk>/', UsuarioRetrieveUpdateDestroy.as_view(), name='usuario-detail'),
]