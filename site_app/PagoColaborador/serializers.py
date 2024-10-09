from rest_framework import serializers

from .models import PagoColaborador


class PagoColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoColaborador
        fields = "__all__"

    def create(self, validated_data):
        return PagoColaborador.objects.create(**validated_data)
