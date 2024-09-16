from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ObligacionFiscal,Usuario
from .serializers import ObligacionFiscalSerializer

# Controlador para manejar las obligaciones fiscales
class ObligacionesFiscalesController(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get(self, request):
        usuario = request.user  # Obtenemos el usuario autenticado
        pais_residencia = usuario.pais_residencia  # Obtenemos el país de residencia del usuario

        # Filtramos las obligaciones fiscales según el país de residencia del usuario
        if pais_residencia == "Argentina":
            obligaciones = ObligacionFiscal.objects.filter(usuario_id=usuario)  # Filtramos por el usuario
        else:
            obligaciones = []  # Si no es de Argentina, devolvemos una lista vacía por ahora

        serializer = ObligacionFiscalSerializer(obligaciones, many=True)
        return Response(serializer.data)