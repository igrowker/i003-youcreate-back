from rest_framework import serializers
from .models import Ingreso  # Asegúrate de que el modelo exista


class IngresoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingreso
        fields = "__all__"
