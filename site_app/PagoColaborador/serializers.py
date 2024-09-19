from rest_framework import serializers
from .models import PagoColaborador  # Asegúrate de que el modelo exista

class PagoColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoColaborador
        fields = '__all__'