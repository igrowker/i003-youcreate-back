from rest_framework import serializers
from .models import ObligacionFiscal


# Serializador para el modelo ObligacionFiscal
class ObligacionFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObligacionFiscal # Modelo que vamos a serializar
        fields = ['tipo_impuesto', 'monto_a_pagar', 'fecha_vencimiento', 'usuario_id']  # Campos que incluimos en la respuesta JSON

