from rest_framework import serializers
from .models import ObligacionFiscal


# Serializador para el modelo ObligacionFiscal
class ObligacionFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObligacionFiscal # Modelo que vamos a serializar
        fields = ['tipo_impuesto', 'monto_a_pagar', 'fecha_vencimiento','estado_pago','email_automatico']  # Campos que incluimos en la respuesta 
        read_only_fields = ['tipo_impuesto', 'monto_a_pagar', 'fecha_vencimiento'] # Campos que solo se pueden leer, no se pueden modificar en la respuesta JSON
        update_fields = ['estado_pago', 'email_automatico'] # Campos que se pueden actualizar en la respuesta JSON

