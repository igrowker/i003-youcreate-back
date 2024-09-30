from rest_framework import serializers
from .models import ActionLog

class ActionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionLog
        fields = '__all__'  
