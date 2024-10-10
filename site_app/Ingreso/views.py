from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import (
    APIView,
)  # Para crear vistas basadas en clases y definir metodos HTTP

from .serializers import IngresoSerializer
from .service import IngresosService


class CrearIngresoView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def post(self, request):
        usuario_id = request.data.get("usuario_id")
        monto = request.data.get("monto")
        origen = request.data.get("origen")
        fecha = request.data.get("fecha", None)  # Opcional

        # Llamar al servicio para crear el ingreso
        ingreso = self.ingresos_service.crear_ingreso(usuario_id, monto, origen, fecha)

        # Devolver la respuesta
        return Response(
            {
                "id": ingreso.id,
                "monto": ingreso.monto,
                "origen": ingreso.origen,
                "fecha": ingreso.fecha,
                "usuario_id": ingreso.usuario_id.id,
            },
            status=status.HTTP_201_CREATED,
        )


class IngresosView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id):
        ingresos = self.ingresos_service.obtener_ingresos_usuario(usuario_id)
        if not ingresos:
            return Response(
                {"message": "No se encontraron ingresos para el usuario"},
                status=status.HTTP_200_OK,
            )
        # Convierto los objetos Ingreso a JSON
        serializer = IngresoSerializer(ingresos, many=True)
        return Response(serializer.data)


class IngresosTotalesView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id):
        # Llamamos al servicio para obtener los ingresos totales
        ingresos_totales = self.ingresos_service.obtener_ingresos_totales(usuario_id)
        # Retorno el resultado ya en formato compatible con JSON (dicc)
        if not ingresos_totales:
            return Response(
                {"message": "No se encontraron ingresos para el usuario"},
                status=status.HTTP_200_OK,
            )
        return Response(ingresos_totales)


class IngresosPorMesView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id, mes):
        # Llamamos al servicio para obtener los ingresos por mes
        ingresos_por_mes = self.ingresos_service.obtener_ingresos_de_un_mes(
            usuario_id, mes
        )
        if not ingresos_por_mes:
            return Response(
                {"message": "No se encontraron ingresos para el usuario"},
                status=status.HTTP_200_OK,
            )
        serializer = IngresoSerializer(ingresos_por_mes, many=True)
        return Response(serializer.data)


class IngresosPorAnioView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id, anio):
        # Llamamos al servicio para obtener los ingresos por anio
        ingresos_por_anio = self.ingresos_service.obtener_ingresos_de_un_anio(
            usuario_id, anio
        )
        if not ingresos_por_anio:
            return Response(
                {"message": "No se encontraron ingresos para el usuario"},
                status=status.HTTP_200_OK,
            )
        serializer = IngresoSerializer(ingresos_por_anio, many=True)
        return Response(serializer.data)


class IngresoTotalPorMes(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id, mes, anio):
        # Llamamos al servicio para obtener los ingresos totales de un mes
        ingresos_total = self.ingresos_service.obtener_ingreso_total_en_un_mes(
            usuario_id, mes, anio
        )
        if not ingresos_total:
            return Response(
                {
                    "message": "No se encontraron ingresos para el usuario en el año indicado"
                },
                status=status.HTTP_200_OK,
            )

        # Retornamos el diccionario directamente
        return Response(ingresos_total)


class IngresoTotalPorAnio(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id, anio):
        # Llamamos al servicio para obtener los ingresos totales de un anio
        ingresos_total = self.ingresos_service.obtener_ingreso_total_en_un_anio(
            usuario_id, anio
        )
        if not ingresos_total:
            return Response(
                {
                    "message": "No se encontraron ingresos para el usuario en el año indicado"
                },
                status=status.HTTP_200_OK,
            )

        # Retornamos el diccionario directamente
        return Response(ingresos_total)
