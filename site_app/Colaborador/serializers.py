from rest_framework import serializers
from .models import Colaborador  # Asegúrate de que el modelo exista

class ColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = '__all__'