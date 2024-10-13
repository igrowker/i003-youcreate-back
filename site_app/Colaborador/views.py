from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Colaborador
from .serializers import ColaboradorSerializer


class ColaboradorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
