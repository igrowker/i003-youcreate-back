from rest_framework import serializers

from .models import PagoColaborador


class PagoColaboradorSerializer(serializers.ModelSerializer):
    nombre_colaborador = serializers.CharField(
        source="colaborador_id.nombre", read_only=True
    )

    class Meta:
        model = PagoColaborador
        fields = "__all__"
