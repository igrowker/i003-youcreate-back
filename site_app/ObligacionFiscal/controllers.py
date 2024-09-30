from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .services import ObligacionesFiscalesService
from .repositories import ObligacionesFiscalesRepository
from .models import ObligacionFiscal
from .serializers import ObligacionFiscalSerializer
from Usuario.models import CustomUser
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .tasks import enviar_notificacion_vencimiento 

class ObligacionesFiscalesController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Obtiene las obligaciones fiscales calculadas y almacenadas del usuario autenticado"""
        usuario = request.user
        
        # Cálculo de las obligaciones fiscales
        servicio = ObligacionesFiscalesService(usuario)
        servicio.manejar_obligaciones()

        # Obtener las obligaciones ya guardadas
        repo = ObligacionesFiscalesRepository(usuario)
        obligaciones = repo.obtener_obligaciones_fiscales()
        enviar_notificacion_vencimiento() 

        # Serialización de los resultados
        serializer = ObligacionFiscalSerializer(obligaciones, many=True)
        return Response({"obligaciones": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            obligacion = ObligacionFiscal.objects.get(id=id)
            serializer = ObligacionFiscalSerializer(obligacion, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObligacionFiscal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)