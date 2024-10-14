from datetime import datetime
from rest_framework import serializers

from .models import Ingreso


# Se crea la clase IngresoSerializer para converitir los datos a formato JSON o deserializar los mismos
class IngresoSerializer(serializers.ModelSerializer):
    class Meta:  # Especifica los detalles a serializar
        model = Ingreso
        fields = ["monto", "origen", "fecha", "categoria", "descripcion"]


class CrearIngresosSerializer(serializers.ModelSerializer):
    monto = serializers.DecimalField(max_digits=50, decimal_places=2)
    origen = serializers.CharField(max_length=255)
    categoria = serializers.CharField(max_length=255)
    descripcion = serializers.CharField(
        max_length=255, required=False, allow_blank=True
    )
    fecha = serializers.DateField(
        format="%d/%m/%Y",  # Formato de salida
        input_formats=[
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
        ],  # Formatos de entrada aceptados
        required=False,
    )

    def validate_fecha(self, value):
        """
        Validación personalizada para asegurarse de que la fecha no está en el futuro.
        """
        if value > datetime.today().date():
            raise serializers.ValidationError("La fecha no puede ser en el futuro.")
        return value

    class Meta:
        model = Ingreso
        fields = ["monto", "origen", "fecha", "categoria", "descripcion"]
