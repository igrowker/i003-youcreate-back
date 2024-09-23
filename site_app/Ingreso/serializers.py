from rest_framework import serializers
from .models import Ingreso

#Se crea la clase IngresoSerializer para converitir los datos a formato JSON o deserializar los mismos 
class IngresoSerializer(serializers.ModelSerializer):
    class Meta: #Especifica los detalles a serializar
        model = Ingreso #basado en el modelo Ingreso
        fields = ['id', 'monto', 'origen', 'fecha', 'usuario_id']

#Se crea un serializer NO basado en un modelo para poder devolver campos especificos
class IngresoPorFechaSerializer(serializers.Serializer):
    fecha = serializers.DateField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
