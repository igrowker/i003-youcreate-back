# ObligacionFiscal/controllers.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .services import ObligacionesFiscalesService
from .repositories import ObligacionesFiscalesRepository

class ObligacionesFiscalesController(APIView):
    permission_classes = [AllowAny]  # Asegura que el usuario esté autenticado

    def get(self, request):
        """Obtiene las obligaciones fiscales personalizadas del usuario autenticado"""
        usuario_id = request.user.id  # Obtener el ID del usuario autenticado
        repo = ObligacionesFiscalesRepository(usuario_id)
        obligaciones = repo.obtener_obligaciones_fiscales()
        return Response({"obligaciones": obligaciones}, status=status.HTTP_200_OK)

    def post(self, request):
        """Calcula y almacena nuevas obligaciones fiscales para el usuario autenticado"""
        usuario = request.user  
        if not usuario.is_authenticated:
            return Response({"error": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)
        servicio = ObligacionesFiscalesService(usuario)
        servicio.manejar_obligaciones()
        return Response({"mensaje": "Obligaciones fiscales calculadas y almacenadas."}, status=status.HTTP_201_CREATED)
