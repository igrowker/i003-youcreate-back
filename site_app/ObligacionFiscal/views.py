from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import ObligacionFiscal
from .serializers import ObligacionFiscalSerializer

class ObligacionesFiscalesController(APIView):
    #permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder
    permission_classes = [AllowAny] # Permitir acceso sin autenticación temporalmente

    def get(self, request):
        usuario = request.user  # Obtenemos el usuario autenticado

        # Filtramos las obligaciones fiscales según el usuario
        obligaciones = ObligacionFiscal.objects.filter(usuario_id=usuario)

        # Serializamos las obligaciones
        serializer = ObligacionFiscalSerializer(obligaciones, many=True)
        return Response(serializer.data)
