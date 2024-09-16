from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ObligacionFiscal
from .serializers import ObligacionFiscalSerializer

# Controlador para manejar las obligaciones fiscales
class ObligacionesFiscalesController(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get(self, request):
        usuario = request.user  # Obtenemos el usuario autenticado
        obligaciones = ObligacionFiscal.objects.filter(usuario=usuario)  # Filtramos por el usuario
        serializer = ObligacionFiscalSerializer(obligaciones, many=True)  # Serializamos las obligaciones
        return Response(serializer.data)  # Devolvemos las obligaciones en formato JSON