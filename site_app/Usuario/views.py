from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Usuario
from .serializers import UsuarioSerializer

#para listar y crear usuarios
class UsuarioListCreate(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

#para obtener, actualizar y eliminar un usuario por su id
class UsuarioRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer