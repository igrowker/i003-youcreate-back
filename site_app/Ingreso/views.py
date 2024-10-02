from rest_framework.views import APIView #Para crear vistas basadas en clases y definir metodos HTTP
from rest_framework.response import Response #Extiende la clase HttpResponde y facilita el trabajo con APIs en formato JSON 
from .service import IngresosService
from .serializers import IngresoPorAnioSerializer
from calendar import month_name
from rest_framework.response import Response
from rest_framework import status 

class IngresosView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id):
        ingresos = self.ingresos_service.obtener_ingresos_usuario(usuario_id)
        
        if not ingresos:
            return Response([], status=status.HTTP_204_NO_CONTENT)  # O el estado que prefieras

        # Convertir los resultados a una lista de diccionarios para la respuesta
        data = [
            {'origen': ingreso['origen'], 'total': ingreso['total']} 
            for ingreso in ingresos
        ]

        return Response(data)

    
class IngresosTotalesView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id):
        # Llamamos al servicio para obtener los ingresos totales
        ingresos_totales = self.ingresos_service.obtener_ingresos_totales(usuario_id)
        #Retorno el resultado ya en formato compatible con JSON (dicc)
        return Response(ingresos_totales)

class IngresosPorMesView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id, mes):
        # Llamamos al servicio para obtener los ingresos por mes
        ingresos_por_mes = self.ingresos_service.obtener_ingresos_por_mes(usuario_id, mes)
        # Convertimos el número del mes a su nombre
        mes_nombre = month_name[mes]  # 'Enero' para 1, 'Febrero' para 2, etc.
        # Creamos un conjunto de datos para la respuesta
        total_ingresos = sum(ingreso.monto for ingreso in ingresos_por_mes)
        # Estructuramos los datos para la respuesta JSON
        response_data = [{
            'mes': mes_nombre,
            'total': total_ingresos
        }]
        # Retornamos los datos en formato JSON
        return Response(response_data)

class IngresosPorAnioView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id, anio):
        # Llamamos al servicio para obtener los ingresos por anio
        ingresos_por_anio = self.ingresos_service.obtener_ingresos_por_anio(usuario_id, anio)
        #Convierto el QuerySet en un conjunto de datos JSON 
        serializer = IngresoPorAnioSerializer(ingresos_por_anio, many=True)
        #Retorno los datos serializados en formato JSON  
        return Response(serializer.data)    
