from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import PagoColaborador
from .serializers import PagoColaboradorSerializer
from .services import PagosColaboradoresService
from Colaborador.models import Colaborador

class PagoColaboradorPagination(PageNumberPagination):
    page_size = 10

class PagoColaboradorViewSet(viewsets.ModelViewSet):
    # Ordenar por id
    queryset = PagoColaborador.objects.all().order_by('id')  
    serializer_class = PagoColaboradorSerializer
    pagination_class = PagoColaboradorPagination 
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        colaborador_id = data.get('colaborador_id')
        monto = data.get('monto')
        fecha_pago = data.get('fecha_pago')
        descripcion = data.get('descripcion')

        try:
            colaborador = Colaborador.objects.get(id=colaborador_id)
        except Colaborador.DoesNotExist:
            return Response({"detail": "Colaborador no encontrado."}, status=404)

        # Llamar al servicio para registrar el pago
        try:
            pago = PagosColaboradoresService.registrar_pago(colaborador_id, monto, fecha_pago, descripcion)
            serializer = self.get_serializer(pago)
            return Response(serializer.data, status=201)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)

    def list(self, request, *args, **kwargs):
        colaborador_id = request.query_params.get('colaborador_id')
        if colaborador_id:
            pagos = self.queryset.filter(colaborador_id=colaborador_id)
        else:
            pagos = self.get_queryset()

        # Aplicar paginación
        page = self.paginate_queryset(pagos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(pagos, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # Obtener el pago por ID
        try:
            pago = self.get_object()
        except PagoColaborador.DoesNotExist:
            return Response({"detail": "Pago no encontrado."}, status=404)

        # Actualizar los campos del pago
        serializer = self.get_serializer(pago, data=request.data, partial=True)  # `partial=True` permite actualizaciones parciales
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
