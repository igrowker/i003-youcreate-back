from rest_framework import viewsets
from .models import ActionLog
from .serializers import ActionLogSerializer

class ActionLogViewSet(viewsets.ModelViewSet):
    queryset = ActionLog.objects.all()
    serializer_class = ActionLogSerializer
