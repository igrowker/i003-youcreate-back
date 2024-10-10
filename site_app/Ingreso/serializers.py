from rest_framework import serializers
from .models import Ingreso

#Se crea la clase IngresoSerializer para converitir los datos a formato JSON o deserializar los mismos 
class IngresoSerializer(serializers.ModelSerializer):
    class Meta: #Especifica los detalles a serializar
        model = Ingreso
        fields = ['monto', 'origen', 'fecha', 'categoria', 'descripcion']



