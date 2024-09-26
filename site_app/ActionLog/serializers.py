from rest_framework import serializers
from .models import ActionLog

class ActionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionLog
        fields = '__all__'  # O especifica los campos que desees incluir
