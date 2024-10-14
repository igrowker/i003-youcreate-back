# services.py
from rest_framework.exceptions import ValidationError
from .models import Colaborador
from .serializers import ColaboradorSerializer

def crear_colaborador(colaborador_data, usuario, context=None):
    serializer = ColaboradorSerializer(data=colaborador_data, context=context)
    if serializer.is_valid():
        colaborador = serializer.save(usuario=usuario)
        return colaborador
    else:
        raise ValidationError(serializer.errors)
