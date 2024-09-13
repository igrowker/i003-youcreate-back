from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import ObligacionFiscal
from .serializers import ObligacionFiscalSerializer

class ObligacionFiscalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ObligacionFiscal.objects.all()
    serializer_class = ObligacionFiscalSerializer