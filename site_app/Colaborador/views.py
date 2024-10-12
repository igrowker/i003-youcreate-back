from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Colaborador
from .serializers import ColaboradorSerializer


class ColaboradorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
