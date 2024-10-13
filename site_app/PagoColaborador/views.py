from decimal import Decimal

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import PagoColaborador
from .serializers import PagoColaboradorSerializer
from .services import PagosColaboradoresService


class PagoColaboradorPagination(PageNumberPagination):
    page_size = 10


class PagoColaboradorViewSet(viewsets.ModelViewSet):
    queryset = PagoColaborador.objects.all().order_by("id")
    serializer_class = PagoColaboradorSerializer
    pagination_class = PagoColaboradorPagination
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            pago = PagosColaboradoresService.registrar_pago(
                colaborador_id=data["colaborador_id"],
                nombre=data["nombre"],
                monto=data["monto"],
                fecha_pago=data["fecha_pago"],
                descripcion=data["descripcion"],
                metodo_pago=data["metodo_pago"],
            )
            serializer = self.get_serializer(pago)
            return Response(serializer.data, status=201)
        except ValueError as e:
            return Response({"detail": str(e)}, status=404)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)

    def list(self, request, *args, **kwargs):
        pagos = self.get_queryset()

        page = self.paginate_queryset(pagos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(pagos, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        pago_id = self.kwargs.get("pk")
        try:
            if "monto" in request.data:
                request.data["monto"] = Decimal(request.data["monto"])

            pago = PagosColaboradoresService.actualizar_pago(pago_id, **request.data)
            if pago is not None:
                serializer = self.get_serializer(pago)
                return Response(serializer.data)
            return Response({"detail": "Pago no encontrado."}, status=404)
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)

    def destroy(self, request, *args, **kwargs):
        pago_id = self.kwargs.get("pk")
        if PagosColaboradoresService.eliminar_pago(pago_id):
            return Response(status=204)
        return Response({"detail": "Pago no encontrado."}, status=404)
