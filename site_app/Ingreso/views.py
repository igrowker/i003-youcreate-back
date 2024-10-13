from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import (
    APIView,
)  # Para crear vistas basadas en clases y definir métodos HTTP

from .serializers import IngresoSerializer, CrearIngresosSerializer
from .service import IngresosService


class CrearIngresoView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def post(self, request):
        serializer = CrearIngresosSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data

            monto = validated_data.get("monto")
            origen = validated_data.get("origen")
            fecha = validated_data.get("fecha")
            categoria = validated_data.get("categoria")
            descripcion = validated_data.get("descripcion")

        # Llamar al servicio para crear el ingreso
        ingreso = self.ingresos_service.crear_ingreso(
            usuario_id=request.user,
            monto=monto,
            origen=origen,
            categoria=categoria,
            descripcion=descripcion,
            fecha=fecha,
        )

        # Devolver la respuesta
        return Response(
            {
                "id": ingreso.id,
                "monto": ingreso.monto,
                "origen": ingreso.origen,
                "fecha": ingreso.fecha,
                "usuario_id": ingreso.usuario_id.id,
                "categoria": ingreso.categoria,
                "descripcion": ingreso.descripcion,
            },
            status=status.HTTP_201_CREATED,
        )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngresosView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id):
        ingresos = self.ingresos_service.obtener_ingresos_usuario(usuario_id)
        if not ingresos:
            return not_found_response()
        # Convierto los objetos Ingreso a JSON
        serializer = IngresoSerializer(ingresos, many=True)
        return Response(serializer.data)


class IngresosTotalesView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id):
        # Llamamos al servicio para obtener los ingresos totales
        ingresos_totales = self.ingresos_service.obtener_ingresos_totales(usuario_id)
        # Retorno el resultado ya en formato compatible con JSON (dicc)
        if not ingresos_totales:
            return not_found_response()
        return Response(ingresos_totales)


class IngresosPorMesView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id, mes, anio):
        # Llamamos al servicio para obtener los ingresos por mes
        ingresos_por_mes = self.ingresos_service.obtener_ingresos_de_un_mes(
            usuario_id, mes, anio
        )
        if not ingresos_por_mes:
            return not_found_response()
        serializer = IngresoSerializer(ingresos_por_mes, many=True)
        return Response(serializer.data)


class IngresosPorAnioView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id, anio):
        # Llamamos al servicio para obtener los ingresos por anio
        ingresos_por_anio = self.ingresos_service.obtener_ingresos_de_un_anio(
            usuario_id, anio
        )
        if not ingresos_por_anio:
            return not_found_response()
        serializer = IngresoSerializer(ingresos_por_anio, many=True)
        return Response(serializer.data)


class IngresoTotalPorMes(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id, mes, anio):
        # Llamamos al servicio para obtener los ingresos totales de un mes
        ingresos_total = self.ingresos_service.obtener_ingreso_total_en_un_mes(
            usuario_id, mes, anio
        )
        if not ingresos_total:
            return not_found_response()

        # Retornamos el diccionario directamente
        return Response(ingresos_total)


class IngresoTotalPorAnio(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id, anio):
        # Llamamos al servicio para obtener los ingresos totales de un anio
        ingresos_total = self.ingresos_service.obtener_ingreso_total_en_un_anio(
            usuario_id, anio
        )
        if not ingresos_total:
            return not_found_response()

        # Retornamos el diccionario directamente
        return Response(ingresos_total)


def not_found_response():
    return Response(
        {
            "message": "No se encontraron ingresos para el usuario o para el mes/año indicado"
        },
        status=status.HTTP_404_NOT_FOUND,
    )
