from rest_framework import viewsets
from .models import Colaborador
from .serializers import ColaboradorSerializer

class ColaboradorViewSet(viewsets.ModelViewSet):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer
