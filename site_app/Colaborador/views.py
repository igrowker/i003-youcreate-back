from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Colaborador
from .serializers import ColaboradorSerializer
from .services import crear_colaborador

class ColaboradorViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer

    def create(self, request, *args, **kwargs):
        colaborador_data = request.data
        # TODO: "nombre" del colaborador es el nombre del usuario, cambiar para el nombre del pago
        colaborador = crear_colaborador(colaborador_data, request.user, context={"request": request})
        return Response(
            ColaboradorSerializer(colaborador).data,
            status=status.HTTP_201_CREATED
        )
