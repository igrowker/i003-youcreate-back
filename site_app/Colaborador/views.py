from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Colaborador
from .serializers import ColaboradorSerializer

class ColaboradorListCreate(generics.ListCreateAPIView):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer

class ColaboradorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer