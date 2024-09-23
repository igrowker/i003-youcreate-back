from rest_framework.views import APIView #Para crear vistas basadas en clases y definir metodos HTTP
from rest_framework.response import Response #Extiende la clase HttpResponde y facilita el trabajo con APIs en formato JSON 
from .service import IngresosService
from .serializers import IngresoSerializer, IngresoPorFechaSerializer

class IngresosView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id):
        ingresos = self.ingresos_service.obtener_ingresos_usuario(usuario_id)
        #Convierto el QuerySet en un conjunto de datos JSON 
        serializer = IngresoSerializer(ingresos, many=True)
        #Retorno los datos serializados en formato JSON  
        return Response(serializer.data)

class IngresosTotalesView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id):
        ingresos_totales = self.ingresos_service.obtener_ingresos_totales(usuario_id)
        #Retorno el resultado ya en formato compatible con JSON (dicc)
        return Response(ingresos_totales)

class IngresosPorFechaView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingresos_service = IngresosService()

    def get(self, request, usuario_id):
        ingresos_por_fecha = self.ingresos_service.obtener_ingresos_por_fecha(usuario_id)
        #Convierto el QuerySet en un conjunto de datos JSON 
        serializer = IngresoPorFechaSerializer(ingresos_por_fecha, many=True)
        #Retorno los datos serializados en formato JSON  
        return Response(serializer.data)
