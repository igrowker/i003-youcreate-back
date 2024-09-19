from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import Ingreso
from .serializers import IngresoSerializer

class IngresoListCreate(generics.ListCreateAPIView):
    queryset = Ingreso.objects.all()
    serializer_class = IngresoSerializer

class IngresoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingreso.objects.all()
    serializer_class = IngresoSerializer