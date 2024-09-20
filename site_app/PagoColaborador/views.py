
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import PagoColaborador
from .serializers import PagoColaboradorSerializer
from .services import PagosColaboradoresService

class PagoColaboradorPagination(PageNumberPagination):
    page_size = 10

class PagoColaboradorViewSet(viewsets.ModelViewSet):
    queryset = PagoColaborador.objects.all()
    serializer_class = PagoColaboradorSerializer
    pagination_class = PagoColaboradorPagination 

    def create(self, request, *args, **kwargs):
        data = request.data
        colaborador_id = data.get('colaborador_id')
        monto = data.get('monto')
        fecha_pago = data.get('fecha_pago')
        descripcion = data.get('descripcion')
        pago = PagosColaboradoresService.registrar_pago(colaborador_id, monto, fecha_pago, descripcion)
        serializer = self.get_serializer(pago)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        pago_id = kwargs.get('pk')
        data = request.data
        monto = data.get('monto')
        fecha_pago = data.get('fecha_pago')
        descripcion = data.get('descripcion')
        pago = PagosColaboradoresService.actualizar_pago(pago_id, monto, fecha_pago, descripcion)
        if pago is None:
            return Response({"detail": "Pago no encontrado"}, status=404)
        serializer = self.get_serializer(pago)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        colaborador_id = request.query_params.get('colaborador_id')
        if colaborador_id:
            pagos = PagosColaboradoresService.obtener_historial_pagos(colaborador_id)
        else:
            pagos = self.get_queryset()

        # Aplicar paginación
        page = self.paginate_queryset(pagos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Si no se usa paginación, devolver todos los resultados
        serializer = self.get_serializer(pagos, many=True)
        return Response(serializer.data)
