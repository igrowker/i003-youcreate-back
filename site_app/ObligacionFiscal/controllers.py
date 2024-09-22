# ObligacionFiscal/controllers.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .services import ObligacionesFiscalesService
from .repositories import ObligacionesFiscalesRepository
from .models import ObligacionFiscal
from .serializers import ObligacionFiscalSerializer
from Usuario.models import CustomUser

class ObligacionesFiscalesController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtiene las obligaciones fiscales calculadas y almacenadas del usuario autenticado"""
        usuario = request.user
        print(f"Usuario autenticado: {usuario.nombre}")
        
        # Cálculo de las obligaciones fiscales
        servicio = ObligacionesFiscalesService(usuario)
        servicio.manejar_obligaciones()

        # Obtener las obligaciones ya guardadas
        repo = ObligacionesFiscalesRepository(usuario)
        obligaciones = repo.obtener_obligaciones_fiscales()

        # Serialización de los resultados
        serializer = ObligacionFiscalSerializer(obligaciones, many=True)
        return Response({"obligaciones": serializer.data}, status=status.HTTP_200_OK)
