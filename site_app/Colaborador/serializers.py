from rest_framework import serializers

from .models import Colaborador


class ColaboradorSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Colaborador
        fields = "__all__"
