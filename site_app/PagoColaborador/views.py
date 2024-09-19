from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import PagoColaborador
from .serializers import PagoColaboradorSerializer

class PagoColaboradorListCreate(generics.ListCreateAPIView):
    queryset = PagoColaborador.objects.all()
    serializer_class = PagoColaboradorSerializer

class PagoColaboradorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PagoColaborador.objects.all()
    serializer_class = PagoColaboradorSerializer