from rest_framework import serializers
from .models import ObligacionFiscal


class ObligacionFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObligacionFiscal
        fields = "__all__"
